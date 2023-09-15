import socket

# Client details
client_ip = '127.0.0.1'
client_port = 12345

# Create a socket for communication
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific IP and port
server_socket.bind((client_ip, client_port))

# Listen for incoming connections
server_socket.listen(1)

print("Server is listening for incoming connections...")

# Accept a client connection
client_socket, client_address = server_socket.accept()
print("Client connected:", client_address)

while True:
    # Get the command from the user
    command = input("Enter command (or 'exit' to quit): ")

    if command.lower() == 'exit':
        break

    # Send the command to the client
    client_socket.send(command.encode())

    # Receive and display the output from the client
    response = client_socket.recv(4096).decode()
    print(response)

# Close the connection with the client
client_socket.close()
print("Client disconnected")

# Close the server socket
server_socket.close()

