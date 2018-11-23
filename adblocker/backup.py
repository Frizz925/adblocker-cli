import shutil
import os


class FileBackup:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

    def backup(self):
        shutil.copy(self.source, self.destination)

    def restore(self):
        shutil.copy(self.destination, self.source)
        os.unlink(self.destination)
