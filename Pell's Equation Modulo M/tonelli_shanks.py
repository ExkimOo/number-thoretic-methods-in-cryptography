def sqrt_mod(a: int, p: int) -> int:
    if legendre_symbol(a, p) != 1:
        return 0
    elif a == 0:
        return 0
    elif p == 2:
        return 0
    elif p % 4 == 3:
        return pow(a, (p + 1) >> 2, p)

    s = p - 1
    e = 0
    while s % 2 == 0:
        s >>= 1
        e += 1

    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1

    x = pow(a, (s + 1) >> 1, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e

    while True:
        t = b
        m = 0

        for m in range(r):
            if t == 1:
                break

            t = pow(t, 2, p)

        if m == 0:
            return x

        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m


def legendre_symbol(a: int, p: int) -> int:
    m = pow(a, (p - 1) >> 1, p)
    return -1 if m == p - 1 else m
