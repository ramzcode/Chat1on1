import socket
import threading
import sys

# Maintain a list of connected clients
clients = {}

# Flag to indicate if the server should continue running
server_running = True

def handle_client(client_socket, client_address):
    while True:
        try:
            # Receive data from the client
            data = client_socket.recv(1024).decode()
            if not data:
                break

            print(f"\nReceived from client {client_address}:")
            print(data)
            print("Enter message to send to client: ", end="", flush=True)

            if data.strip().lower() == "quit":
                break

        except ConnectionResetError:
            break

    # Remove the client from the list upon disconnection
    remove_client(client_address)
    client_socket.close()

def send_to_all_clients(message, sender_address):
    # Send the message to all connected clients except the sender
    for address, socket in clients.items():
        if address != sender_address:
            try:
                socket.send(message.encode())
            except ConnectionResetError:
                remove_client(address)

def send_to_client(recipient_address, message):
    # Send the message to a specific client
    if recipient_address in clients:
        try:
            clients[recipient_address].send(message.encode())
        except ConnectionResetError:
            remove_client(recipient_address)

def remove_client(client_address):
    if client_address in clients:
        client_socket = clients[client_address]
        del clients[client_address]
        print(f"Client {client_address} disconnected")

def start_server():
    global server_running  # Declare the server_running flag as global

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(5)

    print("Server started and listening on port 8000")
    print("Enter message to send to client: ", end="", flush=True)

    while server_running:
        client_socket, client_address = server_socket.accept()
        print(f"Client {client_address} connected")

        # Add the client to the list of connected clients
        clients[client_address] = client_socket

        # Start a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

        # Start a new thread to listen for server console input and send messages
        server_thread = threading.Thread(target=handle_server_input)
        server_thread.start()

    # Close all client connections before exiting
    for client_socket in clients.values():
        client_socket.close()

def handle_server_input():
    while True:
        message = input("Enter message to send to client (type 'quit' to exit): ")
        if message.strip().lower() == "quit":
            send_to_all_clients("quit", None)
            server_running = False  # Update the server_running flag to stop the server
            sys.exit(0)  # Terminate the server program
            break
        else:
            send_to_all_clients(message, None)

start_server()

