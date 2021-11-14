from typing import Optional


def gcd(a: int, b: int) -> Optional[tuple[int, int, int]]:
    if min(a, b) < 0:
        raise ValueError('a and b must be greater then zero')
    if a < b:
        a, b = b, a
    u = (a, 1, 0)
    v = (b, 0, 1)
    while v[0] != 0:
        q = u[0] // v[0]
        t = (u[0] % v[0], u[1] - q*v[1], u[2] - q*v[2])
        u, v = v, t
    return u
