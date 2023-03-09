# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

import click
from rich import print

from orthw.commandbase import CommandBase, command_group


# ----------------------------------
# Command Line options and arguments


class OrtHWCommand(CommandBase):
    """orthw command - init"""

    _command_name: str = "init"

    def init(self, source_code_dir: str) -> None:
        print("\n[sandy_brown]This command is not implemented yet.[/sandy_brown]")


@command_group.command()
@click.argument("source_code_dir", type=click.Path(exists=True))
def init(source_code_dir: str) -> None:
    OrtHWCommand().init(source_code_dir)
