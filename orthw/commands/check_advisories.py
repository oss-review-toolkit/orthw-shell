# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

from orthw.commandbase import CommandBase, command_group

# ----------------------------------
# Command Line options and arguments


class CheckAdvisoriesCommand(CommandBase):
    """orthw commnand - check-advisories"""

    _command_name: str = "check-advisories"

    def __init__(self) -> None:
        pass


@command_group.command()
def check_advisories() -> None:
    CheckAdvisoriesCommand().process()
