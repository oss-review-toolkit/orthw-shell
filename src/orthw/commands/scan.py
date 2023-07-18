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

from orthw.commands import command_group
from orthw.utils import logging
from orthw.utils.process import run


class OrtHwCommand:
    """orthw command - scan"""

    _command_name: str = "scan"

    def scan(
        self,
        ort_file: str,
        output_dir: str | None = None,
        format_: str = "JSON",
        docker: bool = False,
    ) -> int:
        """Use Ort analyzer command on provided source dir

        Args:
            ort_file (str): Analyzer file.
            format_ (str, optional): Format of the result output. Defaults to "JSON".
            output_dir (str | None, optional): Specified output dir or cuurent dir
            docker (bool, optional): If is runing on docker. Defaults to False.
        """

        if not Path(ort_file):
            logging.error(f"Path for ort file {ort_file} do not exists. Bailing out.")
            return 1
        workdir = Path(ort_file).parent

        args: list[str] = [
            "ort",
            "scan",
            "--output-formats",
            format_,
            "--ort-file",
            "analyzer-result.json",
        ]

        # Execute external run
        return run(
            args=args,
            is_docker=docker,
            workdir=workdir,
            output_dir=Path(output_dir) if output_dir else Path.cwd(),
        )


@command_group.command(
    options_metavar="NO_SCAN_CONTEXT",
    short_help="Run ort analyze command on provided source code directory.",
    context_settings={
        "allow_extra_args": True,
        "ignore_unknown_options": True,
    },
)
@click.option("--format", "-f", "format_", default="JSON")
@click.option("--output-dir", type=click.Path(exists=False), required=False)
@click.option("--ort-file", type=click.Path(exists=False), required=True)
@click.pass_context
def scan(ctx: click.Context, ort_file: str, format_: str, output_dir: str) -> None:
    """Run ort analyze command on provided source code directory"""
    OrtHwCommand().scan(ort_file=ort_file, format_=format_, output_dir=output_dir, docker=bool("docker" in ctx.obj))
