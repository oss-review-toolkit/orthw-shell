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


def create(package_id: str) -> None:
    require_initialized()

    scan_results_storage_dir: Path = config.scan_results_storage_dir
    ort_config_license_classifications_file: Path = config.ort_config_license_classifications_file
    non_offending_license_categories: str = config.non_offending_license_categories
    non_offending_license_ids: str = config.non_offending_license_ids
    ort_config_package_configurations_dir: Path = config.ort_config_package_configurations_dir

    args: list[str] = [
        "orth",
        "package-configuration",
        "create",
        "--scan-results-storage-dir",
        scan_results_storage_dir.as_posix(),
        "--package-id",
        package_id,
        "--create-hierarchical-dirs",
        "--generate-path-excludes",
        "--license-classifications-file",
        ort_config_license_classifications_file,
        "--non-offending-license-categories",
        "'" + non_offending_license_categories + "'",
        "--non-offending-license-ids",
        "'" + non_offending_license_ids + "'",
        "--output-dir",
        ort_config_package_configurations_dir.as_posix(),
        "--force-overwrite"
    ]

    run(args=args)


@package_config_group.command(
    context="PACKAGE_CONFIG",
    name="create",
    help="""
        Creates one package configuration for given package id, if a corresponding scan result exists.

        Examples:

        orthw package-config create Maven:org.apache.curator:curator-framework:2.13.0
    """,
    short_help="Creates one package configuration for given package id."
)
@click.argument("package_id")
def __create(package_id: str) -> None:
    """Creates one package configuration for given package id."""
    create(package_id=package_id)
