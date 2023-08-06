#!/usr/bin/env python

import click

# internals
from . import credentials
from . import terminal
from . import utils


@click.group()
def cli():
    pass


@cli.command()
@click.option('--tabulate', '-t', is_flag=True, help="Present results as table.")
def info(tabulate):
    data = [
        {
            "name": "new token",
            "token": "eyJhbGciOiJIU***qNegSkFo",
            "date_expiration": "2050-12-31T00:00:00.000Z",
            "active": True
        },
        {
            "name": "new token i will delete",
            "token": "eyJhbGciOiJIU***QMpgNOxg",
            "date_expiration": "2050-12-31T00:00:00.000Z",
            "active": False
        },
        {
            "name": "tctl-190070690681122--auto-generated",
            "token": "eyJhbGciOiJIU***h9o33UDY",
            "date_expiration": "2050-12-31T00:00:00.000Z",
            "active": True
        },
        {
            "name": "tctl-190070690681122--auto-generated",
            "token": "eyJhbGciOiJIU***ijLMErQQ",
            "date_expiration": "2050-12-31T00:00:00.000Z",
            "active": True
        }]

    if tabulate:
        click.echo(utils.to_table(data))
    else:
        click.echo(utils.to_json(data))


@cli.command()
def logo():
    click.echo(terminal.logo)


@cli.command()
@click.option('--delete', is_flag=True, help="Deletes token from disk.")
def config(delete):
    """Initialize, authorize, and configure the tctl tool.

    Retreives and stores your token in as an encrypted file on disk.
    """
    if delete:
        credentials.delete()

    return credentials.config(source="config")

