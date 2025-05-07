import socket
import os
import sys

# Buffer size for receiving data
BUFFER_SIZE = 1024

def print_menu():
    """Display menu options"""
    print("\nAvailable commands:")
    print("1. CDIR - Create directory on server using client's process ID")
    print("2. DELFILE <filename> - Delete a file from server")
    print("3. DELDIR - Delete the directory created for this client")
    print("4. DATE - Get current date")
    print("5. LIST - List content of server directory")
    print("6. QUIT - Exit the program")
    return input("\nEnter command: ").strip()

def get_client_pid():
    """Get client process ID"""
    return os.getpid()

def tcp_client(host, port):
    """TCP client implementation"""
    try:
        # Create TCP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port} via TCP")
        
        while True:
            cmd = print_menu()
            
            # Process command input
            if cmd.upper() == "CDIR":
                cmd = f"CDIR {get_client_pid()}"
            elif cmd.upper().startswith("DELFILE"):
                if len(cmd.split()) < 2:
                    print("Error: Please specify filename (DELFILE <filename>)")
                    continue
            elif cmd.upper() == "DELDIR":
                cmd = f"DELDIR {get_client_pid()}"
            elif cmd.upper() not in ["DATE", "LIST", "QUIT"]:
                print("Invalid command!")
                continue
            
            # Send command to server
            client_socket.sendall(cmd.encode('utf-8'))
            
            # Receive response
            response = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            print(f"\nServer response:\n{response}")
            
            # Exit if command was QUIT
            if cmd.upper() == "QUIT":
                break
                
        client_socket.close()
        
    except ConnectionRefusedError:
        print(f"Connection refused. Make sure the server is running at {host}:{port}")
    except Exception as e:
        print(f"Error: {str(e)}")

def udp_client(host, port):
    """UDP client implementation"""
    try:
        # Create UDP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(f"Using UDP to connect to server at {host}:{port}")
        
        while True:
            cmd = print_menu()
            
            # Process command input
            if cmd.upper() == "CDIR":
                cmd = f"CDIR {get_client_pid()}"
            elif cmd.upper().startswith("DELFILE"):
                if len(cmd.split()) < 2:
                    print("Error: Please specify filename (DELFILE <filename>)")
                    continue
            elif cmd.upper() == "DELDIR":
                cmd = f"DELDIR {get_client_pid()}"
            elif cmd.upper() not in ["DATE", "LIST", "QUIT"]:
                print("Invalid command!")
                continue
            
            # Send command to server
            client_socket.sendto(cmd.encode('utf-8'), (host, port))
            
            # Receive response - set timeout for receiving data
            client_socket.settimeout(5.0)
            try:
                response, _ = client_socket.recvfrom(BUFFER_SIZE)
                response = response.decode('utf-8')
                print(f"\nServer response:\n{response}")
            except socket.timeout:
                print("Request timed out. Make sure server is running.")
                break
            
            # Exit if command was QUIT
            if cmd.upper() == "QUIT":
                break
                
        client_socket.close()
        
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    # Check command line arguments
    if len(sys.argv) < 4:
        print("Usage: python ftpclient.py <host> <port> <protocol>")
        print("Protocol can be TCP or UDP")
        sys.exit(1)
    
    host = sys.argv[1]
    
    try:
        port = int(sys.argv[2])
    except ValueError:
        print("Port must be an integer")
        sys.exit(1)
        
    protocol = sys.argv[3].upper()
    
    if protocol == "TCP":
        tcp_client(host, port)
    elif protocol == "UDP":
        udp_client(host, port)
    else:
        print("Invalid protocol. Use TCP or UDP")
        sys.exit(1)

if __name__ == "__main__":
    main()