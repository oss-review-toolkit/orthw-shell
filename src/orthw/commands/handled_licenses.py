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

from orthw import config
from orthw.utils.cmdgroups import command_group
from orthw.utils.process import run


def handled_licenses() -> None:
    """_summary_"""

    args: list[str] = [
        "orth",
        "list-license-categories",
        "--license-classifications-file",
        config.ort_config_license_classifications_file.as_posix(),
    ]

    run(args)


@command_group.command(
    context="NO_SCAN_CONTEXT",
    name="handled-licenses"
)
def __handled_licenses() -> None:
    handled_licenses()
