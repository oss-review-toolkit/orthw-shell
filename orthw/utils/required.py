# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

import shutil
import sys
from pathlib import Path

from orthw import config
from orthw.utils import logging

required_commands = ["curl", "md5sum", "xz"]


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
            logging.error(f"Missing required command [bright_yellow]{command}[/].", extra={"markup": True})
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
    for command in required_commands:
        if not required_command(command):
            return False
    return True


def require_initialized() -> None:
    """Check the base config directories required for operations"""
    dot_dir: Path | None = config.get("dot_dir")
    target_url_file: Path | None = config.get("target_url_file")
    scan_result_file: Path | None = config.get("scan_result_file")

    if (
        dot_dir is None
        or not dot_dir.is_dir()
        or target_url_file is None
        or not target_url_file.is_file()
        or scan_result_file is None
        or not scan_result_file.is_file()
    ):
        logging.error("The working directory is not initialized. Please run 'orthw init <target-url>' first.")
        sys.exit(1)
