import threading
from socket import *

s = socket(AF_INET, SOCK_STREAM)
host = "127.0.0.1"
port = 6500
s.bind((host, port))
s.listen()

clients = []
aliases = []
connected_clients = 0  # Track the number of connected clients

def broadcast(message, sender_client):
    for client in clients:
        if client != sender_client:  # Exclude sender client
            client.send(message)

def handle_client(client):
    global connected_clients  # Access the global count of connected clients
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)  # Pass sender client to broadcast
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat room!'.encode('utf-8'), client)  # Pass sender client to broadcast
            aliases.remove(alias)
            connected_clients -= 1  # Decrement the count of connected clients
            if connected_clients == 0:
                s.close()  # Close the server socket if no clients are connected
            break

def receive():
    global connected_clients  # Access the global count of connected clients
    while True:
        print("server is running and listening...")
        print("!! if you need to leave the chat room write 'end' !! ")
        client, addr = s.accept()
        connected_clients += 1  # Increment the count of connected clients
        print(f'connection is established with {str(addr)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        print(f'the alias of this client is {alias}'.encode('utf-8'))
        broadcast(f'{alias} has connected to the client room'.encode('utf-8'), client)  # Pass sender client to broadcast
        client.send('you are connected!'.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive()
