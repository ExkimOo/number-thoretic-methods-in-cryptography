from diemitko import generate_prime
from convert import ascii_to_num, num_to_ascii
from gmpy2 import mpz, mul, sub, gcd, gcdext, powmod


def generate_c_d(number, exclude=1):
    for c in range(3, number):
        if gcd(c, number) == 1:  
            _, d, _ = gcdext(c, number)
            while d < 0:
                d += number

            return c, d


def main():
    A_p = generate_prime(30, 11)
    A_q = generate_prime(30, 13)
    A_N = mul(A_p, A_q)
    A_φ = mul(sub(A_p, 1), sub(A_q, 1))
    A_c, A_d = generate_c_d(A_φ)

    B_p = generate_prime(30, 11)
    B_q = generate_prime(30, 13)
    B_N = mul(B_p, B_q)
    B_φ = mul(sub(B_p, 1), sub(B_q, 1))
    B_c, B_d = generate_c_d(B_φ)
    
    m = input('\n\n' + 'Enter your message: ')
    m_number = ascii_to_num(m)

    print()
    print('[Public Data]'.center(200))
    print()
    print('Alice d: ', A_d)
    print('Alice N: ', A_N)
    print('Bob d: ', B_d)
    print('Bob N: ', B_N)
    print('\nMessage in ASCII coding: ', m_number, '\n')

    print('[Sending of Data]'.center(200))
    print()
    msg = ''
    for i in range(0, len(m_number), len(str(B_N))-1):
        part = m_number[i:(lambda x: x if x < len(m_number) else len(m_number))(i+len(str(B_N))-1)]
        print((str(int(i / (len(str(B_N))-1)) + 1) + ' part: '), part, '\n')

        zeroes = ''
        for i in part:
            if i == '0':
                zeroes += '0'
            else:
                break
        
        print('[Alice Encrypting]'.center(200))
        print()
        e = powmod(mpz(part), B_d, B_N)
        print('e = m^Bob_d mod Bob_N =', e)
        print()

        print('[Bob Decrypting]'.center(200))
        print()
        part_recieved = powmod(e, B_c, B_N)
        print('m = e^Bob_c mod Bob_N =', part_recieved)
        print()
        
        msg += zeroes + str(part_recieved)
    
    print('[Ending of Sending Data]'.center(200))
    print()
    msg = num_to_ascii(str(msg))
    print('Message recieved: ', msg)


if __name__ == '__main__':
    main()