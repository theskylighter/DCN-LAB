import socket
import struct
import sys
import threading

if len(sys.argv) != 3:
    print("Usage: python3 multicastCalc.py <Multicast IP> <Port>")
    sys.exit(1)

mcast_ip = sys.argv[1]
port = int(sys.argv[2])

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', port))

# Join multicast group
mreq = struct.pack("4sl", socket.inet_aton(mcast_ip), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print("Welcome to My Multicast Calculator! Enter 'Exit' to quit.")

# Function to receive and process messages
def receive_messages():
    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode()

        # If it's a result (contains '='), just print
        if '=' in message:
            print(f"Result from {addr[0]}: {message}")
        else:
            print(f"Equation from {addr[0]}: {message}")
            try:
                result = eval(message)
                result_str = f"{message}={result}"
            except:
                result_str = f"{message}=Invalid"
            sock.sendto(result_str.encode(), (mcast_ip, port))

# Start receiver thread
recv_thread = threading.Thread(target=receive_messages, daemon=True)
recv_thread.start()

# Main loop for user input
while True:
    user_input = input()
    if user_input.lower() == "exit":
        print("Exiting.")
        break
    sock.sendto(user_input.encode(), (mcast_ip, port))