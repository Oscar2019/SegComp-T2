import random
import time
import math
import os
from util import extend_gcd, inver_mut_mod, pot

max = 1024

random.seed(time.time())


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
        a = int.from_bytes(os.urandom(max_num//8), "big")
        if miller_rabin(a, raoud_num):
            res = a
            break
    return res


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
        e = int.from_bytes(os.urandom(random.randint(16, 40)), "big")
        pode, d = inver_mut_mod(e, phi_n)
        if pode:
            break

    public_key = (e, n)
    private_key = (d, n)
    # print("len(n) = ", len(n))
    # print("public_key = ", public_key)
    # print("len(e) = ", len(e))
    # print("private_key = ", private_key)
    # print("len(d) = ", len(d))

    return (public_key, private_key, n)

def int_to_bytes_size(n):
    m = n
    res = 0
    while m != 0:
        res += 1
        m //= 256
    
    return res

def rsa_encript(msg, key):
    bytes_values_len = len(msg)
    num_msg = int.from_bytes(msg, "big")
    num_cript_msg = pot(num_msg, key[0], key[1])
    cript_msg = num_cript_msg.to_bytes(int_to_bytes_size(key[1]), "big")
    return cript_msg
    # return num_cript_msg
    
def rsa_decript(msg, key):
    num_msg = int.from_bytes(msg, "big")
    num_decript_msg = pot(num_msg, key[0], key[1])
    decript_msg = int.to_bytes(num_decript_msg, int_to_bytes_size(num_decript_msg), "big")

    return decript_msg

def main():
    # tam max da msg é 27
    key = rsa_key_generator()
    msg = b"0"*35
    print("msg = ", msg)
    msg = rsa_encript(msg, key[0])
    print("msg = ", msg)
    msg = rsa_decript(msg, key[1])
    print("msg = ", msg)

if __name__ == "__main__":
    main()

    
