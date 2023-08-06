
import click

@click.group()
def cli():
    pass


@cli.command()
def help():
    click.echo("""
Hello!
""")
