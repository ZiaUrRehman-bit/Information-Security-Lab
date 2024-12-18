import socket  # Import the socket library to handle network connections.
import threading  # Import the threading library to handle multiple clients simultaneously.

# Connection Data
host = '127.0.0.1'  # The local host address (localhost).
port = 55555  # The port on which the server will listen for incoming connections.

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a new socket using IPv4 (AF_INET) and TCP (SOCK_STREAM).
server.bind((host, port))  # Bind the socket to the specified host and port.
server.listen()  # Listen for incoming connections.

# Lists For Clients and Their Nicknames
clients = []  # List to keep track of all connected client sockets.
nicknames = []  # List to keep track of client nicknames.

# Sending Messages To All Connected Clients
def broadcast(message):
    # Function to send a message to all connected clients.
    for client in clients:  # Iterate over each client in the clients list.
        client.send(message)  # Send the message to the current client.

# Handling Messages From Clients
def handle(client):
    # Function to handle communication with a client.
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)  # Receive a message from the client (with a buffer size of 1024 bytes).
            broadcast(message)  # Broadcast the received message to all other clients.
        except:
            # If an error occurs (e.g., client disconnects), handle the exception.
            # Removing And Closing Clients
            index = clients.index(client)  # Get the index of the client in the clients list.
            clients.remove(client)  # Remove the client from the clients list.
            client.close()  # Close the client's socket.
            nickname = nicknames[index]  # Get the client's nickname from the nicknames list using the index.
            broadcast('{} left!'.format(nickname).encode('ascii'))  # Broadcast a message indicating the client has left.
            nicknames.remove(nickname)  # Remove the client's nickname from the nicknames list.
            break  # Break out of the while loop to stop handling this client.

# Receiving / Listening Function
def receive():
    # Function to accept and handle incoming client connections.
    while True:
        # Accept Connection
        client, address = server.accept()  # Accept a new connection from a client.
        print("Connected with {}".format(str(address)))  # Print the address of the connected client.

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))  # Send a request for the client to send their nickname.
        nickname = client.recv(1024).decode('ascii')  # Receive the client's nickname.
        nicknames.append(nickname)  # Add the client's nickname to the nicknames list.
        clients.append(client)  # Add the client's socket to the clients list.

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))  # Print the client's nickname.
        broadcast("{} joined!".format(nickname).encode('ascii'))  # Broadcast a message indicating the client has joined.
        client.send('Connected to server!'.encode('ascii'))  # Send a confirmation message to the client.

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))  # Create a new thread to handle this client.
        thread.start()  # Start the new thread.

# Start the server to receive and handle clients.
receive()
