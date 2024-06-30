import socket
import os


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen(1)

if __name__ == "__main__":
    main()