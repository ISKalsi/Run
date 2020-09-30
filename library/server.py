import socket
import threading
import json

HEADER = 1
FORMAT = 'utf-8'
PORT = 7777
# SERVER = socket.gethostbyname(socket.gethostname())
SERVER = '192.168.29.32'
ADDR = (SERVER, PORT)

clientList = {"count": 0, "id": [], "players": {}}
disconnected = {}
available = [i for i in range(4)]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


class State:
    idle, active, jump = range(3)
    full, disconnected, exit = range(-3, 0)


def send(conn):
    jsonObj = json.dumps(clientList)
    conn.send(jsonObj.encode(FORMAT))


def handleClient(conn, addr):
    ID: int = -1
    ip = addr[0]

    if ip in disconnected:
        print(f"\n[RECONNECTED] {ip}")
        ID = disconnected[ip]
        del disconnected[ip]
    elif available:
        print(f"[NEW CONNECTION] {addr}")

        ID = available[0]
        # noinspection PyTypeChecker
        clientList["id"].append(ID)
        clientList["count"] += 1
    else:
        clientList["id"].append(ID)
        send(conn)
        conn.close()
        return

    clientList["players"][ID] = State.idle
    send(conn)

    while True:
        # noinspection PyBroadException
        try:
            msg = conn.recv(1024)

            if msg:
                current = json.loads(msg.decode(FORMAT))
                if current == State.exit:
                    print("[Player ID: ", ID, "] Exit.", sep='')
                    # noinspection PyTypeChecker
                    del clientList["players"][ID]
                    clientList["id"].remove(ID)
                    available.append(ID)
                    clientList["count"] -= 1

                    conn.close()
                    print("[CONNECTION CLOSED]\n")
                    return
                elif current == State.disconnected:
                    break
                # noinspection PyTypeChecker
                clientList["players"][ID] = current

            send(conn)

        except socket.error as e:
            print("(Server Side) ", e)
            break
        except json.decoder.JSONDecodeError as e:
            print("(Server Side) ", e)
        except:
            print("(Server Side) some other shit")

    disconnected[ip] = ID
    print("[Player ID: ", ID, "] Disconnect.", sep='')
    conn.close()


def start():
    server.listen()
    print("[LISTENING ON] ", SERVER)
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handleClient, args=(conn, addr))
        thread.start()
        print("\n[ACTIVE CONNECTIONS] ", threading.activeCount() - 1)


print("[STARTING SERVER]...")
start()
