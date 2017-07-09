import threading
import zmq
import json
import time
import sys

user_name = 'default'
if len(sys.argv) < 2:
    print ("usage: chat_client.py <username>")
    raise SystemExit
else:
    user_name = sys.argv[1]

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5000")
lock = threading.Lock()

# send type:count mesg
# read a message
# send message, if user typed anything
# fetch any messages, and print them

def send(data):
    socket.send(json.dumps(data))

def recv():
    return json.loads(socket.recv())


def fetch_messages():
    global current_count
    while True:
        time.sleep(0.3)
        with lock:
            send({'type': 'fetch', 'from': current_count})
            fetch_response = recv()
            messages = fetch_response['messages']

        current_count += len(messages)
        for m in messages:
            if m[1] != user_name:
                print("{0}: {1}".format(m[1],m[0]))

def get_messages_count():
    send({'type': 'count'})
    data = recv()
    return data.get('count', 0)
    

def send_message(msg):
    message = {'type': 'post', 'msg' : msg, 'user' : user_name } 
    send(message)
    recv()

# Get messages starting from the end 
current_count = get_messages_count()

# Fetch Messages Thread
threading.Thread(target=fetch_messages).start()

# Send Messages Main
while True:

    msg = raw_input('> ')
    if msg:
        with lock:
            send_message(msg)
