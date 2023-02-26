# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

import logging

import psycopg2
from rich.pretty import pprint

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


def list_scan_results(config: Config, package_id: str) -> None:
    # Prevent SQL injection with literals
    safe_pid = psycopg2.sql.Literal(package_id)
    sql = "SELECT ROW_NUMBER() OVER (ORDER BY identifier) as index,identifier"
    f"FROM scan_results WHERE identifier LIKE {safe_pid}"  # nosec B606

    pprint(query_scandb(config, sql))
