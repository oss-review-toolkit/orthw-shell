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

from pathlib import Path

from appdirs import AppDirs
from yaml_settings_pydantic import BaseYamlSettings, YamlSettingsConfigDict


class Config(BaseYamlSettings):
    """Base config object. Reads default orthw config file or set default"""

    configdir: Path = Path(AppDirs("orthw").user_config_dir)
    configfile: Path = Path(AppDirs("orthw").user_config_dir) / "config.yml"

    model_config = YamlSettingsConfigDict(yaml_files=configfile.as_posix(), extra="allow")

    configuration_home: Path = configdir / "ort-config"
    enabled_advisors: str | None = "osv"
    exports_home: Path = configdir / "exports"
    gitlab_host: str | None = "gitlab.example.com"
    gitlab_token: str | None = None
    ignore_excluded_rule_ids: str | None = None
    netrc_login: str | None = None
    netrc_machine: str | None = None
    netrc_password: str | None = None
    non_offending_license_categories: str | None = None
    non_offending_license_ids: str | None = None
    ort_docker_image: str = "ghcr.io/oss-review-toolkit/ort:latest"
    ort_docker_registry_password: str | None = None
    ort_docker_registry_server: str | None = None
    ort_docker_registry_username: str | None = None
    ort_home: Path = configdir / "ort"
    ort_jvm_options: str | None = "-Xmx16G"
    ort_options: str | None = "--info"
    orth_jvm_options: str | None = "-Xmx16G"
    orth_options: str | None = None
    scancode_home: Path = configdir / "scancode-toolkit"
    scancode_version: str = "32.0.8"
    scandb_db: str | None = None
    scandb_host: str | None = None
    scandb_password: str | None = None
    scandb_port: str | None = None
    scandb_schema: str | None = None
    scandb_user: str | None = None

    # Config directory files
    evaluation_md5_sum_file: Path = configdir / "evaluation-md5sum.txt"
    evaluation_result_file: Path = configdir / "evaluation-result.json"
    package_configuration_md5_sum_file: Path = configdir / "package-configuration-md5sum.txt"
    package_curations_md5_sum_file: Path = configdir / "package-curations-md5sum.txt"
    scan_result_file: Path = configdir / "scan-result.json"
    scan_results_storage_dir: Path = configdir / "scan-results"
    target_url_file: Path = configdir / "target-url.txt"
    temp_dir: Path = configdir / "tmp"

    # Configuration (repository) files
    ort_config_copyright_garbage_file: Path = configuration_home / "copyright-garbage.yml"
    ort_config_custom_license_texts_dir: Path = configuration_home / "custom-license-texts"
    ort_config_how_to_fix_text_provider_script: Path = configuration_home / "how-to-fix-text-provider.kts"
    ort_config_license_classifications_file: Path = configuration_home / "license-classifications.yml"
    ort_config_notice_templates_dir: Path = configuration_home / "notice-templates"
    ort_config_package_configuration_dir: Path = configuration_home / "package-configurations"
    ort_config_package_curations_dir: Path = configuration_home / "curations"
    ort_config_resolutions_file: Path = configuration_home / "resolutions.yml"
    ort_config_rules_file: Path = configuration_home / "evaluator.rules.kts"

    # Exports (repository) files
    exports_license_finding_curations_file: Path = exports_home / "license-finding-curations.yml"
    exports_path_excludes_file: Path = exports_home / "path-excludes.yml"
    exports_vcs_url_mapping_file: Path = exports_home / "vcs-url-mapping.yml"

    # Initialized orthw directory input / output files:
    copyrights_debug_file: Path = Path("copyrights-debug.txt")
    copyrights_file: Path = Path("copyrights.txt")
    cyclone_dx_report_file: Path = Path("cyclone-dx-report.xml")
    evaluated_model_report_file: Path = Path("evaluated-model.json")
    gitlab_license_model_report_file: Path = Path("gl-license-scanning-report.json")
    html_report_file: Path = Path("report.html")
    repository_configuration_file: Path = Path("ort.yml")
    spdx_json_report_file: Path = Path("report.spdx.json")
    spdx_yaml_report_file: Path = Path("report.spdx.yml")
    webapp_report_file: Path = Path("webapp.html")
