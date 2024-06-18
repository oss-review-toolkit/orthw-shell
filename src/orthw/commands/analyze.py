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

from pathlib import Path

import click
from docker.models.containers import Container

from orthw import config
from orthw.utils import logging
from orthw.utils.cmdgroups import command_group
from orthw.utils.process import run


def analyze(
    workdir: str,
    output_dir: str | None = None,
    format_: str = "JSON",
    docker: bool = False,
) -> int | Container:
    """Run ORT Analyzer on given source code directory to find used dependencies.
   
    orthw analyze
    
    Args:
        workdir (str): Source directory to be analyzed.
        format_ (str, optional): Format of the result output. Defaults to "JSON".
        output-dir (str | None, optional): Specified output dir or current dir
        docker (bool, optional): If is runing on docker. Defaults to False.
    Returns:
        int | Container: Status code for local runs or Container object for docker runs
    """

    args: list[str] = [
        "ort",
        "analyze",
        "--output-formats",
        format_,
        "--input-dir",
        Path(workdir).expanduser().as_posix(),
    ]

    if not docker:
        if config.ort_config_package_curations_dir.exists():
            args.append("--package-curations-dir")
            args.append(config.ort_config_package_curations_dir.as_posix())
        else:
            logging.warning("No curations folder available. Running without curations.")

    # Execute external run
    return run(
        args=args,
        is_docker=docker,
        workdir=Path(workdir),
        output_dir=Path(output_dir) if output_dir else Path.cwd(),
    )


@command_group.command(
    context="NO_SCAN_CONTEXT",
    name="analyze",
    help="""
        Run ORT Analyzer on given source code directory to determine dependencies.

        Examples:

        orthw analyze --work-dir /home/ort-user/ort-scans/mime-types/ --output_dir /home/ort-user/ort-scans/mime-types/
    """,
    no_args_is_help=True,
    short_help="Run ORT Analyzer on given source code directory to find used dependencies.",
)
@click.option("--format", "-f", "format_", default="JSON")
@click.option("--output-dir", type=click.Path(exists=False), required=False)
@click.option("--work-dir", type=click.Path(), required=True)
@click.pass_context
def __analyze(ctx: click.Context, workdir: str, format_: str, output_dir: str) -> None:
    """Run ORT Analyzer on given source code directory to find used dependencies."""
    analyze(workdir=work-dir, format_=format_, output_dir=output-dir, docker=bool("docker" in ctx.obj))
