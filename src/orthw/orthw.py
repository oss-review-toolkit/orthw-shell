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

import importlib
import pkgutil
import sys
from pathlib import Path

import click

from orthw.utils import logging
from orthw.utils.cmdgroups import command_group
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
                self.module_import(path)

    def module_import(self, path: Path) -> None:
        """Iterate over the commands directory and import the commands

        Args:
            path (Path): Start path to iterate
        """
        for command in path.iterdir():
            if command.is_file():
                command_name = command.stem
                import_path = command.parent.as_posix()[command.as_posix().index("commands") :].replace("/", ".")
                # We expect that we will find the commands under orthw.commands
                importlib.import_module(f"orthw.{import_path}.{command_name}")
            elif command.is_dir():
                # Ignore pycache
                if command.stem == "__pycache__":
                    continue
                self.module_import(command)

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
