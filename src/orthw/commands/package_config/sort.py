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


def sort_(package_id: str) -> None:
    require_initialized()

    args: list[str] = [
        "orth",
        "package-configuration",
        "sort",
        package_configuration_file
    ]

    run(args=args)

    print("Sorted entries in repository configuration file " + repository_configuration_file + ".")


@package_config_group.command(
    context="PACKAGE_CONFIG",
    name="sort",
    help="""
        Sorts alphabetically the excludes and curation entries of the package configuration file
        for given package id.

        Examples:

        orthw package-config sort Maven:org.apache.curator:curator-framework:2.13.0
    """,
    short_help="Sorts alphabetically entries of the package configuration file for given package id."
)
@click.argument("package_id")
def __sort(package_id: str) -> None:
    """Sorts alphabetically entries of the package configuration file for given package id."""
    sort_(package_id=package_id)
