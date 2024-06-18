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

from orthw import config
from orthw.utils import logging
from orthw.utils.cmdgroups import repository_group
from orthw.utils.process import run
from orthw.utils.required import require_initialized


def generate_project_excludes() -> None:
    require_initialized()

    scan_result_file: Path = config.scan_result_file
    repository_configuration_file: Path = config.repository_configuration_file

    args: list[str] = [
        "orth",
        "repository-configuration",
        "generate-project-excludes",
        "--ort-file".
        scan_result_file.as_posix(),
        "--repository-configuration-file",
        repository_configuration_file.as_posix()
    ]

    run(args=args)


@repository_group.command(
    context="REPOSITORY_CONFIG",
    name="generate-project-excludes",
    help="""
        Generates path excludes in the ort.yml file for all definition files which are not yet excluded.
    """,
    short_help="Generates path excludes in the ort.yml file for all definition files which are not yet excluded."
)
def ___generate_project_excludes() -> None:
    """Generates path excludes in the ort.yml file for all definition files which are not yet excluded."""
    generate_project_excludes()
