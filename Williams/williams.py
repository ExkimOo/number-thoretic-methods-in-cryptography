from sympy.ntheory import legendre_symbol, jacobi_symbol
from gmpy2 import mpz, gcd, gcdext, powmod, sub, add, mul, is_prime
from diemitko import generate_prime
from num_sqrt import Num_sqrt
from convert import ascii_to_num, num_to_ascii


def calculate_indexes(number):
    indexes = {int(number): -1}

    while number != 1:
        if number % 2 == 0:
            indexes[int(number/2)] = -1

            number = int(number/2)

        else:
            indexes[int((number - 1)/2)] = -1
            indexes[int((number - 1)/2+1)] = -1
            
            if int((number-1)/2 + 1) % 2 == 1:
                number = int((number-1)/2 + 1)
            else:
                number = int((number-1)/2)
    
    return indexes


def X(i, X1, value_1, value_2, mod):
    if i % 2 == 0:
        return mpz(sub(mul(mpz(2), mpz(pow(value_1, 2))), mpz(1)) % mod)
    else:
        return mpz(sub(mul(mul(mpz(2), mpz(value_1)), value_2), mpz(X1)) % mod)

def Y(i, Y1, value_1, value_2, mod):
    if i % 2 == 0:
        return mpz(mul(mul(mpz(2), mpz(value_1)), value_2) % mod)
    else:
        return mpz(sub(mul(mul(mpz(2), mpz(value_1)), value_2), mpz(Y1)) % mod)


