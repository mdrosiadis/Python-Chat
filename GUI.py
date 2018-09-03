from tkinter import *

def login(r):
	global frame2

	print('imhere')
	frame2.tkraise()


def refresh(event):
	global loginScreen
	global frame2


	#loginScreen.grid(row=0, column=0, sticky="nsew")
	#frame2.grid(row=0, column=0, sticky="nsew")

	if event :
		if event.width < 200 or event.height < 250 :
			return
		loginScreen.place(x = event.width/2 - 100, y = event.height/2 - 100 )
		frame2.place(x = event.width/2 - 100, y = event.height/2 - 100 )
	else :
		loginScreen.grid(row=0, column=0, sticky="nsew")
		frame2.grid(row=0, column=0, sticky="nsew")


root = Tk()
root.title('DaChat!')
root.geometry('200x400')

loginScreen  = Frame(root)

loginLabel = Label(loginScreen, text = 'Login', font = ('Times', 30))
loginLabel.grid(column = 1)

userLabel = Label(loginScreen, text = 'Username')
userLabel.grid(row =1, column = 0)

passLabel = Label(loginScreen, text = 'Password')
passLabel.grid(row = 2,column = 0)

userEntry = Entry(loginScreen)
userEntry.grid(row = 1, column = 1)

passEntry = Entry(loginScreen)
passEntry.grid(row = 2, column = 1)

loginButton = Button(loginScreen, text = 'Login', command = lambda: login(root))
loginButton.grid(row = 3, column = 1)

#loginScreen.pack()

frame2 = Frame(root)
l = Label(frame2, text = 'Logged in!').pack()

refresh(None)
loginScreen.tkraise()

root.bind("<Configure>", refresh)


root.mainloop()
