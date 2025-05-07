import socket

def start_client():
    # Define server host and port (same as server)
    # host = '192.168.31.87'  # localhost
    # host = '127.0.0.1'  # localhost
    # port = 12345        # Port number
    # -----------------------------
    #defaults
    hostname= socket.gethostname()
    host = socket.gethostbyname(hostname)
    port =12345

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((host, port))
    print(f"Connected to server at {host}:{port}")

    while True:
        # Send a message to the server
        message = input("You (client): ")
        client_socket.sendall(message.encode())
        if message.lower() == 'exit':
            print("Closing connection with server.")
            break

        # Receive response from the server
        response = client_socket.recv(1024).decode()
        print(f"Server: {response}")
        
        if(message.lower()=='exit'):
            client_socket.send("Adios Amigo!")
            client_socket.close()
            break

    # Close the connection
    client_socket.close()

if __name__ == "__main__":
    start_client()
