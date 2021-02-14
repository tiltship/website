package main

import (
	"bytes"
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"github.com/jackc/pgconn"
	"github.com/jackc/pgx/v4/pgxpool"
	"github.com/labstack/echo/v4"
	"github.com/stretchr/testify/assert"
)

const (
	setupSql = `drop table if exists signups;
               
                 create table if not exists signups(
                   email VARCHAR PRIMARY KEY CHECK (email != ''),
                   created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
                   tracking_data JSON NOT NULL CHECK (tracking_data != 'null'::json)
                 );

                 drop table if exists events;               
                 create table if not exists events(
                   subtype VARCHAR NOT NULL,
                   created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
                   tracking_data JSON NOT NULL CHECK (tracking_data != 'null'::json)
                 );
`
)

func mustExec(t testing.TB, conn *pgxpool.Pool, sql string, arguments ...interface{}) (commandTag pgconn.CommandTag) {
	var err error
	if commandTag, err = conn.Exec(context.Background(), sql, arguments...); err != nil {
		t.Fatalf("Exec unexpectedly failed with %v: %v", sql, err)
	}
	return
}

func testPool() *pgxpool.Pool {
	config, err := pgxpool.ParseConfig("postgres://root@localhost:5433/test")
	handle(err)

	ctx := context.Background()
	pool, err := pgxpool.ConnectConfig(ctx, config)
	handle(err)

	return pool
}

func TestSignupAdsSignupAndErrorsOnDuplicate(t *testing.T) {
	pool := testPool()
	defer pool.Close()

	mustExec(t, pool, setupSql)

	request := `{"email": "foo", "tracking_data": { "foo": "bar" }}`
	body := bytes.NewReader([]byte(request))

	req := httptest.NewRequest(http.MethodPost, "/signups", body)
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()

	c := echo.New().NewContext(req, rec)

	s := &Server{pool}

	err := s.CreateSignup(c)
	assert.Nil(t, err)

	res := new(CreationResponse)
	json.Unmarshal([]byte(rec.Body.String()), res)
	assert.True(t, res.Created.Before(time.Now()))

	body = bytes.NewReader([]byte(request))
	req = httptest.NewRequest(http.MethodPost, "/signups", body)
	req.Header.Set("Content-Type", "application/json")
	rec = httptest.NewRecorder()
	c = echo.New().NewContext(req, rec)
	err = s.CreateSignup(c)
	e, ok := err.(*echo.HTTPError)
	assert.True(t, ok)
	assert.Equal(t, e.Code, 400)
	assert.Contains(t, e.Message, "already")
}

func TestSignupErrorsOnEmptyBody(t *testing.T) {
	pool := testPool()
	defer pool.Close()

	mustExec(t, pool, setupSql)

	request := ``
	body := bytes.NewReader([]byte(request))

	req := httptest.NewRequest(http.MethodPost, "/signups", body)
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()

	c := echo.New().NewContext(req, rec)

	s := &Server{pool}

	err := s.CreateSignup(c)
	e, ok := err.(*echo.HTTPError)
	assert.True(t, ok)
	assert.Equal(t, e.Code, 400)
	assert.Contains(t, e.Message, "not valid")
}

func TestEventsPost(t *testing.T) {
	pool := testPool()
	defer pool.Close()

	mustExec(t, pool, setupSql)

	request := `{"subtype": "baz", "tracking_data": { "foo": "bar" }}`
	body := bytes.NewReader([]byte(request))

	req := httptest.NewRequest(http.MethodPost, "/events", body)
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()

	c := echo.New().NewContext(req, rec)

	s := &Server{pool}

	err := s.CreateEvent(c)
	assert.Nil(t, err)

	res := new(CreationResponse)
	json.Unmarshal([]byte(rec.Body.String()), res)
	assert.True(t, res.Created.Before(time.Now()))
}
