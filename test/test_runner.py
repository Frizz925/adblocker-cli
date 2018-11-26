from adblocker.logging import Logging, DummyLogging
from adblocker.runner import Task, TaskRunner, TaskError
from adblocker import DEBUG

import unittest2

EXC_MESSAGE = 'This is an expected exception'


class TestRunner(unittest2.TestCase):
    def test_task_runner(self):
        def exception_task():
            raise Exception(EXC_MESSAGE)
        tasks = [Task('exception', exception_task)]
        logging = Logging() if DEBUG else DummyLogging()
        runner = TaskRunner(logging)
        with self.assertRaises(TaskError) as cm:
            runner.run(tasks)
        self.assertIn(EXC_MESSAGE, str(cm.exception))
