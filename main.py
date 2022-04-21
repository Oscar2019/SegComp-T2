import random
import time
import math
import os 

max = (1 << 1025) - 1

random.seed(time.time())

def extend_gcd(n, m):
    """
    https://www.youtube.com/watch?v=0oP6XLTI2tY
    https://pt.wikipedia.org/wiki/Algoritmo_de_Euclides_estendido
    https://www.geeksforgeeks.org/euclidean-algorithms-basic-and-extended/
    """
    if(m == 0):
        return n, 1, 0
    value_gcd, y0, x0 = extend_gcd(m, n%m)
    y1 = x0
    x1 = y0 - n // m * x0
    return value_gcd, y1, x1

def inver_mut_mod(n, mod):
    value_gcd, y0, x0 = extend_gcd(n, mod)
    if value_gcd != 1:
        return (False, None)
    return (True, y0 % mod)
    
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

"""
n é o número que será testado 
k é o número de rodadas
"""
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
        a = int.from_bytes(os.urandom(18), "big")
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

def prime_generator(max_num, raoud_num = 15):
    res = 0
    while True:
        a = int.from_bytes(os.urandom(18), "big")
        if miller_rabin(a, raoud_num):
            res = a
            break
    return res

foi = 0

def rsa_key_generator():
    p = prime_generator(max)
    q = prime_generator(max)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = 0
    d = 0
    while True:
        """
        e * d = phi_n x + 1
        d = (phi_n x + 1) / e 
        inverse of e
        """
        e = int.from_bytes(os.urandom(18), "big")
        pode, d = inver_mut_mod(e, phi_n)
        if pode:
            break

    public_key = e
    private_key = d

    return (public_key, private_key, n)


    
