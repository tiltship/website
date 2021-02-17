from datetime import datetime

import psycopg2
import pytest

from consumer import Consumer, ConsumerWorkError


@pytest.fixture()
def db():
    with psycopg2.connect(
        dbname="defaultdb", user="root", host="localhost", port="5433"
    ) as conn:
        with conn.cursor() as cur:
            q = """
            CREATE DATABASE IF NOT EXISTS test;
            USE test;
            """
            cur.execute(q)
            conn.commit()

            yield (conn, cur)

            q = """
            DROP DATABASE test;
            """
            cur.execute(q)
            conn.commit()


def test_consumer_no_commits_returns_unix_start(db):
    conn, cur = db
    consumer = Consumer(conn, "foo", "offsets")
    cur.execute(consumer.create_query)
    conn.commit()

    offset = consumer.get_offset()
    assert offset == datetime(1970, 1, 1)


def test_consumer_creates_table_if_not_exists(db):
    conn, _ = db

    consumer = Consumer(conn, "foo", "offsets")
    offset = consumer.get_offset()
    assert offset == datetime(1970, 1, 1)

    offset = consumer.get_offset()
    assert offset == datetime(1970, 1, 1)


def test_consumer_returns_last_commit(db):
    conn, _ = db
    consumer = Consumer(conn, "foo", "offsets")

    new_offset = consumer.new_offset()
    consumer.commit(new_offset)

    offset = consumer.get_offset()
    assert offset == new_offset


def test_consumer_passes_offsets_to_work_fn(db):
    conn, _ = db
    consumer = Consumer(conn, "foo", "offsets")

    new_offset = consumer.new_offset()
    consumer.commit(new_offset)

    def work(old, new):
        assert old == new_offset

    consumer.do_work(work)


def test_consumer_throws_consumer_work_error_on_exception(db):
    conn, _ = db
    consumer = Consumer(conn, "foo", "offsets")

    new_offset = consumer.new_offset()
    consumer.commit(new_offset)

    def work(old, new):
        assert old != new_offset

    with pytest.raises(ConsumerWorkError):
        consumer.do_work(work)
