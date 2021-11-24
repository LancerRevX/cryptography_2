from unittest import TestCase
import rsa


class TestRsa(TestCase):
    def setUp(self):
        self.public_key_1, self.private_key_1 = rsa.create_keys(17, 599, 11)

    def test_create_keys(self):
        self.assertEqual(((17, 26), (5, 26)), rsa.create_keys(2, 13, 17))
        self.assertEqual(((7, 33), (3, 33)), rsa.create_keys(3, 11, 7))
        self.assertEqual((self.public_key_1, self.private_key_1), rsa.create_keys(17, 599, 11))

    def test_encrypt(self):
        self.assertRaises(rsa.exceptions.InvalidMessage, rsa.encode, (17, 26), 'ы')
        self.assertEqual(
            'hello',
            rsa.encode(
                self.public_key_1,
                rsa.encode(
                    self.private_key_1,
                    'hello'
                )))

    def test_decrypt(self):
        self.assertEqual(
            'hello',
            rsa.encode(
                self.private_key_1,
                rsa.encode(
                    self.public_key_1,
                    'hello'
                )))
        self.assertEqual(
            'привет',
            rsa.encode(
                self.private_key_1,
                rsa.encode(
                    self.public_key_1,
                    'привет'
                )))
