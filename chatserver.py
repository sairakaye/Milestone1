from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accepting_clients():
    while True:
        client, client_address = SERVER.accept()
        client.send(bytes("You have connected to the chat room", "utf8"))
        addresses[client] = client_address
        Thread(target=handling, args=(client,)).start()


# Function that gets all names of the clients
def all_clients():
    global client_names
    client_names = "Active Users: "

    for names in usernames:
        if names not in client_names:
            client_names = client_names + names + ","


def handling(client):
    global client_names
    name = client.recv(1024).decode("utf8")
    # for each socket in clients
    for s in clients:
        # continuously accept username inputs while the name is taken
        while clients[s] == name:
            client.send(bytes('Username is already taken, Please enter another.', "utf8"))
            name = client.recv(1024).decode("utf8")

    client.send(bytes('Welcome %s! If you ever want to quit, input -\'q\'.' % name, "utf8"))
    joined_message = "%s has joined the chat!" % name

    # broadcast the joined message to the global chat room
    broadcast(bytes(joined_message, "utf8"))
    clients[client] = name
    usernames.append(name)

    while True:
        all_clients()
        ''' 
        Check if message is not q, 
        If no,
            Check if the message has "@" in front. 
            If yes, it will be sent as a private message. 
            Otherwise, it will be sent as a global message
        Otherwise,
            Close the client
            Delete it from the list of sockets
        '''
        client.send(bytes(client_names, "utf8"))
        message = client.recv(1024)
        if message != bytes("q", "utf8"):
            if bytes("@","utf8") in message:
                dest = message.decode("utf8") # decode message
                mes = dest # assign message to another var
                mes = mes[mes.find(" ")+1:] # fix sent message to remove @
                mes = bytes(mes, "utf8") # convert fixed message to bytes
                dest = dest[1:] # get name to be sent to
                dest = dest[:dest.find(" ")] # find the space
                for s in clients: # search clients dictionary to know address
                    if clients[s] == dest or clients[s] == name:
                        privateMessage(mes, s, name + ": ")
                        print(name + "(%s:%s)" % addresses[client] + ": " + message.decode("utf8"))
            else:
                broadcast(message, name + ": ")
                print(name + " (%s:%s)" % addresses[client] + ": " + message.decode("utf8"))
        else:
            client.close()
            print("Connection %s:%s is disconnected." % addresses[client])
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            usernames.remove(name)
            break


def broadcast(message, prefix=""):
    for s in clients:
        s.send(bytes(prefix, "utf8") + message)


def privateMessage(message, name, prefix=""):
    name.send(bytes(prefix, "utf8") + message)


clients = {} # dictionary of names, with socket address as the key
addresses = {} # dictionary of client addresses with client address as the key
usernames = [] # list of usernames
client_names = ""
name = ""

HOST = '127.0.0.1'
PORT = 49152
ADDRESS = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDRESS)

if __name__ == "__main__":
    SERVER.listen(5)
    print("The server is now active!")
    print("Server Address: %s:%s" % ADDRESS)
    ACCEPTING_T = Thread(target=accepting_clients)
    ACCEPTING_T.start()
    ACCEPTING_T.join()
    SERVER.close()