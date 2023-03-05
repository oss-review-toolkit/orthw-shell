# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

from pathlib import Path

import click

from orthw import config
from orthw.commandbase import CommandBase, command_group
from orthw.utils import logging
from orthw.utils.process import run


class Command(CommandBase):
    """orthw command - analyze"""

    _command_name: str = "analyze"

    def analyze(self, source_code_dir: str, format: str = "JSON") -> None:
        """Use Ort analyzer command on provided source dir

        :param source_code_dir: Source directory to be evaluated
        :type source_code_dir: str
        """

        args: list[str] = [
            "ort",
            "analyze",
            "--input-dir",
            source_code_dir,
            "--output-dir",
            Path.cwd().as_posix(),
            "--output-formats",
            format,
        ]

        pcd = config.get("ort_config_package_curations_dir")
        if pcd and pcd.exists():
            args.append("--package-curations-dir")
            args.append(pcd.as_posix())
        else:
            logging.warning("No curations folder available. Running without curations.")

        # Execute external run
        run(args=args)


@command_group.command()
@click.option("--format", "-f", default="JSON")
@click.argument("source_code_dir", type=click.Path(exists=True))
def analyze(source_code_dir: str, format: str) -> None:
    Command().analyze(source_code_dir, format)
