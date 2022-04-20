import random
import time
import math

max = (1 << 1025) - 1

random.seed(time.time())

def inverModular(x, y):
    if math.gcd(x, y) != 1:
        return None
    u1, u2, u3 = 1, 0, x
    v1, v2, v3 = 0, 1, y

    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % y

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
    math
    d = inverModular(e, n)
    d = (phi_n * 2 + 1) // e
    d %= phi_n

    print("(e * d) % phi_n = ", (e * d) % phi_n)
    if (e * d) % phi_n == 1:
        print("foi")

    public_key = e
    private_key = d

    return (public_key, private_key, n)

print(rsa_key_generator())
    
