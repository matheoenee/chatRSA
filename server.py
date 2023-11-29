# Server programm
import socket
import sys
import os

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

pid = os.fork()

#connexion suceed
while 1:
    if pid == 0:
        client_msg = connection.recv(1024).decode()
        if client_msg != "END":
            print("[Client] > %s" % (client_msg))
            print(client_msg)
        else:
            #server_msg = "END" ça marche ?
            break # ça marche pas vraiment
    else:
        server_msg = input("[Server] > ")
        connection.sendall(server_msg.encode())
        if server_msg == "END":
            break #marche bien mais provoque un problème du côté client
print("[-] Connection closed.")
connection.close()
#sys.exit() #ne marche pas

"""
soucis actuels :
- mauvaie mise en page dès que 2 messages s'envoie à la suite
- probème de fermeture de serveur : Normal ?
"""