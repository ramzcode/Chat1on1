import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
import sys

# Maintain a list of connected clients
clients = {}

# Event to signal the server thread to stop
stop_event = threading.Event()

def handle_client(client_socket, client_address):
    while not stop_event.is_set():
        try:
            # Receive data from the client
            data = client_socket.recv(1024).decode()
            if not data:
                break

            print(f"\nReceived from client {client_address}:")
            print(data)

        except ConnectionResetError:
            break

    # Remove the client from the list upon disconnection
    remove_client(client_address)

def send_to_all_clients(message, sender_address):
    # Send the message to all connected clients except the sender
    for address, socket in clients.items():
        if address != sender_address:
            try:
                socket.send(message.encode())
            except ConnectionResetError:
                remove_client(address)

def remove_client(client_address):
    if client_address in clients:
        client_socket = clients[client_address]
        client_socket.close()
        del clients[client_address]
        print(f"Client {client_address} disconnected")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(5)
    server_socket.settimeout(1)  # Set a timeout value for accept()

    print("Server started and listening on port 8000")

    while not stop_event.is_set():
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Client {client_address} connected")

            # Add the client to the list of connected clients
            clients[client_address] = client_socket

            # Start a new thread to handle the client
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()

        except socket.timeout:
            continue

    # Close all client sockets
    for client_socket in clients.values():
        client_socket.close()

    # Close the server socket
    server_socket.close()

def send_message():
    message = message_entry.get()
    if message.strip():
        send_to_all_clients(message, None)
        message_entry.delete(0, tk.END)

def quit_server():
    stop_event.set()
    window.destroy()

# Create the main window
window = tk.Tk()
window.title("Server")

# Create a scrolled text area to display received messages
scrolled_text = scrolledtext.ScrolledText(window, width=50, height=10)
scrolled_text.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

# Create an entry field for sending messages
message_entry = tk.Entry(window, width=40)
message_entry.grid(row=1, column=0, padx=10, pady=10)

# Create a button to send messages
send_button = tk.Button(window, text="Send", width=10, command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10)

# Create a button to quit the server
quit_button = tk.Button(window, text="Quit", width=10, command=quit_server)
quit_button.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

# Redirect console output to the scrolled text area
class ConsoleRedirector:
    def write(self, message):
        scrolled_text.insert(tk.END, message)
        scrolled_text.see(tk.END)

sys.stdout = ConsoleRedirector()

# Start the server in a separate thread
server_thread = threading.Thread(target=start_server)
server_thread.start()

# Start the GUI event loop
window.mainloop()

