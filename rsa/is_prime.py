from .exceptions import NumberNotNaturalError


def is_prime(number: int):
    if number <= 0:
        raise NumberNotNaturalError
    for i in range(number // 2, 1, -1):
        if number % i == 0:
            return False
    return True
