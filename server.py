from pickle import TRUE
import socket
import threading


PORT = 1373 # Port to listen on
MESSAGE_LENGTH_SIZE = 64 # Need MESSAGE_LENGTH_SIZE to get message length to know how much to recieve


def main() :
    address = socket.gethostbyname(socket.gethostname()) # Get Address automatically
    HOST_INFORMATION = (address, PORT)
    # Initialize server socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server :
        server.bind(HOST_INFORMATION)
        start_server(server)


def start_server(server : socket.socket) :
    server.listen()
    while True :
        conn, address = server.accept()
        t = threading.Thread(target= connection_handler, args= (conn, address))
        t.start()

def connection_handler(conn : socket.socket, address : socket._RetAddress):
    print("[NEW CONNECTION] connected from {}".format(address))
    conn.close()

if __name__ == '__main__' :
    main()