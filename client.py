import socket
import string

PORT = 1373 # Port to listen on
MESSAGE_LENGTH_SIZE = 64 # Server needs MESSAGE_LENGTH_SIZE to get message length to know how much to recieve

def main() :
    address = socket.gethostbyname(socket.gethostname()) # Get Address automatically
    HOST_INFORMATION = (address, PORT)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client :
        client.connect(HOST_INFORMATION)
        send_msg(client, "test")
        

def send_msg(client : socket.socket, msg : string):
    pass

if __name__ == '__main__' :
    main()