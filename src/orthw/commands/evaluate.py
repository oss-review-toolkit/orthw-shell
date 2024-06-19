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


def evaluate(
    ort_file: Path,
    output_dir: str | None = None,
    format_: str = "JSON",
    docker: bool = False,
) -> int | Container:
    """Use Ort evaluate command on provided source dir

    :param source_code_dir: Source directory to be evaluated
    :type source_code_dir: str
    """

    if not Path(ort_file):
        logging.error(f"Path for ort file {ort_file} do not exists. Bailing out.")
        return 1
    workdir = Path(ort_file).parent.absolute()

    args: list[str] = [
        "ort",
        "evaluate",
        "--copyright-garbage-file",
        config.ort_config_copyright_garbage_file.as_posix(),
        "--package-curations-dir",
        config.ort_config_package_curations_dir.as_posix(),
        "--output-formats",
        format_,
        "--ort-file",
        ort_file.name,
        "--repository-configuration-file",
        config.repository_configuration_file.as_posix(),
        "--rules-file",
        config.ort_config_rules_file.as_posix(),
        "--license-classifications-file",
        config.ort_config_license_classifications_file.as_posix(),
        "--package-configuration-dir",
        config.ort_config_package_configuration_dir.as_posix(),
    ]

    # Execute external run
    return run(
        args=args,
        is_docker=docker,
        workdir=workdir,
        output_dir=Path(output_dir) if output_dir else workdir,
    )


@command_group.command(
    name="evaluate",
    context="NO_SCAN_CONTEXT",
    short_help="Run ort evaluate command on provided source code directory",
)
@click.option("--format", "-f", "format_", default="JSON")
@click.option("--output-dir", type=click.Path(exists=False), required=False)
@click.option("--ort-file", type=click.Path(exists=False), required=True)
@click.pass_context
def __evaluate(ctx: click.Context, ort_file: str, format_: str, output_dir: str) -> None:
    """Run ort evaluate command on provided source code directory"""
    evaluate(ort_file=Path(ort_file), format_=format_, output_dir=output_dir, docker=bool("docker" in ctx.obj))
