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
import tempfile
from pathlib import Path
from urllib.parse import urlparse

import click
import requests
import yaml
from docker.models.containers import Container

from orthw import config
from orthw.utils import logging
from orthw.utils.cmdgroups import command_group
from orthw.utils.process import run


def init(target_url: str) -> int | Container:
    parsed_url = urlparse(target_url)
    filename: str = Path(parsed_url.path).name
    extension: str = Path(parsed_url.path).suffix

    logging.debug(f"filename: {filename}")
    logging.debug(f"extension: {extension}")

    evaluation_md5_sum_file: Path = config.evaluation_md5_sum_file
    if evaluation_md5_sum_file.exists():
        evaluation_md5_sum_file.unlink()

    # Early check of the file naming and extensions
    if extension not in [".xz", ".json", ".yml", ".yaml"]:
        logging.error(f"Cannot initialize with the given file {filename}. The file extension is unexpected.")
        return 1

    # Parse and retrieve target scan result file
    if not parsed_url.scheme or parsed_url.scheme not in ["http", "https"] or not parsed_url.netloc:
        logging.error(f"Can't parse {target_url}.")
        return 1

    response = requests.get(url=target_url, timeout=120)
    if response.status_code != 200:
        logging.error(f"Can't retrieve {target_url}")
        return 1

    response_data = lzma.decompress(response.content) if extension == ".xz" else response.content

    if extension == ".yml" or extension == ".yaml":
        data = yaml.safe_load(response_data)
    elif extension == ".json":
        data = json.loads(response_data)

    # We don't need a fixed scan_result_file as this is a shell temporary measure.
    # Use proper Temp directory to realize he operation one single time
    with tempfile.NamedTemporaryFile(suffix=".json") as temp_file:
        scan_result_file: Path = Path(temp_file.name)
        try:
            with scan_result_file.open("w") as output:
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

        status = run(args)
        if status:
            return 1

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
    context="SCAN_CONTEXT",
)
@click.argument("target_url")
def __init(target_url: str) -> None:
    init(target_url=target_url)
