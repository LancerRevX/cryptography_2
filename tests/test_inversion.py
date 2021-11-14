from unittest import TestCase
from lab1 import inversion


class TestInversion(TestCase):
    def test_inversion(self):
        self.assertEqual(2, inversion(5, 9))