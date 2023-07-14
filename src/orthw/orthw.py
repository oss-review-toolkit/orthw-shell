# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro
from __future__ import annotations

import importlib
import pkgutil
import sys
from pathlib import Path

import click

from orthw.commands import command_group
from orthw.utils import logging
from orthw.utils.required import bootstrap_commands


class OrtHw:
    """OrtHw main class"""

    def __init__(self) -> None:
        """OrtHw command initialization as plugin"""

        # Check if we are in development mode
        # Then add local path to sys.path
        cwd = Path(__file__).parent
        if cwd.parent.as_posix() == "src":
            sys.path.append(cwd.as_posix())

        for module in pkgutil.iter_modules():
            if module.name.startswith("orthw") and hasattr(module.module_finder, "path"):
                path = Path(module.module_finder.path) / module.name / "commands"
                for command in path.iterdir():
                    if command.is_file():
                        command_name = command.stem
                        # We expect that we will find the commands under the name commands/command.py
                        importlib.import_module(f"orthw.commands.{command_name}")

    def run(self) -> int:
        """Main function call"""
        if not bootstrap_commands():
            return 1
        try:
            cli = click.CommandCollection(sources=command_group().commands())
            cli()
            return 0
        except Exception as e:
            logging.error(f"Error: {e}")
            return 1

    @property
    def commands(self) -> list[click.MultiCommand] | None:
        """Return the dynamic commands from plugins"""
        return command_group().commands()


def main() -> int:
    exit_code: int = OrtHw().run()
    return exit_code


if __name__ == "__main__":
    main()
