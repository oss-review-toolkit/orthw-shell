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

from pathlib import Path

from orthw import config
from orthw.utils import logging
from orthw.utils.cmdgroups import package_config_group
from orthw.utils.process import run
from orthw.utils.required import require_initialized


def clean(package_id: str) -> None:
    require_initialized()

    package_configuration_file: Path = "FIXME find_package(package_id)"
    scan_result_file: Path = config.evaluation_result_file

    args: list[str] = [
        "orth",
        "package-configuration",
        "remove-entries",
        "--package-configuration-file".
        package_configuration_file,
        "--ort-file",
        ort_config_resolutions_file.as_posix()
    ]

    run(args=args)


@package_config_group.command(
    context="PACKAGE_CONFIG",
    name="clean",
    help="""
        Removes all path excludes and license finding curations from package configuration file
        which do not match any files or license findings.
    """,
    short_help="Removes all excludes and curations from package configuration file which do not match any findings.",
)
@click.argument("package_id")
def __clean(package_id: str) -> None:
    """Removes all excludes and curations from package configuration file which do not match any findings."""
    clean(package_id=package_id)
