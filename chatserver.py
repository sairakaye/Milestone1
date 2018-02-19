from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accepting_clients():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Mukha mo! Type mo pangalan mo tapos enter. Type ka ba?", "utf8"))
        addresses[client] = client_address
        Thread(target=handling, args=(client,)).start()


def handling(client):
    name = client.recv(1024).decode("utf8")
    client.send(bytes('Welcome %s! If you ever want to quit, mama mo. Mag-\'q\' ka lang para umalis.' % name, "utf8"))
    joined_message = "%s has joined the chat! YAAAAAAAS." % name
    broadcast(bytes(joined_message, "utf8"))
    clients[client] = name

    while True:
        message = client.recv(1024)
        if message != bytes("q", "utf8"):
            broadcast(message, name + ": ")
            print(name + " (%s:%s)" % addresses[client] + ": " + message.decode("utf8"))
        else:
            client.send(bytes("q", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break

def broadcast(message, prefix=""):
    for s in clients:
        s.send(bytes(prefix, "utf8") + message)


clients = {}
addresses = {}

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