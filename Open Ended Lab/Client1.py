import socket  # Import the socket library for network communication.
import threading  # Import the threading library to handle concurrency.

# Choosing Nickname
nickname = input("Choose your nickname: ")  # Prompt the user to enter a nickname.

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a new socket object using IPv4 (AF_INET) and TCP (SOCK_STREAM).
client.connect(('127.0.0.1', 55555))  # Connect to the server running on localhost (127.0.0.1) at port 55555.

# Listening to Server and Sending Nickname
def receive():
    # Function to listen for incoming messages from the server.
    while True:
        try:
            # Receive Message From Server
            message = client.recv(1024).decode('ascii')  # Receive a message from the server with a buffer size of 1024 bytes and decode it from ASCII.

            # If 'NICK' Send Nickname
            if message == 'NICK':  # If the message from the server is 'NICK',
                client.send(nickname.encode('ascii'))  # Send the user's nickname back to the server.
            else:
                print(message)  # Print any other message received from the server.

        except:
            # Close Connection When Error
            print("An error occurred!")  # Print an error message.
            client.close()  # Close the client socket.
            break  # Exit the loop and stop listening.

# Sending Messages To Server
def write():
    # Function to send messages from the client to the server.
    while True:
        # Format the message to include the nickname and input message.
        message = '{}: {}'.format(nickname, input(''))  # Format the message with the user's nickname.
        client.send(message.encode('ascii'))  # Send the message to the server encoded in ASCII.

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)  # Create a new thread to handle receiving messages from the server.
receive_thread.start()  # Start the receive thread.

write_thread = threading.Thread(target=write)  # Create a new thread to handle sending messages to the server.
write_thread.start()  # Start the write thread.
