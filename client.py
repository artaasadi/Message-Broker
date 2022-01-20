from email import message
from pydoc import cli
import socket
import sys


PORT = 1373 # Port to listen on
MESSAGE_LENGTH_SIZE = 64 # Server needs MESSAGE_LENGTH_SIZE to get message length to know how much to recieve
ENCODING = 'ascii' # Ascii encoding for messages


def main() :
    address = socket.gethostbyname(socket.gethostname()) # Get Address automatically
    #HOST_INFORMATION = (address, PORT)
    HOST_INFORMATION = (sys.argv[1], int(sys.argv[2]))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client :
        client.connect(HOST_INFORMATION)
        if sys.argv[3] == "publish" :
            publish(client, sys.argv[4], sys.argv[5])
        elif sys.argv[3] == "subscribe" :
            subscribe(client, sys.argv[4:])
        

def publish(client : socket.socket, topic, body) :
    message = "publish " + topic + " " + body
    msg = message.encode(ENCODING)
    msg_length = str(len(msg)).encode(ENCODING)
    msg_length += b' ' * (MESSAGE_LENGTH_SIZE - len(msg_length))

    client.send(msg_length)
    client.send(msg)

def subscribe(client : socket.socket, topics) :
    message = "subscribe"
    for topic in topics :
        message += " " + topic
    msg = message.encode(ENCODING)
    msg_length = str(len(msg)).encode(ENCODING)
    msg_length += b' ' * (MESSAGE_LENGTH_SIZE - len(msg_length))

    client.send(msg_length)
    client.send(msg)
    listen(client)
    

def listen(client) :
    print(client.recv(1))

def connection_handler(conn : socket.socket, address):
    with conn:
        print("[NEW CONNECTION] connected from {}".format(address))
        while True :
            received = conn.recv(MESSAGE_LENGTH_SIZE).decode(ENCODING)
            if not received :
                break
            msg_length = int(received)
            msg = conn.recv(msg_length).decode(ENCODING)
            print("[MESSAGE RECEIVED] {}".format(msg))
    print("[CONNECTION DISCONNECTED] {}".format(address))



if __name__ == '__main__' :
    main()