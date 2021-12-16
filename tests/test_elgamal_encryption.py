import unittest
from elgamal_encryption import encrypt, decrypt, get_public_key


class TestElgamal(unittest.TestCase):
    def test_elgamal(self):
        message = 15

        public_key = get_public_key(23, 5, 13)
        self.assertEqual(public_key, 21)

        encrypted_message = encrypt(message, 23, 5, public_key, 7)
        self.assertEqual(encrypted_message, (17, 12))

        self.assertEqual(message, decrypt(encrypted_message, 23, 13))
