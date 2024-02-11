import socket
import threading
import time

host = "0.0.0.0"
users = {}

def accessNewClients(server):
    global users
    while True:
        user, adress = server.accept()
        ip = str(adress).replace("(","").replace(")","").replace("'","").split(",")[0]
        users[user] = ip
        user.send( ("Server: Hi "+ip+", we are connected!").encode("utf-8"))
        threading.Thread(target=receive, args=(user,), daemon=True).start()

def receive(user):
    global users
    while True:
        data = user.recv(1024)
        print(users[user]+": " + data.decode("utf-8"))
        for i in users.keys():
            if i != user:
                i.send(     (str(users[user])+ ": " + data.decode("utf-8")).encode("utf-8")       )


def waitForClient():
    global users
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, 13000))
    server.listen()
    print("Server is ready")
    user, adress = server.accept()
    ip = str(adress).replace("(","").replace(")","").replace("'","").split(",")[0]
    users[user] = ip
    user.send( ("Server: Hi "+ip+", we are connected").encode("utf-8"))
    threading.Thread(target=receive, args=(user,), daemon=True).start()
    threading.Thread(target=accessNewClients, args=(server,), daemon=True).start()
    while True:
        data = input()
        for i in users.keys():
            i.send( ("Server: "+ data).encode("utf-8"))

if __name__ == "__main__":
    waitForClient()