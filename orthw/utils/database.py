# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

import logging

import psycopg2

from orthw.config import Config


def query_scandb(config: Config, sql: str) -> list[tuple[str, str]] | None:
    try:
        conn = psycopg2.connect(
            database=config.get("scandb_db"),
            user=config.get("scandb_user"),
            password=config.get("scandb_password"),
            host=config.get("scandb_host"),
            port=config.get("scandb_port"),
        )
    except psycopg2.Error as e:
        logging.error("Fail to connect to Postgres database.")
        logging.error(e.diag.message_primary)
        return None

    cursor = conn.cursor()
    cursor.execute(sql)

    # Get results from query
    data: list[tuple[str, str]] = cursor.fetchall()

    conn.close()

    return data
