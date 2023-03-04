# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

import sys

import psycopg2
from dict2obj import Dict2Obj
from rich.pretty import pprint

from orthw import config
from orthw.utils import logging


def query_scandb(sql: str) -> list[tuple[str, str]] | None:
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


def list_scan_results(package_id: str) -> None:
    # Prevent SQL injection with literals
    safe_pid = psycopg2.sql.Literal(package_id)
    sql = "SELECT ROW_NUMBER() OVER (ORDER BY identifier) as index,identifier"
    f"FROM scan_results WHERE identifier LIKE {safe_pid}"  # nosec B606

    pprint(query_scandb(sql))


def ort_postgres_config() -> object:
    scandb = {
        "db": config.env("SCANDB_DB"),
        "host": config.env("SCANDB_HOST"),
        "port": config.env("SCANDB_PORT"),
        "schema": config.env("SCANDB_SCHEMA"),
        "user": config.env("SCANDB_USER"),
        "password": config.env("SCANDB_PASSWORD"),
    }

    for key, value in scandb.items():
        if value is None:
            logging.error(f"No env value [bright_white]SCANDB_{key.upper()}[/] !", extra={"markup": True})
            sys.exit(1)

    return Dict2Obj(scandb)
