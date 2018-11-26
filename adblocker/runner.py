from .logging import Logging
from six import raise_from
import sys


class TaskRunner:
    def __init__(self, logging=None, error_handler=None):
        if logging is None:  # pragma: no cover
            logging = Logging(stdout=sys.stdout, stderr=sys.stderr)
        self._logging = logging
        self._error_handler = error_handler

    def run(self, tasks):
        context = TaskRunnerContext()
        for task in tasks:
            message = self._get_message_for_task(task)
            self._logging.log(' > %s... ' % message, newline=False)
            try:
                result = task.run(context)
                context.results[task.name] = result
                context.last_result = result
            except Exception as exc:
                self._logging.log('FAIL!')
                if self._error_handler is None:
                    raise_from(TaskError(task, exc), exc)
                result = self._error_handler(exc, task=task, context=context)
                raise_from(HandledTaskError(task, exc, result=result), exc)
            self._logging.log('OK.')
        self._logging.log('Finished.')

    def _get_message_for_task(self, task):
        if task.description is None:
            return '[%s] Running' % task.name
        else:
            return '[%s] %s' % (task.name, task.description)


class TaskRunnerContext:
    def __init__(self):
        self.results = {}
        self.last_result = None


class Task:
    def __init__(self, name, target, description=None, args=(), kwargs={}):
        self._args = args
        self._kwargs = kwargs

        self.name = name
        self.target = target
        self.description = description

    def run(self, context):
        if hasattr(self.target, '__runner_aware'):
            return self.target(context, args=self._args, kwargs=self._kwargs)
        else:
            return self.target(*self._args, **self._kwargs)


class TaskError(Exception):
    def __init__(self, task, exc):
        super(TaskError, self).__init__('[%s] %s' % (task.name, str(exc)))
        self.task = task
        self.exc = exc


class HandledTaskError(TaskError):
    def __init__(self, task, exc, result=None):
        super(HandledTaskError, self).__init__(task, exc)
        self.handler_result = result


def runner_aware(func):
    def wrapper(context, args=(), kwargs={}):
        return func(context, *args, **kwargs)

    setattr(wrapper, '__runner_aware', True)
    return wrapper
