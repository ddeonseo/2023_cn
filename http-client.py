import socket

TCP_IP = '168.188.126.81'
TCP_PORT = 80
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
request = "GET /index.html HTTP/1.1\r\nhost:networks.cnu.ac.kr\r\n\r\n"
s.send(request.encode())
data = s.recv(BUFFER_SIZE)
s.close()

print('recieved data:', data.decode('utf-8'))