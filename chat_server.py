import zmq
import json


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:5000")

messages = []

"""
{'type': 'count'}
{'type': 'fetch', 'from': 10}
{'type': 'post', 'message': 'Hi Boris'}
"""


def handle(msg):
	# load JSON, returin the right result, JSON encoded
	data = json.loads(msg)
	data_type = data.get('type')
	result = None

	if data_type == 'count':
		result = {'count': len(messages)}
	elif data_type == 'fetch':
		result = {'messages': messages[data['from']:]}
	elif data_type =='post':
		messages.append(data['msg'])
		result = {'count': len(messages)}
	if result:
		return json.dumps(result)
	else:
		return json.dumps({'error':"Error, valid types are : count , fetch, post"})

 
while True:
	msg = socket.recv()
	print("Got", msg)
	result = handle(msg)
	socket.send(result)
