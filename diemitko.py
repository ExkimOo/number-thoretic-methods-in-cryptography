import random
import sympy
from gmpy2 import mpz, f_div, is_odd, mul, powmod, add, sub, mpfr

def generate_prime(size, q, base = 10):
    
    if q is None:
        sympy.prime(size)

    N = mpz(base**(size-1))
    u = mpz(0)

    N1 = f_div(N, q)
    N2 = f_div(mpz(mul(N, mpfr(random.random()))), q)
    N = add(N1, N2)

    if is_odd(N):
        N = add(N, 1)
    
    while True:
        p = add(mul(add(N, u), q), 1)

        if powmod(2, sub(p, 1), p) == 1 and powmod(2, add(p, u), p) != 1:
            break

        u = add(u, 2)
    
    return p



