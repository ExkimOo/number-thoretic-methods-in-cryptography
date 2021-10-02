from DiffieHellman import generate_p_g
from gmpy2 import mpz, mul, add, sub, powmod
from diemitko import generate_prime
from random import randint
from convert import ascii_to_num, num_to_ascii


def main():
    p, g = generate_p_g()

    A_secret_key = generate_prime(155, 29)
    B_secret_key = generate_prime(155, 31)

    A_public_key = powmod(g, A_secret_key, p)
    B_public_key = powmod(g, B_secret_key, p)

    m = input('\n\n' + 'Enter your message:'.rjust(37) + ' ')#'Hello world! Hello world! Hello world!Hello world! Hello world! Hello world!Hello world! Hello world! Hello world!'
    m_number = ascii_to_num(m)

    print('Message in ASCII coding:'.rjust(37), m_number)
    print()
    print('[Public Data]'.center(200))
    print()
    print('p: '.rjust(37), p)
    print('g: '.rjust(37), g)

    print('[Sending of Data]'.center(200))
    print()
    msg = ''
    for i in range(0, len(m_number), len(str(p))-1):
        part = m_number[i:(lambda x: x if x < len(m_number) else len(m_number))(i+len(str(p))-1)]
        print((str(int(i / (len(str(p))-1)) + 1) + ' part: ').rjust(37), part, '\n')

        zeroes = ''
        for i in part:
            if i == '0':
                zeroes += '0'
            else:
                break
    
        A_k = mpz(randint(1, p-2))
        A_r = powmod(g, A_k, p)
        A_e = powmod(mul(mpz(part), powmod(B_public_key, A_k, p)), mpz(1), p)

        print('[Alice Encrypting]'.center(200))
        print()
        print('Randomly chosen k: '.rjust(37), A_k)
        print('r = g^k mod p = '.rjust(37), A_r)
        print('e = m*B[public key]^k mod p = '.rjust(37), A_e)
        print()
        print('[Sending Couple (r,e) to Bob]'.center(200))
        print()

        part_recieved = powmod(mul(A_e, powmod(A_r, sub(sub(p, 1), B_secret_key), p)), mpz(1), p)

        print('[Bob Decrypting]'.center(200))
        print()
        print('m = e * r^(p-1-B[private key]) mod p = '.rjust(37), part_recieved)
        print()

        msg += zeroes + str(part_recieved)

    print('[Ending of Sending Data]'.center(200))
    print()

    msg = num_to_ascii(msg)
    print('Message recieved: '.rjust(37), msg)


if __name__ == '__main__':
    main()
