from pkgutil import extend_path
import random
import time
import math

max = (1 << 1025) - 1

random.seed(time.time())

def extend_gcd(n, m):
    if(m == 0):
        # (gcd, x0, y0)
        return (n, 1, 0)
    value_gcd, y0, x0 = extend_gcd(m, n%m)
    y1 = x0
    x1 = y0 + n // m * x0
    return (value_gcd, y1, x1)

"""
e * d mod phi_n = 1
e * d - 1 mod phi_n = 0
e * d - 1 = phi_n * x


gcd(e, phi_n) = 1
e * y + phi_n * w = 1 
"""
def inver_mut_mod(n, mod):
    value_gcd, y0, x0 = extend_gcd(n, mod)
    # print("value_gcd = ", value_gcd)
    # print("y0 = ", y0)
    # print("x0 = ", x0)
    if value_gcd != 1:
        return (False, None)
    return y0 % mod
    
def pot(b, e, m):
    res = 1
    b %= m
    while e != 0:
        if e % 2 != 0:
            res *= b
            res %= m
        b *= b
        b %= m
        e //= 2
    return res

def miller_rabin (n, k = 1):
    if n % 2 == 0:
        return False
    
    d = n - 1
    r = 0
    r2 = 1
    while d % 2 == 0:
        d //= 2
        r += 1
        r2 <<= 1

    for _ in range(k):
        a = random.randint(2, n-2)
        x = pot(a, d, n)
        erro = True
        if x == 1 or x == n-1:
            erro = False
        else:
            m = 0
            while m < r-1:
                x = (x * x) % n
                if x == n - 1:
                    erro = False
                m += 1
        if erro == True:
            return False
    return True

def prime_generator(n, m = 15):
    res = 0
    while True:
        a = random.randint(3, n)
        if miller_rabin(a, m):
            res = a
            break
    return res

def rsa_key_generator():
    p = prime_generator(max)
    q = prime_generator(max)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = 3
    while math.gcd(e, phi_n) != 1:
        e += 2
        e %= phi_n
    """
    e * d = phi_n x + 1
    d = (phi_n x + 1) / e 
    inverse of e

    """
    d = inver_mut_mod(e, phi_n)
    # print("inver_mut_mod(e, phi_n) = ", inver_mut_mod(e, phi_n))
    d = inverModular(e, phi_n)
    # print("inverModular(e, phi_n) = ", inverModular(e, phi_n))
    # d = (phi_n * 2 + 1) // e
    # d %= phi_n

    # print("(e * d) % phi_n = ", (e * d) % phi_n)
    if (e * d) % phi_n == 1:
        print("foi")

    public_key = e
    private_key = d

    return (public_key, private_key, n)

rsa_key_generator()
# print(rsa_key_generator())
    
