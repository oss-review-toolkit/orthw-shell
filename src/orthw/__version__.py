# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

from __future__ import annotations

from typing import TYPE_CHECKING

import importlib_metadata as metadata

if TYPE_CHECKING:
    from collections.abc import Callable


# The metadata.version that we import for Python 3.7 is untyped, work around
# that.
version: Callable[[str], str] = metadata.version

try:
    __version__ = version("otto")
except metadata.PackageNotFoundError:
    # We are running from a git checkout, so we don't have metada
    from pathlib import Path

    import toml

    pyproject = toml.loads((Path(__file__).parent.parent.parent / "pyproject.toml").read_text())
    __version__ = pyproject["tool"]["poetry"]["version"]
