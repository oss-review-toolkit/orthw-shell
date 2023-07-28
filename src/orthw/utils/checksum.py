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

import hashlib
from enum import Enum
from pathlib import Path

from orthw import config
from orthw.utils import logging


class FolderType(Enum):
    CONFIGURATION = 1
    CURATIONS = 2


def check_evaluation_md5_sum() -> bool:
    """Checks whether the evaluator inputs changed."""
    evaluation_md5_sum_file: Path = config.path("evaluation_md5_sum_file")
    package_configuration_md5_sum_file: Path = config.path("package_configuration_md5_sum_file")
    package_curations_md5_sum_file: Path = config.path("package_curations_md5_sum_file")

    if evaluation_md5_sum_file.exists():
        md5_res = get_folder_md5(FolderType.CONFIGURATION)
        if md5_res:
            with Path.open(package_configuration_md5_sum_file, "w") as md5file:
                md5file.write(md5_res)
        md5_res = get_folder_md5(FolderType.CURATIONS)
        if md5_res:
            with Path.open(package_curations_md5_sum_file, "w") as md5file:
                md5file.write(md5_res)

        with Path.open(evaluation_md5_sum_file) as md5file:
            hashes = md5file.readlines()

        for entry in hashes:
            filehash, filename = entry.split("  ")

            try:
                with Path.open(Path(filename), mode="rb") as file_:
                    hashlib.md5(file_.read()).hexdigest()  # noqa: S324
            except OSError:
                logging.error(f"File {filename} not found.")
                return False

        # Remove package configuration, but why ?
        package_configuration_md5_sum_file.unlink()

        return True

    return False


def get_folder_md5(folder_type: str | FolderType) -> str | None:
    """_summary_

    :param folder_type: Basic enumeration for FDolderType or a direct folder
    :type folder_type: str | FolderType
    :return: md5 value of the directory or None if an invalid value is provided
    :rtype: str | None
    """

    folder: Path | None = None

    if isinstance(folder_type, FolderType):
        if folder_type == FolderType.CONFIGURATION:
            folder = config.path("ort_config_package_configuration_dir")
        elif folder_type == FolderType.CURATIONS:
            folder = config.path("ort_config_package_curations_dir")
    elif isinstance(folder_type, str):
        folder = Path(folder_type)

    if not folder or not folder.exists():
        logging.error("No valid entry for folder_type.")
        return None

    if folder:
        sorted_file_list: list[Path] = sorted(folder.glob("**/*.yml"))

        hashed_file_list = hashlib.md5()  # noqa: S324
        for file in sorted_file_list:
            with Path.open(file, mode="rb") as f:
                digest = hashlib.file_digest(f, "md5")
                logging.debug(f"{digest.hexdigest()}  {file.as_posix()}".encode())
                hashed_file_list.update(f"{digest.hexdigest()}  {file.as_posix()}".encode())

    return hashed_file_list.hexdigest()
