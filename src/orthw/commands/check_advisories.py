# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro
from __future__ import annotations

from orthw.commands import command_group

# ----------------------------------
# Command Line options and arguments


class CheckAdvisoriesCommand:
    """orthw commnand - check-advisories"""

    _command_name: str = "check-advisories"

    def __init__(self) -> None:
        pass

    def process(self) -> None:
        pass


@command_group.command(
    context_settings={"orthw_group": "SCAN_CONTEXT"},
    short_help="Check the advisories.",
)
def check_advisories() -> None:
    CheckAdvisoriesCommand().process()
