import socket
import threading
import json

server_ip = 'localhost'
server_port = 9999

accounts = [{'username': 'mike', 'password' : 'mike', 'nickname' : 'Mike'}, 
            {'username': 'lukas', 'password' : 'lukas', 'nickname' : 'Lukas'},
            {'username': 'john', 'password' : '1234', 'nickname' : 'John'}]


activeClients = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((server_ip, server_port))

server.listen(5)

print('$- Listening on {}:{} '.format(server_ip, server_port))

def handle_client(client_socket):

    request = client_socket.recv(1024)


    data = checkData(request)

    if data == None:
        client_socket.close()
        return



    found = False

    for account in accounts:
        if data['username'] == account['username']:
            found = True
            
            if data['password'] == account['password']:
                for client in activeClients:
                    if account['nickname'] == client['nickname']:
                        client_socket.send(bytes("DACHAT" + str(json.dumps({'response' : 'rejected', 'error' : 'User already connected!'})),'utf-8'))
                        return

                client_socket.send(bytes("DACHAT" + str(json.dumps({'response' : 'connected', 'nickname' : account['nickname']})),'utf-8'))
                members = ''
                for client in activeClients:
                    client['socket'].send(bytes("DACHAT" + str(json.dumps({'response' : 'newnick', 'nickname' : account['nickname']})),'utf-8'))
                    members = members + client['nickname'] + '#'
                activeClients.append({'socket' : client_socket, 'nickname' : account['nickname']})
                if len(members) != 0 :
                    members = members[:-1]
                    client_socket.send(bytes("DACHAT" + str(json.dumps({'response' : 'newnick', 'nickname' : members})),'utf-8'))
                connectedClient(client_socket, account['nickname'])
                #client_socket.send(bytes("Succesfully Connected as " + account['nickname'],'utf-8'))
                

            else:
                client_socket.send(bytes("DACHAT" + str(json.dumps({'response' : 'rejected', 'error' : 'Wrong Password'})),'utf-8'))
                #client_socket.send(bytes("Wrong Password!",'utf-8')
                break
    if not found:
        #client_socket.send(bytes("Unknown Username!",'utf-8'))
        client_socket.send(bytes("DACHAT" + str(json.dumps({'response' : 'rejected', 'error' : 'Username not Found!'})),'utf-8'))

    #client_socket.send(bytes("1K για το chain 300 για το φουτερ",'utf-8'))

    #client_socket.close()

def connectedClient(client_socket, nickname):

    print(nickname + ' connected!')

    while True:

        data = client_socket.recv(4096)

        data = checkData(data)

        print('Got DATA')

        if data == None:
            print('Server Closed conetion!')
            client_socket.close()
            return

        if data['type'] == 'quit' :
            client_socket.send(bytes('DACHAT' + str(json.dumps({'response' : 'quit'})), 'utf-8'))
            print(nickname + ' disconected!')
            for client in activeClients:
                if nickname == client['nickname']:
                    activeClients.remove(client)
                    break
            client_socket.close()
            return
        if data['type'] == 'chat' :
            userFound = False
            for client in activeClients:
                if data['target'] == client['nickname']:
                    print(nickname + ' sending a message to ' + client['nickname'] +'!')
                    client['socket'].send(bytes('DACHAT' + str(json.dumps({'response' : 'message', 'from' : nickname, 'message' : data['message']})), 'utf-8'))
                    userFound = True
                    break
            if not userFound :
                client_socket.send(bytes('DACHAT'+str(json.dumps({'response' : 'message', 'from' : 'SYSTEM', 'message' : 'ERROR: User ' + data['target'] + ' not found!'})),'utf-8'))


#data in bytes, return dict if the received data were accepted, else None
def checkData(data):

    data = str(data,'utf-8')

    if data[:6] != 'DACHAT':
        print('$- Denied request: ' , data)
        return None

    print('$- Received: ', data)

    data = data[6:]

    data = json.loads(data)

    return data




while True:

    client, addr = server.accept()

    print('Accepted connection from: {}:{}'.format(addr[0], addr[1]))

    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
