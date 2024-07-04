import socket
import threading
import gzip

def handle_client(client_socket, client_address):
    '''
    Handle a single client connection.
    '''
    # Receive the request from the client
    request = client_socket.recv(1024).decode()
    # Split the request into lines
    parsed_request = request.split("\r\n")

    # Extract the method (GET, POST, etc.) and URL from the request
    method = parsed_request[0].split(" ")[0]
    url = request.split(" ")[1]

    # Handle GET requests
    if method == "GET":
        # If the URL is "/", return a 200 OK response
        if url == "/":
            response = "HTTP/1.1 200 OK\r\n\r\n"
        # If the URL starts with "/echo/", return the provided string
        elif url.startswith('/echo/'):
            string = url.split("/echo/")[1]
            # If the client supports gzip compression, compress the string
            if 'Accept-Encoding' in request:
                compressed_string = gzip.compress(string.encode('utf-8'))
                response = (
                    f'HTTP/1.1 200 OK\r\n'
                    'Content-Type: text/plain\r\n'
                    f'Content-Length: {len(string)}\r\n'
                    'Content-Encoding: gzip\r\n\r\n'
                    f'{compressed_string}'
                ).encode('utf-8')
            # If the client does not support gzip compression, return the string as is
            else:
                response = (
                    f'HTTP/1.1 200 OK\r\n'
                    'Content-Type: text/plain\r\n'
                    f'Content-Length: {len(string)}\r\n\r\n'
                    f'{string}'
                ).encode('utf-8')
        # If the URL starts with "/user-agent", return the user agent string
        elif url.startswith('/user-agent'):
            user_agent = parsed_request[3].split(': ')[1]
            response = (
                f'HTTP/1.1 200 OK\r\n'
                'Content-Type: text/plain\r\n'
                f'Content-Length: {len(user_agent)}\r\n\r\n'
                f'{user_agent}'
            ).encode('utf-8')
        # If the URL starts with "/files", return the content of the specified file
        elif url.startswith('/files'):
            file_path = url.split("/files/")[1]
            with open(file_path, 'rb') as file:
                file_data = file.read()
            response = (
                f'HTTP/1.1 200 OK\r\n'
                'Content-Type: text/plain\r\n'
                f'Content-Length: {len(file_data)}\r\n\r\n'
                f'{file_data.decode("utf-8")}'
            ).encode('utf-8')
        # If the URL does not match any of the above, return a 404 Not found response
        else:
            response = "HTTP/1.1 404 Not found\r\n\r\n".encode('utf-8')
    # Handle POST requests
    elif method == "POST":
        file_path = url.split("/files/")[1]
        # Write the request body to the specified file
        with open(file_path, 'wb') as file:
            file.write(parsed_request[-1].encode())
        response = "HTTP/1.1 201 Created\r\n\r\n".encode('utf-8')
    # If the method is neither GET nor POST, return a 400 Bad Request response
    else:
        response = "HTTP/1.1 400 Bad Request\r\n\r\n".encode('utf-8')

    client_socket.sendall(response)


def main():
    '''
    Start the server and handle incoming client connections.
    '''
    # Create a server socket
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    # Put the server socket into listening mode
    server_socket.listen(1)

    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        # Create a new thread to handle the client connection
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()
    

if __name__ == "__main__":
    main()