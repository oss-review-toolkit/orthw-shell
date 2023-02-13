# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

import os

from orthw.commandbase import CommandBase, command_group


# ----------------------------------
# Command Line options and arguments


class CleanCommand(CommandBase):
    """orthw commnand - clean"""

    _command_name: str = "clean"

    def __init__(self) -> None:
        pass

    def process(self) -> None:
        try:
            dotdir = self.config.get("dotdir")
            if dotdir and dotdir.is_dir():
                os.removedirs(dotdir)
                self.log.info(f"Removed directory {dotdir}")
        except OSError:
            self.log.error(f"Removing directory {dotdir}")
        try:
            config_file = self.config.get("repository_configuration_file")
            if config_file and config_file.is_file():
                config_file.unlink(missing_ok=True)
                self.log.info(f"Removed file {config_file}")
        except OSError:
            self.log.error(f"Error removing directory {self.config.get('repository_configuration_file')}")


@command_group.command()
def clean() -> None:
    CleanCommand().process()
