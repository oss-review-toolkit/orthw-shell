# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro
from __future__ import annotations

import subprocess  # nosec
import sys
from pathlib import Path
from typing import Any

from orthw.utils import admin, console, logging
from orthw.utils.required import required_command


def run(args: list[str], console_output: bool = True, output_file: Path | None = None) -> int | Any:
    """Run a process with defined arguments

    :param args: Arguments
    :type args: list[str]
    :param console_output: If you want to have command output, defaults to True
    :type console_output: bool, optional
    :param output_file: If the output need to be redirected to a file
    :type output_file: Path | str | None, optional
    :return: Process resulting code
    :rtype: int | Any
    """

    if admin():
        logging.error("This script is not allowed to run as admin.")
        sys.exit(1)

    # Expect first argument be the required command
    main_cmd = required_command(args[0])
    if not main_cmd:
        return None

    # Replace main command with path qualified one
    args[0] = main_cmd

    logging.debug(f"command line: [bright_green]{' '.join(args)}[/]")

    if output_file:
        try:
            with Path.open(output_file, "w") as f:
                proc = subprocess.Popen(args, stdout=f)  # noqa: S603
                f.close()
        except OSError:
            logging.error(f"Can't open file {output_file} to write.")
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
