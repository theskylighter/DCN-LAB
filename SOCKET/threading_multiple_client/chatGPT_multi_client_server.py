import threading
import socket



def handle_client(clientObj, addr):
    print(f"Connection established with {addr} on Thread: {threading.current_thread().name}")

    
    while True:
        try:
            # Receive message from client
            message = clientObj.recv(1024).decode('utf-8')
            if not message:
                break  # If message is empty, client has disconnected
            
            print(f"{threading.current_thread().name} Received from client: {message}")
            
            if message.lower() == 'exit':
                clientObj.sendall("Adios Amigo!".encode("utf-8"))
                break
            
            # Send response to client
            response = input(f"{threading.current_thread().name} Send to client: ")
            clientObj.sendall(response.encode("utf-8"))

        except Exception as e:
            print(f"Error: {e}")
            break

    clientObj.close()
    print(f"Connection closed with {addr}")
    return

def start_server():
    # Defaults
    hostname = socket.gethostname()
    ipAddr = socket.gethostbyname(hostname)
    port = 12345

    # Create socket
    sockObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockObj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow reuse of address
    print("Creating socket obj")

    # Bind socket
    sockObj.bind((ipAddr, port))
    print("Binding socket obj to ", ipAddr, " ", port)

    # Listen for connections
    sockObj.listen(5)
    print("Listening for incoming connections...")

    while True:
        clientObj, addr = sockObj.accept()
        print(f"New connection from {addr}")
        # Start a new thread for the client
        client_thread = threading.Thread(target=handle_client, args=(clientObj, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server()
