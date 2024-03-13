import socket
import ssl

HOST = 'echo.localhost.com'
PORT = 8892
CERT = 'echoCA.crt'
KEY = 'echoCA.key'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(CERT, KEY)

    with context.wrap_socket(s, server_side=True) as ss:
        print('Start server')
        while True:
            try:
                conn, addr = ss.accept()
                with conn:
                    print('Connected by', addr)
                    while True:
                        data = conn.recv(1500)
                        if not data:
                            break
                        conn.sendall(data)
            except KeyboardInterrupt:
                print('Shutdown server')
                break
