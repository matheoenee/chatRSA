# Client programm
import socket
import sys

host = '127.0.0.1' # accept all host
port_number = 8080

# socket waiting for connection
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

try:
    my_socket.connect((host, port_number))
except socket.error:
    print("ERROR : socket connection.")
    sys.exit()
print(f"[+] Connection established wither server {host} on port {port_number}.")

connected = 1
while(connected):
    client_msg = input("[Client] > ")
    my_socket.sendall(client_msg.encode())
    if client_msg != "END":
        server_msg = my_socket.recv(1024).decode()
        if server_msg != "END":
            print("[Server] > %s" % (server_msg))
        else:
            connected = 0
    else:
        connected = 0

print("[-] Connection closed.")
my_socket.close()