from lab1 import mod_exp
from sympy import isprime
from rsa.exceptions import NumberNotPrimeError, NumberNotNaturalError


def generate_q(start_q):
    if not isprime(start_q):
        raise NumberNotPrimeError
    q = start_q + 1
    p = q*2 + 1
    while not isprime(q) or not isprime(p):
        q += 1
        p = q*2 + 1
    return q


def generate_g(q, start_g):
    p = 2*q + 1
    if not isprime(q) or not isprime(p):
        raise NumberNotPrimeError
    for g in range(start_g + 1, p-1):
        if mod_exp(g, q, p) != 1:
            return g
    return None


def calculate_secret_key(g, p, a, b):
    if not a >= 1 or not b >= 1:
        raise NumberNotNaturalError
    q = (p - 1) // 2
    if not isprime(q):
        raise NumberNotPrimeError('q is not prime')
    if not isprime(p):
        raise NumberNotPrimeError('p is not prime')
    if not 1 < g < p-1 or mod_exp(g, q, p) == 1:
        raise ValueError('invalid g')
    A = mod_exp(g, a, p)
    B = mod_exp(g, b, p)
    K = mod_exp(A, b, p)
    return A, B, K
