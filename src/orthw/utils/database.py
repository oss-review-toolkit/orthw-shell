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
from dict2obj import Dict2Obj
from rich.pretty import pprint

from orthw import config
from orthw.utils import admin, logging


def query_scandb(sql: str) -> list[tuple[str, str]] | None:
    if admin():
        logging.error("This script is not allowed to run as admin.")
        sys.exit(1)

    scandb = ort_postgres_config()

    try:
        conn = psycopg2.connect(
            database=scandb.db,  # type: ignore
            user=scandb.user,  # type: ignore
            password=scandb.password,  # type: ignore
            host=scandb.host,  # type: ignore
            port=scandb.port,  # type: ignore
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
        "db": config.get("scandb_db"),
        "host": config.get("scandb_host"),
        "port": config.get("scandb_port"),
        "schema": config.get("scandb_schema"),
        "user": config.get("scandb_user"),
        "password": config.get("scandb_password"),
    }

    for key, value in scandb.items():
        if value is None:
            logging.error(f"No env value [bright_white]SCANDB_{key.upper()}[/] !")
            sys.exit(1)

    return Dict2Obj(scandb)
