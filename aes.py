from constant import sbox
from rijndael_finite_number import RijndaelFiniteNumber

def sub_bytes(matriz):
    res = [[ 0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            res[i][j] = RijndaelFiniteNumber(sbox[matriz[i][j]])
    return res
    
def shift_rows(matriz):
    res = [[ 0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            res[i][j] = matriz[i][(j+i)%4]
    return res

def mix_columns(matriz):
    mat_aux = [
        [2, 3, 1, 1],
        [1, 2, 3, 1],
        [1, 1, 2, 3],
        [3, 1, 1, 2]
    ]
    mat_aux = [list(map(RijndaelFiniteNumber, mat_aux[i])) for i in range(4)]
    res = [[ 0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            for k in range(4):
                res[i][j] += mat_aux[i][k] * matriz[k][j]
    # matriz = res
    return res 

def round_key(matriz, key):
    res = [[matriz[i][j] ^ key[i][j] for j in range(4)] for i in range(4)]
    return res

def extend_key(key):
    res = []
    res.append(key)
    x = RijndaelFiniteNumber(1)
    x_1 = RijndaelFiniteNumber(2)
    for i in range(1, 11):
        res.append([[ RijndaelFiniteNumber(0) for _ in range(4)] for _ in range(4)])
        for j in range(4):
            res[i][j][0] = RijndaelFiniteNumber(sbox[res[i-1][(j + 1)%4][3]])
        for j in range(4):
            res[i][j][0] = res[i-1][j][0] ^ res[i-1][j][3]
        res[i][0][0] ^= x
        x *= x_1
        for k in range(1, 4):
            for j in range(4):
                res[i][j][k] = res[i-1][j][k] ^ res[i][j][k-1]

    return res

def encrypt_block(key, msg):
    # print('msg = ', msg)
    key = [[ RijndaelFiniteNumber(key[i*4+j]) for j in range(4)] for i in range(4)]
    extended_key = extend_key(key)
    
    msg = [[ RijndaelFiniteNumber(msg[i*4+j] if i*4+j < len(msg) else 0) for j in range(4)] for i in range(4)]

    msg = round_key(msg, extended_key[0])
    for i in range(1, 10):
        msg = sub_bytes(msg)
        msg = shift_rows(msg)
        msg = mix_columns(msg)
        msg = round_key(msg, extended_key[i])

    msg = sub_bytes(msg)
    msg = shift_rows(msg)
    msg = round_key(msg, extended_key[10])
    
    res = b"".join([b"".join(map(lambda x: x.to_bytes(1, 'big'), line)) for line in msg])
    # print('res = ', res)
    return res
    

def add_nonce(nonce, value, size = 128):
    return (int.from_bytes(nonce, 'big') + value).to_bytes(16, 'big')

def xor_bytes(val_1, val_2):
    size = min(len(val_1), len(val_2))
    return b"".join([(val_1[i] ^ val_2[i]).to_bytes(1, 'big') for i in range(size)])

def ctr_encrypt_decrypt(key, msg, nonce):
    BLOCK_SIZE = 16
    BLOCK_NUM = (len(msg) + BLOCK_SIZE - 1) // BLOCK_SIZE
    vet = []
    for i in range(BLOCK_NUM):
        block = encrypt_block(key, add_nonce(nonce, i))
        # print("block = ", block)
        vet.append(xor_bytes(block, msg[i*BLOCK_SIZE: (i+1)*BLOCK_SIZE]))
    res = b"".join(vet)
    # print("res = ", res)
    return res
    

def main():
    key = 'abcdefghijklmnop'
    key = key.encode()
    mat = 'oscar_etcheaverry_barbosa_madureira_da_silva'
    mat = mat.encode()
    ctr_encrypt_decrypt(key, ctr_encrypt_decrypt(key, mat, b"abcdefghijklmnop"), b"abcdefghijklmnop")
    # print(encrypt_block(key, mat))
    

if __name__ == "__main__":
    main()

"""

[1, 2, 3, 4]
[2, 3, 4, 1]
[3, 4, 1, 2]
[4, 2, 3, 1]



[1, 2, 3, 4, 5]
[2, 3, 4, 5, 1]
[3, 4, 5, 1, 2]
[1, 2, 3, 4, 5]
[1, 2, 3, 4, 5]
"""