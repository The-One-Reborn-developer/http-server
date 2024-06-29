import socket


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen(1)

    while True:
        client_socket, _ = server_socket.accept()  # Wait for client
        try:
            client_socket.recv(1024)  # Receive HTTP request
            client_socket.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: 13\r\n\r\nHello, world!")  # Send HTTP response
        except BrokenPipeError:
            print("BrokenPipeError: client disconnected")
        finally:
            client_socket.close()


if __name__ == "__main__":
    main()