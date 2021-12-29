import unittest
from sha_1 import sha1
from sha_1 import SHA1Hash


class TestSha1(unittest.TestCase):
    def test_sha1(self):
        self.assertEqual('d8f4590320e1343a915b6394170650a8f35d6926', sha1('sha'))
        self.assertEqual('ba79baeb9f10896a46ae74715271b7f586e74640', sha1('Sha'))
        self.assertEqual('da39a3ee5e6b4b0d3255bfef95601890afd80709', sha1(''))
        self.assertEqual('2fd4e1c67a2d28fced849ee1bb76e7391b93eb12', sha1('The quick brown fox jumps over the lazy dog'))
        self.assertEqual('9e32295f8225803bb6d5fdfcc0674616a4413c1b', sha1('В чащах юга жил бы цитрус? Да, но фальшивый экземпляр!'))


class TestSha1Git(unittest.TestCase):
    def test_sha1(self):
        self.assertEqual('d8f4590320e1343a915b6394170650a8f35d6926', SHA1Hash(bytes('sha', 'utf-8')).final_hash())