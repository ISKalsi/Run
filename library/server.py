import socket
import threading
import json
import sys
from library.constants import State

HEADER = 1000
FORMAT = 'utf-8'
PORT = 7777
# SERVER = socket.gethostbyname(socket.gethostname())
SERVER = '192.168.29.59'
ADDR = (SERVER, PORT)

clientList = {"count": 0, "id": [], "players": {}}
disconnected = {}
available = ([i for i in range(4)])
available.reverse()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handleClient(conn, addr):
    def send(*args):
        jsonByteObj = json.dumps((clientList, *args)).encode(FORMAT)
        conn.send(jsonByteObj + (HEADER - sys.getsizeof(jsonByteObj)) * b' ')

    ID: int = -1
    ip = addr[0]

    if ip in disconnected:
        print(f"\n[RECONNECTED] {ip}")
        ID, score = disconnected[ip]
        del disconnected[ip]
    elif available:
        print(f"[NEW CONNECTION] {addr}")

        ID = available.pop()
        # noinspection PyTypeChecker
        clientList["id"].append(ID)
        clientList["id"].sort(reverse=True)
        clientList["count"] += 1
        score = 0
    else:
        send(ID)
        conn.close()
        return

    clientList["players"][ID] = (State.idle, score)
    send(ID)

    while True:
        # noinspection PyBroadException
        try:
            msg = conn.recv(HEADER)

            if msg:
                current, score = json.loads(msg.decode(FORMAT))
                if current == State.exit:
                    conn.send(b"0")
                    conn.close()

                    print("[Player ID: ", ID, "] Exit.", sep='')
                    # noinspection PyTypeChecker
                    del clientList["players"][ID]
                    clientList["id"].remove(ID)
                    available.append(ID)
                    clientList["id"].sort(reverse=True)
                    clientList["count"] -= 1

                    print("[CONNECTION CLOSED]\n")
                    return
                elif current == State.disconnected:
                    break
                # noinspection PyTypeChecker
                clientList["players"][ID] = (current, score)

            send()

        except socket.error as e:
            print("(Server Side) SOCKET: ", e)
            break
        except json.decoder.JSONDecodeError as e:
            print("(Server Side) JSON: ", e)
        except Exception as e:
            print("(Server Side) some other shit", e)

    clientList["players"][ID] = (State.disconnected, score)
    disconnected[ip] = (ID, score)
    print("[Player ID: ", ID, "] Disconnect.", sep='')
    conn.close()


def start():
    try:
        server.listen()
        print("[LISTENING ON] ", SERVER)
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handleClient, args=(conn, addr))
            thread.start()
            print("\n[ACTIVE CONNECTIONS] ", threading.activeCount() - 1)
    except socket.error as e:
        print("(Server Side)", e)
    except KeyboardInterrupt:
        server.close()
        print("[SERVER CLOSED]")


print("[STARTING SERVER]...")
start()
