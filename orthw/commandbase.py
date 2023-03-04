# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

import click
import logging as stdlogger

from orthw.utils import logging
from orthw.utils.orthwclickgroup import OrthwClickGroup


class CommandBase:
    """orthw command base class"""

    _command_name: str = "Base Class"


@click.group(cls=OrthwClickGroup)
@click.option("-d", "--debug/--no-debug", default=False)
def command_group(debug: bool) -> None:
    if debug:
        logging.setLevel(stdlogger.DEBUG)
