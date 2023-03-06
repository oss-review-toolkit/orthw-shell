# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Helio Chissini de Castro

import click

from .orthw import OrtHw


def main() -> None:
    app = OrtHw()
    app.run()

    cli = click.CommandCollection(sources=app.commands)

    # Call click
    cli()


if __name__ == "__main__":
    main()
