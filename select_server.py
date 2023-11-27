# Example usage:
#
# python select_server.py 3490

import sys
import socket
import select


def run_server(port):
    # init a listening socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen()

    # init set of sockets pass to select() AND include the listening socket
    socket_set = {server_socket}

    while True:
        # wait for a socket to become readable
        readable, _, _ = select.select(socket_set, [], [])

        # loop through the readable sockets
        for s in readable:
            if s is server_socket:
                # A listening socket has detected a new connection - accept it
                client_socket, address = server_socket.accept()
                socket_set.add(client_socket)
                print(f"{address}: connected")
            else:
                # A client socket has data for us
                data = s.recv(1024)
                if data:
                    # Data - print it
                    print(f"{s.getpeername()} {len(data)} bytes: {data}")
                else:
                    # No data - client has disconnected
                    address = s.getpeername()
                    socket_set.remove(s)
                    s.close()
                    print(f"{address}: disconnected")

#--------------------------------#
# Do not modify below this line! #
#--------------------------------#

def usage():
    print("usage: select_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
