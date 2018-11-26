from adblocker.lock import FileLock, LockStateException

import os
import unittest2

LOCK_FILE = os.path.join(os.path.dirname(__file__), 'test.lock')


class TestLock(unittest2.TestCase):
    def setUp(self):
        self.remove_lock_file()
        self.lock = FileLock(LOCK_FILE)

    def test_acquire(self):
        self.lock.raise_for_acquire()
        # Make sure it's okay to call acquire twice
        self.lock.acquire()
        self.lock.acquire()
        self.assertTrue(self.lock.locked)

        with self.assertRaises(LockStateException) as cm:
            self.lock.raise_for_acquire()
        self.assertIn('state is acquired', str(cm.exception))

    def test_acquire_with_file(self):
        self.create_lock_file()
        # Make sure it's okay to call acquire while lock file exists
        self.lock.acquire()
        with self.assertRaises(LockStateException) as cm:
            self.lock.raise_for_acquire()
        self.assertIn('state is acquired', str(cm.exception))

    def test_release(self):
        # Make sure it's okay to call release while lock file doesn't exist
        self.lock.release()
        with self.assertRaises(LockStateException) as cm:
            self.lock.raise_for_release()
        self.assertIn('state is released', str(cm.exception))

    def test_release_with_file(self):
        self.create_lock_file()
        self.lock.raise_for_release()
        # Make sure it's okay to call release twice
        self.lock.release()
        self.lock.release()
        self.assertFalse(self.lock.locked)

        with self.assertRaises(LockStateException) as cm:
            self.lock.raise_for_release()
        self.assertIn('state is released', str(cm.exception))

    def test_acquire_then_release(self):
        self.lock.raise_for_acquire()
        self.lock.acquire()
        self.lock.raise_for_release()
        self.lock.release()

    def create_lock_file(self):
        os.close(os.open(LOCK_FILE, os.O_CREAT | os.O_RDWR))

    def remove_lock_file(self):
        if os.path.exists(LOCK_FILE):
            os.unlink(LOCK_FILE)

    def tearDown(self):
        self.remove_lock_file()
