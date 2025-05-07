import socket
import sys
import threading

if len(sys.argv) != 3:
    print("Usage: python3 MyCalculator.py <Broadcast IP> <Port>")
    sys.exit(1)

broadcast_ip = sys.argv[1]
port = int(sys.argv[2])

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Bind to all interfaces
try:
    sock.bind(('', port))
except socket.error as e:
    print(f"Bind failed: {e}")
    sys.exit(1)

print(f"Welcome to Calculator!")
print(f"Listening on broadcast address {broadcast_ip}:{port}")
print("Enter mathematical expressions or 'Exit' to quit")

def receive_messages():
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            message = data.decode()

            # If it's a result (contains '='), just print
            if '=' in message:
                print(f"Result from {addr[0]}: {message}")
            else:
                print(f"Equation from {addr[0]}: {message}")
                try:
                    # Use safer eval with limited scope
                    result = eval(message, {"__builtins__": {}}, {})
                    result_str = f"{message}={result}"
                except:
                    result_str = f"{message}=Invalid"
                sock.sendto(result_str.encode(), (broadcast_ip, port))
        except Exception as e:
            print(f"Error: {e}")

# Start receiver thread
recv_thread = threading.Thread(target=receive_messages, daemon=True)
recv_thread.start()

# Main loop for user input
while True:
    try:
        user_input = input()
        if user_input.lower() == "exit":
            print("Exiting.")
            break
        sock.sendto(user_input.encode(), (broadcast_ip, port))
    except Exception as e:
        print(f"Error: {e}")