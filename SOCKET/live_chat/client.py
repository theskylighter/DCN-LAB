import socket

def start_client():
    # Define server host and port (same as server)
    # host = '192.168.31.87'  # localhost
    host = '127.0.0.1'  # localhost
    port = 12345        # Port number

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((host, port))
    print(f"Connected to server at {host}:{port}")

    # Send a message to the server
    message = "Hello, Pratham Shivam this side \t Shalvin Bharosewala on the other side!"
    client_socket.send(message.encode('utf-8'))
    print("Message sent to the server.")

    # Close the connection
    client_socket.close()

if __name__ == "__main__":
    start_client()
