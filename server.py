# Server programm
import socket
import sys

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
print("[+] Client connected %s, port %s" % (address[0],address[1]))

connected = 1
while(connected):
    client_msg = connection.recv(1024).decode()
    if client_msg != "END":
        print("[Client] > %s" % (client_msg))
        server_msg = input("[Server] > ")
        connection.sendall(server_msg.encode())
        if server_msg == 'END':
            connected = 0
    else:
        connected = 0
print("[-] Connection closed.")
connection.close()