import socket

# Define server address and port
server_address = ("127.0.0.1", 12345)

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(server_address)

print(f"UDP Server is listening on {server_address}")

while True:
    # Receive data from client
    data, client_address = server_socket.recvfrom(1024)
    
    if not data:
        break
    
    message = data.decode()
    print(f"Received from {client_address}: {message}")
    
    if message.lower() == "exit":
        print(f"Client {client_address} disconnected.")
        continue
    
    response = input("Reply to client: ")
    server_socket.sendto(response.encode(), client_address)
