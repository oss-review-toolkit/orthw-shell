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
import git
import git.repo

from orthw import config
from orthw.utils.cmdgroups import command_group


def find_license_url(license_id: str) -> str:
    if license_id.startswith("LicenseRef-scancode-"):
        key = license_id.strip("LicenseRef-scancode-")
        license_file_path = f"src/licensedcode/data/licenses/{key}.LICENSE"

        license_file: Path = config.scancode_home / license_file_path
        if license_file.exists():
            git_repo = git.repo.Repo(config.scancode_home.as_posix())
            revision = git_repo.git.rev_parse("HEAD")
            return f"https://github.com/nexB/scancode-toolkit/blob/{revision}/{license_file_path}"

    return f"https://spdx.org/licenses/{license_id}.html"


@command_group.command(
    name="find-license-url",
    context="NO_SCAN_CONTEXT",
)
@click.argument("license-id")
def __find_license_url(license_id: str) -> None:
    find_license_url(license_id=license_id)
