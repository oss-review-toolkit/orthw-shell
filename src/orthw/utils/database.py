# Copyright 2023 The ORTHW Project Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# License-Filename: LICENSE
from __future__ import annotations

import sys

import psycopg2
from psycopg2.sql import Literal
from pydantic import BaseModel
from rich.pretty import pprint

from orthw import config
from orthw.utils import admin, logging


class PostgresConfig(BaseModel):
    pg_db: str | None = config.scandb_db
    pg_host: str | None = config.scandb_host
    pg_port: str | None = config.scandb_port
    pg_schema: str | None = config.scandb_schema
    pg_user: str | None = config.scandb_user
    pg_password: str | None = config.scandb_password

    def __init__(self) -> None:
        for key, value in self.__dict__.items():
            if value is None:
                logging.error(f"No env value [bright_white]SCANDB_{key.upper()}[/] !")
                sys.exit(1)


def query_scandb(sql: Literal) -> list[tuple[str, str]] | None:
    if admin():
        logging.error("This script is not allowed to run as admin.")
        sys.exit(1)

    scandb = PostgresConfig()

    try:
        conn = psycopg2.connect(
            database=scandb.pg_db,
            user=scandb.pg_user,
            password=scandb.pg_password,
            host=scandb.pg_host,
            port=scandb.pg_port,
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
    safe_pid = Literal(package_id)
    sql: Literal[str] = Literal(
        "SELECT ROW_NUMBER() OVER (ORDER BY identifier) as index,identifier"
        f"FROM scan_results WHERE identifier LIKE {safe_pid}",
    )

    pprint(query_scandb(sql))
