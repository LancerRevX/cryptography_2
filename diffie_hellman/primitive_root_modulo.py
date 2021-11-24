from lab1 import gcd, mod_exp
from rsa import euler


def is_primitive_root_modulo(g, m):
    raise NotImplementedError
    if gcd(g, m)[0] != 1:
        return False
    e = euler(m)
    # if mod_exp(g, e // 2, m)