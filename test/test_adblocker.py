import unittest2
import adblocker


class TestAdblocker(unittest2.TestCase):
    def test_fetch(self):
        adblock_list = adblocker.fetch_adblock_list()
        self.assertTrue(type(adblock_list) is str)
