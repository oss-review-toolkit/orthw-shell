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

exports_path_excludes_file: Path = config.exports_path_excludes_file

def import_path_excludes() -> None:
    require_initialized()

    scan_result_file: Path = config.scan_result_file
    repository_configuration_file: Path = config.repository_configuration_file
    exports_vcs_url_mapping_file: Path = config.exports_vcs_url_mapping_file

    args: list[str] = [
        "orth",
        "repository-configuration",
        "import-path-excludes",
        "--path-excludes-file",
        exports_path_excludes_file.as_posix(),
        "--ort-file".
        scan_result_file.as_posix(),
        "--repository-configuration-file",
        repository_configuration_file.as_posix(),
        "--vcs-url-mapping-file",
        exports_vcs_url_mapping_file.as_posix()
    ]

    run(args=args)


@repository_group.command(
    context="REPOSITORY_CONFIG",
    name="import-path-excludes",
    help="Imports path excludes by repository from {file} into the ort.yml file."
        .format(file=config.exports_license_finding_curations_file),
    short_help="Import path excludes by repository from {file} into the ort.yml file."
        .format(file=config.exports_license_finding_curations_file)
)
def __import_path_excludes() -> None:
    """Imports path excludes by repository from a file into the ort.yml file."""
    import_path_excludes()
