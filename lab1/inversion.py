from .gcd import gcd


def inversion(e: int, z: int) -> int:
    if gcd(e, z)[0] != 1:
        raise ValueError('e and z must be mutually simple')
    u = (z, 0)
    v = (e, 1)
    while v[0] != 0:
        q = u[0] // v[0]
        t = (u[0] % v[0], u[1] - q*v[1])
        u, v = v, t
    d = u[1]
    return d if d > 0 else d + z