# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

import importlib.util
import logging
import os
import sys
from pathlib import Path
from typing import Any, List

import click

from orthw.commands import command_group
from orthw.utils.required import bootstrap_commands


class OrtHw:
    """OrtHw main class"""

    _plugins: List[Any] = []

    def __init__(self) -> None:
        # Load plugins is specified
        cwd: Path = Path(__file__)
        os.chdir(cwd.parent)

        path = Path("commands")
        if not path.exists():
            logging.info("No commands found !")

        for command in path.iterdir():
            if command.is_file():
                command_name = command.stem
                # We expect that we will find the commands under the name commands/command.py
                spec = importlib.util.find_spec(f"orthw.commands.{command_name}")
                if spec is not None:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)  # type: ignore
                    self._plugins.append(module)

    def run(self) -> None:
        """Main function call"""
        if not bootstrap_commands():
            sys.exit(1)

    @property
    def commands(self) -> List[click.MultiCommand] | None:
        """Return the dynamic commands from plugins"""
        return command_group().commands()
