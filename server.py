import socket
import threading
import time
import random

Rooms = []

#Проверка валидности ipv4
def validate_ipv4(ip):
    parts = ip.split('.')
    if len(parts) !=  4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        num = int(part)
        if num <  0 or num >  255:
            return False
    return True

class Player:
    def __init__(self, connection, ip: str, name: str):
        if not validate_ipv4(ip): raise ValueError("Not valid ip")
        self.connection = connection
        self.ip = ip
        self.name = name

    def __str__(self):
        return str(self.ip) + " " + str(self.name)


#Класс Комнаты, содержит инфу о игроках, уникальный(случайный) айди комнаты
class Room:
    def __init__(self, player_1: Player, player_2: Player):
        #if player_1.ip == player_2.ip: raise ValueError("You can't connect two same players")
        self.player_1 = player_1
        self.player_2 = player_2
        self.uid = hex(random.randint(0,1048576))[2:] # 2**20

    def __str__(self):
        return (str(self.player_1_ip)+" "+str(self.player_2_ip)+" "+str(self.uid))


    #def draw_rect(self):
    #    pyray.draw_rectangle(self.pos_x, self.pos_y, self.width, self.height, self.color)


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

def start_server(port: int):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen()
    print("Server is ready")
    connection, adress = server.accept()

if __name__ == "__main__":
    start_server(34543)