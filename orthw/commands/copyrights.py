# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

from rich import print

from orthw.commandbase import CommandBase, command_group


# ----------------------------------
# Command Line options and arguments


class OrtHWCommand(CommandBase):
    """orthw command - copyrights"""

    _command_name: str = "copyrights"

    def process(self) -> None:
        print("\n[sandy_brown]This command is not implemented yet.[/sandy_brown]")


@command_group.command()
def copyrights() -> None:
    OrtHWCommand().process()
