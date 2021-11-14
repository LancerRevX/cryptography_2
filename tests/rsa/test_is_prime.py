from unittest import TestCase
from rsa import is_prime
from rsa import exceptions as rsa_exceptions


class TestIsPrime(TestCase):
    def test_is_prime(self):
        self.assertEqual(True, is_prime(1))
        self.assertEqual(True, is_prime(2))
        self.assertEqual(True, is_prime(3))
        self.assertEqual(False, is_prime(4))
        self.assertEqual(True, is_prime(5))
        self.assertEqual(False, is_prime(6))
        self.assertRaises(rsa_exceptions.NumberNotNaturalError, is_prime, 0)
        self.assertRaises(rsa_exceptions.NumberNotNaturalError, is_prime, -1)
