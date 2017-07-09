import threading
import zmq
import json
import time

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5000")


current_count = None
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
		time.sleep(0.2)
		with lock:
			send({'type': 'fetch', 'from': current_count})
			messages = recv()['messages']
		current_count += len(messages)
		for m in messages:
			print('*', m)


send({'type': 'count'})
data = recv()
current_count = data.get('count', 0)

threading.Thread(target=fetch_messages).start()
while True:
	mesg = raw_input('> ')
	if mesg:
		with lock:
			send({'type': 'post', 'msg': mesg})
			recv()
