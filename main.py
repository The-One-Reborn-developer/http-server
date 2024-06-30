import socket
import os


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen(1)

    client_socket, _ = server_socket.accept()

    request = client_socket.recv(1024).decode()
    
    url = request.split(" ")[1]

    if url == "/":
        response = "HTTP/1.1 200 OK\r\n\r\n"
    else:
        response = "HTTP/1.1 404 Not found\r\n\r\n"

    client_socket.sendall(response.encode())

if __name__ == "__main__":
    main()