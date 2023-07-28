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

import sys
from pathlib import Path

from jinja2 import Template

from orthw.utils import logging


def get_template(template: str) -> str:
    """Try to retrieve the template file from templates dir

    :param template: Name of the template without extension
    :type template: str
    :return: Template file
    :rtype: str
    """
    template_file: str = ""
    template_dir: Path = Path(__file__).resolve().parent
    template_filename: Path = template_dir / f"{template}.jinja2"

    try:
        with Path.open(template_filename) as inputfile:
            template_file = "\n".join(inputfile.readlines())
        return template_file
    except OSError:
        logging.error(f"Can't find template file {template}.")
        sys.exit(1)


def render_txt(template: str, data: dict[str, str]) -> str:
    """Return a processed txt template

    :param template: Template requested
    :type template: str
    :param data: data to be replaced in template
    :type data: dict[str, str]
    :return: Processed template
    :rtype: str
    """
    template_code = get_template(template=f"{template}.txt")

    template_j2 = Template(template_code)

    return template_j2.render(data)
