import socket
import pyautogui
import json
from threading import Thread
from tkinter import *
import tkinter.scrolledtext as tkst
import tkinter.ttk as ttk


def checkData(data):

    data = str(data,'utf-8')

    if data[:6] != 'DACHAT':
        #print('$- Denied request: ' , data)
        return None

    #print('$- Received: ', data)

    data = data[6:]

    data = json.loads(data)

    return data

def listenLoop(socket):

	print('Now Listening for Incoming Messages!')

	while True:

		data = socket.recv(4096)

		data = checkData(data)

		if data['response'] == 'message' :
			print(data['from'] + ': ' + data['message']) 

		if data['response'] == 'quit' :
			print('Quitting Chat!')
			socket.close()
			break





target_host = "localhost"
target_port = 9999

username = pyautogui.prompt(text = 'Username:', title = 'Connect To Chat', default = '')
password = pyautogui.password(text = 'Password:', title = 'Connect To Chat', default = '', mask = '*')

data  = str(json.dumps({'username' : username, 'password' : password}))

data = bytes('DACHAT'+data, 'utf-8')

print(data)


print(type(data))

# create a socket object
try:
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((target_host,target_port))
	client.send(data)
	response = client.recv(4096)
	
	#response = str(response, 'utf-8')
	response = checkData(response)

	if response['response'] == 'connected':
		myNickname = response['nickname']
		print('Succesfully Connected as ' + myNickname + '!')
		Thread(target = listenLoop, args = (client,)).start()
	elif response['response'] == 'rejected' :
		print(response['error'])
		print('Client Closed conetion!')
		client.close()
		

	print(response)


	print('Send messages with formtat: <nickname> -> <message> , or QUIT to quit')

	while True:
		userinput = input('$- ')

		if userinput == 'QUIT':
			client.send(bytes('DACHAT'+ str(json.dumps({'type' : 'quit'})),'utf-8'))
			break

		if ' -> ' in userinput:
			data = userinput.split(' -> ')
			if len(data) == 2 :
				client.send(bytes('DACHAT' + str(json.dumps({'type' : 'chat', 'target' : data[0], 'message' : data[1]})),'utf-8'))
			else :
				print('WRONG FORMAT! TO MANY ->')
		else :
			print('WRONG FORMAT! NO ->')


except Exception as e:
	print(e)
finally:
	#client.close()
	pass

input()


