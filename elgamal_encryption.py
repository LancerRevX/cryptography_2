from random import randint
from sympy import isprime, randprime, is_primitive_root, gcd
from typing import Optional


class ElgamalError(Exception): pass
class InvalidMessageError(ElgamalError): pass
class InvalidEncryptedMessageError(ElgamalError): pass
class InvalidPError(ElgamalError): pass
class InvalidPOrderError(ElgamalError): pass
class InvalidGError(ElgamalError): pass
class InvalidKError(ElgamalError): pass
class InvalidPublicKeyError(ElgamalError): pass
class InvalidPrivateKeyError(ElgamalError): pass


def generate_p(order: int) -> int:
    if order < 0:
        raise InvalidPOrderError
    return randprime(10**order, 10**(order+1))


def generate_g(p: int, start_g: int = 0) -> int:
    if not isprime(p):
        raise InvalidPError
    g = start_g + 1 if start_g >= 2 else 2
    while True:
        if gcd(g, p) == 1 and is_primitive_root(g, p):
            return g
        g += 1


def generate_private_key(p):
    if not isprime(p):
        raise InvalidPError
    if p < 5:
        return None
    return randint(2, p-2)


def get_public_key(p, g, c):
    if not isprime(p):
        raise InvalidPError
    if gcd(g, p) != 1 or not is_primitive_root(g, p):
        raise InvalidGError
    if not 1 < c < p - 1:
        raise InvalidPrivateKeyError
    return pow(g, c, p)


def encrypt(m: int, p: int, g: int, d: int, k: Optional[int] = None) -> tuple[int, int]:
    if not 1 <= m < p:
        raise InvalidMessageError
    if not isprime(p):
        raise InvalidPError
    if gcd(g, p) != 1 or not is_primitive_root(g, p):
        raise InvalidGError
    if not 1 <= d < p:
        raise InvalidPublicKeyError
    if k is None:
        k = randint(2, p-2)
    elif not 1 < k < p-1:
        raise InvalidKError
    r = pow(g, k, p)
    e = m * pow(d, k) % p
    return r, e


def decrypt(m: tuple[int, int], p: int, c: int):
    r, e = m
    if not 1 <= r < p or not 1 <= e < p:
        raise InvalidMessageError
    if not isprime(p):
        raise InvalidPError
    if not 1 < c < p-1:
        raise InvalidPrivateKeyError
    return e * pow(r, p - 1 - c) % p