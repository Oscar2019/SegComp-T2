
from constant import sbox

def sub_bytes(matriz):
    for i in range(4):
        for j in range(4):
            matriz[i][j] = sbox[matriz[i][j]]
    return matriz
    
def shift_rows(matriz):
    for i in range(4):
        vet_aux = [0 for _ in range(4)]
        for j in range(4):
            vet_aux[j] = matriz[i][(j+i)%4]
        matriz[i] = vet_aux
    return matriz

def mix_columns(matriz):
    mat_aux = [
        [2, 3, 1, 1],
        [1, 2, 3, 1],
        [1, 1, 2, 3],
        [3, 1, 1, 2]
    ]
    res = [[ 0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            for k in range(4):
                # a = mat_aux[i][k]
                # b = matriz[k][j]
                # c = res[i][j] + a * b
                # res[i][j] = c
                res[i][j] += mat_aux[i][k] * matriz[k][j]
    matriz = res
    return res 

def main():
    mat = [[0,1,2,3],[0,1,2,3],[0,1,2,3],[0,1,2,3]]
    print(mat)
    mat = sub_bytes(mat)
    print(mat)
    mat = shift_rows(mat)
    print(mat)
    mat = mix_columns(mat)
    print(mat)

if __name__ == "__main__":
    main()