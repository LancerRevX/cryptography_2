import unittest
from shamirs_secret_sharing import shamir


class TestShamir(unittest.TestCase):
    def test_shamir(self):
        self.assertEqual((14, 15, 19, 10), shamir(10, 23, 7, 19, 5, 9))

