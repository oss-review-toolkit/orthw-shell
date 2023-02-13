# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

from pathlib import Path
from typing import Dict
import logging
import sys

import yaml


class Config:
    """Base config object. Reads default orthw config file or set default"""

    _ortproject_dir: Path = Path.home() / "ort-project"

    # Default config file
    _config: Dict[str, str] = {
        "configuration_home": (_ortproject_dir / "ort-project/config").as_posix(),
        "ort_home": (_ortproject_dir / "ort").as_posix(),
        "scancode_home": (_ortproject_dir / "scancode-toolkit").as_posix(),
        "exports_home": (_ortproject_dir / "exports").as_posix(),
        "orthw_home": (_ortproject_dir / "orthw").as_posix(),
    }

    _configfile: Path = Path.home() / ".config" / "orthw"
    _project_default: Path = Path.home() / "ort-project"
    _dotdir: Path = Path.home() / ".orthw"
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
                    yaml.dump(self._config, yamlconfig)
            except IOError:
                self._log.error(f"Can't create the default config file {self._configfile} !")
                sys.exit(1)

        # Add default variables
        self.populate_defaults()
        print(self.config)

    def populate_defaults(self) -> None:
        # Dot directory files
        self.__add("evaluation_md5_sum_file", self._dotdir / "evaluation-md5sum.txt")
        self.__add("evaluation_result_file", self._dotdir / "evaluation-result.json")
        self.__add("package_configuration_md5_sum_file", self._dotdir / "package-configuration-md5sum.txt")
        self.__add("package_curations_md5_sum_file", self._dotdir / "package-curations-md5sum.txt")
        self.__add("scan_result_file", self._dotdir / "scan-result.json")
        self.__add("scan_results_storage_dir", self._dotdir / "scan-results")
        self.__add("target_url_file", self._dotdir / "target-url.txt")
        self.__add("temp_dir", self._dotdir / "tmp")

        # Configuration (repository) files
        cfg_home = self.get("configuration_home", as_path=True)
        if isinstance(cfg_home, Path):
            self.__add("ort_config_copyright_garbage_file", cfg_home / "copyright-garbage.yml")
            self.__add("ort_config_custom_license_texts_dir", cfg_home / "custom-license-texts")
            self.__add("ort_config_how_to_fix_text_provider_script", cfg_home / "how-to-fix-text-provider.kts")
            self.__add("ort_config_license_classifications_file", cfg_home / "license-classifications.yml")
            self.__add("ort_config_notice_templates_dir", cfg_home / "notice-templates")
            self.__add("ort_config_package_configuration_dir", cfg_home / "package-configurations")
            self.__add("ort_config_package_curations_dir", cfg_home / "curations")
            self.__add("ort_config_resolutions_file", cfg_home / "resolutions.yml")
            self.__add("ort_config_rules_file", cfg_home / "evaluator.rules.kts")

        # Exports (repository) files:
        exports_home = self.get("exports_home", as_path=True)
        if isinstance(exports_home, Path):
            self.__add("exports_license_finding_curations_file", exports_home / "license-finding-curations.yml")
            self.__add("exports_path_excludes_file", exports_home / "path-excludes.yml")
            self.__add("exports_vcs_url_mapping_file", exports_home / "vcs-url-mapping.yml")

        # Initialized orthw directory input / output files:
        self.__add("copyrights_file", "copyrights.txt")
        self.__add("copyrights_debug_file", "copyrights-debug.txt")
        self.__add("cyclone_dx_report_file", "cyclone-dx-report.xml")
        self.__add("evaluated_model_report_file", "evaluated-model.json")
        self.__add("gitlab_license_model_report_file", "gl-license-scanning-report.json")
        self.__add("html_report_file", "report.html")
        self.__add("repository_configuration_file", "ort.yml")
        self.__add("spdx_json_report_file", "report.spdx.json")
        self.__add("spdx_yaml_report_file", "report.spdx.yml")
        self.__add("webapp_report_file", "webapp.html")

    def get(self, config_entry: str, as_path: bool = False) -> str | Path | None:
        """Return the value of the configured key

        :param config_entry: Desired config parameter
        :type config_entry: str
        :param as_path: If you want real Path object instead of pure posix
        :type as_path: bool
        :return: Configured value|
        :rtype: str
        """
        if config_entry in self._config:
            if as_path:
                return Path(self._config[config_entry])
            return self._config[config_entry]
        return None

    def __add(self, config_entry: str, path: str | Path) -> None:
        """Add entry in the default config to be used

        :param config_entry: Parameter to be created
        :type config_entry: str | Path
        :param path: Complete path to be assigned
        :type path: Path
        """

        self._config[config_entry] = path.as_posix() if isinstance(path, Path) else path

    @property
    def configfile(self) -> str:
        """Return a string representation of configfile path

        :return: String from _configfile
        :rtype: str
        """
        return self._configfile.as_posix()

    @property
    def config(self) -> Dict[str, str]:
        """Return the configured dictionaire

        :return: Ort config values
        :rtype: Dict[str, str]
        """
        return self._config