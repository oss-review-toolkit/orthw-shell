# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

import click

import logging


class CommandBase:
    """orthw command base class"""

    _command_name: str = "Base Class"

    def __init__(self) -> None:
        logging.debug(f"Initialized command {self._command_name}")


@click.group()
def command_group() -> None:
    pass
