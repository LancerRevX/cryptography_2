import unittest
from lab1 import gcd


class TestGcd(unittest.TestCase):
    def test_gcd(self):
        self.assertEqual((3, 2, -3), gcd(24, 15))
        self.assertEqual(1, gcd(5, 9)[0])

