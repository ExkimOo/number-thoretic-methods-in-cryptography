from diemitko import generate_prime
from gmpy2 import mpz, add, sub, mul, div, powmod, gcdext
from convert import ascii_to_num, num_to_ascii


def main():
    while True:
        p = generate_prime(17, 5)
        if p % 4 == 3:
            break
    while True:
        q = generate_prime(17, 7)
        if q % 4 == 3:
            break
    N = mul(p, q)

    print('p:'.rjust(37), p)
    print('q:'.rjust(37), q)
    
    m = input('Enter a Message:'.rjust(37) + ' ')
    m_number = ascii_to_num(m)

    print()
    print('[Public Data]'.center(200) + '\n')
    print('N: '.rjust(37), N)
    print('Message in ASCII coding: '.rjust(37), m_number, '\n')

    print('[Sending of Data]'.center(200))
    msg = ''
    for i in range(0, len(m_number), len(str(p))-1):
        part = m_number[i:(lambda x: x if x < len(m_number) else len(m_number))(i+len(str(p))-1)]
        print()
        print((str(int(i / (len(str(p))-1)) + 1) + ' part: ').rjust(37), part, '\n')

        zeroes = ''
        for i in part:
            if i == '0':
                zeroes += '0'
            else:
                break
        
        part_length = len(part)
        c = powmod(mpz(part), mpz(2), N)
        m_p = powmod(c, mpz(div(add(p, mpz(1)), mpz(4))), p)
        m_q = powmod(c, mpz(div(add(q, mpz(1)), mpz(4))), q)
        _, y_p, y_q = gcdext(p, q)

        r_1 = add(mul(mul(y_p, p) % N, m_q) % N, mul(mul(y_q, q) % N, m_p) % N) % N
        r_2 = sub(N, r_1)
        r_3 = sub(mul(mul(y_p, p) % N, m_q) % N, mul(mul(y_q, q) % N, m_p) % N) % N
        r_4 = sub(N, r_3)

        print('r1 ='.rjust(37), r_1)
        print('r2 ='.rjust(37), r_2)
        print('r3 ='.rjust(37), r_3)
        print('r4 ='.rjust(37), r_4)

        if len(str(r_1)) <= part_length:
            msg += zeroes + str(r_1)
        elif len(str(r_2)) <= part_length:
            msg += zeroes + str(r_2)
        elif len(str(r_3)) <= part_length:
            msg += zeroes + str(r_3)
        elif len(str(r_4)) <= part_length:
            msg += zeroes + str(r_4)

    msg = num_to_ascii(msg)
    print('[Ending of Sending Data]'.center(200) + '\n')
    print('Message:'.rjust(37), msg)


if __name__ == '__main__':
    main()