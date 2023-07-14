# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

from pathlib import Path
from urllib import request
from urllib.parse import urlparse

import click
import lzma
import yaml
import json

from orthw import config
from orthw.commands import command_group
from orthw.utils import logging
from orthw.utils.process import run


class OrtHWCommand:
    """orthw command - init"""

    _command_name: str = "init"

    def init(self, target_url: str) -> None:
        target_url_file: Path = Path(config.get("target_url_file"))
        temp_file = Path(urlparse(target_url).path)
        filename: str = temp_file.name
        extension: str = temp_file.suffix

        logging.debug(f"target_url_file: {target_url_file}")
        logging.debug(f"temp_file: {temp_file}")
        logging.debug(f"filename: {filename}")
        logging.debug(f"extension: {extension}")

        evaluation_md5_sum_file: Path = Path(config.get("evaluation_md5_sum_file"))
        if evaluation_md5_sum_file.exists():
            evaluation_md5_sum_file.unlink()

        # Early check of the file naming and extensions
        if ".xz" not in filename and ".json" not in filename and ".yml" not in filename and ".yaml" not in filename:
            logging.error(f"Cannot initialize with the given file {filename}. The file extension is unexpected.")
            return

        try:
            with open(target_url_file, "w") as output:
                output.write(target_url)
        except IOError:
            logging.error(f"Unable to create output file {target_url_file.as_posix()}.")
            return

        # Retrieve target scan result file
        response = request.urlopen(target_url)  # nosec

        if extension == ".xz":
            data = lzma.decompress(response.read())
        else:
            data = response.read()

        if ".yml" in filename or ".yaml" in filename:
            data = yaml.safe_load(data)

        scan_result_file: Path = config.path("scan_result_file")
        try:
            with open(scan_result_file, "w") as output:
                json.dump(data, output)
        except IOError:
            logging.error(f"Cannot open {scan_result_file.as_posix()} to write.")
            return

        args: list[str] = [
            "orth",
            "extract-repository-configuration",
            "--repository-configuration-file",
            config.get("repository_configuration_file"),
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
            config.get("scan_results_storage_dir"),
        ]

        run(args)


@command_group.command()
@click.argument("target_url")
def init(target_url: str) -> None:
    OrtHWCommand().init(target_url=target_url)
