from test import test_cli
import unittest2

suite = unittest2.TestLoader().loadTestsFromModule(test_cli)
runner = unittest2.TextTestRunner()
runner.run(suite)
