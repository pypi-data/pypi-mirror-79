"""
Channeling main module.
"""
import channeling as app

from textwrap import dedent
import click
import logging
import sys

logger = logging.getLogger(__name__)

@click.group()
@click.version_option(version=app.__version__,
    message="%(prog)s %(version)s - {}".format(app.__copyright__))
@click.option('-d', '--debug', is_flag=True,
    help="Enable debug mode with output of each action in the log.")
@click.pass_context
def cli(ctx, **kwargs): # pragma: no cover
    logging.basicConfig(
        format = '%(asctime)s.%(msecs)03d, %(levelname)s: %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S',
        filename = None,
        level = logging.DEBUG if ctx.params.get('debug') else logging.WARNING,
        )

@cli.command()
def run(**kwargs): # pragma: no cover
    "Run bot service."
    print("Did I do good?")

if __name__ == '__main__': # pragma: no cover
    cli()

