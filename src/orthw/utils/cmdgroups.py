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
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro
from __future__ import annotations

import logging as stdlogger

import click

from orthw.__version__ import __version__
from orthw.utils import logging
from orthw.utils.orthwclickgroup import OrtHwClickGroup


@click.group(cls=OrtHwClickGroup)
@click.version_option(__version__, "-v", "--version", prog_name="OrthHW", message="%(prog)s version %(version)s")
@click.option("-d", "--debug", is_flag=True, default=False, help="Enable debug mode.")
@click.option("--docker", is_flag=True, default=False, help="Run inside docker container.")
@click.option("--logfile", required=False, help="Set the log output to specified file.")
@click.pass_context
def command_group(ctx: click.Context, debug: bool, docker: bool, logfile: str) -> None:
    ctx.obj = {}
    if debug:
        logging.setLevel(stdlogger.DEBUG)
        ctx.obj["debug"] = True
    # Set the operations to run with configured container
    if docker:
        ctx.obj["docker"] = True
    if logfile:
        filehandler = stdlogger.FileHandler(
            logfile,
            mode="w",
            encoding="UTF-8",
        )
        if debug:
            filehandler.setLevel(stdlogger.DEBUG)
        logging.addHandler(filehandler)


# Subgroup for package config operations
@command_group.group(
    cls=OrtHwClickGroup,
    name="package-config",
    options_metavar="PACKAGE_CONFIG",
)
@click.pass_context
def package_config_group(ctx: click.Context) -> None:
    """Operations related to package configuration."""


# Subgroup for repository config operations
@command_group.group(
    cls=OrtHwClickGroup,
    name="repository-config",
    options_metavar="REPOSITORY_CONFIG",
)
@click.pass_context
def repository_group(ctx: click.Context) -> None:
    """Operations related to package configuration."""
