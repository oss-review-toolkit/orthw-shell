# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

import click

from orthw.commandbase import CommandBase, command_group
from orthw.utils.process import run

#   package_id=$2
#   require_initialized

#   evaluate
#   echo "Downloading sources for $2."
#   orth list-licenses \
#     --ort-file $evaluation_result_file \
#     --package-id $package_id \
#     --repository-configuration-file $repository_configuration_file \
#     --package-configuration-dir $ort_config_package_configuration_dir \
#     --apply-license-finding-curations \
#     --omit-excluded


class Command(CommandBase):
    """orthw command - licenses"""

    _command_name: str = "licenses"

    def licenses(self, package_id: str, source_code_dir: str | None = None) -> None:
        """licenses

        :param package_id: Id of package
        :type package_id: str
        """

        args: list[str] = [
            "ort",
            "list-licenses",
            "--package-id",
            package_id,
            "--apply-license-finding-curations",
            "--omit-excluded",
        ]

        evaluation_result_file = self.config.get("evaluation_result_file")
        if evaluation_result_file:
            args += ["--ort-file", evaluation_result_file.as_posix()]

        repository_configuration_file = self.config.get("repository_configuration_file")
        if repository_configuration_file:
            args += ["--repository-configuration-file", repository_configuration_file.as_posix()]

        ort_config_package_configuration_dir = self.config.get("ort_config_package_configuration_dir")
        if ort_config_package_configuration_dir:
            args += ["--package-configuration-dir", ort_config_package_configuration_dir.as_posix()]

        if source_code_dir:
            args += ["--source-code-dir", source_code_dir]

        # Execute external run
        run(args=args, live_output=True)


@command_group.command()
@click.option("--source-code-dir", default=None)
@click.argument("package_id")
def licenses(package_id: str, source_code_dir: str | None) -> None:
    Command().licenses(package_id, source_code_dir=source_code_dir)
