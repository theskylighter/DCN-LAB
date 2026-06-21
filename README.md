# 🌐 DCN Lab Reference Guide (4th Semester)

Welcome to the **Data Communication and Networking (DCN) Lab** repository! This project contains Python implementations of fundamental networking algorithms, error detection/correction mechanisms, and socket-based networking architectures.

---

## 📌 Table of Contents
1. [📂 Repository Structure & Directory Map](#-repository-structure--directory-map)
2. [🔍 Module Breakdown & Theory](#-module-breakdown--theory)
3. [🪲 Critical Bugs & Quirks (Educational Focus)](#-critical-bugs--quirks-educational-focus)
4. [🚀 How to Run the Code](#-how-to-run-the-code)
5. [📚 Resources & Further Learning](#-resources--further-learning)

---

## 📂 Repository Structure & Directory Map

Below is an overview of the codebase. The links below are relative paths compatible with GitHub's file browser:

*   📂 **Root Directory**
    *   📄 [ip_addressing.py](ip_addressing.py) - IP address classification and Classless Inter-Domain Routing (CIDR) subnet calculator.
*   📂 **[checkSUM](checkSUM)** - Error detection using sums and polynomials.
    *   📄 [8bit_16bit.py](checkSUM/8bit_16bit.py) - 8-bit and 16-bit One's Complement checksum.
    *   📄 [crc.py](checkSUM/crc.py) - Standard Cyclic Redundancy Check (CRC) encoder/decoder using binary division.
    *   📄 [crc-pratham.py](checkSUM/crc-pratham.py) - Alternative implementation of CRC with string manipulation.
*   📂 **[hamming code](hamming%20code)** - Error correction using Hamming distance.
    *   📄 [hamming.py](hamming%20code/hamming.py) - Dynamic Hamming Code generator and error corrector (works for any data length).
    *   📄 [hamming(7,4).py](hamming%20code/hamming(7,4).py) - Standard Hamming (7,4) implementation with hardcoded parity equations.
*   📂 **[multicast_calc](multicast_calc)** - Multi-client UDP calculations.
    *   📄 [MyCalculator.py](multicast_calc/MyCalculator.py) - UDP Broadcast peer-to-peer calculator.
    *   📄 [MyCalculator1.py](multicast_calc/MyCalculator1.py) - UDP Multicast calculator utilizing IGMP group membership.
*   📂 **[SOCKET](SOCKET)** - Core socket programming exercises.
    *   📂 **[assignment 2](SOCKET/assignment%202)**
        *   📄 [ftpclient.py](SOCKET/assignment%202/ftpclient.py) - Protocol-agnostic (TCP/UDP) FTP-like client.
        *   📄 [ftpserver.py](SOCKET/assignment%202/ftpserver.py) - Multi-threaded FTP-like server handling both TCP and UDP.
        *   📄 [server.py](SOCKET/assignment%202/server.py) - Simple TCP echo connection script (boilerplate).
    *   📂 **[live_chat](SOCKET/live_chat)**
        *   📄 [client.py](SOCKET/live_chat/client.py) & [server.py](SOCKET/live_chat/server.py) - Barebones one-off TCP packet exchange.
        *   📄 [client2.py](SOCKET/live_chat/client2.py) & [server2.py](SOCKET/live_chat/server2.py) - Turn-based interactive TCP chat server and client.
        *   📂 **[UDP](SOCKET/live_chat/UDP)**
            *   📄 [client2.py](SOCKET/live_chat/UDP/client2.py) & [server2.py](SOCKET/live_chat/UDP/server2.py) - Turn-based UDP interactive chat room.
    *   📂 **[tcp_multiport](SOCKET/tcp_multiport)**
        *   📄 [tcp_multiport.py](SOCKET/tcp_multiport/tcp_multiport.py) - Multi-threaded multi-port server running services on port 5000, 6000, and 7000.
        *   📄 [client2.py](SOCKET/tcp_multiport/client2.py) - Test chat client for the multiport server.
    *   📂 **[threading_multiple_client](SOCKET/threading_multiple_client)**
        *   📄 [client.py](SOCKET/threading_multiple_client/client.py) - Client script for connection tests.
        *   📄 [multi_client_server.py](SOCKET/threading_multiple_client/multi_client_server.py) - Static thread pool server accepting clients on pre-spawned threads.
        *   📄 [chatGPT_multi_client_server.py](SOCKET/threading_multiple_client/chatGPT_multi_client_server.py) - Dynamic multi-threaded TCP server spinning new threads on-demand.
        *   📄 [chatGPT_banning_multi_client_server.py](SOCKET/threading_multiple_client/chatGPT_banning_multi_client_server.py) - Multi-threaded server containing a firewall blacklist (contains educational bugs!).

---

## 🔍 Module Breakdown & Theory

### 1. IP Addressing & Subnet Calculator (`ip_addressing.py`)
*   **Concepts**: IPv4 Classes (A, B, C, D, E), CIDR Notation (e.g., `/28`), Subnet Masks, Network Address, Broadcast Address, and Usable Host Range.
*   **Class Ranges (based on the first octet)**:
    *   **Class A**: $0 - 127$ (Subnet Mask: `255.0.0.0`)
    *   **Class B**: $128 - 191$ (Subnet Mask: `255.255.0.0`)
    *   **Class C**: $192 - 223$ (Subnet Mask: `255.255.255.0`)
    *   **Class D (Multicast)**: $224 - 239$
    *   **Class E (Experimental)**: $240 - 255$
*   **How it works**: It parses the CIDR block using Python's standard `ipaddress` library to automatically compute masks and host boundaries, combined with custom conditional logic to identify classes.

### 2. Error Detection (Checksum & CRC)
*   **One's Complement Checksum (`8bit_16bit.py`)**:
    *   **Sender**: Calculates sum of all data words. If a carry bit occurs beyond the bit limit (8 or 16), it is wrapped around and added to the least significant bit (One's Complement Sum). The checksum is the bitwise negation (`~`) of this sum.
    *   **Receiver**: Sums all data words *plus* the checksum. If the result is all 1s (e.g., `0xFF` or `0xFFFF`), the transmission is error-free.
*   **Cyclic Redundancy Check (`crc.py` & `crc-pratham.py`)**:
    *   Uses **Modulo-2 division** (which is implemented using bitwise **XOR** instead of subtraction).
    *   **Encoding**: Appends $N$ zeros (where $N = \text{length of generator} - 1$) to the original data, divides by the generator polynomial, and replaces the $N$ zeros with the calculated remainder.
    *   **Decoding**: Divides the received frame by the generator polynomial. If the remainder is all zeros, no error has occurred.

### 3. Error Correction (Hamming Code)
*   **Theory**: Hamming code inserts parity bits at power-of-two indices ($1, 2, 4, 8, \dots$). Parity bit $P_i$ checks all data positions whose binary representation has a $1$ in the $i$-th position.
    *   **Formula**: The number of parity bits $r$ needed for $m$ data bits satisfies: 
        $$2^r \ge m + r + 1$$
*   **`hamming.py` (Dynamic)**: Calculates the number of required parity bits dynamically based on input length, distributes parity bits, computes XOR sums, and is capable of detecting and correcting a single flipped bit by locating the exact error index (binary index pointing to the corrupted bit).
*   **`hamming(7,4).py` (Static)**: Specifically targets 4 data bits and adds 3 parity bits to make a 7-bit codeword. Parity logic is hardcoded:
    *   $P_1 = D_1 \oplus D_2 \oplus D_4$ (positions 1, 3, 5, 7)
    *   $P_2 = D_1 \oplus D_3 \oplus D_4$ (positions 2, 3, 6, 7)
    *   $P_3 = D_2 \oplus D_3 \oplus D_4$ (positions 4, 5, 6, 7)

### 4. Socket Programming Basics
*   **TCP vs UDP**:
    *   **TCP** (`SOCK_STREAM`): Connection-oriented, guarantees delivery, requires handshake (`connect` / `accept`).
    *   **UDP** (`SOCK_DGRAM`): Connectionless, faster, no ordering guarantees, uses `sendto` / `recvfrom`.
*   **Multi-Port Services (`tcp_multiport.py`)**: Demonstrates how a single machine can run distinct network processes on multiple ports by spawning blocking listener threads for each designated port.
*   **P2P Calculator (`MyCalculator.py` & `MyCalculator1.py`)**:
    *   Instead of standard client-server models, these tools listen for mathematical equations.
    *   **Broadcast version** (`MyCalculator.py`): Messages are sent to `255.255.255.255` or subnet broadcast IP. Every device on the local network segment receives and runs calculations.
    *   **Multicast version** (`MyCalculator1.py`): Message is sent to class D range `224.0.0.0 - 239.255.255.255`. Only devices that have joined the multicast group receive it.

---

## 🪲 Critical Bugs & Quirks (Educational Focus)

When reviewing the codebase for exams or lab files, make note of these bugs present in the scripts:

### 🚨 1. Blacklist Logic Bug in `chatGPT_banning_multi_client_server.py`
In [chatGPT_banning_multi_client_server.py](SOCKET/threading_multiple_client/chatGPT_banning_multi_client_server.py):
```python
banned_ip_list=["127.0.0.1"]

while True:
    clientObj, addr = sockObj.accept()
    print(f"New connection from {addr}")
    if(addr in banned_ip_list):
        print(f"this IP is in banned list {addr}")
        clientObj.sendall("your ip has been banned by server".encode("utf-8"))

    # Start a new thread for the client
    client_thread = threading.Thread(target=handle_client, args=(clientObj, addr))
    client_thread.start()
```
*   **What's wrong?**
    1.  `addr` is a tuple `(IP_string, Port_integer)` (e.g., `("127.0.0.1", 54321)`). Comparing a tuple `addr` directly to a list of strings `banned_ip_list` (`addr in banned_ip_list`) will **always return False**. The comparison should check `addr[0] in banned_ip_list`.
    2.  Even if the condition matched, there is no `else` block or `continue` statement. The script will send the ban message but **still launch a new thread and handle the connection anyway**.
*   **How to fix it:**
    ```python
    if addr[0] in banned_ip_list:
        print(f"IP {addr[0]} is banned.")
        clientObj.sendall("your ip has been banned by server".encode("utf-8"))
        clientObj.close()
        continue # Skip spawning thread
    ```

### 🚨 2. Standard Input (`stdin`) Clashing in Multi-Threaded Server
In [multi_client_server.py](SOCKET/threading_multiple_client/multi_client_server.py):
```python
response = input(f"{threading.current_thread} Send to client: ")
```
*   **What's wrong?** If multiple clients connect concurrently, multiple threads will simultaneously block on `input()`. This leads to race conditions on the terminal input—which thread gets the characters you type? The UI gets messy, and you cannot direct messages to specific clients reliably.
*   **Solution**: For interactive chatting with multiple concurrent clients, you should implement an asynchronous mechanism, a GUI, or use a broadcast-based chat where messages from one client are forwarded to all other clients, rather than using raw server terminal inputs.

### 🚨 3. Single-Connection Socket Boilerplate in `server.py`
In [server.py (assignment 2)](SOCKET/assignment%202/server.py):
*   The header comments ask for a server that can accept "multiple connections at any given time, with multiplexed I/O operations".
*   **What's wrong?** The script does not contain thread execution, `select.select()`, or asynchronous handlers. It accepts exactly one client connection, exchanges one string, and immediately closes. It is **not** multiplexed. Reference [chatGPT_multi_client_server.py](SOCKET/threading_multiple_client/chatGPT_multi_client_server.py) or `select` module tutorials to write a multiplexed server.

---

## 🚀 How to Run the Code

### 🔌 Running TCP/UDP FTP System
First, start the server in one terminal:
```powershell
# Starts TCP on port 8000 and UDP on port 8001
python "SOCKET/assignment 2/ftpserver.py"
```
Next, launch the client in another terminal specifying Host, Port, and Protocol (`TCP` or `UDP`):
```powershell
# Using TCP
python "SOCKET/assignment 2/ftpclient.py" 127.0.0.1 8000 TCP

# Using UDP
python "SOCKET/assignment 2/ftpclient.py" 127.0.0.1 8001 UDP
```

### 💬 Running Multi-Client Chat Servers
Start the server:
```powershell
python "SOCKET/threading_multiple_client/chatGPT_multi_client_server.py"
```
In secondary terminals, run multiple instances of the client:
```powershell
python "SOCKET/threading_multiple_client/client.py"
```

### 🧮 Running Broadcast & Multicast Calculators
Open multiple terminals to simulate different machines on the subnet.

**For UDP Broadcast Calculator**:
```powershell
# Format: python MyCalculator.py <Broadcast IP> <Port>
# Using the local loopback broadcast:
python "multicast_calc/MyCalculator.py" 127.0.0.1 9999
```
*Type mathematical equations like `2+3*4` in any window, and see the calculated response broadcasted instantly across all terminals!*

**For UDP Multicast Calculator**:
```powershell
# Format: python MyCalculator1.py <Multicast IP> <Port>
# Note: Multicast addresses must be in Class D range (e.g., 224.1.1.1)
python "multicast_calc/MyCalculator1.py" 224.1.1.1 9999
```

---

## 📚 Resources & Further Learning

To deep dive into the theoretical concepts used in this lab, explore the following resources:

### 📖 Standard Official Documentation
*   [Python Socket Module](https://docs.python.org/3/library/socket.html) - Low-level networking interface.
*   [Python ipaddress Module](https://docs.python.org/3/library/ipaddress.html) - IPv4/IPv6 manipulation library.
*   [Python threading Module](https://docs.python.org/3/library/threading.html) - Thread-based parallelism.

### 🌐 Networking Theory & Tutorials
*   [GeeksforGeeks: Computer Network Tutorials](https://www.geeksforgeeks.org/computer-network-tutorials/) - Detailed articles on IP addressing, CRC, Checksum, and Hamming Code.
*   [Computer Networking: A Top-Down Approach](https://jimurob.github.io/computer-networking-a-top-down-approach/) - Companion material for the classic textbook by Kurose & Ross.
*   [Beej's Guide to Network Programming](https://beej.us/guide/bgnet/) - The ultimate guide to C socket programming, highly valuable for understanding socket states under the hood.

### 🛠️ Interactive Calculators & Visualizations
*   [IP Subnet Calculator](https://www.subnet-calculator.com/) - Tool to verify subnet ranges, broadcast addresses, and masks.
*   [Hamming Code (7, 4) Interactive Simulation](https://www.youtube.com/watch?v=373EKgI7OPE) - Explains error correction conceptually.
*   [CRC Calculator](http://www.sunshine2k.de/coding/javascript/crc/crc_js.html) - Visual calculation of CRC remainder using modulo-2 division.
