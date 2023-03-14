# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

from pathlib import Path

import click
import git

from orthw import config
from orthw.commandbase import CommandBase, command_group


class Command(CommandBase):
    """orthw command - find-license-url"""

    _command_name: str = "find-license-url"

    def find_license_text_url(self, license_id: str) -> str:
        if license_id.startswith("LicenseRef-scancode-"):
            key = license_id.strip("LicenseRef-scancode-")
            license_file_path = f"src/licensedcode/data/licenses/{key}.LICENSE"

            license_file: Path = config.path("scancode_home") / license_file_path
            if license_file.exists():
                git_repo = git.Repo(config.get("scancode_home"))
                revision = git_repo.git.rev_parse("HEAD")
                return f"https://github.com/nexB/scancode-toolkit/blob/{revision}/{license_file_path}"

        return f"https://spdx.org/licenses/{license_id}.html"


@command_group.command()
@click.argument("license-id")
def find_license_url(license_id: str) -> None:
    Command().find_license_text_url(license_id=license_id)
