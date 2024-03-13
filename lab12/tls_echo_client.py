import socket
import ssl

HOST = 'echo.localhost.com'
PORT = 8892
CERT = 'echoCA.crt'

text = input('Input text: ').strip()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    context = ssl.create_default_context()
    context.load_verify_locations(CERT)
    with context.wrap_socket(s, server_hostname=HOST) as ss:
        ss.connect((HOST, PORT))
        ss.sendall(text.encode('utf-8'))
        data = ss.recv(1500)
        data = data.decode('utf-8')

print(f'Received: {data}')
