from tkinter import *
import tkinter.scrolledtext as tkst
import tkinter.ttk as ttk
import socket
import json
from threading import Thread
from tkinter import messagebox

def checkData(data):

    data = str(data,'utf-8')

    if data[:6] != 'DACHAT':
        #print('$- Denied request: ' , data)
        return None

    #print('$- Received: ', data)

    data = data[6:]

    data = json.loads(data)

    return data
'''
def login(r):
	global nb
	global userEntry
	global passEntry

	username = userEntry.get()
	password = passEntry.get()
	print(username, ' ', password)
	nb.grid(row = 0 , column = 0, sticky = 'NSEW')
'''
def hi():
	print('hi')


class Chat():

	def __init__(self, master, notebook, nick):
		self.master = master
		self.frame = ttk.Frame(notebook)
		self.nickname = nick
		self.textBox = tkst.ScrolledText(self.frame, wrap = WORD, height = 19, width = 34)
		self.textBox.config(state = DISABLED)
		self.textBox.pack()	
		self.responseEntry = Entry(self.frame)
		self.responseEntry.pack()
		self.sendButton = Button(self.frame, text = 'Send', command = self.send)
		self.sendButton.pack()

	def send(self):
		txt = self.responseEntry.get()
		#self.responseEntry.set(text = '')
		self.master.client.send(bytes('DACHAT' + str(json.dumps({'type' : 'chat', 'target' : self.nickname, 'message' : txt})),'utf-8'))
		self.textBox.config(state = NORMAL)
		self.textBox.insert(INSERT, 'Me: ' + txt + '\n')
		self.textBox.config(state = DISABLED)

class LoginScreen():

	def __init__(self, master):

		self.master = master

		frame = Frame(master.root)
		
		self.loginLabel = Label(frame, text = 'Login', font = ('Times', 30))
		self.loginLabel.grid(column = 1)

		self.userLabel = Label(frame, text = 'Username')
		self.userLabel.grid(row =1, column = 0)

		self.passLabel = Label(frame, text = 'Password')
		self.passLabel.grid(row = 2,column = 0)

		self.userEntry = Entry(frame)
		self.userEntry.grid(row = 1, column = 1)

		self.passEntry = Entry(frame, show = '*')
		self.passEntry.grid(row = 2, column = 1)

		self.loginButton = Button(frame, text = 'Login', command = self.login)
		self.loginButton.grid(row = 3, column = 1)

		frame.place(x = 50, y =  100)

	def login(self):
		print('LOGGED IN!')

		target_host = "localhost"
		target_port = 9999

		self.master.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.master.client.connect((target_host,target_port))
		
		data  = str(json.dumps({'username' : self.userEntry.get(), 'password' : self.passEntry.get()}))

		data = bytes('DACHAT'+data, 'utf-8')	

		self.master.client.send(data)
		response = self.master.client.recv(4096)
	
		#response = str(response, 'utf-8')
		response = checkData(response)

		if response['response'] == 'connected':
			self.master.myNickname = response['nickname']
			print('Succesfully Connected as ' + self.master.myNickname + '!')
			self.master.mainscreen = MainWindow(self.master)
			#Thread(target = listenLoop, args = (client,)).start()
		elif response['response'] == 'rejected' :
			print(response['error'])
			print('Client Closed conetion!')
			messagebox.showwarning('DaChat!', response['error'])
			self.master.client.close()
		

		print(response)
		


		


class MainWindow():

	def __init__(self, master):
		
		self.master = master
		frame = Frame(master.root)
		self.nb = ttk.Notebook(frame)
		self.nb.pack()
		txt = 'Logged in as ' + self.master.myNickname
		self.me = Label(frame, text = txt)
		self.me.pack(side = LEFT)

		for name in ('Mike', 'John', 'Lukas'):
			c = Chat(self.master, self.nb, name)
			self.nb.add(c.frame, text = c.nickname)

		frame.pack()

class DACHAT:

	def __init__(self):
		self.root = Tk()
		self.root.title('DaChat!')
		self.root.geometry('300x400')
		self.root.resizable(0, 0)
		#mainscreen = MainWindow(self)
		logscreen = LoginScreen(self)
		self.root.mainloop()





app = DACHAT()




'''
nb = ttk.Notebook(root)
#nb.grid(row = 0 , column = 0, sticky = 'NSEW')
tab1 = Chat(nb, 'mike')
tab2 = Chat(nb, 'john')

nb.add(tab1.frame, text = tab1.nickname)
nb.add(tab2.frame, text = tab2.nickname)

#loginScreen.tkraise()
#lol = Chat(root, 'mike')

#root.bind("<Configure>", refresh)
'''


