import socket
import threading
import json

HEADER = 1
FORMAT = 'utf-8'
PORT = 7777
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

clientList = {"count": 0, "operation": 0}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


class State:
    new, idle, active, jump = range(4)
    exit = -1
    disconnected = -2


def send(conn):
    jsonObj = json.dumps(clientList)
    conn.send(jsonObj.encode(FORMAT))


def handleClient(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")

    i = clientList["count"]
    # noinspection PyTypeChecker
    clientList[i] = (i, State.idle, True)
    clientList["operation"] = 1
    clientList["count"] += 1
    send(conn)

    while True:
        try:
            msg = conn.recv(1024)

            if msg:
                player = json.loads(msg.decode(FORMAT))
                if player[1] == State.exit or player[1] == State.disconnected:
                    break
                elif player[1] == State.new:
                    continue

                # noinspection PyTypeChecker
                clientList[player[0]] = (player[0], player[1], player[2])

            send(conn)

        except socket.error as e:
            print("(Server Side) ", e)
            break

    # noinspection PyTypeChecker
    del clientList[i]
    clientList["count"] -= 1

    conn.close()
    print("[CONNECTION CLOSED]\n")


def start():
    server.listen()
    print("[LISTENING ON] ", SERVER)
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handleClient, args=(conn, addr))
        thread.start()
        print("\n[ACTIVE CONNECTIONS] ", threading.activeCount()-1)


print("[STARTING SERVER]...")
start()
