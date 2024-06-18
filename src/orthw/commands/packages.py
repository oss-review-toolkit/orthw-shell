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

from rich import print

from pathlib import Path

import click

from orthw import config
from orthw.utils import logging
from orthw.utils.cmdgroups import command_group
from orthw.utils.process import run
from orthw.utils.required import require_initialized


def packages() -> None:
    require_initialized()

    scan_result_file: Path = config.scan_result_file

    args: list[str] = [
        "orth",
        "list-packages",
        "--ort-file",
        scan_result_file.as_posix()
    ]

    run(args=args)

@command_group.command(
    context="SCAN_CONTEXT",
    name="packages",
    help="Lists ids of the packages within initialized ORT result file.",
    short_help="List ids of the packages within initialized ORT result file."
)
def __packages() -> None:
    packages()
