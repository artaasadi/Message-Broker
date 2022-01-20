import socket
import threading


PORT = 1373 # Port to listen on
MESSAGE_LENGTH_SIZE = 64 # Need MESSAGE_LENGTH_SIZE to get message length to know how much to recieve
ENCODING = 'ascii' # Ascii encoding for messages


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
        threading.Thread(target= connection_handler, args= (conn, address)).start()

def connection_handler(conn : socket.socket, address):
    with conn:
        print("[NEW CONNECTION] connected from {}".format(address))
        while True :
            received = conn.recv(MESSAGE_LENGTH_SIZE).decode(ENCODING)
            if not received :
                break
            msg_length = int(received)
            msg = conn.recv(msg_length).decode(ENCODING)
            msg = msg.split()
            if msg[0] == "subscribe":
                send_ping(conn)
            print("[MESSAGE RECEIVED] {}".format(msg))
    print("[CONNECTION DISCONNECTED] {}".format(address))

def send_ping(conn : socket.socket) :
    conn.send(b'1')


if __name__ == '__main__' :
    main()