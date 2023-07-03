import socket

host = '127.0.0.1'
port = 9000 

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)

print("Waiting for a client connection...")

client_socket, client_address = server_socket.accept()
print("--------------- Client connected ---------------")

def encrypt(message, public_key):
    e, n = public_key
    encrypted_message = []
    for char in message:
        encrypted_char = pow(ord(char), e, n)
        encrypted_message.append(encrypted_char)
    return encrypted_message

def decrypt(encrypted_message, private_key):
    d, n = private_key
    decrypted_message = ""
    for char in encrypted_message:
        decrypted_char = chr(pow(char, d, n))
        decrypted_message += decrypted_char
    return decrypted_message


def generate_keys():
    p = 17
    q = 19

    n = p * q

    phi = (p - 1) * (q - 1)

    e = 7

    d = mod_inverse(e, phi)

    return ((e, n), (d, n))

def mod_inverse(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError("No modular inverse exists")
    return x % m

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

public_key, private_key = generate_keys()



while True:
    encrypted_message = client_socket.recv(1024).decode()
    decrypted_message = decrypt(eval(encrypted_message), private_key)
    print("\033[34mReceived message from client: \033[0m", decrypted_message)

    if decrypted_message == "bye":
        break

    response = input("\033[32mEnter your response: \033[0m")
    encrypted_response = encrypt(response, public_key)
    client_socket.send(str(encrypted_response).encode())

client_socket.close()
server_socket.close()
