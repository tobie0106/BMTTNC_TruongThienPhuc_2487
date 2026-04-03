from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
import socket
import threading

# ====== CONNECT SERVER ======
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

# ====== RSA KEY ======
client_key = RSA.generate(2048)

# nhận public key server
server_key = RSA.import_key(client_socket.recv(2048))

# gửi public key client
client_socket.send(client_key.publickey().export_key())

# nhận AES key (đã mã hóa)
encrypted_aes_key = client_socket.recv(2048)

# giải mã AES key
cipher_rsa = PKCS1_OAEP.new(client_key)
aes_key = cipher_rsa.decrypt(encrypted_aes_key)


# ====== AES FUNCTIONS ======
def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv + ciphertext


def decrypt_message(key, encrypted_message):
    iv = encrypted_message[:AES.block_size]
    ciphertext = encrypted_message[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted.decode()


# ====== RECEIVE THREAD ======
def receive_messages():
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            message = decrypt_message(aes_key, data)
            print("\nReceived:", message)
        except:
            break


threading.Thread(target=receive_messages, daemon=True).start()


# ====== SEND MESSAGE ======
while True:
    msg = input("Enter message (exit to quit): ")
    encrypted = encrypt_message(aes_key, msg)
    client_socket.send(encrypted)

    if msg == "exit":
        break

client_socket.close()
