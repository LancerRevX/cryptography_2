from unittest import TestCase
from lab1 import mod_exp


class TestModExp(TestCase):
    def test_mod_exp(self):
        self.assertEqual(445, mod_exp(4, 13, 497))
