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