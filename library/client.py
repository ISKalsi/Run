import socket
import json
import threading
import pygame


class Client:
    # SERVER = socket.gethostbyname(socket.gethostname())
    SERVER = '192.168.29.32'
    PORT = 7777
    ADDR = (SERVER, PORT)
    FORMAT = 'utf-8'
    clientList = {}

    class State:
        idle, active, jump = range(3)
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

    try:
        clientList = sock.recv(2048).decode(client.FORMAT)
        Client.clientList = json.loads(clientList)
    except socket.error as e:
        print("Arre? Starting mei hi error?! ", e)

    client.id = Client.clientList["count"] - 1
    info = (client.id, client.current, True)

    try:
        while True:
            jsonObj = json.dumps(info)
            sock.send(jsonObj.encode(Client.FORMAT))

            if client.current == client.State.disconnected or client.current == client.State.exit or not pygame.display.get_active():
                info = (client.id, client.currentState, True)
                jsonObj = json.dumps(info)
                sock.send(jsonObj.encode(Client.FORMAT))
                break
            else:
                clientList = sock.recv(1024).decode(client.FORMAT)
                if clientList:
                    Client.clientList = json.loads(clientList)

            info = (client.id, client.currentState, True)
    except socket.error as e:
        print("(Client Side) ", e)

    print("Disconnected Client: ", client.id)
    sock.close()
