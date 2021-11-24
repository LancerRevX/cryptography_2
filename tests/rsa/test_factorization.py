from unittest import TestCase
from rsa.factorization import factorize


class TestFactorization(TestCase):
    def test_factorization(self):
        self.assertEqual([3, 3], factorize(9))
        self.assertEqual([5, 3], factorize(15))
        self.assertEqual([11, 11, 7, 5, 3, 3, 2, 2, 2, 2], factorize(609840))
