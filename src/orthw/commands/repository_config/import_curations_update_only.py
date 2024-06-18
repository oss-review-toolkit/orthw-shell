# Copyright 2024 The ORTHW Project Authors
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



def import_curations_update_only() -> None:
    require_initialized()

    exports_license_finding_curations_file: Path = config.exports_license_finding_curations_file
    scan_result_file: Path = config.scan_result_file
    repository_configuration_file: Path = config.repository_configuration_file

    args: list[str] = [
        "orth",
        "repository-configuration",
        "import-license-finding-curations",
        "--license-finding-curations-file",
        exports_license_finding_curations_file,
        "--ort-file".
        scan_result_file.as_posix(),
        "--repository-configuration-file",
        repository_configuration_file.as_posix(),
        "--update-only-existing"
    ]

    run(args=args)


@repository_group.command(
    context="REPOSITORY_CONFIG",
    name="import-curations-update-only",
    help="Imports license finding curations from {file} to update existing entries in the ort.yml file."
        .format(file=config.exports_license_finding_curations_file),
    short_help="Imports license finding curations from {file} to update existing entries in the ort.yml file."
        .format(file=config.exports_license_finding_curations_file)
)
def __import_curations_update_only() -> None:
    """Import license finding curations from a file to update existing entries in the ort.yml file."""
    import_curations_update_only()
