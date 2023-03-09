# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

from pathlib import Path

from orthw import config
from orthw.commandbase import CommandBase, command_group
from orthw.utils import logging


class Command(CommandBase):
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


@command_group.command()
def clean() -> None:
    Command().process()
