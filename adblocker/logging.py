import sys


class Logging:
    def __init__(self, stdout=sys.stdout, stderr=sys.stderr):
        self.stdout = stdout
        self.stderr = stderr

    def log(self, message, **kwargs):
        self.stdout.write(self.format_message(message, **kwargs))

    def error(self, message, **kwargs):
        self.stderr.write(self.format_message(message, **kwargs))

    def format_message(self, message, newline=True):
        return message if not newline else message + '\n'


class DummyLogging(Logging):
    def log(self, message, **kwargs):
        pass

    def error(self, message, **kwargs):
        pass
