# importing the necessary modules.
import socket
import sys
import errno

# defining the header length.
HEADER_LENGTH = 10

# defining the IP address and Port Number.
IP = "127.0.0.1"
PORT = 1234

# Getting the name of the client.
my_username = input("Username: ")

"""
Creating a client socket and providing the address family (socket.AF_INET) and type of connection (socket.SOCK_STREAM), i.e. using TCP connection.
"""
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connecting the socket with the IP address and Port Number.
client_socket.connect((IP, PORT))

"""
Setting the connection to a non-blocking state so that the recv() function call will not get blocked. It will return some exceptions only.
"""
client_socket.setblocking(False)

# Setting the username and header.
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')

"""
Here, we have encoded the username into bytes, counted the number of bytes, and then prepared a header of fixed size, that we have encoded to bytes as well.
"""

# sending the data.
client_socket.send(username_header + username)




# running an infinite loop to send continuous client requests.
while True:
    # Getting user input.
    message = input(f'{my_username} > ')

    # Sending the non-empty message.
    if message:
        """
        encode the message into bytes, counted the number of bytes, and then prepared a header of fixed size, that we have encoded to bytes as well.
        """
        message = message.encode('utf-8')
        header_message = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        # sending the message.
        client_socket.send(header_message + message)

    try:
        # looping over the received messages and printing them.
        while True:
            # getting the header.
            username_header = client_socket.recv(HEADER_LENGTH)

            # If no header is accepted then finish the connection.
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            # Converting the header to an int value.
            username_length = int(username_header.decode('utf-8').strip())

            # Decoding the received username.
            username = client_socket.recv(username_length).decode('utf-8')

            # Decoding the received message.
            header_message = client_socket.recv(HEADER_LENGTH)
            length_message = int(header_message.decode('utf-8').strip())
            message = client_socket.recv(length_message).decode('utf-8')

            # Printing the message.
            print(f'{username} > {message}')

    except IOError as e:
        # handling the normal error on nonblocking connections.
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()

        # If we did not receive anything, then continue.
        continue

    except Exception as e:
        print('Reading error: '.format(str(e)))
        sys.exit()
