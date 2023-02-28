# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

import os

from orthw.commandbase import CommandBase, command_group
from orthw.utils import logging


# ----------------------------------
# Command Line options and arguments


class Command(CommandBase):
    """orthw commnand - clean"""

    _command_name: str = "clean"

    def __init__(self) -> None:
        pass

    def process(self) -> None:
        try:
            dotdir = self.config.get("dotdir")
            if dotdir and dotdir.is_dir():
                os.removedirs(dotdir)
                logging.info(f"Removed directory {dotdir}")
        except OSError:
            logging.error(f"Removing directory {dotdir}")
        try:
            config_file = self.config.get("repository_configuration_file")
            if config_file and config_file.is_file():
                config_file.unlink(missing_ok=True)
                logging.info(f"Removed file {config_file}")
        except OSError:
            logging.error(f"Error removing directory {self.config.get('repository_configuration_file')}")


@command_group.command()
def clean() -> None:
    Command().process()
