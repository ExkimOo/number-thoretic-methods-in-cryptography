from gmpy2 import mpz, mul, add

class Num_sqrt:
    def __init__(self, a=0, b=0, c=0, n=1):
        self.a = mpz(mpz(a) % n)
        self.b = mpz(mpz(b) % n)
        self.c = mpz(c)
        self.n = mpz(n)

    def get_conjugate(self):
        return Num_sqrt(self.a, -self.b, self.c, self.n)
    
    def __mul__(self, other):
        return Num_sqrt(add(mul(self.a, other.a), mul(mul(self.b, other.b), self.c)) % self.n, 
                        add(mul(self.a, other.b), mul(self.b, other.a)) % self.n,
                        self.c, self.n)

    def __div__(self, other):
        return Num_sqrt()

    def __repr__(self):
        return str(self.a) + ' + ' + str(self.b) + '√' + str(self.c)

    def get_first_component(self):
        return self.a

    def get_second_component(self):
        return self.b
