# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro
from __future__ import annotations

import click

from orthw.commands import command_group
from orthw.commands.find_license_url import Command as OrtHwCommand
from orthw.templates import render_txt
from orthw.utils import console


class Command:
    """orthw command - generate-license-classification-request"""

    _command_name: str = "generate-license-classification-request"

    def process(self, license_id: str, stdout: bool = True) -> str:
        # Template data to replace
        data: dict[str, str] = {
            "license_id": license_id,
            "license_url": OrtHwCommand().find_license_text_url(license_id),
        }
        output = render_txt("license_classification_request", data)
        if stdout:
            console.print(output)
        return output


@command_group.command()
@click.argument("license-id")
def generate_license_classification_request(license_id: str) -> None:
    Command().process(license_id)
