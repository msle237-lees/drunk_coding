from modules.NP import NP
import socket
import time

client_socket = NP(socket.AF_INET, socket.SOCK_STREAM)
client_socket.bind(('127.0.0.1', 9999))
client_socket.listen(1)
conn, addr = client_socket.accept()
print(f'Connected by client: {addr}.')
time.sleep(1)
while True:
    data = client_socket.recv_string_as_bytes()

    print(data)