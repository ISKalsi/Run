import socket
import json


class Client:
    SERVER = socket.gethostbyname(socket.gethostname())
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
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(Client.ADDR)
            self._recv()

            self.id = Client.clientList["count"] - 1
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
        if self.isClient:
            self._send((self.id, new, True))
            self._recv()

    def _send(self, info):
        jsonObj = json.dumps(info)
        self.client.send(jsonObj.encode(Client.FORMAT))

        if self.current == self.State.disconnected:
            print("Disconnected Client: ", self.id)
        elif self.current == self.State.exit:
            print("Exit Client: ", self.id)
        else:
            self._recv()

    def _recv(self):
        clientList = self.client.recv(2048).decode(self.FORMAT)
        if clientList:
            Client.clientList = json.loads(clientList)

    def __del__(self):
        self.currentState = self.State.disconnected
        Client.clientList["count"] -= 1
