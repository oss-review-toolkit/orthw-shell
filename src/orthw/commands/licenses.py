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

import click

from orthw import config
from orthw.commands import command_group
from orthw.utils.process import run
from orthw.utils.required import require_initialized


class Command:
    """orthw command - licenses"""

    _command_name: str = "licenses"

    def licenses(self, package_id: str, source_code_dir: str | None = None) -> None:
        """licenses

        :param package_id: Id of package
        :type package_id: str
        """

        require_initialized()

        args: list[str] = [
            "ort",
            "list-licenses",
            "--package-id",
            package_id,
            "--apply-license-finding-curations",
            "--omit-excluded",
        ]

        evaluation_result_file: str = config.get("evaluation_result_file")
        args += ["--ort-file", evaluation_result_file]

        repository_configuration_file: str = config.get("repository_configuration_file")
        args += ["--repository-configuration-file", repository_configuration_file]

        ort_config_package_configuration_dir: str = config.get("ort_config_package_configuration_dir")
        args += ["--package-configuration-dir", ort_config_package_configuration_dir]

        if source_code_dir:
            args += ["--source-code-dir", source_code_dir]

        # Execute external run
        run(args=args)


@command_group.command(
    context_settings={"orthw_group": "SCAN_CONTEXT"},
)
@click.option("--source-code-dir", default=None)
@click.argument("package_id")
def licenses(package_id: str, source_code_dir: str | None) -> None:
    Command().licenses(package_id, source_code_dir=source_code_dir)
