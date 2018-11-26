from adblocker.cli import run_cli
from adblocker.runner import HandledTaskError
from adblocker.logging import Logging, DummyLogging
from adblocker import DEBUG

import unittest2
import os
import stat

FILENAME = os.path.join(os.path.dirname(__file__), 'hosts.txt')
TEST_FILES = [
    FILENAME,
    FILENAME + '.bak',
    FILENAME + '.lock',
]


class TestCLI(unittest2.TestCase):
    def assertFileExists(self, filename):
        self.assertTrue(os.path.exists(filename))

    def assertFileNotExists(self, filename):
        self.assertFalse(os.path.exists(filename))

    def setUp(self):
        self.cli = create_cli_wrapper()
        self.clear_test_files()

    def test_successful(self):
        self.do_add_call_test()
        self.do_remove_call_test()

    def test_missing_file(self):
        test_file = '/tmp/_not_exists'
        with self.assertRaises(HandledTaskError) as cm:
            self.cli('add', test_file)
        self.assertIn('not found', str(cm.exception))

    def test_unreadable_file(self):
        self.create_test_file(os.O_WRONLY)
        os.chmod(FILENAME, stat.S_IWRITE)
        with self.assertRaises(HandledTaskError) as cm:
            self.cli('add', FILENAME)
        self.assertIn('No read access', str(cm.exception))

    def test_unwritable_file(self):
        self.create_test_file(os.O_RDONLY)
        os.chmod(FILENAME, stat.S_IREAD)
        with self.assertRaises(HandledTaskError) as cm:
            self.cli('add', '/etc/hosts')
        self.assertIn('No write access', str(cm.exception))

    def test_multiple_add_calls(self):
        with self.assertRaises(HandledTaskError) as cm:
            self.do_add_call_test()
            self.do_add_call_test()
        self.assertIn('state is acquired', str(cm.exception))

    def test_single_remove_call(self):
        self.create_test_file()
        with self.assertRaises(HandledTaskError) as cm:
            self.do_remove_call_test()
        self.assertIn('state is released', str(cm.exception))

    def test_invalid_argument(self):
        with self.assertRaises(ValueError) as cm:
            self.cli('dummy')
        self.assertIn('Unknown mode', str(cm.exception))

    def do_add_call_test(self):
        os.close(os.open(FILENAME, os.O_CREAT | os.O_RDWR))
        self.cli('add', FILENAME)
        # Make sure backup and lock files exist
        self.assertFileExists(FILENAME + '.bak')
        self.assertFileExists(FILENAME + '.lock')

    def do_remove_call_test(self):
        self.cli('remove', FILENAME)
        # Make sure backup and lock files are removed
        self.assertFileNotExists(FILENAME + '.bak')
        self.assertFileNotExists(FILENAME + '.lock')

    def tearDown(self):
        self.clear_test_files()

    def create_test_file(self, flags=0):
        os.close(os.open(FILENAME, os.O_CREAT | flags))

    def clear_test_files(self):
        for filename in TEST_FILES:
            self.remove_if_exists(filename)

    def remove_if_exists(self, filename):
        if os.path.exists(filename):
            os.unlink(filename)


def create_cli_wrapper():
    logging = Logging() if DEBUG else DummyLogging()

    def wrapper(*args):
        run_cli(*args, logging=logging)
    return wrapper
