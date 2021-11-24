from .exceptions import NumberNotNaturalError
from .is_prime import is_prime


def factorize(number: int) -> list[int]:
    if number <= 0:
        raise NumberNotNaturalError
    result = []
    if number == 1:
        result.append(number)
    while number > 1:
        if is_prime(number):
            result.append(number)
            break
        for divisor in range(number // 2, 1, -1):
            if number % divisor == 0 and is_prime(divisor):
                while number % divisor == 0:
                    number //= divisor
                    result.append(divisor)
                break
    return result
