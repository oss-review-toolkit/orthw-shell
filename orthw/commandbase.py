# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

import click
import logging as stdlogger

from orthw.config import Config
from orthw.utils import logging
from orthw.utils.orthwclickgroup import OrthwClickGroup


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
        logging.setLevel(stdlogger.DEBUG)
