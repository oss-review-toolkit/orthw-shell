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


@command_group.command(
    context_settings={"orthw_group": "NO_SCAN_CONTEXT"},
)
@click.argument("license-id")
def generate_license_classification_request(license_id: str) -> None:
    Command().process(license_id)
