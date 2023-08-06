#!/usr/bin/env python

import dotenv
import click
import uuid
import os
import sys
from stdiomask import getpass

from base64 import b64encode as _b64encode, b64decode as _b64decode
import uuid as _uuid

from pathlib import Path

# internals
from . import remote
from . import terminal


_token = {
    "id": _uuid.getnode(),
    "name": "tctl-{uuid}--auto-generated".format(uuid=_uuid.getnode())
}

env_path = Path.home() / '.tradologics'

if not Path.exists(env_path):
    Path.touch(env_path)

dotenv.load_dotenv(env_path)


def delete():
    Path.delete(env_path)
    confirm = input("\nAre you sure you want to delete your credentials? [y/N]: ")
    if confirm not in ["y", "Y"]:
        click.echo("ABORTED")
        sys.exit(0)

    click.echo("\nDeleting... ", nl=False)
    click.echo(click.style("SUCCESS", fg="green"))
    click.echo("NOTE: tctl will need to be re-configured in order to work.")
    sys.exit(0)


def obfuscate(byt, password):
    mask = password.encode()
    lmask = len(mask)
    return bytes(c ^ mask[i % lmask] for i, c in enumerate(byt))


def encrypt(txt):
    return _b64encode(obfuscate(txt.encode(), hex(_token['id']))).decode()


def decrypt(txt):
    return obfuscate(_b64decode(txt.encode()), hex(_token['id'])).decode()


def config(source=None):
    click.echo(terminal.prompt)

    # if message:
    #     click.echo(message)
    #     click.echo("-----------------------------------------------------\n")

    dotenv.load_dotenv(env_path, verbose=True)
    no_token = not os.getenv("TOKEN")

    if no_token:
        click.echo("HELLO 👋")

        if source != "config":
            click.echo("""
tctl isn't configured on this machine yet.

Please have your API Key and Secret Key handy in
order to configure tctl.

Let's get started...

-----------------------------------------------------
""")
        else:
            click.echo("""
Welcome to the tctl!
""")

    else:
        click.echo("""Currently using CustomerId: {customer_id}""".format(
            customer_id=os.getenv("CUSTOMER_ID")))

        update = input("\nReplace it with a new one? [y/N]: ")
        if update not in ["y", "Y"]:
            click.echo("ABORTED")
            sys.exit(0)

    api_key = input("API Key:     ")
    api_secret = getpass("API Secret:  ")

    click.echo("\nValidating... ", nl=False)

    headers = {
        "TGX-API-KEY": api_key,
        "TGX-API-SECRET": api_secret
    }

    tokens = remote.api.get("/tokens?full=true", headers=headers)

    tctl_token = None
    for token in tokens:
        if token["name"] == _token["name"]:
            tctl_token = token
            break

    if not tctl_token:
        res = remote.api.post(
            "/token",
            json={"name": _token['name'], "ttl": -1},
            headers=headers)

        tctl_token = res.get("token")

    # write token
    dotenv.set_key(env_path, "TOKEN", encrypt(tctl_token))

    # get custoemer data
    res = remote.api.get(
        "/me", headers=remote.bearer_token(tctl_token))

    for key in ["name", "email", "customer_id"]:
        dotenv.set_key(env_path, key.upper(), res.get(key))

    click.echo(click.style("SUCCESS\n", fg="green"))
    click.echo("tctl is now configured! 🎉")

    if source == "config":
        click.echo("\nPlease run your command again")
