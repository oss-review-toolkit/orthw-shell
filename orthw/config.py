# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

from pathlib import Path
from typing import Dict
import logging
import sys

import yaml
from dict2obj import Dict2Obj


class Config:
    """Base config object. Reads default orthw config file or set default"""

    _ortproject_dir: Path = Path.home() / "ort-project"

    _orthwconfig_default = {
        "configuration_home": (_ortproject_dir / "/ort-project/config").as_posix(),
        "ort_home": (_ortproject_dir / "ort").as_posix(),
        "scancode_home": (_ortproject_dir / "scancode-toolkit").as_posix(),
        "exports_home": (_ortproject_dir / "exports").as_posix(),
        "orthw_home": (_ortproject_dir / "orthw").as_posix(),
    }

    # Default config file
    _config: Dict[str, str] = Dict2Obj(_orthwconfig_default)
    _configfile: Path = Path.home() / ".config" / "orthw"
    _project_default: Path = Path.home() / "ort-project"
    dotdir: Path = Path.home() / ".orthw"

    _log = logging.getLogger("rich")

    def __init__(self, configfile: str | None = None) -> None:
        # Point the main configfile to custom
        if configfile:
            self._configfile = Path(configfile)

        self.__readconfig()

    def __readconfig(self) -> None:
        try:
            with open(self.configfile, "r") as yamlconfig:
                self._config = yaml.safe_load(yamlconfig)
        except IOError:
            self._log.warning(
                f"Missing the required configuration file {self._configfile}.\n"
                "The default config file will be created. Please customize it according to\n"
                "https://github.com/oss-review-toolkit/orthw#3-create-your-orthw-configuration."
            )
            # Generate the default config file
            Path.mkdir(Path.home() / ".config", exist_ok=True)
            try:
                with open(self._configfile, "w") as yamlconfig:
                    yaml.dump(self._orthwconfig_default, yamlconfig)
            except IOError:
                self._log.error(f"Can't create the default config file {self._configfile} !")
                sys.exit(1)

    def get(self, config_entry: str) -> str | None:
        """Return the value of the configured key

        :param config_entry: Desired config parameter
        :type config_entry: str
        :return: Configured value
        :rtype: str
        """
        if config_entry in self._config:
            return self._config[config_entry]
        return None

    @property
    def configfile(self) -> str:
        """Return a string representation of configfile path

        :return: String from _configfile
        :rtype: str
        """
        return self._configfile.as_posix()
