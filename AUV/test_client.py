from modules.NP import NP
import socket

client_socket = NP(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 9999))
print('Connected to server.')

while True:
    data = client_socket.recv()
    print(data)