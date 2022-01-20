from multiprocessing.connection import wait
import socket
import sys
import threading

PORT = 1373 # Port to listen on
MESSAGE_LENGTH_SIZE = 64 # Server needs MESSAGE_LENGTH_SIZE to get message length to know how much to recieve
ENCODING = 'ascii' # Ascii encoding for messages


def send_msg(client : socket.socket, message) :
    msg = message.encode(ENCODING)
    msg_length = str(len(msg)).encode(ENCODING)
    msg_length += b' ' * (MESSAGE_LENGTH_SIZE - len(msg_length))

    client.send(msg_length)
    client.send(msg)

def quit(client : socket.socket) :
    message = "quit"
    send_msg(client, message)

def publish(client : socket.socket, topic, body) :
    message = "publish " + topic
    for b in body :
        message += " " + b
    send_msg(client, message)

def listener(client : socket.socket, a) :
    while True :
        received = client.recv(MESSAGE_LENGTH_SIZE).decode(ENCODING)
        if not received :
            break
        msg_length = int(received)
        msg = client.recv(msg_length).decode(ENCODING)
        if msg == "closed" :
            print("[CONNECTION CLOSED]")
            create_connection()
        print("[MESSAGE RECEIVED] {}".format(msg))

def subscribe(client : socket.socket, topics) :
    message = "subscribe"
    for topic in topics :
        message += " " + topic
    send_msg(client, message)
    

def order_listener(client : socket.socket) :
    while True :
        order = input().split()
        if order[0] == "publish" :
            if len(order) == 1 :
                print("Please input topic and message body!!!")
                continue
            if len(order) == 2 :
                print("Please input message body!!!")
                continue
            publish(client, order[1], order[2:])
        elif order[0] == "subscribe" :
            if len(order) == 1 :
                print("Please input topics!!!")
                continue
            subscribe(client, order[1:])
        elif order[0] == "ping" :
            pass
        elif order[0] == "pong" :
            pass
        elif order[0] == "quit" :
            quit(client)


def create_connection() :
    try :
        client_input = input("Please enter the connection setting as [ADDRESS] [PORT] : ")
        if client_input == "default" :
            address = socket.gethostbyname(socket.gethostname())
            HOST_INFORMATION = (address, PORT)
        else :
            address, input_port = tuple(client_input.split())
            HOST_INFORMATION = (address, int(input_port))
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client :
            client.connect(HOST_INFORMATION)
            threading.Thread(target=listener, args=(client, 1)).start() # Resreve a thread for subscribing
            print("[CONNECTION ESTABLISHED]")
            order_listener(client)
    except Exception as e :
        print(e)
        create_connection()


def main() :
    address = socket.gethostbyname(socket.gethostname()) # Get Address automatically
    try:
        if sys.argv[1] == "." and sys.argv[2] == "." :
            HOST_INFORMATION = (address, PORT) # default setting
        else :
            HOST_INFORMATION = (sys.argv[1], int(sys.argv[2])) # manual setting
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client :
            client.connect(HOST_INFORMATION)
            if sys.argv[3] == "publish" :
                publish(client, sys.argv[4], sys.argv[5])
            elif sys.argv[3] == "subscribe" :
                subscribe(client, sys.argv[4:])
            threading.Thread(target=listener, args=(client, 1)).start() # Resreve a thread for subscribing
            order_listener(client)
    except Exception as e:
        print(e)
        create_connection()



    

if __name__ == '__main__' :
    main()