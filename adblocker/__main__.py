from .logging import Logging
from .runner import HandledTaskError
from .cli import run_cli
from . import DEBUG, HOSTS_FILE

import click
import sys


@click.group('adblocker')
@click.version_option('0.1', prog_name='adblocker')
def cli():
    pass


@click.command('add', help='Add adblock list to hosts file')
@click.argument('filename', default=HOSTS_FILE)
def add(filename):
    run_cli_then_exit('add', filename)


@click.command('remove', help='Remove adblock list from hosts file')
@click.argument('filename', default=HOSTS_FILE)
def remove(filename):
    run_cli_then_exit('remove', filename)


def run_cli_then_exit(*args):
    logging = Logging()
    try:
        run_cli(*args, logging=logging)
    except Exception as exc:
        if DEBUG:
            raise
        if not isinstance(exc, HandledTaskError):
            logging.error(str(exc))
        sys.exit(1)


cli.add_command(add)
cli.add_command(remove)


if __name__ == '__main__':
    cli()
