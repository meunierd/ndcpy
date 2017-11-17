import unittest
from datetime import datetime

from tests.fixtures.images import FDI_PATH
from tests.fixtures.ndcs import BIN_PATH

from ndc import NDC


class TestNDC(unittest.TestCase):
    def setUp(self):
        self.ndc = NDC(BIN_PATH)
        self.expected = ('A', '', '15', datetime(2017, 12, 7, 7, 36, 44))

    def test_list(self):
        self.assertEqual([self.expected], self.ndc.list(FDI_PATH))

    def test_find(self):
        self.assertEqual(self.expected, self.ndc.find(FDI_PATH, 'A'))
        self.assertEqual(None, self.ndc.find(FDI_PATH, 'Z'))

    def test_find_all(self):
        self.assertEqual([self.expected], self.ndc.find_all(FDI_PATH, 'A'))
