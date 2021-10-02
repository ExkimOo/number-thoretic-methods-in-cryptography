from gmpy2 import mpz, mul, add, sub, powmod
from diemitko import generate_prime
import pyecm


def generate_p_g():
    while True:
        q = generate_prime(155, 13)
        p = add(mul(mpz(2), q), 1)
        print('p candidate: ', p)
        if powmod(2, sub(p, 1), p) == 1:
            p_factorized = list(pyecm.factors(p, False, True, 1, 1))
            if len(p_factorized) == 1:
                print('\n', p, ' - is prime')
                for g in range(1, p):
                    if powmod(g, q, p) != 1:
                        return p, mpz(g)


def main():
    p, g = generate_p_g()

    A_secret_key = generate_prime(155, 29)
    B_secret_key = generate_prime(155, 31)

    A_public_key = powmod(g, A_secret_key, p)
    B_public_key = powmod(g, B_secret_key, p)

    A_message = powmod(B_public_key, A_secret_key, p)
    B_message = powmod(A_public_key, B_secret_key, p)
   
    print('\nPublic data\np: ', p, '\ng: ', g, '\n')
    print('Alice secret key: ', 155*'*')
    print('Alice public key: ', A_public_key)
    print('Bob secret key:   ', 155*'*')
    print('Bob public key:   ', B_public_key, '\n')
    
    print('Common key calculated from Alice: ', A_message)
    print('Common key calculated from Bob:   ', B_message)


if __name__ == '__main__':
    main()