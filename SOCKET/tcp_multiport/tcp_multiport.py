import socket
import threading

# Chat Handler on Port 5000
def handle_chat(conn):
    while True:
        msg = conn.recv(1024).decode()
        if not msg or msg.lower() == "exit":
            break
        print("[Chat]", msg)
        conn.send(f"Echo: {msg}".encode())
    conn.close()

# File Service Handler on Port 6000
def handle_file(conn):
    print("Sending dummy file name...")
    conn.send(b"sample_file.txt")
    conn.close()

# Main server setup
def start_server(port, handler):
    server = socket.socket()
    server.bind(('localhost', port))
    server.listen(5)
    print(f"[+] Server listening on port {port}")
    while True:
        conn, addr = server.accept()
        print(f"[!] Connection from {addr} on port {port}")
        threading.Thread(target=handler, args=(conn,)).start()
        server.close

# Start both services
threading.Thread(target=start_server, args=(5000, handle_chat)).start()
threading.Thread(target=start_server, args=(6000, handle_chat)).start()
threading.Thread(target=start_server, args=(7000, handle_file)).start()
