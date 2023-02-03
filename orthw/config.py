# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

from pathlib import Path
from typing import Any, List

import logging
import yaml


defaults = {"test": "test"}


class Config:
    """Base config object. Reads default orthw config file or set default"""

    # Default config file
    _config: List[Any] | None = None
    _configfile: Path = Path.home() / ".config" / ".orthw"

    def __init__(self, configfile: str | None = None) -> None:
        # Set default if no ccustom config file is passed
        if configfile:
            self._configfile = Path(configfile)

    def __readconfig(self) -> bool:
        try:
            with open(self.configfile, "r") as yamlconfig:
                self._config = yaml.safe_load(yamlconfig)
        except IOError:
            logging.error(
                "Missing the required configuration file '$orthw_config_file'."
                "Please create that file following the installation instructions, see "
                "https://github.com/oss-review-toolkit/orthw#3-create-your-orthw-configuration."
            )
        return False

    @property
    def configfile(self) -> str:
        """Return a string representation of configfile path

        :return: String from _configfile
        :rtype: str
        """
        return self._configfile.as_posix()
