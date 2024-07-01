import socket
import threading

def handle_client(client_socket, client_address):
    request = client_socket.recv(1024).decode()
    parsed_request = request.split("\r\n")

    method = parsed_request[0].split(" ")[0]
    url = request.split(" ")[1]

    if method == "GET":
        if url == "/":
            response = "HTTP/1.1 200 OK\r\n\r\n"
        elif url.startswith('/echo/'):
            string = url.split("/echo/")[1]
            response = (
                f'HTTP/1.1 200 OK\r\n'
                'Content-Type: text/plain\r\n'
                f'Content-Length: {len(string)}\r\n\r\n'
                f'{string}'
            ).encode('utf-8')
        elif url.startswith('/user-agent'):
            user_agent = parsed_request[3].split(': ')[1]
            response = (
                f'HTTP/1.1 200 OK\r\n'
                'Content-Type: text/plain\r\n'
                f'Content-Length: {len(user_agent)}\r\n\r\n'
                f'{user_agent}'
            ).encode('utf-8')
        else:
            response = "HTTP/1.1 404 Not found\r\n\r\n".encode('utf-8')
    else:
        response = "HTTP/1.1 400 Bad Request\r\n\r\n".encode('utf-8')

    client_socket.sendall(response)


def main():
    '''
    Start the server and handle incoming client connections.
    '''
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen(1)

    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()
    

if __name__ == "__main__":
    main()