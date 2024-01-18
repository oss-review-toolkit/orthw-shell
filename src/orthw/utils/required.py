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

import shutil
import sys
from pathlib import Path

from orthw import config
from orthw.utils import logging

required_commands = ["md5sum"]


def required_command(command: str) -> str:
    """Perform a check on system to see if the provided command is available

    :param command: Command to ve evaluated on system
    :type command: str
    :return: Command or
    :rtype: bool
    """
    try:
        cmd = shutil.which(command)
        if not cmd:
            logging.error(f"Missing required command [bright_yellow]{command}[/].")
            sys.exit(1)
        return cmd
    except shutil.Error as ex:
        logging.error(f"Something wrong went in the evaluation of {command} executable.\n", ex)
        sys.exit(1)


def bootstrap_commands() -> bool:
    """Check the necessry basic commands on start

    :return: _description_
    :rtype: bool
    """
    return all(required_command(command) for command in required_commands)


def require_initialized() -> None:
    """Check the base config directories required for operations"""
    target_url_file: Path = config.target_url_file

    if target_url_file is None or not target_url_file.is_file():
        logging.error("The working directory is not initialized. Please run 'orthw init <target-url>' first.")
        sys.exit(1)
