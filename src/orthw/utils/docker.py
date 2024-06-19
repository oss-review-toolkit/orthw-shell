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

import sys
from pathlib import Path

import docker
from docker.models.containers import Container
from docker.types import Mount

from orthw import config
from orthw.utils import logging
from orthw.utils.required import required_command


def _run_in_docker(
    args: list[str],
    console_output: bool = True,
    output_file: Path | None = None,
    detached: Path | None = None,
    workdir: Path | None = None,
    output_dir: Path | None = None,
) -> Container:
    """_summary_

    Args:
        args (list[str]): Command and arguments
        console_output (bool, optional): If you want to have command output. Defaults to True.
        output_file (Path | None, optional): If the output need to be redirected to a file. Defaults to None.
        workdir (Path | None, optional): Work directory.
        output_dir (Path | None, optional): Output dir is necessary to pass along.
    Returns:
        int: result code
    """
    mounts: list[Mount] = []
    client = docker.from_env()
    docker_image: str = config.ort_docker_image

    # Check if docker is available on system
    if not required_command("docker"):
        sys.exit(1)

    # Mount proper dirs
    real_workdir: Path = workdir if workdir else Path.cwd()
    logging.debug(f"Mounting [bright_green]{real_workdir}[/bright_green] as /workspace")
    mounts.append(Mount("/workspace", real_workdir.as_posix(), type="bind"))
    args = ["/workspace" if entry == real_workdir.as_posix() else entry for entry in args]

    if output_dir:
        mounts.append(Mount("/output", output_dir.as_posix(), type="bind"))
        args.append("--output-dir")
        args.append("/output")

    # Get main command as entrypoint
    entrypoint = args.pop(0)
    # Join arguments as string
    arguments = " ".join(args)

    # Run container with proper mounts and command
    logging.debug(
        f"Running [bright_green]{docker_image}[/bright_green] container with:\n"
        f"[green]entrypoint:[/green] {entrypoint}\n"
        f"[green]arguments:[/green] {arguments}\n",
    )
    container = client.containers.run(
        docker_image,
        entrypoint=entrypoint,
        command=arguments,
        mounts=mounts,
        working_dir="/workspace",
        detach=True,
    )

    return container
