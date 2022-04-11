import random
import time
import math

max = (1 << 1025) - 1

random.seed(time.time())

def pot(b :int, e :int, m :int) -> int:
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

def miller_rabin (n :int, k :int = 1) -> bool:
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


while True:
    a = random.randint(3, max)
    if miller_rabin(a, 1):
        print(a)
        break
    