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

from pathlib import Path

import click

from orthw.utils.cmdgroups import command_group
from orthw.utils.database import PostgresConfig
from orthw.utils.process import run


def create_analyzer_results(package_ids_file: Path) -> None:
    # Get database config
    scandb = PostgresConfig()

    args: list[str] = [
        "orth",
        "create-analyzer-result",
        "--package-ids-file",
        package_ids_file.as_posix(),
        "-P",
        f"ort.scanner.storages.postgres.connection.url=jdbc:postgresql://{scandb.pg_host}:{scandb.pg_port}/{scandb.pg_db}",
        "-P",
        f"ort.scanner.storages.postgres.connection.schema={scandb.pg_schema}",
        "-P",
        f"ort.scanner.storages.postgres.connection.username={scandb.pg_user}",
        "-P",
        f"ort.scanner.storages.postgres.connection.password={scandb.pg_password}",
        "-P",
        "ort.scanner.storages.postgres.connection.sslmode=require",
        "--ort-file",
        "./synthetic-analyzer-result.json"
    ]

    run(args=args)


@command_group.command(
    context="NO_SCAN_CONTEXT",
    name="create-analyzer-results"
)
@click.argument("package-ids-file", type=click.Path(exists=True))
def __create_analyzer_results(package_ids_file: Path) -> None:
    create_analyzer_results(package_ids_file)
