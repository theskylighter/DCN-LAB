# Write an Echo_server using TCP to estimate the round trip time from client to the server. The
# server should be such that it can accept multiple connections at any given time , with
# multiplexed I/O operations

import socket
import time

HOST= "127.0.0.1"
PORT= 12345

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((HOST,PORT))
server.listen()

client_socket,client_addr =server.accept()
mesg="helllo client"
client_socket.sendall(mesg.encode("utf-8"))

received_mesg = client_socket.recv(1024)
print(f"message from {client_addr} : {received_mesg}")

client_socket.close()
server.close()
