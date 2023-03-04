# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

import ctypes
import os
import logging as stdlogger

from rich.console import Console

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
