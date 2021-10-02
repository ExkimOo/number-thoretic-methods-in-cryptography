from diemitko import generate_prime
from gmpy2 import gcd, gcdext, mpz, powmod
from random import randint
from convert import ASCIItoNum, NumtoASCII


def generate_c_d(prime, exclude=1):
    while True:
        c = randint(1, 1000)
        if gcd(c, prime - 1) == 1:
            _, d, _ = gcdext(c, prime-1)
            while d < 0:
                d += prime-1

            return c, d


def main():
    p = generate_prime(155, 41)    
    m = input('\n\n' + 'Enter your message:'.rjust(37) + ' ')

    m_number = ASCIItoNum(m)
    print('Message in ASCII coding:'.rjust(37), m_number, '\n')

    print('p: '.rjust(37), p)
    print()
    print('[Sending of Data]'.center(200))
    print()
    msg = ''
    for i in range(0, len(m_number), len(str(p))-1):
        part = m_number[i:(lambda x: x if x < len(m_number) else len(m_number))(i+len(str(p))-1)]
        print((str(int(i / (len(str(p))-1)) + 1) + ' part:').rjust(37), part)

        zeroes = ''
        for i in part:
            if i == '0':
                zeroes += '0'
            else:
                break

        A_c, A_d = generate_c_d(p)
        B_c, B_d = generate_c_d(p, A_c)

        print()
        print('A[c]:'.rjust(37), A_c)
        print('A[d]:'.rjust(37),  A_d)
        print('B[c]:'.rjust(37), B_c)
        print('B[d]:'.rjust(37), B_d)
        print()

        X1 = powmod(mpz(part), A_c, p)
        X2 = powmod(X1, B_c, p)
        X3 = powmod(X2, A_d, p)
        X4 = powmod(X3, B_d, p)
        msg += zeroes + str(X4)

        print('Alice : x1 = m^A[c] mod p ='.rjust(37), X1)
        print()
        print('[Sending x1 to Bob]'.center(200))
        print()
        print('Bob: x2 = x1^B[c] mod p ='.rjust(37), X2)
        print()
        print('[Sending x2 to Alice]'.center(200))
        print()
        print('Alice: x3 = x2^A[d] mod p ='.rjust(37), X3)
        print()
        print('[Sending x3 to Bob]'.center(200))
        print()
        print('Bob: x4 = x3^B[d] mod p ='.rjust(37), X4)
        print()

    print('[Ending of Sending Data]'.center(200))
    print()

    msg = NumtoASCII(msg)
    print('Message recieved:'.rjust(37), msg)


if __name__ == '__main__':
    main()