# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

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
            with open(package_configuration_md5_sum_file, "w") as md5file:
                md5file.write(md5_res)
        md5_res = get_folder_md5(FolderType.CURATIONS)
        if md5_res:
            with open(package_curations_md5_sum_file, "w") as md5file:
                md5file.write(md5_res)

        with open(evaluation_md5_sum_file, "r") as md5file:
            hashes = md5file.readlines()

        for entry in hashes:
            filehash, filename = entry.split("  ")
            if not filehash == hashlib.md5(open(filename, "rb").read()).hexdigest():  # nosec
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

        hashed_file_list = hashlib.md5()  # nosec
        for file in sorted_file_list:
            with open(file, "rb") as f:
                digest = hashlib.file_digest(f, "md5")
                logging.debug(f"{digest.hexdigest()}  {file.as_posix()}".encode("utf-8"))
                hashed_file_list.update(f"{digest.hexdigest()}  {file.as_posix()}".encode("utf-8"))

    return hashed_file_list.hexdigest()
