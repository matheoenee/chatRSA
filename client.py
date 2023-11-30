# Client programm
import signal
import socket
import sys
import os
from rsa import *

host = '127.0.0.1' # accept all host
port_number = 8080

# socket waiting for connection
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

try:
    my_socket.connect((host, port_number))
except socket.error:
    print("ERROR : socket connection.")
    sys.exit()

# Connexion succeed
print(f"[+] Connection established with server {host} on port {port_number}.")

# RSA Handshake
print("\n[RSA] Starting RSA Handshake.")
print("[RSA] Generating client public and private key...")
# RSA Server data
n, d, e = RSA_key()
client_msg = str(n)
my_socket.sendall(client_msg.encode())
print("[RSA] Client public key sent.")
print("[RSA] Waiting for server public key...")
server_msg = my_socket.recv(1024).decode()
n_server= int(server_msg)
print(f"[RSA] Server public key is ({n_server}, 65537).")
print("[RSA] Handshake completed.\n")

pid = os.fork()

if pid == 0:
    # Child process (send messages)
    while(1):
        client_msg = input()
        # encode with RSA (server public key)
        my_socket.sendall(client_msg.encode())
        if client_msg == "\quit":
            os.kill(os.getppid(), signal.SIGTERM)
            break
else:
    # Parent process (receive messages)
    while(1):
        server_msg = my_socket.recv(1024).decode()
        # decode with RSA (server private key)
        if server_msg != "\quit":
            print("[Server] > %s" % (server_msg))
        else:
            os.kill(pid, signal.SIGTERM)
            break


print("\n[-] Connection closed.")
my_socket.close()
sys.exit()
