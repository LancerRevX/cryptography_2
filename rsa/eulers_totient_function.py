from .exceptions import NumberNotNaturalError
from .is_prime import is_prime
from .factorization import factorize
from collections import Counter


def euler(n: int) -> int:
    if not n > 0:
        raise NumberNotNaturalError
    if is_prime(n):
        return n - 1
    result = 1
    factors = Counter(factorize(n))
    for p in factors.keys():
        result *= p**factors[p] - p**(factors[p]-1)
    return result

