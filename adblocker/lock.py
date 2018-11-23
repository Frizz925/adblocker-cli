import os


class FileLock:
    def __init__(self, lockfile):
        self.lockfile = lockfile
        self.locked = self.check()
        self.fd = None

    def check(self):
        return os.path.exists(self.lockfile)

    def acquire(self):
        if self.locked:
            return
        self.fd = os.open(self.lockfile, os.O_CREAT | os.O_EXCL | os.O_RDONLY)
        self.locked = True

    def release(self):
        if not self.locked:
            return
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None
        os.unlink(self.lockfile)
        self.locked = False

    def raise_for_acquire(self):
        if self.locked:
            raise LockStateException('Current state is acquired')
        if self.check():
            raise FileExistsError('Lockfile already exists at ' + self.lockfile)
        if self.fd is not None:
            raise LockStateException('File descriptor for lockfile already exists! (The lockfile may have been abruptly removed)')

    def raise_for_release(self):
        if not self.locked:
            raise LockStateException('Current state is released')
        if not self.check():
            raise FileNotFoundError('Lockfile not found at ' + self.lockfile)


class LockStateException(Exception):
    pass
