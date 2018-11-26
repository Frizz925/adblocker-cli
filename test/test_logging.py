from adblocker.logging import Logging

import os
import unittest2

LOGGING_DIR = os.path.dirname(__file__)
STDOUT_FILE = os.path.join(LOGGING_DIR, 'stdout.txt')
STDERR_FILE = os.path.join(LOGGING_DIR, 'stderr.txt')


class TestLogging(unittest2.TestCase):
    def setUp(self):
        self.create_log_files()

    def test_file_logging(self):
        with open(STDOUT_FILE, 'w') as stdout:
            with open(STDERR_FILE, 'w') as stderr:
                logging = Logging(stdout, stderr)
                logging.log('This is stdout')
                logging.error('This is stderr')

        with open(STDOUT_FILE, 'r') as f:
            self.assertIn('This is stdout', f.read())
        with open(STDERR_FILE, 'r') as f:
            self.assertIn('This is stderr', f.read())

    def tearDown(self):
        self.remove_log_files()

    def create_log_files(self):
        self.create_log_file(STDOUT_FILE)
        self.create_log_file(STDERR_FILE)

    def create_log_file(self, filename):
        if not os.path.exists(filename):
            os.close(os.open(filename, os.O_CREAT))
        os.chmod(filename, 436)

    def remove_log_files(self):
        self.remove_log_file(STDOUT_FILE)
        self.remove_log_file(STDERR_FILE)

    def remove_log_file(self, filename):
        if os.path.exists(filename):
            os.unlink(filename)
