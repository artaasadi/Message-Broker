import socket
import sys

PORT = 1373 # Port to listen on
MESSAGE_LENGTH_SIZE = 64 # Server needs MESSAGE_LENGTH_SIZE to get message length to know how much to recieve
ENCODING = 'ascii' # Ascii encoding for messages

def main() :
    address = socket.gethostbyname(socket.gethostname()) # Get Address automatically
    HOST_INFORMATION = (address, PORT)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client :
        client.connect(HOST_INFORMATION)
        for msg in sys.argv :
            send_msg(client, msg)
        

def send_msg(client : socket.socket, message):
    msg = message.encode(ENCODING)
    msg_length = str(len(msg)).encode(ENCODING)
    msg_length += b' ' * (MESSAGE_LENGTH_SIZE - len(msg_length))

    client.send(msg_length)
    client.send(msg)

if __name__ == '__main__' :
    main()