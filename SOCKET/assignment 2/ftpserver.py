import socket
import os
import threading
import time
import shutil
from datetime import datetime

# Server configuration
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
TCP_PORT = 8000     # Port for TCP connection
UDP_PORT = 8001     # Port for UDP connection
BUFFER_SIZE = 1024  # Buffer size for receiving data

def get_date():
    """Return current date in Unix format"""
    return datetime.now().strftime("%a %b %d %H:%M:%S %Y")

def list_directory():
    """List content of current directory"""
    try:
        return '\n'.join(os.listdir('.'))
    except Exception as e:
        return f"Error listing directory: {str(e)}"

def create_directory(client_pid):
    """Create directory using client's process ID"""
    dir_name = str(client_pid)
    try:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            return f"Directory '{dir_name}' created successfully"
        else:
            return f"Directory '{dir_name}' already exists"
    except Exception as e:
        return f"Error creating directory: {str(e)}"

def delete_file(filename):
    """Delete specified file"""
    try:
        if os.path.isfile(filename):
            os.remove(filename)
            return f"File '{filename}' deleted successfully"
        else:
            return f"File '{filename}' does not exist"
    except Exception as e:
        return f"Error deleting file: {str(e)}"

def delete_directory(client_pid):
    """Delete directory created for client"""
    dir_name = str(client_pid)
    try:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            return f"Directory '{dir_name}' deleted successfully"
        else:
            return f"Directory '{dir_name}' does not exist"
    except Exception as e:
        return f"Error deleting directory: {str(e)}"

def process_command(command_data):
    """Process client command and return response"""
    parts = command_data.strip().split(" ")
    command = parts[0]
    
    if command == "DATE":
        return get_date()
    elif command == "LIST":
        return list_directory()
    elif command == "CDIR":
        if len(parts) > 1:
            return create_directory(parts[1])
        else:
            return "Error: Client PID not provided for CDIR command"
    elif command == "DELFILE":
        if len(parts) > 1:
            return delete_file(parts[1])
        else:
            return "Error: Filename not provided for DELFILE command"
    elif command == "DELDIR":
        if len(parts) > 1:
            return delete_directory(parts[1])
        else:
            return "Error: Client PID not provided for DELDIR command"
    elif command == "QUIT":
        return "Thanks"
    else:
        return "Invalid command. Available commands: CDIR, DELFILE, DELDIR, DATE, LIST, QUIT"

def handle_tcp_client(client_socket, addr):
    """Handle TCP client connection"""
    print(f"TCP connection from {addr}")
    
    try:
        while True:
            # Receive data from client
            data = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            if not data:
                break
                
            print(f"Received from {addr}: {data}")
            
            # Process command
            response = process_command(data)
            
            # Send response back to client
            client_socket.sendall(response.encode('utf-8'))
            
            # If client wants to quit, break the loop
            if data.strip() == "QUIT":
                break
                
    except Exception as e:
        print(f"Error handling TCP client {addr}: {str(e)}")
    finally:
        # Close client connection
        client_socket.close()
        print(f"TCP connection from {addr} closed")

def start_tcp_server():
    """Start TCP server in a separate thread"""
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        tcp_server.bind((HOST, TCP_PORT))
        tcp_server.listen(5)
        print(f"TCP server listening on {HOST}:{TCP_PORT}")
        
        while True:
            client_socket, addr = tcp_server.accept()
            client_thread = threading.Thread(target=handle_tcp_client, args=(client_socket, addr))
            client_thread.daemon = True
            client_thread.start()
            
    except Exception as e:
        print(f"TCP server error: {str(e)}")
    finally:
        tcp_server.close()

def handle_udp_requests():
    """Handle UDP client requests"""
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        udp_socket.bind((HOST, UDP_PORT))
        print(f"UDP server listening on {HOST}:{UDP_PORT}")
        
        while True:
            # Receive data and client address
            data, client_addr = udp_socket.recvfrom(BUFFER_SIZE)
            data = data.decode('utf-8')
            print(f"UDP request from {client_addr}: {data}")
            
            # Process command
            response = process_command(data)
            
            # Send response back to client
            udp_socket.sendto(response.encode('utf-8'), client_addr)
            
    except Exception as e:
        print(f"UDP server error: {str(e)}")
    finally:
        udp_socket.close()

if __name__ == "__main__":
    print("Starting FTP server...")
    print("Available commands: CDIR, DELFILE, DELDIR, DATE, LIST, QUIT")
    
    # Start TCP server in a separate thread
    tcp_thread = threading.Thread(target=start_tcp_server)
    tcp_thread.daemon = True
    tcp_thread.start()
    
    # Start UDP server in the main thread
    handle_udp_requests()