def main():
    p = -1
    q = -1
    n = -1

    δ_p = 0
    δ_q = 0
    c = 2
    s = 2
    e, d = 2, 2

    while True:
        p = generate_prime(9, 5)
        while is_prime(p) == False:
            p = generate_prime(9, 5)

        q = generate_prime(9, 5)
        while is_prime(q) == False:
            q = generate_prime(9, 5)

        δ_p = legendre_symbol(c, p)
        δ_q = legendre_symbol(c, q)

        if δ_p % 4 == -p % 4 and δ_q % 4 == -q % 4:
            break

        c += 1

    n = p*q
    print('p = ' + str(p) + ', q = ' + str(q))
    print('n = p*q = ' + str(n))
    
    
    while True:
        if jacobi_symbol(s**2-c, n) == -1 and gcd(s, n) == 1:
            break
        else:
            s += 1

    print('c = ' + str(c) + ', s = ' + str(s))
    
    m = int((p - δ_p)*(q - δ_q) / 4)

    while True:
        d += 1
        if gcd(d, m) == 1:
            _, e, _ = gcdext(mpz(d), mpz(m))
            e = mpz(mul(e, mpz((m+1)/2)) % m)
            break

    print('d = ' + str(d) + ', e = ' + str(e))
    print()
    print('(n, e, c, s) is public')
    print()
    
    msg = input('Message = ')
    m_number = ascii_to_num(msg)
    print('Message in ASCII coding:', m_number)
    print('[Encrypting]')
    print()
    
    msg = ''
    for i in range(0, len(m_number), len(str(n))-1):
        part = m_number[i:(lambda x: x if x < len(m_number) else len(m_number))(i+len(str(n))-1)]
        print()
        print((str(int(i / (len(str(n))-1)) + 1) + ' part: ').rjust(37), part, '\n')

        zeroes = ''
        for i in part:
            if i == '0':
                zeroes += '0'
            else:
                break

        part = int(part)

        _, inversed, _ = gcdext(part**2-c % n, n)
        if jacobi_symbol(part**2-c, n) == 1:
            b1 = 0
            alpha = Num_sqrt(mul(add(mpz(pow(part, 2, n)), c), inversed), mul(mpz(2), mul(mpz(part), mpz(inversed % n))), c, n)
        elif jacobi_symbol(part**2-c, n) == -1:
            b1 = 1
            _, inversed_1, _ = gcdext(mpz(s**2-c), n)
            a = mul(mul(add(mul(add(mpz(pow(part, 2, n)), c), add(mpz(pow(s, 2, n)), c)), mul(mpz(4*s*c), part)), mpz(inversed % n)), mpz(inversed_1 % n))
            b = mpz((2*s*(part**2+c)+2*part*(s**2+c))*inversed*inversed_1)
            alpha = Num_sqrt(a, b, c, n)  

        print('Alpha =', alpha)

        b2 = alpha.get_first_component() % 2
        print('b1 = ' + str(b1) + ', b2 = ' + str(b2))

        dicX = calculate_indexes(e)
        dicY = calculate_indexes(e)
        dicX[1] = alpha.get_first_component()
        dicY[1] = alpha.get_second_component()

        for i in sorted(dicX.keys()):
            if i != 1:
                if i % 2 == 0:
                    dicX[i] = X(i, dicX[1], dicX[int(i/2)], 0, n)
                    dicY[i] = Y(i, dicY[1], dicX[int(i/2)], dicY[int(i/2)], n)
                else:
                    dicX[i] = X(i, dicX[1], dicX[int((i-1)/2)], dicX[int((i-1)/2)+1], n)
                    dicY[i] = Y(i, dicY[1], dicX[int((i-1)/2)], dicY[int((i-1)/2)+1], n)

        _, inversed_Y, _ = gcdext(dicY[e], n)
        E = dicX[e]*inversed_Y % n
        print('E = ' + str(E))
        print()
        print('(' + str(E) + ', ' + str(b1) + ', ' + str(b2) + ') is the cryptotext')
        print()

        print('[Decrypting]')
        print()

        _, inversed, _ = gcdext(E**2-c, n)
        alpha_2e = Num_sqrt(mpz((E**2+c)*inversed), 2*E*inversed, c, n)
        
        dicX_decrypting = calculate_indexes(d)
        dicY_decrypting = calculate_indexes(d)
        dicX_decrypting[1] = alpha_2e.get_first_component()
        dicY_decrypting[1] = alpha_2e.get_second_component()

        for i in sorted(dicX_decrypting.keys()):
            if i != 1:
                if i % 2 == 0:
                    dicX_decrypting[i] = X(i, dicX_decrypting[1], dicX_decrypting[int(i/2)], 0, n)
                    dicY_decrypting[i] = Y(i, dicY_decrypting[1], dicX_decrypting[int(i/2)], dicY_decrypting[int(i/2)], n)
                else:
                    dicX_decrypting[i] = X(i, dicX_decrypting[1], dicX_decrypting[int((i-1)/2)], dicX_decrypting[int((i-1)/2)+1], n)
                    dicY_decrypting[i] = Y(i, dicY_decrypting[1], dicX_decrypting[int((i-1)/2)], dicY_decrypting[int((i-1)/2)+1], n)
        
        if dicX_decrypting[d] % 2 == b2:
            alpha_decrypting = Num_sqrt(dicX_decrypting[d], dicY_decrypting[d], c, n)
        else:
            alpha_decrypting = Num_sqrt(-dicX_decrypting[d], -dicY_decrypting[d], c, n)

        print('Alpha_2ed =', alpha_decrypting)

        if b1 == 0:
            alpha_stroke = alpha_decrypting
        else:
            _, inversed, _ = gcdext(mpz((s**2-c) % n), n)
            alpha_stroke = alpha_decrypting*Num_sqrt(s, -1, c, n)*Num_sqrt(s, -1, c, n)*Num_sqrt(inversed, 0, c, n)

        print('Alpha_stroke =', alpha_stroke)

        _, inversed, _ = gcdext(mpz(((alpha_stroke.get_first_component()-1)**2-alpha_stroke.get_second_component()**2*c) % n), n)
        part = -2*alpha_stroke.get_second_component()*c*inversed % n

        msg += zeroes + str(int(part))
        print('Part recieved: ' + str(part))
    
    msg = num_to_ascii(msg)
    print('Message recieved: ' + msg)


if __name__ == '__main__':
    main()