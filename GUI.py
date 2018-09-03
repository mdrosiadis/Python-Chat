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
        return None

    data = data[6:]

    data = json.loads(data)

    return data


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
		self.responseEntry.delete(0, END)
		if txt = '' :
			return
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

		target_host = "localhost"
		target_port = 9999
		
		data  = str(json.dumps({'username' : self.userEntry.get(), 'password' : self.passEntry.get()}))

		data = bytes('DACHAT'+data, 'utf-8')	

		try :
			self.master.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.master.client.connect((target_host,target_port))
			self.master.client.send(data)
			response = self.master.client.recv(4096)
			response = checkData(response)
		except Exception:
			messagebox.showerror('DaChat!', 'Unable to connect to DaChat server!')
			return
	
		

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

		self.connected = [self.master.myNickname]

		self.getConnected()

		frame.pack()
		Thread(target = self.listener).start()

	def getConnected(self):

		for i in range(len(self.connected)):
			if type(self.connected[i]) == str:
				c = Chat(self.master, self.nb, self.connected[i])
				self.connected[i] =  c
				self.nb.add(c.frame, text = c.nickname)

	def listener(self):

		while True:

			data = self.master.client.recv(4096)

			data = checkData(data)

			if data['response'] == 'message' :
				for c in self.connected:
					if data['from'] == c.nickname:
						c.textBox.config(state = NORMAL)
						c.textBox.insert(INSERT, c.nickname + ': ' + data['message'] + '\n')
						c.textBox.config(state = DISABLED)
						messagebox.showinfo('DaChat!', 'New message from ' + c.nickname + '!')
						break

			if data['response'] == 'newnick' :
				
				members = data['nickname'].split('#')
				for member in members:
					self.connected.append(member)
				self.getConnected()


			if data['response'] == 'quit' :
				print('Quitting Chat!')
				self.master.client.close()
				return
				break

class DACHAT:

	def __init__(self):
		self.root = Tk()
		self.root.title('DaChat!')
		self.root.geometry('300x400')
		self.root.resizable(0, 0)
		#mainscreen = MainWindow(self)
		logscreen = LoginScreen(self)
		self.root.protocol("WM_DELETE_WINDOW", self.close)
		self.root.mainloop()

	def close(self):
		try :
			self.client.send(bytes('DACHAT' + str(json.dumps({'type' : 'quit'})),'utf-8'))
		except Exception as e:
			print(e)
		self.root.destroy()



app = DACHAT()
