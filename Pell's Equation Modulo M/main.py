from gmpy2 import gcdext, mpz, powmod, add, sub, mul, div
from sympy import legendre_symbol, sieve
from tonelli_shanks import sqrt_mod
import pyecm

def get_solution(prime):
    if prime != 2 and prime != 3:
        for i in range(0, prime, 1):
                if legendre_symbol(34*i**2-1, prime) == 1:

                    x = sqrt_mod(34*i**2-1, prime)
                    y = i

                    # print(prime, i, 'Residue')
                    # print('x =', x, 'y =', y)
                    # print('x**2 % ', prime, ' =', x**2 % prime)
                    # print('-34*y**2 % ', prime, ' =', -34*y**2 % prime)
                    # print('34*y**2-1 % ', prime, ' =', (34*y**2-1) % prime)
                    # print()

                    return mpz(x), mpz(y)
    elif prime == 2:
        x = 1
        y = 0

        return mpz(x), mpz(y)
    else:
        return mpz(0), mpz(1)

def lift_solution(prime, x_initial, y_initial, power):
    if power == 1:
        return x_initial, y_initial
    else:
        if prime != 2 and prime != 3:
            a = mpz(34*y_initial**2-1)
            x = x_initial
            y = y_initial
            for i in range(1, power):
                _, y, _ = gcdext(2*x, prime**i)
                x = (x - (x**2 - a)*y) % prime**(i+1)
                
                
            if x == x_initial:
                x = -x_initial
                y = y_initial
                for i in range(1, power):
                    _, y, _ = gcdext(2*x, prime**i)
                    x = (x - (x**2 - a)*y) % prime**(i+1)
                
            return x, y_initial

        elif prime == 2:
            if power <= 5:
                return mpz(1), mpz(1)
            else:
                x = 1
                y = 1
                a = mpz(34*1**2-1)
                for i in range(6, power+1):
                    k = 0
                    if (int((x**2 - a) / 2**(i-1))) % 2 == 1:
                        k = 1
                    x = x + k*2**(i-2)

            return x, y

        elif prime == 3:
            remainders = []
            for i in range(3**power):
                if i**2 % 3**power not in remainders:
                    remainders.append(i**2 % 3**power)

            for i in range(3**power):
                if (34*i**2-1) % 3**power in remainders:
                    y = i
                    for x in range(3**power):
                        if x**2 % 3**power == (34*i**2-1) % 3**power:

                            return x, y

def main():
    # sieve.extend(50)
    # print(sieve._list)
    # solutions = []
    # for prime in sieve._list:
    #     solutions.append([prime, get_solution(prime)])
    # print(solutions)
    # for solution in solutions[2:]:
    #     print('Prime =', solution[0])
    #     print(lift_solution(solution[0], solution[1][0], solution[1][1], 15))
    
    # x, y = lift_solution(2, 1, 1, 10)
    # print(x, y)
    # print(x**2 % 2**10 == (34*y**2-1) % 2**6)

    number = 25
    for number in range(1000000000, 1000000100):
        factors_list = list(pyecm.factors(number, False, True, 1, 1))
        # print(factors_list)

        solutions = []
        count = 1
        if len(factors_list) == 1:
                x, y = get_solution(factors_list[0])
                x, y = lift_solution(factors_list[0], x, y, count)
                solutions.append([factors_list[0], count, x, y])
        else:
            for i in range(len(factors_list) - 1):

                    if factors_list[i] == factors_list[i+1]:
                        count += 1
                        if i != len(factors_list) - 2:
                            continue
                    else:
                        if i == len(factors_list) - 2:
                            x, y = get_solution(factors_list[i+1])
                            x, y = lift_solution(factors_list[i+1], x, y, 1)
                            solutions.append([factors_list[i+1], 1, x, y])
                    
                    x, y = get_solution(factors_list[i])
                    x, y = lift_solution(factors_list[i], x, y, count)
                    solutions.append([factors_list[i], count, x, y])
                    count = 1
            
        # print(solutions)

        x0, y0 = 0, 0
        for s in solutions:
            _, reverse, _ = gcdext(mpz(number/s[0]**s[1]), s[0]**s[1])
            x0 = add(x0, mul(mul(mpz(div(number, s[0]**s[1])), reverse), s[2])) #% number
            y0 = add(y0, mul(mul(mpz(div(number, s[0]**s[1])), reverse), s[3])) #% number
            # x0 = x0 + int(number/s[0]**s[1])*reverse*s[2]
            # y0 = y0 + int(number/s[0]**s[1])*reverse*s[3]

        x0 = x0 % number
        y0 = y0 % number
        # if x0**2 % number == (34*y0**2-1) % number:
        print('x^2 - 34y^2 = -1 mod', number, '  |  Answer:', ('x = ' + str(x0)).ljust(13), ('y = ' + str(y0)).ljust(11), powmod(x0, 2, number) == sub(mul(powmod(y0, 2, number), 34), 1) % number)
        print(' '*36, '  |  Answer:', ('x = ' + str(-x0 % number)).ljust(13), ('y = ' + str(y0)).ljust(11), powmod(-x0 % number, 2, number) == sub(mul(powmod(y0, 2, number), 34), 1) % number)
        if y0 != 0:
            print(' '*36, '  |  Answer:', ('x = ' + str(x0)).ljust(13), ('y = ' + str(-y0 % number)).ljust(11), powmod(x0, 2, number) == sub(mul(powmod(-y0 % number, 2, number), 34), 1) % number)
            print(' '*36, '  |  Answer:', ('x = ' + str(-x0 % number)).ljust(13), ('y = ' + str(-y0 % number)).ljust(11), powmod(-x0 % number, 2, number) == sub(mul(powmod(-y0 % number, 2, number), 34), 1) % number)

        # print(powmod(x0, 2, number), sub(mul(powmod(y0, 2, number), 34), 1) % number)

main()