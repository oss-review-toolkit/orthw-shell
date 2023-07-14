# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro
from __future__ import annotations

from rich import print

from orthw.commands import command_group


class OrtHWCommand:
    """orthw command - analyze-in-docker"""

    _command_name: str = "analyze-in-docker"

    def process(self) -> None:
        print("\n[sandy_brown]This command is not implemented yet.[/sandy_brown]")


@command_group.command(
    context_settings={"orthw_group": "NO_SCAN_CONTEXT"},
)
def analyze_in_docker() -> None:
    OrtHWCommand().process()
