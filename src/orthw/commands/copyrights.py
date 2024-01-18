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

from orthw import config
from orthw.utils import logging
from orthw.utils.cmdgroups import command_group
from orthw.utils.process import run
from orthw.utils.required import require_initialized


def copyrights(package_id: str = "") -> None:
    """OrtHW Command

    :param package_id: Package ID, defaults to ""
    :type package_id: str, optional
    """

    require_initialized()

    ort_config_copyright_garbage_file: Path = config.ort_config_copyright_garbage_file
    ort_config_package_configuration_dir: Path = config.ort_config_package_configuration_dir
    scan_result_file: Path = config.scan_result_file
    if not scan_result_file or not ort_config_package_configuration_dir or not ort_config_copyright_garbage_file:
        logging.error("Invalid configuration.")
        return

    args: list[str] = ["orth", "list-copyrights", "--ort-file", scan_result_file.as_posix()]

    if package_id:
        args += ["--package-id", package_id]
        run(args=args)
    else:
        args += [
            "--package-configuration-dir",
            ort_config_package_configuration_dir.as_posix(),
            "--copyright-garbage-file",
            ort_config_package_configuration_dir.as_posix(),
        ]

        run(args=args, output_file=config.path("copyrights_file"))

        args += ["--show-raw-statements"]
        run(args=args, output_file=config.path("copyrights_debug_file"))


@command_group.command(
    name="copyrigths",
    options_metavar="SCAN_CONTEXT",
)
@click.argument("package-id", type=str, default="")
def __copyrights(package_id: str) -> None:
    copyrights(package_id)
