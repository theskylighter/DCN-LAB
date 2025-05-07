import socket

HOST = '192.168.x.x'  # Replace with the server's IP address
PORT = 12345
BUFFER_SIZE = 1024

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    client_socket.connect((HOST, PORT))
    print(f"Connected to server at {HOST}:{PORT}")

    while True:
        # Send a message to the server
        message = input("You (client): ")
        client_socket.sendall(message.encode())
        if message.lower() == 'exit':
            print("Closing connection with server.")
            break

        # Receive response from the server
        response = client_socket.recv(BUFFER_SIZE).decode()
        print(f"Server: {response}")

except Exception as e:
    print(f"Error: {e}")

finally:
    client_socket.close()
    print("Client shutdown.")
