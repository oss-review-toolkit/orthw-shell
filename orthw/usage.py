# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

import click
from rich.console import Console

from orthw.config import Config as OrtHWConfig


class OrthwClickGroup(click.Group):
    def format_usage(self, ctx: click.Context, formatter: click.HelpFormatter) -> None:
        config = OrtHWConfig(defaults_only=True)
        console = Console(force_terminal=True)
        console.print(
            "\n[bright_white]Usage:\n"
            "\nConfiguration:\n\n"
            f"[bright_green]configuration-home:[/bright_green] {config.config['configuration_home']}\n"
            f"[bright_green]ort-home:[/bright_green] {config.config['ort_home']}\n"
            f"[bright_green]scancode-home:[/bright_green] {config.config['scancode_home']}\n"
            f"[bright_green]exports_home:[/bright_green] {config.config['exports_home']}\n"
            "[/bright_white]"
        )
