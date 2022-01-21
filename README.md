# Message-Broker
### Description
A client-server program. Clients can connect to server to share their contents and subscribe to specific topics and get shared contents.
This project uses pythons socket library for socket programming.
Server sends a ping every 10 seconds to check the connection and Client should answer each of them with a pong. In case of server not getting any response from the client after three periods, it will close the connection and remove the client from the list.
Clients also can quit from server connection.

### Run

Server :

    $ python server.py
    
Client :

    $ python client.py {HOST IP (or . for default)} {PORT (or . for default)} {Order (optional)}
    
### Usage

In case of not giving HOST IP and PORT as the system arguments to client.py, or disconnecting from the server, the client program requests for HOST IP and PORT. By typing "default" it consideres them as default.

Client Orders :
> **publish [topic] [message]** : publishes the given message with the given topic for the subscribers of the given topic.
>
> **subscribe [topics]** : subscribe to the given topics and get the messages of the topics (adds the client to the subscription list of the topic)
>
> **dont answer ping** : disables pong respons in case of testing ping pong respons
>
> **answer ping** : enables pong respons in case of testing ping pong respons
>
> **quit** : close the connection (not the client app)
