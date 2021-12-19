import unittest
from md5 import md5


class TestMd5(unittest.TestCase):
    def test_md5(self):
        self.assertEqual('1bc29b36f623ba82aaf6724fd3b16718', md5('md5'))
        self.assertEqual('9e107d9d372bb6826bd81d3542a419d6', md5('The quick brown fox jumps over the lazy dog'))
