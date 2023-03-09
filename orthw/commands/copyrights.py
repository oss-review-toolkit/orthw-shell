# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

import click

from orthw import config
from orthw.commandbase import CommandBase, command_group
from orthw.utils import logging
from orthw.utils.process import run
from orthw.utils.required import require_initialized


class Command(CommandBase):
    """orthw command - copyrights"""

    _command_name: str = "copyrights"

    def copyrights(self, package_id: str = "") -> None:
        """OrtHW Command

        :param package_id: Package ID, defaults to ""
        :type package_id: str, optional
        """

        require_initialized()

        ort_config_copyright_garbage_file: str = config.get("ort_config_copyright_garbage_file")
        ort_config_package_configuration_dir: str = config.get("ort_config_package_configuration_dir")
        scan_result_file: str = config.get("scan_result_file")
        if not scan_result_file or not ort_config_package_configuration_dir or not ort_config_copyright_garbage_file:
            logging.error("Invalid configuration.")
            return

        args: list[str] = ["orth", "list-copyrights", "--ort-file", scan_result_file]

        if package_id:
            args += ["--package-id", package_id]
            run(args=args)
        else:
            args += [
                "--package-configuration-dir",
                ort_config_package_configuration_dir,
                "--copyright-garbage-file",
                ort_config_package_configuration_dir,
            ]

            run(args=args, output_file=config.get("copyrights_file"))

            args += ["--show-raw-statements"]
            run(args=args, output_file=config.get("copyrights_debug_file"))


@command_group.command()
@click.argument("package-id", type=str, default="")
def copyrights(package_id: str) -> None:
    Command().copyrights(package_id)
