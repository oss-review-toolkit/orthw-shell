# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

import logging

import click

from orthw.config import Config
from orthw.utils.logging import log
from orthw.utils.usage import OrthwClickGroup


class CommandBase:
    """orthw command base class"""

    _command_name: str = "Base Class"
    _config: Config = Config()

    @property
    def config(self) -> Config:
        """Return config object

        :return: Config object from OrtHW
        :rtype: Config
        """
        return self._config


@click.group(cls=OrthwClickGroup)
@click.option("-d", "--debug/--no-debug", default=False)
def command_group(debug: bool) -> None:
    if debug:
        log.setLevel(logging.DEBUG)
