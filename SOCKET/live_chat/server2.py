import socket

HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 12345
BUFFER_SIZE = 1024

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_socket.bind((HOST, PORT))
server_socket.listen(5)  # Allow up to 5 pending connections
print(f"Server listening on {HOST}:{PORT}...")

try:
    # Accept incoming connection
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")

    while True:
        # Receive message from client
        message = client_socket.recv(BUFFER_SIZE).decode()
        if not message:
            print("Client disconnected.")
            break
        print(f"Client: {message}")

        # Send response back to client
        response = input("You (server): ")
        client_socket.sendall(response.encode())
        if response.lower() == 'exit':
            print("Closing connection with client.")
            break

except Exception as e:
    print(f"Error: {e}")

finally:
    client_socket.close()
    server_socket.close()
    print("Server shutdown.")
