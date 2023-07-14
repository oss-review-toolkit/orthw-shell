# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro
from __future__ import annotations

import logging as stdlogger

import click

from orthw.__version__ import __version__
from orthw.utils import logging
from orthw.utils.orthwclickgroup import OrtHwClickGroup


@click.group(cls=OrtHwClickGroup)
@click.version_option(__version__, "-v", "--version", prog_name="OrthHW", message="%(prog)s version %(version)s")
@click.option("-d", "--debug/--no-debug", default=False, help="Enable debug mode.")
@click.option("--logfile", required=False, help="Set the log output to specified file.")
def command_group(debug: bool, logfile: str) -> None:
    if debug:
        logging.setLevel(stdlogger.DEBUG)
    if logfile:
        filehandler = stdlogger.FileHandler(
            logfile,
            mode="w",
            encoding="UTF-8",
        )
        if debug:
            filehandler.setLevel(stdlogger.DEBUG)
        logging.addHandler(filehandler)
