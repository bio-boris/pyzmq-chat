# pyzmq-chat
Chatroom with pyzmq

Server runs in the background

Users can send messages, and see all messages since they connected.

This uses the REQUEST/REPLY messaging pattern with pyZMQ.
The client uses the main thread to send messages, and runs request messages on a seperate thread. 


# Future Ideas: Serve this chatroom with Tornado
