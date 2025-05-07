import socket

def start_server():
    # Define server host and port
    host = '192.168.31.249'  # localhost
    port = 12345        # Port number

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the host and port
    server_socket.bind((host, port))

    # Start listening for incoming connections (max 1 client in queue)
    server_socket.listen(1)
    print(f"Server is listening on {host}:{port}...")
# -----------------------------------
    # Accept a connection from a client
    conn, addr = server_socket.accept()
    print(f"Connection established with {addr}")

    # Receive a message from the client
    message = conn.recv(1024).decode('utf-8')
    print(f"Received from client: {message}")

    # Close the connection
    conn.close()
    
# -----------------------------
    # # Accept a connection from a client
    # conn, addr = server_socket.accept()
    # print(f"Connection established with {addr}")

    # # Receive a message from the client
    # message = conn.recv(1024).decode('utf-8')
    # print(f"Received from client: {message}")

    # # Close the connection
    # conn.close()
# ----------------------------------------
    server_socket.close()
    # print("Server has shut down.")

if __name__ == "__main__":
    start_server()
