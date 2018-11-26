from six import string_types

import unittest2
import adblocker


class TestAdblocker(unittest2.TestCase):
    def test_fetch(self):
        adblock_list = adblocker.fetch_adblock_list()
        self.assertTrue(isinstance(adblock_list, string_types))
