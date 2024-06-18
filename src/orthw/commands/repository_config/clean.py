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

import click

from pathlib import Path

from orthw import config
from orthw.commands import evaluate
from orthw.utils import logging
from orthw.utils.cmdgroups import repository_group
from orthw.utils.process import run
from orthw.utils.required import require_initialized


def clean(source_code_dir: str) -> None:
    require_initialized()

    # FIXME implement args to call evaluate
    evaluate()

    evaluation_result_file: Path = config.evaluation_result_file
    repository_configuration_file: Path = config.repository_configuration_file
    ort_config_resolutions_file: Path = config.ort_config_resolutions_file

    logging.debug(f"source_code_dir: {source_code_dir}")

    args: list[str] = [
        "orth",
        "repository-configuration",
        "remove-entries",
        "--ort-file",
        evaluation_result_file.as_posix(),
        "--repository-configuration-file".
        repository_configuration_file.as_posix(),
        "--source-code-dir",
        source_code_dir,
        "--resolutions-file",
        ort_config_resolutions_file.as_posix()
    ]

    run(args=args)


@repository_group.command(
    name="clean",
    context="REPOSITORY_CONFIG",
    help="""
        Removes all non-matching path and scope excludes as well as rule violation resolutions from the ort.yml file.
    """,
    short_help="Removes all non-matching entries from the ort.yml file."
)
@click.argument("source_code_dir")
def __clean(source_code_dir: str) -> None:
    "Removes all non-matching entries from the ort.yml file."
    clean(source_code_dir=source_code_dir)
