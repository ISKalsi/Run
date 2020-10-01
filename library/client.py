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
        full, disconnected, exit = range(-3, 0)

    def __init__(self, Player, clientList, ID):
        self.Player = Player
        self.currentState = self.State.idle

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
        self.currentState = self.State.disconnected
        if self.isClient:
            del Client.clientList["players"][f"{self.id}"]
            Client.clientList["count"] -= 1


def handleServer(client):
    sock = client.sock

    try:
        clientList = sock.recv(1024).decode(client.FORMAT)
        C, ID = Client.clientList, client.id = json.loads(clientList)

        if ID == -1:
            print("Game full. Exiting...")
            sock.close()
            return

    except socket.error as e:
        print("Arre? Starting mei hi error?! ", e)

    try:
        while True:
            jsonObj = json.dumps(client.currentState)
            sock.send(jsonObj.encode(Client.FORMAT))

            if not pygame.display.get_active():
                client.currentState = client.State.disconnected

            if client.currentState == client.State.disconnected or client.currentState == client.State.exit:
                jsonObj = json.dumps(client.currentState)
                sock.send(jsonObj.encode(Client.FORMAT))
                break
            else:
                clientList = sock.recv(1024).decode(client.FORMAT)
                if clientList:
                    Client.clientList = json.loads(clientList)[0]
    except socket.error as e:
        print("(Client Side) ", e)

    print("Disconnected Client: ", client.id)
    sock.close()
