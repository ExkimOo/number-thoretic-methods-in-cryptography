from random import randint
from gmpy2 import mpz, gcdext
from tinyec.registry import *
from convert import ascii_to_num, num_to_ascii


def main():
    curve = get_curve('brainpoolP160r1')
    p = curve.field.p

    A_c = randint(1, curve.field.n - 1)
    A_d = A_c*curve.g

    B_c = randint(1, curve.field.n - 1)
    B_d = B_c*curve.g

    m = input('Enter your message:'.rjust(37) + ' ')
    m_number = ascii_to_num(m)

    print('Message in ASCII coding:'.rjust(37), m_number)
    print()
    print('[Public Data]'.center(200))
    print()
    print('Curve:'.rjust(37), curve)
    print('G:'.rjust(37), curve.g)
    print('Alice public key:'.rjust(37), A_d)
    print('Bob public key:'.rjust(37), B_d)
    print()

    print('[Sending of Data]'.center(200))
    print()
    msg = ''
    for i in range(0, len(m_number), len(str(p))-1):
        part = m_number[i:(lambda x: x if x < len(m_number) else len(m_number))(i+len(str(p))-1)]
        print((str(int(i / (len(str(p))-1)) + 1) + ' part:').rjust(37) + ' ', part, '\n')

        zeroes = ''
        for i in part:
            if i == '0':
                zeroes += '0'
            else:
                break

        while True:
            A_k = randint(1, curve.field.n - 1)
            P = A_k*B_d
            if P.x != 0:
                break

        R = A_k*curve.g
        e = int(part)*P.x % p

        print('[Alice Encrypting]'.center(200))
        print()
        print('R = k*G ='.rjust(37), R)
        print('P = k*B[public key] = (x, y) ='.rjust(37), P)
        print('e = m*x mod p ='.rjust(37), e)
        print()
        print('[Sending Couple (R,e) to Bob]'.center(200))
        print()

        Q = B_c*R
        _, x_inversed, _ = gcdext(mpz(Q.x), mpz(p))
        part_recieved = e*x_inversed % p

        print('[Bob Decrypting]'.center(200))
        print()
        print('Q = B[private key]*R = (x, y) ='.rjust(37), Q)
        print('m = e*x^(-1) mod p ='.rjust(37), part_recieved)
        print()

        msg += zeroes + str(part_recieved)

    print('[Ending of Sending Data]'.center(200) + '\n')

    msg = num_to_ascii(msg)
    print('Message recieved: '.rjust(37), msg)


if __name__ == '__main__':
    main()