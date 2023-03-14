# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

from orthw import config
from orthw.commandbase import CommandBase, command_group
from orthw.utils.process import run


class Command(CommandBase):
    """orthw command - handled-licenses"""

    _command_name: str = "handled-licenses"

    def process(self) -> None:
        """_summary_"""

        args: list[str] = [
            "orth",
            "list-license-categories",
            "--license-classifications-file",
            config.get("ort_config_license_classifications_file"),
            "--group-by-category",
        ]

        run(args)


@command_group.command()
def handled_licenses_by_category() -> None:
    Command().process()
