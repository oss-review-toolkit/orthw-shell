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

import subprocess  # nosec
import sys
from pathlib import Path

from docker.models.containers import Container

from orthw.utils import admin, console, logging
from orthw.utils.docker import _run_in_docker
from orthw.utils.required import required_command


def run(
    args: list[str],
    console_output: bool = False,
    output_file: Path | None = None,
    workdir: Path | None = None,
    output_dir: Path | None = None,
    is_docker: bool = False,
) -> int | Container:
    """Run a process with defined arguments in the proper setting for bare metal or docker

    Args:
        args (list[str]): Command and arguments
        console_output (bool, optional): If you want to have command output. Defaults to True.
        output_file (Path | None, optional): If the output need to be redirected to a file. Defaults to None.
        workdir (Path | None, optional): Work directory.
        output_dir (Path | None, optional): Output dir is necessary to pass along.
        docker (bool, optional): If the command need to be run inside docker container. Defaults to False.

    Returns:
        int: result code
    """

    if workdir:
        # We need expand user since docker can't resolve it
        workdir = Path(workdir).expanduser()
        logging.debug(f"Work dir: {workdir}")
        if not workdir.exists():
            logging.error(f"Work dir {workdir} do not exists. Bailing out.")
    if output_dir:
        # We need expand user since docker can't resolve it
        output_dir = Path(output_dir).expanduser()
        logging.debug(f"Output dir: {output_dir}")
        if not output_dir.exists():
            # Try create output dir if not exists or fail
            try:
                output_dir.mkdir(parents=True)
            except OSError:
                logging.error(f"Can't create output dir {output_dir}. Bailing out.")
                sys.exit(1)

    if is_docker:
        return _run_in_docker(
            args,
            console_output=console_output,
            workdir=workdir,
            output_dir=output_dir,
        )
    else:
        return __run_host(
            args,
            console_output=console_output,
            output_file=output_file,
            workdir=workdir,
            output_dir=output_dir,
        )


def __run_host(
    args: list[str],
    console_output: bool = True,
    output_file: Path | None = None,
    workdir: Path | None = None,
    output_dir: Path | None = None,
) -> int:
    """Run the requested command in bare metal

    Args:
        args (list[str]): Command and arguments
        console_output (bool, optional): If you want to have command output. Defaults to True.
        output_file (Path | None, optional): If the output need to be redirected to a file. Defaults to None.
        workdir (Path | None, optional): Work directory.
        output_dir (Path | None, optional): Output dir is necessary to pass along.
    Returns:
        int: _description_
    """
    if admin():
        logging.error("This script is not allowed to run as admin.")
        sys.exit(1)

    # Expect first argument be the required command
    main_cmd = required_command(args[0])
    if not main_cmd:
        return 1

    # Replace main command with path qualified one
    args[0] = main_cmd

    # Append output dirs if provided
    if output_dir:
        args.append("--output-dir")
        args.append(output_dir.as_posix())

    logging.debug(f"command line: [bright_green]{' '.join(args)}[/]")

    if output_file:
        try:
            with Path.open(output_file, "w") as f:
                proc = subprocess.Popen(args, stdout=f)  # noqa: S603
                f.close()
        except OSError:
            logging.error(f"Can't open file {output_file} to write.")
            sys.exit(1)
    else:
        proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  # noqa: S603
        if console_output and proc.stdout:
            while True:
                output = proc.stdout.readline()
                if proc.poll() is not None:
                    break
                if output:
                    line = output.decode("utf-8").strip()
                    # Avoid funny ort log output that ressemble markup closing tag
                    if "[/" in line:
                        line = line.replace("[", "").replace("]", "")
                    console.print(line, style="bright_white")

    res = proc.wait()
    logging.debug(f"Return code: {res}")
    return res
