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


def find(package_id: str) -> str:
    require_initialized()

    ort_config_package_configurations_dir: Path = config.ort_config_package_configurations_dir

    args: list[str] = [
        "orth",
        "package-configuration",
        "find",
        "--package-configurations-dir",
        ort_config_package_configurations_dir.as_posix(),
        "--package-id",
        package_id
    ]

    run(args=args)


@package_config_group.command(
    context="PACKAGE_CONFIG",
    name="find",
    help="""
        Searches ort configuration for a package configurations given package id.

        Examples:

        orthw package-config find Maven:org.apache.curator:curator-framework:2.13.0
    """,
    short_help="Searches ort configuration for a package configurationfors with given package id."
)
@click.argument("package_id")
def __find(package_id: str) -> None:
    """Searches ort configuration for a package configurationfors with given package id."""
    find(package_id=package_id)
