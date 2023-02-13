# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

import logging

import click

from orthw.config import Config


class CommandBase:
    """orthw command base class"""

    _command_name: str = "Base Class"
    _log = logging.getLogger("rich")
    _config: Config = Config()

    def __init__(self) -> None:
        self.log.debug(f"Initialized command {self._command_name}")

    def process(self) -> None:
        self.log.warning("This command don't do anything at this moment.")

    @property
    def log(self) -> logging.Logger:
        return logging.getLogger("rich")

    @property
    def config(self) -> Config:
        """Return config object

        :return: Config object from OrtHW
        :rtype: Config
        """
        return self._config


@click.group()
@click.option("-d", "--debug/--no-debug", default=False)
def command_group(debug: bool) -> None:
    if debug:
        logging.getLogger("rich").setLevel(logging.DEBUG)
