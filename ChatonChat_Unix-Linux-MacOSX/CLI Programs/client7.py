import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            # Receive messages from the server
            message = client_socket.recv(1024).decode()
            if not message:
                break

            #print("Received from server:", message)
            print(f"\nReceived from server:", message)
            #print(data)
            print("Enter message to send to client: ", end="", flush=True)

        except ConnectionResetError:
            break

    # Close the client socket upon disconnection
    client_socket.close()
    print("Disconnected from server")

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8000))

    # Start a separate thread to receive messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        # Send message to the server
        message = input("Enter message: ")
        client_socket.send(message.encode())

    # Close the client socket
    client_socket.close()

start_client()

