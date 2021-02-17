from typing import Iterator

import psycopg2
from environs import Env
from google.ads.google_ads.client import GoogleAdsClient
from psycopg2.extensions import connection

from consumer import Consumer
from google_clicks import create_click_conversion


def query(conn: connection, q: str, vals: tuple = ()) -> Iterator[tuple]:
    with conn:
        with conn.cursor() as cur:
            cur.execute(q, vals)
            for record in cur:
                yield record


def report_conversions(conn, client, customer_id, old, new):
    q = """
        SELECT created, tracking_data->>'gclid'
        FROM signups
        WHERE created > %s
        AND created <= %s
        AND tracking_data->>'gclid' IS NOT NULL
    """

    rows = query(conn, q, (old, new))

    for created, gclid in rows:
        # TODO: handle google errors
        res = create_click_conversion(client, customer_id, "ts_signup", gclid, created)
        print(res)


def main():
    env = Env()

    conn = psycopg2.connect(
        dbname=env("PG_DATABASE"),
        user=env("PG_USER"),
        host=env("PG_HOST"),
        port=env("PG_PORT"),
        password=env("PG_PASSWORD"),
    )

    conf_path = env("GOOGLE_ADS_YAML_PATH")
    consumer = Consumer(conn, "signups_ga", "event_consumer_groups")
    client = GoogleAdsClient.load_from_storage(conf_path)
    customer_id = env("GOOGLE_CUSTOMER_ID")

    work = lambda o, n: report_conversions(conn, client, customer_id, o, n)
    consumer.do_work(work)


if __name__ == "__main__":
    main()
