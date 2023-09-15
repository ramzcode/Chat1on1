import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            scrolled_text.insert(tk.END, message + "\n")
            scrolled_text.see(tk.END)
        except ConnectionResetError:
            break

def send_message():
    message = message_entry.get()
    if message.strip():
        client_socket.send(message.encode())
        message_entry.delete(0, tk.END)

def quit_client():
    client_socket.close()
    window.destroy()

# Create the main window
window = tk.Tk()
window.title("Client")

# Create a scrolled text area to display received messages
scrolled_text = scrolledtext.ScrolledText(window, width=50, height=10)
scrolled_text.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

# Create an entry field for sending messages
message_entry = tk.Entry(window, width=40)
message_entry.grid(row=1, column=0, padx=10, pady=10)

# Create a button to send messages
send_button = tk.Button(window, text="Send", width=10, command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10)

# Create a button to quit the client
quit_button = tk.Button(window, text="Quit", width=10, command=quit_client)
quit_button.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

# Create a socket for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the client to the server
server_address = ('localhost', 8000)
client_socket.connect(server_address)

# Start a new thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Start the GUI event loop
window.mainloop()

