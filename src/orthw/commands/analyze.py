# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro
from __future__ import annotations

from pathlib import Path

import click

from orthw import config
from orthw.commands import command_group
from orthw.utils import logging
from orthw.utils.process import run


class OrtHwCommand:
    """orthw command - analyze"""

    _command_name: str = "analyze"

    def analyze(self, source_code_dir: str, format_: str = "JSON") -> None:
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
            format_,
        ]

        pcd = Path(config.get("ort_config_package_curations_dir"))

        if pcd.exists():
            args.append("--package-curations-dir")
            args.append(pcd.as_posix())
        else:
            logging.warning("No curations folder available. Running without curations.")

        # Execute external run
        run(args=args)


@command_group.command(
    context_settings={"orthw_group": "NO_SCAN_CONTEXT"},
    short_help="Run ort analyze command on provided source code directory.",
)
@click.option("--format", "-f", "format_", default="JSON")
@click.argument("source_code_dir", type=click.Path(exists=True))
def analyze(source_code_dir: str, format_: str) -> None:
    """Run ort analyze command on provided source code directory"""
    OrtHwCommand().analyze(source_code_dir, format_)
