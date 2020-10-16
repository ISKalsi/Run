import socket
import json
import threading
import pygame
import sys
from library.constants import State


class Client:
    # SERVER = socket.gethostbyname(socket.gethostname())
    SERVER = '192.168.29.59'
    PORT = 7777
    ADDR = (SERVER, PORT)
    FORMAT = 'utf-8'
    HEADER = 1000
    clientList = {}

    def __init__(self, Player, clientList, ID):
        self.Player = Player
        self.currentState = State.idle

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

    def __del__(self):
        self.currentState = State.disconnected
        if self.isClient and self.id != -1:
            del Client.clientList["players"][f"{self.id}"]
            Client.clientList["count"] -= 1


def handleServer(client):
    sock = client.sock

    try:
        clientList = sock.recv(client.HEADER).decode(client.FORMAT)
        C, ID = Client.clientList, client.id = json.loads(clientList)

        if ID == -1:
            sock.close()
            return

    except socket.error as e:
        print("Arre? Starting mei hi error?! ", e)

    while "Ground" not in client.__dict__:
        pass

    client.Ground.scroll = client.clientList["players"][f"{client.id}"][1]

    try:
        while True:
            jsonObj = json.dumps((client.currentState, client.Ground.scroll))
            sock.send(jsonObj.encode(Client.FORMAT))

            if not pygame.display.get_active():
                client.currentState = State.disconnected

            if client.currentState == State.disconnected or client.currentState == State.exit:
                jsonByteObj = json.dumps((client.currentState, client.Ground.scroll)).encode(Client.FORMAT)
                sock.send(jsonByteObj + (client.HEADER - sys.getsizeof(jsonByteObj)) * b' ')
                sock.recv(10)
                break
            else:
                clientList = sock.recv(client.HEADER).decode(client.FORMAT)
                if clientList:
                    Client.clientList = json.loads(clientList)[0]
    except socket.error as e:
        print("(Client Side) ", e)
    except Exception as e:
        print("(Client Side) ", e)

    print("Disconnected Client: ", client.id)
    sock.close()
