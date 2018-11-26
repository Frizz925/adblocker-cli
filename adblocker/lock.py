import os


class FileLock:
    def __init__(self, lockfile):
        self.lockfile = lockfile
        self.fd = None

    @property
    def locked(self):
        return self.check()

    def check(self):
        return os.path.exists(self.lockfile)

    def acquire(self):
        if self.locked:
            return
        self.fd = os.open(self.lockfile, os.O_CREAT | os.O_EXCL | os.O_RDONLY)

    def release(self):
        if not self.locked:
            return
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None
        os.unlink(self.lockfile)

    def raise_for_acquire(self):
        if self.locked:
            raise LockStateException('Current state is acquired')

    def raise_for_release(self):
        if not self.locked:
            raise LockStateException('Current state is released')


class LockStateException(Exception):
    pass
