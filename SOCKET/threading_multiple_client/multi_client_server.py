import threading , socket

def start_server():
    #defaults
    hostname= socket.gethostname()
    ipAddr = socket.gethostbyname(hostname)
    port =12345



    #create soket
    sockObj=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print("creating socket obj")

    #bind socket
    sockObj.bind((ipAddr,port))
    print("binding socket obj to ",ipAddr," ",port)

    #listen for connnections
    #queue=5

    sockObj.listen(5)
    print("listening for incoming connections")


    def accept_client():
        # Accept a connection from a client
        clientObj, addr = sockObj.accept()
        print(f"Connection established with {addr} on Thread: {threading.current_thread}")

        while True:
            # Receive a message from the client
            message = clientObj.recv(1024).decode('utf-8')
            print(f"{threading.current_thread} Received from client: {message}")
            
            # Close the connection
            
            if(message.lower()=='exit'):
                clientObj.send("Adios Amigo!")
                clientObj.close()
                break
            
            #send message
            message=input(f"{threading.current_thread} Send to client : ")
            clientObj.sendall(message.encode("utf-8"))



    th1=threading.Thread(target=accept_client)
    th2=threading.Thread(target=accept_client)
    th3=threading.Thread(target=accept_client)

    th1.start()
    th2.start()
    th3.start()




if __name__ == "__main__":
    start_server()




