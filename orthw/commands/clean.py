# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

import logging

import click

from orthw.commandbase import CommandBase, command_group

# ----------------------------------
# Command Line options and arguments


class CheckAdvisoriesCommand(CommandBase):
    """orthw commnand - clean"""

    _command_name: str = "check-advisories"


@command_group.command()
@click.option("-d", "--debug", is_flag=True)
def check_advisories(debug: bool) -> None:
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        CheckAdvisoriesCommand()
