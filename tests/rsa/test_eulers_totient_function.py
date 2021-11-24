from unittest import TestCase
from rsa.eulers_totient_function import euler


class TestFactorization(TestCase):
    def test_factorization(self):
        self.assertEqual(12, euler(36))
