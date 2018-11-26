from .lock import FileLock
from .backup import FileBackup
from .runner import TaskRunner, Task, runner_aware
from .logging import Logging
from . import fetch_adblock_list, HOSTS_FILE

import codecs
import os


def run_cli(mode=None, hosts_file=HOSTS_FILE, logging=None):
    if logging is None:  # pragma: no cover
        logging = Logging()

    def check_file_exists():
        if not os.path.exists(hosts_file):
            raise OSError(hosts_file + ' not found')

    def check_file_readable():
        if not os.access(hosts_file, os.R_OK):
            raise OSError('No read access to ' + hosts_file)

    def check_file_writable():
        if not os.access(hosts_file, os.W_OK):
            raise OSError('No write access to ' + hosts_file)

    lock = FileLock(hosts_file + '.lock')
    backup = FileBackup(hosts_file, hosts_file + '.bak')

    tasks = [
        Task('hosts.exists', check_file_exists, 'Checking if hosts file exists'),
        Task('hosts.read', check_file_readable, 'Checking if hosts file is readable'),
        Task('hosts.write', check_file_writable, 'Checking if hosts file is writable'),
    ]
    error_handler = create_error_handler(logging)
    if mode == 'add':
        tasks.extend(add_adblock(logging, lock, backup))
    elif mode == 'remove':
        tasks.extend(remove_adblock(logging, lock, backup))
    else:
        raise ValueError('Unknown mode ' + mode)
    TaskRunner(logging, error_handler=error_handler).run(tasks)


def add_adblock(logging, lock, backup):
    def acquire_lock():
        lock.raise_for_acquire()
        lock.acquire()

    return [
        Task('lock.acquire', acquire_lock, 'Acquiring lock'),
        Task('hosts.backup', backup.backup, 'Backing up hosts file'),
        Task('filter.fetch', fetch_adblock_list, 'Fetching adblock list'),
        Task('hosts.write', write_hosts_file, 'Writing adblock list to hosts file', args=(backup.source,)),
    ]


def remove_adblock(logging, lock, backup):
    return [
        Task('lock.check', lock.raise_for_release, 'Checking for lock'),
        Task('hosts.restore', backup.restore, 'Restoring hosts file'),
        Task('lock.release', lock.release, 'Releasing lock'),
    ]


def create_error_handler(logging, messages={}):
    def error_handler(exc, **kwargs):
        task = kwargs['task']
        name = task.name
        message = messages[name] if name in messages else str(exc)
        logging.error('[%s] [Error] %s' % (name, message))

    return error_handler


@runner_aware
def write_hosts_file(context, hosts_file):
    adblock_list = context.last_result
    with codecs.open(hosts_file, mode='a', encoding='utf-8') as f:
        f.write(adblock_list)
