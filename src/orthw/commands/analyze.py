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

from pathlib import Path

import click

from orthw import config
from orthw.commands import command_group
from orthw.utils import logging
from orthw.utils.process import run


class OrtHwCommand:
    """orthw command - analyze"""

    _command_name: str = "analyze"

    def analyze(
        self,
        source_code_dir: str,
        output_dir: str | None = None,
        format_: str = "JSON",
        docker: bool = False,
    ) -> None:
        """Use Ort analyzer command on provided source dir

        Args:
            source_code_dir (str): Source directory to be analyzed.
            format_ (str, optional): Format of the result output. Defaults to "JSON".
            output_dir (str | None, optional): Specified output dir or cuurent dir
            docker (bool, optional): If is runing on docker. Defaults to False.
        """

        args: list[str] = [
            "ort",
            "analyze",
            "--output-formats",
            format_,
        ]

        if not docker:
            pcd = Path(config.get("ort_config_package_curations_dir"))

            if pcd.exists():
                args.append("--package-curations-dir")
                args.append(pcd.as_posix())
            else:
                logging.warning("No curations folder available. Running without curations.")

        # Execute external run
        run(
            args=args,
            is_docker=docker,
            input_dir=Path(source_code_dir),
            output_dir=Path(output_dir) if output_dir else Path.cwd(),
        )


@command_group.command(
    options_metavar="NO_SCAN_CONTEXT",
    short_help="Run ort analyze command on provided source code directory.",
)
@click.option("--format", "-f", "format_", default="JSON")
@click.argument("source_code_dir", type=click.Path(exists=True))
@click.argument("output_dir", type=click.Path(exists=True), required=False)
@click.pass_context
def analyze(ctx: click.Context, source_code_dir: str, format_: str, output_dir: str) -> None:
    """Run ort analyze command on provided source code directory"""
    OrtHwCommand().analyze(source_code_dir, format_=format_, output_dir=output_dir, docker=bool("docker" in ctx.obj))
