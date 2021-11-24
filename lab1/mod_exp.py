def mod_exp(a: int, x: int, p: int) -> int:  # возведение в степень по модулю
    y, s = 1, a
    t = len(bin(x)[2:])
    for i in range(t):
        if x >> i & 1 == 1:
            y = y * s % p
        s = s * s % p
    return y