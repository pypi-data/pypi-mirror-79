"""
Command Line Application for creating database data for testing.
"""
import click


@click.group()
def cli():
    pass


@cli.command()
def hello_world():
    """
    Example command
    """
    click.echo("Hello world!")


