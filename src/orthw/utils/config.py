# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro
from __future__ import annotations

import os
import sys
from pathlib import Path

import yaml
from appdirs import AppDirs
from dotenv import load_dotenv

from orthw.utils import logging


class Config:
    """Base config object. Reads default orthw config file or set default"""

    _configdir: Path = Path(AppDirs("orthw").user_config_dir)
    _configfile: Path = _configdir / "config.yaml"

    # Default config file
    _config: dict[str, str] = {
        "dot_dir": _configdir.as_posix(),
        "configuration_home": Path(_configdir / "ort-config").as_posix(),
        "ort_home": Path(_configdir / "ort").as_posix(),
        "scancode_home": Path(_configdir / "scancode-toolkit").as_posix(),
        "exports_home": Path(_configdir / "exports").as_posix(),
        "ignore_excluded_rule_ids": "",
        "scancode_version": "30.1.0",
        "enabled_advisors": "osv",
        "non_offending_license_categories": "",
        "non_offending_license_ids": "",
        "scandb_host": "",
        "scandb_port": "",
        "scandb_db": "",
        "scandb_schema": "",
        "scandb_user": "",
        "scandb_password": "",
        "ort_docker_registry_server": "",
        "ort_docker_registry_username": "",
        "ort_docker_registry_password": "",
        "ort_docker_image": "registry.gitlab.com/oss-review-toolkit/ort-gitlab-ci/ort:latest",
        "netrc_machine": "",
        "netrc_login": "",
        "netrc_password": "",
        "gitlab_host": "gitlab.example.com",
        "gitlab_token": "",
        "ort_options": "--info",
        "orth_options": "",
        "ort_jvm_options": "-Xmx16G",
        "orth_jvm_options": "-Xmx16G",
    }

    def __init__(self, configfile: str | None = None, defaults_only: bool = False) -> None:
        # Point the main configfile to custom
        if configfile:
            self._configfile = Path(configfile)

        if not defaults_only:
            self.__readconfig()

        # Add default variables
        self.populate_defaults()

        # Read .env for secrets and dynamic info
        load_dotenv()

    def __readconfig(self) -> None:
        try:
            with Path.open(self._configfile) as yamlconfig:
                config_file = yaml.safe_load(yamlconfig)
                for key, value in config_file.items():
                    self._config[key] = value
        except OSError:
            logging.warning(
                f"Missing the required configuration file {self._configfile}.\n"
                "The default config file will be created. Please customize it according to\n"
                "https://github.com/oss-review-toolkit/orthw#3-create-your-orthw-configuration.\n"
                "Please edit your config file to edit the default options before run it again.\n",
            )
            # Generate the default config file
            try:
                self._configdir.mkdir(exist_ok=True, parents=True)
                with Path.open(self._configfile, "w") as yamlconfig:
                    posix_dict: dict[str, str] = {}
                    for key, value in self._config.items():
                        posix_dict[key] = value
                    yaml.dump(posix_dict, yamlconfig)
                    sys.exit(0)
            except OSError:
                logging.error(f"Can't create the default config file {self._configfile} !")
                sys.exit(1)

    def populate_defaults(self) -> None:
        # Config directory files
        cfgdir: Path = Path(self._configdir)
        self.__add("cfgdir", cfgdir)
        self.__add("evaluation_md5_sum_file", cfgdir / "evaluation-md5sum.txt")
        self.__add("evaluation_result_file", cfgdir / "evaluation-result.json")
        self.__add("package_configuration_md5_sum_file", cfgdir / "package-configuration-md5sum.txt")
        self.__add("package_curations_md5_sum_file", cfgdir / "package-curations-md5sum.txt")
        self.__add("scan_result_file", cfgdir / "scan-result.json")
        self.__add("scan_results_storage_dir", cfgdir / "scan-results")
        self.__add("target_url_file", cfgdir / "target-url.txt")
        self.__add("temp_dir", cfgdir / "tmp")

        # Configuration (repository) files
        cfg_home: Path = Path(self.get("configuration_home"))
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
        exports_home: Path = Path(self.get("exports_home"))
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

    def get(self, config_entry: str) -> str:
        """Return the value of the configured key

        :param config_entry: Desired config parameter
        :type config_entry: str
        :return: Configured value
        :rtype: str | Path
        """
        if config_entry in self._config:
            return self._config[config_entry]
        else:
            logging.error(
                f"Config value {config_entry} is not available."
                f"Please verify correct value in {self._configfile.as_posix()}.",
            )
            sys.exit(1)

    def path(self, config_entry: str) -> Path:
        """Return the value of the configured key

        :param config_entry: Desired config parameter
        :type config_entry: str
        :return: Configured value
        :rtype: str | Path
        """
        if config_entry in self._config:
            return Path(self._config[config_entry])
        else:
            logging.error(
                f"Config value {config_entry} is not available."
                f"Please verify correct value in {self._configfile.as_posix()}.",
            )
            sys.exit(1)

    def env(self, env_entry: str) -> str | None:
        """Return entries that user provide in environment like secrets

        :param env_entry: The env variable
        :type env_entry: str
        :return: Value or none
        :rtype: str | None
        """
        return os.getenv(env_entry)

    def __add(self, config_entry: str, path: str | Path) -> None:
        """Add entry in the default config to be used

        :param config_entry: Parameter to be created
        :type config_entry: str | Path
        :param path: Complete path to be assigned
        :type path: Path
        """

        self._config[config_entry] = path.as_posix() if isinstance(path, Path) else path
