import shelve
from contextlib import contextmanager

import click


@contextmanager
def state_file(path):
    try:
        with shelve.open(str(path), writeback=True) as shelf:
            yield shelf
    except OSError as e:
        if e.errno == 35:
            raise click.ClickException(
                "hackgame is currently running in another process"
            )
        else:
            raise
