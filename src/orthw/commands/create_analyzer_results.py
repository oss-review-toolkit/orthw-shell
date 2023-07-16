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
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro
from __future__ import annotations

from pathlib import Path

import click

from orthw import config
from orthw.commands import command_group
from orthw.utils import logging
from orthw.utils.database import ort_postgres_config
from orthw.utils.process import run


class Command:
    """orthw command - create-analyzer-results"""

    _command_name: str = "create-analyzer-results"

    def create_analyzer_results(self, package_ids_file: Path) -> None:
        scancode_version = config.env("SCANCODE_VERSION")
        if not scancode_version:
            logging.error("Missing [bright_white]SCANCODE_VERSION[/] env.")
            return

        # Get database config
        scandb = ort_postgres_config()

        args: list[str] = [
            "orth",
            "create-analyzer-result",
            "--package-ids-file",
            package_ids_file.as_posix(),
            "--scancode-version",
            scancode_version,
            "-P",
            "ort.scanner.storages.postgres.connection.url=jdbc:"
            f"postgresql://{scandb.host}:{scandb.port}/{scandb.db}",  # type: ignore
            "-P",
            f"ort.scanner.storages.postgres.connection.schema={scandb.schema}",  # type: ignore
            "-P",
            f"ort.scanner.storages.postgres.connection.username={scandb.user}",  # type: ignore
            "-P",
            f"ort.scanner.storages.postgres.connection.password={scandb.password}",  # type: ignore
            "-P",
            "ort.scanner.storages.postgres.connection.sslmode=require",
            "--ort-file",
            "./synthetic-analyzer-result.json",
        ]

        run(args=args)


@command_group.command(
    context_settings={"orthw_group": "NO_SCAN_CONTEXT"},
)
@click.argument("package-ids-file", type=click.Path(exists=True))
def create_analyzer_results(package_ids_file: Path) -> None:
    Command().create_analyzer_results(package_ids_file)
