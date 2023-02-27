# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

import logging
import shutil


required_commands = ["curl", "md5sum", "xz"]


def required_command(command: str) -> str | None:
    """Perform a check on system to see if the provided command is available

    :param command: Command to ve evaluated on system
    :type command: str
    :return: True or Falsed for command existence
    :rtype: bool
    """
    try:
        cmd = shutil.which(command)
        if not cmd:
            logging.error(f"Missing required command [bright_yellow]{command}[/].", extra={"markup": True})
        return cmd
    except shutil.Error as ex:
        logging.error(f"Something wrong went in the evaluation of {command} executable.\n", ex)
        return None


def bootstrap_commands() -> bool:
    """Check the necessry basic commands on start

    :return: _description_
    :rtype: bool
    """
    for command in required_commands:
        if not required_command(command):
            return False
    return True
