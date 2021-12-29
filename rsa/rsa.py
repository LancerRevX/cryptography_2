from lab1 import gcd, inversion, mod_exp
from .is_prime import is_prime
from .exceptions import NumberNotPrimeError, InvalidPublicExponentError, InvalidMessage, NumberNotNaturalError
import logging


def generate_e(p: int, q: int):
    if not is_prime(p) or not is_prime(q):
        raise NumberNotPrimeError
    n = p * q
    euler = (p - 1) * (q - 1)
    for e in range(2, n):
        if gcd(e, euler)[0] == 1:
            return e
    return None


def create_keys(p: int, q: int, e: int) -> tuple[tuple[int, int], tuple[int, int]]:
    if not is_prime(p) or not is_prime(q):
        raise NumberNotPrimeError
    n = p * q
    euler = (p - 1) * (q - 1)
    if not 1 < e < n or gcd(e, euler)[0] != 1:
        raise InvalidPublicExponentError
    public_key = (e, n)
    d = inversion(e, euler)
    private_key = (d, n)
    return public_key, private_key


def encode_text(key: tuple[int, int], message: str) -> str:
    if not key[0] >= 1 or not key[1] >= 1:
        raise NumberNotNaturalError
    result = ''
    for m in message:
        m = ord(m)
        if not 0 <= m < key[1]:
            raise InvalidMessage
        m = mod_exp(m, key[0], key[1])
        result += chr(m)
    return result


def encode_int(key: tuple[int, int], message: int) -> int:
    if not key[0] >= 1 or not key[1] >= 1:
        raise NumberNotNaturalError
    if not 0 <= message < key[1]:
        raise InvalidMessage
    return mod_exp(message, key[0], key[1])
