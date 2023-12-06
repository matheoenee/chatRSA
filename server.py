# Server programm
import signal
import socket
import sys
import os
from rsa import *

address = "172.20.10.13"
#address = "127.0.0.1" #use for local connection
port_number = 8080

# socket waiting for connection
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

try:
    my_socket.bind((address, port_number))
except socket.error:
    print("ERROR : socket binding.")
    sys.exit()

print("[+] Server ready for connection...")

my_socket.listen(socket.SOMAXCONN)
connection, address = my_socket.accept()
# Connexion succeed
print(f"[+] Client connected {address[0]}, port {address[1]}")

# RSA Handshake
print("\n[RSA] Starting RSA Handshake.")
print("[RSA] Generating server public and private key...")
n, d, e = RSA_key() # generating keys here to save time
print("[RSA] Waiting for client public key...")
client_msg = connection.recv(4096).decode()
n_client = int(client_msg)
print(f"[RSA] Client public key is ({n_client}, 65537).")
# RSA Server data
server_msg = str(n)
connection.sendall(server_msg.encode())
print("[RSA] Server public key sent.")
print("[RSA] Handshake completed.\n")

pid = os.fork()

if pid == 0:
    # Child process (send messages)
    # Add RSA
    while(1):
        server_msg = input()
        encrypted_server_msg = str(encrypt(server_msg, n_client))
        connection.sendall(encrypted_server_msg.encode())
        if server_msg == "\quit":
            os.kill(os.getppid(), signal.SIGTERM)
            break
else:
    # Parent process (receive messages)
    while(1):
        encrypted_data = int(connection.recv(4096).decode())
        client_msg = decrypt(encrypted_data, n, d)
        if client_msg != "\quit":
            print(f"[Client] > {client_msg}")
        else:
            os.kill(pid, signal.SIGTERM)
            break

print("\n[-] Connection closed.")   
connection.close()
sys.exit()
