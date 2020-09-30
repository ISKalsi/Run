import socket
import json
import threading
import pygame


class Client:
    SERVER = socket.gethostbyname(socket.gethostname())
    # SERVER = '192.168.29.59'
    PORT = 7777
    ADDR = (SERVER, PORT)
    FORMAT = 'utf-8'
    clientList = {}

    class State:
        new, idle, active, jump = range(4)
        exit = -1
        disconnected = -2

    def __init__(self, Player, clientList, ID):
        self.Player = Player
        if ID is None:
            self.isClient = True
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(Client.ADDR)

            self.id = None

            self.thread = threading.Thread(target=handleServer, args=(self,))
            self.thread.start()
        else:
            self.isClient = False
            Client.clientList = clientList
            self.id = ID

        self.current = self.State.idle

    @property
    def currentState(self):
        return self.current

    @currentState.setter
    def currentState(self, new):
        self.current = new

    def __del__(self):
        self.currentState = self.State.disconnected
        if self.isClient:
            del Client.clientList[f"{self.id}"]
            Client.clientList["count"] -= 1


def handleServer(client):
    sock = client.sock

    clientList = sock.recv(2048).decode(client.FORMAT)
    Client.clientList = json.loads(clientList)

    client.id = Client.clientList["count"] - 1
    info = (client.id, client.current, True)

    while True:
        jsonObj = json.dumps(info)
        sock.send(jsonObj.encode(Client.FORMAT))

        if client.current == client.State.disconnected or client.current == client.State.exit or not pygame.display.get_active():
            break
        else:
            clientList = sock.recv(2048).decode(client.FORMAT)
            if clientList:
                Client.clientList = json.loads(clientList)

        info = (client.id, client.currentState, True)

    print("Disconnected Client: ", client.id)
    sock.close()
