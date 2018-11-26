from test.test_cli import TestCLI
from test.test_adblocker import TestAdblocker

import unittest2
import sys

if __name__ == '__main__':
    test_cases = [
        TestAdblocker,
        TestCLI
    ]

    loader = unittest2.TestLoader()
    suites = map(lambda x: loader.loadTestsFromTestCase(x), test_cases)
    main_suite = unittest2.TestSuite(suites)
    runner = unittest2.TextTestRunner()
    results = runner.run(main_suite)
    if len(results.errors) > 0 or len(results.failures) > 0:
        sys.exit(1)
