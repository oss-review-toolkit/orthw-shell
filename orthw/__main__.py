# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

import logging

import click
from rich.logging import RichHandler

from .orthw import OrtHw


def main() -> None:
    # Setup the main logger message
    logging.basicConfig(level="INFO", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])

    app = OrtHw()
    app.run()

    cli = click.CommandCollection(sources=app.commands)

    # Call click
    cli()


if __name__ == "__main__":
    main()
