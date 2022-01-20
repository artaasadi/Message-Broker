import socket
import threading
import time

PORT = 1373 # Port to listen on
MESSAGE_LENGTH_SIZE = 64 # Need MESSAGE_LENGTH_SIZE to get message length to know how much to recieve
ENCODING = 'ascii' # Ascii encoding for messages

subscribers = {} # A global dictionary is needed

def send_msg(server : socket.socket, message) :
    msg = message.encode(ENCODING)
    msg_length = str(len(msg)).encode(ENCODING)
    msg_length += b' ' * (MESSAGE_LENGTH_SIZE - len(msg_length))

    server.send(msg_length)
    server.send(msg)

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
        last_ping = time.time()
        while True :
            if (time.time() - last_ping) >= 10.0 :
                last_ping = time.time()
                print("10 seconds")
            print(1)
            received = conn.recv(MESSAGE_LENGTH_SIZE).decode(ENCODING)
            print(2)
            if not received :
                pass
            msg_length = int(received)
            msg = conn.recv(msg_length).decode(ENCODING)
            msg = msg.split()
            if msg[0] == "subscribe" :
                send_msg(conn, "1")
            elif msg[0] == "quit" :
                send_msg(conn, "closed")
                break
            print("[MESSAGE RECEIVED] {}".format(msg))
    print("[CONNECTION CLOSED] {}".format(address))



if __name__ == '__main__' :
    main()