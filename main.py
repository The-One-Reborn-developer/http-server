import socket
import os


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen(1)

    client_socket, _ = server_socket.accept()

    client_socket.sendall(b"HTTP/1.1 200 OK\r\n\r\n")

if __name__ == "__main__":
    main()