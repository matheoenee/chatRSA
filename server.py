# Server programm
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
    my_socket.bind((host, port_number))
except socket.error:
    print("ERROR : socket binding.")
    sys.exit()

print("[+] Server ready for connection...")

my_socket.listen(socket.SOMAXCONN)
connection, address = my_socket.accept()
# Connexion succeed
print("[+] Client connected %s, port %s" % (address[0],address[1]))

# RSA Handshake
print("\n[RSA] Starting RSA Handshake.")
print("[RSA] Waiting for client public key...")
client_msg = connection.recv(1024).decode()
n_client = int(client_msg)
print(f"[RSA] Client public key is ({n_client}, 65537).")
print("[RSA] Generating server public and private key...")
# RSA Server data
n, d, e = RSA_key()
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
        connection.sendall(server_msg.encode())
        if server_msg == "\quit":
            os.kill(os.getppid(), signal.SIGTERM)
            break  # marche bien mais provoque un problème du côté client
else:
    # Parent process (receive messages)
    while(1):
        client_msg = connection.recv(1024).decode()
        if client_msg != "\quit":
            print("[Client] > %s" % (client_msg))
        else:
            os.kill(pid, signal.SIGTERM)
            # server_msg = "END" ça marche ?
            break  # ça marche pas vraiment

print("\n[-] Connection closed.")
connection.close()
sys.exit()
