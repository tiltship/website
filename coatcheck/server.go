package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/caarlos0/env/v6"
	"github.com/jackc/pgconn"
	"github.com/jackc/pgx/v4/pgxpool"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

type SignupRequest struct {
	Email        string          `json:"email"`
	TrackingData json.RawMessage `json:"tracking_data"`
}

type Server struct {
	pool *pgxpool.Pool
}

func (s *Server) Health(c echo.Context) error {
	return c.String(http.StatusOK, "we good")
}

func (s *Server) CreateSignup(c echo.Context) error {
	signup := new(SignupRequest)
	if err := c.Bind(signup); err != nil {
		return err
	}

	query := `INSERT INTO signups(email, tracking_data) values($1, $2)`
	_, err := s.pool.Exec(context.Background(), query, signup.Email, signup.TrackingData)

	if e, ok := err.(*pgconn.PgError); ok {
		switch e.Code {
		case "23514":
			return echo.NewHTTPError(http.StatusBadRequest, "Signup data was not valid.")
		case "23505":
			return echo.NewHTTPError(http.StatusBadRequest, "We already have a signup from this email!")
		default:
		}
	}

	if err != nil {
		return err
	}

	return c.JSON(http.StatusCreated, signup)

}

func getPool(cfg *Config) *pgxpool.Pool {
	conString := fmt.Sprintf("postgresql://%s@%s:%s/%s?sslmode=disable", cfg.User, cfg.Host, cfg.Port, cfg.Db)
	config, err := pgxpool.ParseConfig(conString)
	handle(err)

	config.MaxConns = int32(32)

	ctx := context.Background()
	pool, err := pgxpool.ConnectConfig(ctx, config)
	handle(err)

	return pool
}

type Config struct {
	Db       string `env:"PG_DATABASE,required"`
	User     string `env:"PG_USER,required"`
	Password string `env:"PG_PASSWORD,required"`
	Host     string `env:"PG_HOST,required"`
	Port     string `env:"PG_PORT,required"`
}

func getConfig() Config {
	cfg := Config{}
	err := env.Parse(&cfg)
	handle(err)
	return cfg
}

func handle(err error) {
	if err != nil {
		log.Fatal(err)
	}
}

func main() {
	cfg := getConfig()
	pool := getPool(&cfg)

	server := &Server{pool}

	e := echo.New()
	e.Use(middleware.CORS())
	e.POST("/signups", server.CreateSignup)
	e.GET("/health", server.Health)

	e.Logger.Fatal(e.Start(":1323"))
}
