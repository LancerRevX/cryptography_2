from lab1 import gcd, mod_exp, inversion
from sympy import isprime
from sympy.ntheory.generate import randprime


class InvalidVariableError(Exception):
    def __init__(self, variable):
        super().__init__()
        self.variable = variable


def shamir(m: int, p: int, ca: int, da: int, cb: int, db: int) -> tuple[int, int, int, int]:
    if m <= 0 or m >= p:
        raise InvalidVariableError('m')
    if p <= 0 or not isprime(p):
        raise InvalidVariableError('p')
    if ca <= 0 or gcd(ca, p - 1)[0] != 1:
        raise InvalidVariableError('ca')
    if cb <= 0 or gcd(cb, p - 1)[0] != 1:
        raise InvalidVariableError('cb')
    if da <= 0 or ca * da % (p - 1) != 1:
        raise InvalidVariableError('da')
    if db <= 0 or cb * db % (p - 1) != 1:
        raise InvalidVariableError('db')
    x1 = mod_exp(m, ca, p)
    x2 = mod_exp(x1, cb, p)
    x3 = mod_exp(x2, da, p)
    x4 = mod_exp(x3, db, p)
    return x1, x2, x3, x4


def generate_p(order):
    if order < 0:
        raise InvalidVariableError('order')
    return randprime(10**order, 10**(order+1)-1)


def generate_c(start_c, p):
    if not isprime(p):
        raise InvalidVariableError('p')

    def find_c(start_c_):
        c = start_c_
        while gcd(c, p-1)[0] != 1:
            c += 1
        return c
    ca = find_c(start_c if start_c >= 2 else 2)
    cb = find_c(ca + 1)

    return ca, cb


def generate_d(ca, cb, p):
    if not isprime(p):
        raise InvalidVariableError('p')
    if ca < 1 or gcd(ca, p-1)[0] != 1:
        raise InvalidVariableError('ca')
    if cb < 1 or gcd(cb, p-1)[0] != 1:
        raise InvalidVariableError('cb')
    da = inversion(ca, p-1)
    db = inversion(cb, p-1)
    return da, db

