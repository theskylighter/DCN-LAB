import socket

# Define server address and port
# server_address = ("127.0.0.1", 12345)
# server_address = ("192.168.31.87", 12345)
server_address = ("192.168.31.131", 12345)

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(30)

while True:
    message = input("Send to server: ")
    
    client_socket.sendto(message.encode(), server_address)
    
    if message.lower() == "exit":
        print("Disconnected from server.")
        break
    
    # Receive response from server
    data, _ = client_socket.recvfrom(1024)
    print(f"Server: {data.decode()}")
    
client_socket.close()
