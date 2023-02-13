# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

import logging

import click


class CommandBase:
    """orthw command base class"""

    _command_name: str = "Base Class"
    _log = logging.getLogger("rich")

    def __init__(self) -> None:
        self.log.debug(f"Initialized command {self._command_name}")

    @property
    def log(self) -> logging.Logger:
        return logging.getLogger("rich")


@click.group()
@click.option("-d", "--debug/--no-debug", default=False)
def command_group(debug: bool) -> None:
    if debug:
        logging.getLogger("rich").setLevel(logging.DEBUG)
