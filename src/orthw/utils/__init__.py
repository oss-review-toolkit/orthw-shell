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

import ctypes
import logging as stdlogger
import os

from rich.console import Console
from rich.logging import RichHandler

# Setup the main logger message
stdlogger.basicConfig(level="INFO", format="%(message)s", datefmt="[%X]", handlers=[RichHandler(markup=True)])
# Global log variable
logging = stdlogger.getLogger("rich")

# Global console output
console = Console()


def admin() -> bool:
    # We not allow run as a root/admin
    try:
        is_admin = os.getuid() == 0
    except AttributeError:  # We're playing Windows game
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0  # type: ignore

    return is_admin
