import hashlib
import sys
import rsa
import aes
import base64


hash_object = hashlib.sha3_512()

def envia_msg(session_key, nonce, hash_key):
    global hash_object
    print("Digite o nome do arquivo da mensagem:")
    msg_file_name = input()
    msg = ""
    with open(f'{msg_file_name}.txt', 'r') as f:
        msg = "".join(f.readlines())

    msg_bytes = msg.encode()
    base64_bytes = base64.b64encode(msg_bytes)
    hash_object.update(msg_bytes)
    hash = hash_object.hexdigest().encode()

    base64_encrypted = aes.ctr_encrypt_decrypt(session_key, base64_bytes, nonce)
    with open('msg.bin', 'wb') as f:
        f.write(len(base64_encrypted).to_bytes(4, 'big'))
        f.write(base64_encrypted)

    hash_encrypted = rsa.rsa_encript(hash, hash_key)
    with open('hash.bin', 'wb') as f:
        f.write(len(hash_encrypted).to_bytes(4, 'big'))
        f.write(hash_encrypted)

    print("messagem recebida com sucesso!")

def recebe_msg(session_key, nonce, hash_key):

    global hash_object

    msg_bytes = b""
    base64_bytes = b""

    base64_encrypted = b""
    with open('msg.bin', 'rb') as f:
        base64_encrypted_len = int.from_bytes(f.read(4), 'big')
        base64_encrypted = f.read(base64_encrypted_len)

    base64_bytes = aes.ctr_encrypt_decrypt(session_key, base64_encrypted, nonce)
    msg_bytes = base64.b64decode(base64_bytes)
    hash_object.update(msg_bytes)
    hash = hash_object.hexdigest().encode()

    hash_encrypted = b""
    with open('hash.bin', 'rb') as f:
        hash_encrypted_len = int.from_bytes(f.read(4), 'big')
        hash_encrypted = f.read(hash_encrypted_len)
    hash2 = rsa.rsa_decript(hash_encrypted, hash_key)

    if hash == hash2:
        print("messagem recebida com sucesso!")
        print(msg_bytes.decode())
    else:
        print("messagem recebida com erro!")

        

def server(skey):
    public_key, private_key, n = rsa.rsa_key_generator()
    with open('public_key.txt', 'w') as f:
        f.write(str(public_key[0]))
        f.write("\n")
        f.write(str(public_key[1]))

    if skey:
        with open('private_key.txt', 'w') as f:
            f.write(str(private_key[0]))
            f.write("\n")
            f.write(str(private_key[1]))
    
    input("Aperte <ENTER> para receber a chave de sessão.")
    
    session_key_encripted = b""
    nonce_encripted = b""
    with open('session_key.bin', 'rb') as f:
        session_key_encripted_len = int.from_bytes(f.read(4), 'big')
        session_key_encripted = f.read(session_key_encripted_len)
        nonce_encripted_len = int.from_bytes(f.read(4), 'big')
        nonce_encripted = f.read(nonce_encripted_len)
    

    session_key = rsa.rsa_decript(session_key_encripted, private_key)
    nonce = rsa.rsa_decript(nonce_encripted, private_key)

    print("session_key = ", session_key)
    print("nonce = ", nonce)

    print("Chave de sessão recebida.")
    status = "-1"
    while status != "0":
        status = input("Digite 0 para sair, 1 para enviar uma mensagem, 2 para receber uma mensagem: ")
        if status == "1":
            envia_msg(session_key, nonce, private_key)
        elif status == "2":
            recebe_msg(session_key, nonce, private_key)

    

def client():
    public_key = (0, 0)
    nonce = 0
    with open('public_key.txt', 'r') as f:
        public_key = (int(f.readline().strip()), int(f.readline().strip()))
    
    input("Aperte <ENTER> para envivar a chave de sessão.")

    session_key = aes.aes_key_generator()
    nonce = aes.aes_key_generator()
    print("session_key = ", session_key)
    print("nonce = ", nonce)

    session_key_encripted = rsa.rsa_encript(session_key, public_key)
    nonce_encripted = rsa.rsa_encript(nonce, public_key)
    with open('session_key.bin', 'wb') as f:
        f.write(len(session_key_encripted).to_bytes(4, 'big'))
        f.write(session_key_encripted)
        f.write(len(nonce_encripted).to_bytes(4, 'big'))
        f.write(nonce_encripted)
    
    print("Chave de sessão enviada.")
    status = "-1"
    while status != "0":
        status = input("Digite 0 para sair, 1 para enviar uma mensagem, 2 para receber uma mensagem: ")
        if status == "1":
            envia_msg(session_key, nonce, public_key)
        elif status == "2":
            recebe_msg(session_key, nonce, public_key)






def main():
    tipo = 1
    skey = False
    for arg in sys.argv:
        if arg == "-1":
            tipo = 1
        elif arg == "-2":
            tipo = 2
        elif arg == "-s":
            skey = True
    
    if tipo == 1:
        server(skey)
    elif tipo == 2:
        client()

if __name__ == "__main__":
    main()