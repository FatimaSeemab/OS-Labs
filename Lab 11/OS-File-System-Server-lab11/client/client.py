import socket, os

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = input("File System Server IP: ")
sock.connect((ip, 95))

# print("The username of the client is: ",socket.gethostname())
print("The current system's hostname is ", os.uname()[1])
# Receive connection confirmation from server
print('Server:', sock.recv(256).decode())
print('Please keep sending commands to server for execution')
print('Enter "bye" to exit')

while True:
    try:
        command = input('command:')
        sock.sendall(command.encode())
        if command == 'bye':
            print('Connection closed successfully')
            break
        response = sock.recv(512).decode()
        print(response)
        if response == 'Error Occurred, closing connection':
            break
    except:
        print("Error Occurred, closing connection")
        sock.sendall("Error Occurred, closing connection".encode())
        break

sock.close()

