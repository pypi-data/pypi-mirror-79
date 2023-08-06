#!/usr/bin/env python

import click
import sys

# internals
from . import version
from . import config
from . import strategies
# from . import tradehooks
# from . import accounts
# from . import aggregated
# from . import marketdata
# from . import tools
# from . import admin


cli = click.CommandCollection(sources=[
    config.cli,
    strategies.cli,
    # tradehooks.cli,
    # accounts.cli,
    # aggregated.cli,
    # marketdata.cli,
    # tools.cli,
    # admin.cli
])


if __name__ == '__main__':
    arg_string = " ".join(sys.argv)
    if "--version" in arg_string:
        click.echo("\ntctl {version}".format(version=version.version))
        click.echo("Copyrights (c) Tradologics, Inc.")
        click.echo("https://tradologics.com/tctl")
        sys.exit()

    cli()
