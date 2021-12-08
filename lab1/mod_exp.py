def mod_exp(a: int, x: int, p: int) -> int:  # возведение в степень по модулю
    if min(a, x, p) < 0:
        raise ValueError('a, x, p must be whole')
    y, s = 1, a
    t = len(bin(x)[2:])
    for i in range(t):
        if x >> i & 1 == 1:
            y = y * s % p
        s = s * s % p
    return y
