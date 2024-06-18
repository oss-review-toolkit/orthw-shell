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
# License-Filename: LICENSE
from __future__ import annotations

import io
from collections.abc import Callable
from typing import Any, overload

import click
from click.core import _check_multicommand
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
            f"[bright_green]Main config::[/bright_green] {config.configfile}\n"
            f"[bright_green]Configuration home:[/bright_green] {config.configuration_home}\n"
            f"[bright_green]Ort home:[/bright_green] {config.ort_home}\n"
            f"[bright_green]Scancode home:[/bright_green] {config.scancode_home}\n"
            f"[bright_green]Exports home:[/bright_green] {config.exports_home}\n"
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

            context: str | None = None
            alias: str | None = None
            if "obj" in cmd.context_settings:
                if "orthw_context" in cmd.context_settings["obj"]:
                    context = cmd.context_settings["obj"]["orthw_context"]
                if "alias" in cmd.context_settings["obj"]:
                    alias = cmd.context_settings["obj"]["alias"]

            if context in custom_cmd:
                # Ignore if is an alias ( but is registered already)
                if alias == subcommand:
                    continue
                cmd_description = {}
                cmd_description["short_help"] = cmd.short_help if cmd.short_help else ""
                cmd_description["subcommand"] = subcommand
                custom_cmd[context]["content"].append(cmd_description)

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

    def add_command(
        self,
        cmd: click.Command,
        name: str | None = None,
        alias: bool = False,
    ) -> None:
        """Registers another :class:`Command` with this group.  If the name
        is not provided, the name of the command is used.
        """
        name = name or cmd.name

        if alias:
            if "obj" in cmd.context_settings:
                cmd.context_settings["obj"]["alias"] = name
            else:
                cmd.context_settings["obj"] = {"alias": name}
        if name is None:
            raise TypeError("Command has no name.")

        _check_multicommand(self, name, cmd, register=True)
        self.commands[name] = cmd

    @overload
    def command(self, __func: Callable[..., Any]) -> click.Command: ...

    @overload
    def command(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Callable[[Callable[..., Any]], click.Command]: ...

    def command(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Callable[[Callable[..., Any]], click.Command] | click.Command:
        from click.decorators import command

        func: Callable[..., Any] | None = None

        if args and callable(args[0]):
            assert (  # noqa: S101
                len(args) == 1 and not kwargs
            ), "Use 'command(**kwargs)(callable)' to provide arguments."
            (func,) = args
            args = ()

        if self.command_class and kwargs.get("cls") is None:
            kwargs["cls"] = self.command_class

        def decorator(f: Callable[..., Any]) -> click.Command:
            context: str | None = kwargs.pop("context") if "context" in kwargs else None
            cmd: click.Command = command(*args, **kwargs)(f)

            if context:
                if "obj" in cmd.context_settings:
                    cmd.context_settings["obj"]["orthw_context"] = context
                else:
                    cmd.context_settings["obj"] = {"orthw_context": context}

            self.add_command(cmd)
            return cmd

        if func is not None:
            return decorator(func)

        return decorator

    @overload
    def group(self, __func: Callable[..., Any]) -> click.Group:
        pass

    @overload
    def group(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Callable[[Callable[..., Any]], click.Group]:
        pass

    def group(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Callable[[Callable[..., Any]], click.Group] | click.Group | None:
        from click.decorators import group

        func: Callable[..., Any] | None = None

        if args and callable(args[0]):
            assert len(args) == 1 and not kwargs, "Use 'group(**kwargs)(callable)' to provide arguments."  # noqa: S101
            (func,) = args
            args = ()

        if self.group_class is not None and kwargs.get("cls") is None:
            if self.group_class is type:
                kwargs["cls"] = type(self)
            else:
                kwargs["cls"] = self.group_class

        def decorator(f: Callable[..., Any]) -> click.Group:
            context: str | None = kwargs.pop("context") if "context" in kwargs else None
            cmd: click.Group = group(*args, **kwargs)(f)

            if context:
                if "obj" in cmd.context_settings:
                    cmd.context_settings["obj"]["orthw_context"] = context
                else:
                    cmd.context_settings["obj"] = {"orthw_context": context}

            self.add_command(cmd)
            return cmd

        if func is not None:
            return decorator(func)

        return decorator
