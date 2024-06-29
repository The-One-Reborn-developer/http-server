import socket
import os


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen(1)

    while True:
        client_socket, _ = server_socket.accept()  # Wait for client
        request = client_socket.recv(1024).decode()  # Receive HTTP request
        try:
            url = handle_request(request)  # Parse request
            if url == None:  # Not found
                response = b'HTTP/1.1 404 Not Found\r\n\r\n'
            else:  # Found
                if os.path.exists(url):
                    response = b'HTTP/1.1 200 OK\r\n\r\n'
                else:
                    response = b'HTTP/1.1 404 Not Found\r\n\r\n'
            
            client_socket.sendall(response)  # Send HTTP response
        except BrokenPipeError:
            print("BrokenPipeError: client disconnected")
        finally:
            client_socket.close()


def handle_request(request):
    '''
    Parses the request and returns the URL
    '''
    lines = request.split("\r\n")
    if lines:
        first_line = lines[0]
        method, url, protocol = first_line.split()
        return url
    return None


if __name__ == "__main__":
    main()