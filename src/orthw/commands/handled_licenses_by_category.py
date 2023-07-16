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

from orthw import config
from orthw.commands import command_group
from orthw.utils.process import run


class Command:
    """orthw command - handled-licenses"""

    _command_name: str = "handled-licenses"

    def process(self) -> None:
        """_summary_"""

        args: list[str] = [
            "orth",
            "list-license-categories",
            "--license-classifications-file",
            config.get("ort_config_license_classifications_file"),
            "--group-by-category",
        ]

        run(args)


@command_group.command(
    context_settings={"orthw_group": "NO_SCAN_CONTEXT"},
)
def handled_licenses_by_category() -> None:
    Command().process()
