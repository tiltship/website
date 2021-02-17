from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Tuple

import psycopg2
from psycopg2.errors import UndefinedTable
from psycopg2.extensions import connection


class ConsumerWorkError(BaseException):
    pass


def query(conn: connection, q: str, vals: tuple = ()) -> List[Tuple]:
    with conn:
        with conn.cursor() as cur:
            cur.execute(q, vals)
            try:
                return [record for record in cur]
            except psycopg2.ProgrammingError:
                return []


@dataclass(frozen=True)
class Consumer:
    conn: connection
    name: str
    table: str
    delay_seconds: int = 30

    @property
    def create_query(self):
        return f"""
        CREATE TABLE IF NOT EXISTS {self.table}(
          consumer VARCHAR NOT NULL,
          consumer_offset TIMESTAMP NOT NULL,
          created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
          CONSTRAINT "consumer_offset_reasonable" CHECK (created > consumer_offset)
        )
        """

    def _query(self, q, vals=()):
        try:
            return query(self.conn, q, vals)
        except UndefinedTable:
            query(self.conn, self.create_query)
            return query(self.conn, q, vals)

    def get_offset(self) -> datetime:
        q = f"""
        SELECT consumer_offset FROM {self.table}
        WHERE consumer = %s
        ORDER BY created DESC
        LIMIT 1
        """

        try:
            (offset,) = self._query(q, (self.name,))[0]
            return offset
        except IndexError:
            return datetime(1970, 1, 1)

    def commit(self, new_offset):
        q = f"""
        INSERT INTO {self.table} (consumer, consumer_offset) VALUES(%s, %s)
        RETURNING consumer_offset
        """

        res = self._query(q, (self.name, new_offset))
        return res[0]

    def new_offset(self):
        return datetime.utcnow() - timedelta(seconds=self.delay_seconds)

    def consume(self):
        old_offset = self.get_offset()
        new_offset = self.new_offset()
        commit_fn = lambda: self.commit(new_offset)
        return old_offset, new_offset, commit_fn

    def do_work(self, work):
        old, new, cb = self.consume()
        try:
            work(old, new)
        except BaseException as e:
            raise ConsumerWorkError("Could not perform work") from e

        return cb()
