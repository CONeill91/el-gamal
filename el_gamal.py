import random

NUMBER_OF_ITERATIONS = 20
SIZE_OF_KEYS_IN_BITS = 20

def order(p, f, a):
    """
    Practical 1:
    order(p, f, a) will  return  the  order of a in  the  group Z∗p
    where: f is  a  list  of  the  prime  factors of p - 1
    Ensure  that  your  method  works  when f contains  duplicates. Consider where p = 17
    """
    t = p - 1
    for factor in f:
        t_tilda = t // factor
        a_raised = pow(a, t_tilda) % p
        if not a_raised == 1 % p:
            return t
        else:
            t = t_tilda


def findg(p, f):
    """
    Practical 2:
    find(p, f) will return a generator of Z*p where p is a prime and f is a list of the prime factors of p - 1
    """
    while True:
        candidate = random.randint(1, p - 1)
        if order(p, f, candidate) == p - 1:
            return candidate


def pair(d):
    """
    Practical 3:
    pair(d) will return (p, a) containing a safe prime p with d bits and a generator a for Z*p
    A safe prime is a prime q where 2q + 1 is also a prime
    """
    # Half the size of the prime being generated
    length = d // 2
    while True:
        q = gen_d_bit_prime(length)
        if fermat(q, NUMBER_OF_ITERATIONS):
            p = 2 * q + 1
            if fermat(p, NUMBER_OF_ITERATIONS):
                return p, findg(p, [2, q])


def log(p, a, x):
    """
    Practical 4:
    log(p, a, x) will return log a x in the cyclic group Z*p where p is a prime and a is a generator
    """


def egKey(s):
    """
    Practical 5:
    egKey(s) will return a tuple (p, a, x, y) where p is a safe prime, a is a generator, and x & y are the public
    and private components of the Elgamal Key
    """
    prime, generator = pair(s)
    x = random.randint(1, prime)
    y = pow(generator, x) % prime
    return prime, generator, x, y


def egEnc(p, a, y, m):
    """
    Practical 5:
    egEnc(p, a, y, m) will return the tuple (c1, c2)
    """
    k = random.randint(1, p - 1)
    c1 = pow(a, k) % p
    c2 = m * pow(y, k) % p
    return c1, c2



def egDec(p, x, c1, c2):
    """
    Practical 5:
    egDec(p, x, c1, c2) wil return the original message m
    """
    exponent = p - 1 - x
    return pow(c1, exponent) * c2 % p


def main():
    p, a, x, y = egKey(SIZE_OF_KEYS_IN_BITS)
    m = ""
    c1, c2 = egEnc(p, a, y, m)
    mDec = egDec(p, x, c1, c2)
    print(mDec)

##############################################################################################################
############################################## Helper Functions ##############################################
##############################################################################################################

def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n = n // i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


def fermat(x, t):
    if x == 2:
        return True
    if x % 2 == 0:
        return False
    for _ in range(t):
        try:
            candidate = random.randint(1, x - 1)
        except ValueError:
            continue
        if pow(candidate, x - 1) % x != 1:
            return False
    return True


def gen_d_bit_prime(d):
    while True:
        candidate = random.getrandbits(d)
        if fermat(candidate, NUMBER_OF_ITERATIONS):
            return candidate
