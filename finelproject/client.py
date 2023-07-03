import socket

host = '127.0.0.1'
port = 9000 

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

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
    message = input("\033[35mEnter a message: \033[0m")
    encrypted_message = encrypt(message, public_key)
    client_socket.send(str(encrypted_message).encode())

    if message == "bye":
        break

    response = client_socket.recv(1024).decode()
    decrypted_response = decrypt(eval(response), private_key)
    print("\033[31mReceived response from server:\033[0m", decrypted_response)

client_socket.close()
