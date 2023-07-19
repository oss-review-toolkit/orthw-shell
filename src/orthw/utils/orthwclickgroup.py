# Copyright 2023 The ORTHW Project Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro
from __future__ import annotations

import io
from typing import Any

import click
from rich.box import HORIZONTALS
from rich.console import Console
from rich.padding import Padding
from rich.table import Table

from orthw import config


class OrtHwClickGroup(click.Group):
    def format_usage(self, ctx: click.Context, formatter: click.HelpFormatter) -> None:
        """Customization of usage output from Click

        Args:
            ctx (click.Context): Click main context
            formatter (click.HelpFormatter): The help formatter from Click
        """
        sio = io.StringIO()
        console = Console(file=sio, force_terminal=True)

        console.print(
            "\n[bright_white]Usage:\n"
            "\nConfiguration:\n\n"
            f"[bright_green]Main config::[/bright_green] {config.get('dot_dir')}/config.yml\n"
            f"[bright_green]Configuration home:[/bright_green] {config.get('configuration_home')}\n"
            f"[bright_green]Ort home:[/bright_green] {config.get('ort_home')}\n"
            f"[bright_green]Scancode home:[/bright_green] {config.get('scancode_home')}\n"
            f"[bright_green]Exports home:[/bright_green] {config.get('exports_home')}\n"
            "[/bright_white]",
        )

        formatter.write(sio.getvalue())

    def format_options(self, ctx: click.Context, formatter: click.HelpFormatter) -> None:
        """Customization of options output from Click

        Args:
            ctx (click.Context): Click main context
            formatter (click.HelpFormatter): The help formatter from Click
        """
        sio = io.StringIO()
        console = Console(file=sio, force_terminal=True)

        opts = []
        for param in self.get_params(ctx):
            rv = param.get_help_record(ctx)
            if rv is not None:
                opts.append(rv)
        if opts:
            with formatter.section("Options"):
                formatter.write_dl(opts)

        custom_cmd: dict[str, dict[str, Any]] = {
            "SCAN_CONTEXT": {"title": "Commands with scan context", "content": []},
            "NO_SCAN_CONTEXT": {"title": "Commands without scan context", "content": []},
            "REPOSITORY_CONFIG": {"title": "Commands for repository configurations (ort.yml)", "content": []},
            "PACKAGE_CONFIG": {"title": "Commands for package configurations", "content": []},
        }

        for subcommand in self.list_commands(ctx):
            cmd: click.Command | None = self.get_command(ctx, subcommand)

            if cmd is None or cmd.hidden:
                continue

            self.group

            if cmd.options_metavar and cmd.options_metavar in custom_cmd:
                cmd_description = {}
                cmd_description["short_help"] = cmd.short_help if cmd.short_help else ""
                cmd_description["subcommand"] = subcommand
                custom_cmd[cmd.options_metavar]["content"].append(cmd_description)

        for key, value in custom_cmd.items():
            if not len(value["content"]):
                continue
            table = Table(
                title=value["title"],
                title_style="bold yellow",
                title_justify="left",
                show_header=False,
                box=HORIZONTALS,
                min_width=80,
            )
            table.add_column(style="bold green")
            table.add_column()

            # console.rule(f"[bold bright_yellow]{header}:[/bold bright_yellow]\n")
            for group_cmd in value["content"]:
                table.add_row(group_cmd["subcommand"], group_cmd["short_help"])
            console.print(Padding(table, (1, 1)))

        formatter.write(sio.getvalue())
