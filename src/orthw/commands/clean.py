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

from pathlib import Path

from orthw import config
from orthw.commands import command_group
from orthw.utils import logging


class Command:
    """orthw commnand - clean"""

    _command_name: str = "clean"

    def process(self) -> None:
        try:
            dot_dir = Path(config.get("dot_dir"))
            if dot_dir and dot_dir.is_dir():
                print(dot_dir)
                logging.info(f"Removed directory {dot_dir}")
        except OSError:
            logging.error(f"Removing directory {dot_dir}")
        try:
            config_file = Path(config.get("repository_configuration_file"))
            if config_file and config_file.is_file():
                config_file.unlink(missing_ok=True)
                logging.info(f"Removed file {config_file}")
        except OSError:
            logging.error(f"Error removing directory {config.get('repository_configuration_file')}")


@command_group.command(
    context_settings={"orthw_group": "SCAN_CONTEXT"},
    short_help="Clean arifact outputs.",
)
def clean() -> None:
    Command().process()
