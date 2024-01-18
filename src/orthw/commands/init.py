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

import json
import lzma
from pathlib import Path
from urllib import request
from urllib.parse import urlparse

import click
import yaml

from orthw import config
from orthw.utils import logging
from orthw.utils.cmdgroups import command_group
from orthw.utils.process import run


def init(target_url: str) -> int:
    target_url_file: Path = config.target_url_file
    temp_file = Path(urlparse(target_url).path)
    filename: str = temp_file.name
    extension: str = temp_file.suffix

    logging.debug(f"target_url_file: {target_url_file}")
    logging.debug(f"temp_file: {temp_file}")
    logging.debug(f"filename: {filename}")
    logging.debug(f"extension: {extension}")

    evaluation_md5_sum_file: Path = config.evaluation_md5_sum_file
    if evaluation_md5_sum_file.exists():
        evaluation_md5_sum_file.unlink()

    # Early check of the file naming and extensions
    if extension not in [".xz", ".json", ".yml", ".yaml"]:
        logging.error(f"Cannot initialize with the given file {filename}. The file extension is unexpected.")
        return 1

    try:
        with Path.open(target_url_file, "w") as output:
            output.write(target_url)
    except OSError:
        logging.error(f"Unable to create output file {target_url_file.as_posix()}.")
        return 1

    # Retrieve target scan result file
    parsed_url = urlparse(target_url)
    if not parsed_url.scheme or parsed_url.scheme not in ["http", "https"] or not parsed_url.netloc:
        logging.error(f"Cannot retrieve {target_url}.")
        return 1

    parsed_url = urlparse(target_url)
    if not parsed_url.scheme or parsed_url.scheme not in ["http", "https"]:
        logging.error(f"Cannot retrieve {target_url}.")
        return 1
    response = request.urlopen(target_url)  # noqa: S310

    data = lzma.decompress(response.read()) if extension == ".xz" else response.read()

    if ".yml" in filename or ".yaml" in filename:
        data = yaml.safe_load(data)

    scan_result_file: Path = config.scan_result_file
    try:
        with Path.open(scan_result_file, "w") as output:
            json.dump(data, output)
    except OSError:
        logging.error(f"Cannot open {scan_result_file.as_posix()} to write.")
        return 1

    args: list[str] = [
        "orth",
        "extract-repository-configuration",
        "--repository-configuration-file",
        config.repository_configuration_file.as_posix(),
        "--ort-file",
        scan_result_file.as_posix(),
    ]

    run(args)

    args = [
        "orth",
        "import-scan-results",
        "--ort-file",
        scan_result_file.as_posix(),
        "--scan-results-storage-dir",
        config.scan_results_storage_dir.as_posix(),
    ]

    return run(args)


@command_group.command(
    name="init",
    options_metavar="SCAN_CONTEXT",
)
@click.argument("target_url")
def __init(target_url: str) -> None:
    init(target_url=target_url)
