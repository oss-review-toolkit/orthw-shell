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

import click
from psycopg2 import sql
from rich import print

from orthw.utils.cmdgroups import command_group
from orthw.utils.database import list_scan_results, query_scandb


def delete_scan_results(package_id: str) -> None:
    # Prevent SQL injection assigning as literal
    safe_pid = sql.Literal(package_id)

    list_scan_results(package_id=package_id)

    count_sql: str = f"SELECT COUNT(*) FROM scan_results WHERE identifier LIKE '{safe_pid}'"  # nosec B608  # noqa: S608
    count: list[tuple[str, str]] | None = query_scandb(sql=count_sql)

    if not count:
        print("[bright_yellow]No results were found with this package id.[/bright_yellow]")

    print(f"[bright_blue]Found the above $count scan results for query string {package_id}.[/bright_blue]")
    print("[bright_blue]Press enter to delete them.[/bright_blue]")
    input()

    delete_sql: str = f"DELETE FROM scan_results WHERE identifier LIKE {safe_pid}"  # nosec B608  # noqa: S608
    query_scandb(sql=delete_sql)


@command_group.command(
    context="NO_SCAN_CONTEXT",
    name="delete-scan-results"
)
@click.argument("package_id")
def __delete_scan_results(package_id: str) -> None:
    delete_scan_results(package_id)
