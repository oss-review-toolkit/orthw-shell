# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

from rich import print

from orthw.commands import command_group


# ----------------------------------
# Command Line options and arguments


class OrtHWCommand:
    """orthw command - rc-generate-timeout-error-resolutions"""

    _command_name: str = "rc-generate-timeout-error-resolutions"

    def process(self) -> None:
        print("\n[sandy_brown]This command is not implemented yet.[/sandy_brown]")


@command_group.command()
def rc_generate_timeout_error_resolutions() -> None:
    OrtHWCommand().process()
