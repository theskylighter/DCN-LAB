
# ------------------------------------
import socket

client = socket.socket()
client.connect(('localhost', 5000))

while True:
    msg = input("You: ")
    client.send(msg.encode())
    if msg.lower() == "exit":
        break
    print("Server:", client.recv(1024).decode())

client.close()
