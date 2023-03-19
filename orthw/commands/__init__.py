# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

import logging as stdlogger

import click

from orthw.utils import logging
from orthw.utils.orthwclickgroup import OrthwClickGroup


@click.group(cls=OrthwClickGroup)
@click.option("-d", "--debug/--no-debug", default=False)
def command_group(debug: bool) -> None:
    if debug:
        logging.setLevel(stdlogger.DEBUG)
