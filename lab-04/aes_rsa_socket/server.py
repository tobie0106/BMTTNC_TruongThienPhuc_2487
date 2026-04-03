from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import socket
import threading

# ====== INIT SERVER ======
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)

print("Server is running...")

# ====== RSA KEY ======
server_key = RSA.generate(2048)

clients = []  # (socket, aes_key)

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


# ====== HANDLE CLIENT ======
def handle_client(client_socket, client_address):
    print(f"Connected: {client_address}")

    try:
        # gửi public key server
        client_socket.send(server_key.publickey().export_key())

        # nhận public key client
        client_key = RSA.import_key(client_socket.recv(2048))

        # tạo AES key
        aes_key = get_random_bytes(16)

        # mã hóa AES key bằng RSA client
        cipher_rsa = PKCS1_OAEP.new(client_key)
        encrypted_aes_key = cipher_rsa.encrypt(aes_key)
        client_socket.send(encrypted_aes_key)

        clients.append((client_socket, aes_key))

        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            message = decrypt_message(aes_key, data)
            print(f"{client_address}: {message}")

            # broadcast
            for c, key in clients:
                if c != client_socket:
                    try:
                        enc = encrypt_message(key, message)
                        c.send(enc)
                    except:
                        pass

            if message == "exit":
                break

    except Exception as e:
        print("Error:", e)

    finally:
        clients.remove((client_socket, aes_key))
        client_socket.close()
        print(f"Disconnected: {client_address}")


# ====== ACCEPT CLIENT ======
while True:
    client_socket, addr = server_socket.accept()
    thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    thread.start()