import socket
import threading
import random

rooms = []
codec = "utf-8"
'''
Packets
CONNECTION;name
CREATE;uid;password
JOIN;uid;password
'''

class Player:
    def __init__(self, connection, ip: str, name: str):
        self.connection = connection
        self.ip = ip
        self.name = name
        self.uid = hex(random.randint(0,1048576))[2:] # 2**20

    def __str__(self):
        return self.name


#Класс Комнаты, содержит инфу о игроках(игроке), уникальный(случайный) айди комнаты
class Room:
    def __init__(self, player_1: Player, uid: str, password: str):
        self.player_1 = player_1
        if uid == "": self.uid = hex(random.randint(0,1048576))[2:] # 2**20
        else: self.uid = uid
        self.password = password

    def __str__(self):
        if hasattr(self, "player_2"): return (str(self.player_1)+" "+str(self.player_2)+" "+str(self.uid))
        else: return (str(self.player_1)+" "+str(self.uid))

    def connect_player(self, player_2: Player):
        if hasattr(self, "player_2"): return 0
        else: self.player_2 = player_2

# Возвращает клиенту ошибку при всяко-разных ошибках 
def return_error(connection, mistake: str = "Unknown error"):
    connection.send(mistake.encode(codec))

def array_to_string(array):
    s = ""
    if len(s) == 0 : return ""
    for i in range(len(array)):
        if i == len(array)-1: s += str(i)
        else: s += str(i) + "\n"
    return s

def recv_send_room(room, player):
    while True:
        data = player.connection.recv(1024).decode(codec)
        if not data: print("Unknown mistake")
        if data not in ["w","s"]: continue
        if data == "rooms": player.connection.send(array_to_string(rooms).encode(codec))
        else:
            if room.player_1 != player: room.player_1.connection.send(data.encode(codec))
            elif room.player_2 != player: room.player_2.connection.send(data.encode(codec))

def handle_room(room):
    threading.Thread(target=recv_send_room, args=(room, room.player_1), daemon=False).start()
    threading.Thread(target=recv_send_room, args=(room, room.player_2), daemon=False).start()

def create_room(player, room_uid, room_password):
    new_room = Room(player, room_uid, room_password)
    rooms.append(new_room)
    print(new_room)

def join_room(player, room_uid, room_password):
    print(array_to_string(rooms))
    for room in rooms:
        if room.uid == room_uid and room.password == room_password: 
            room.connect_player(player)
            print(room)
            handle_room(room)
            break
    else:
        return_error(player.connection, "Invalid room ID")
        handle_room_connections(player)


def handle_room_connections(player):
    data = player.connection.recv(1024).decode(codec).split(";")
    if not data:
        return_error(player.connection)
        handle_room_connections(player)
        return 0
    if len(data) != 3 : 
        return_error(player.connection)
        handle_room_connections(player)
        return 0
    type = data[0]
    room_uid = data[1]
    room_password = data[2]
    if type == "CREATE": create_room(player, room_uid, room_password)
    elif type == "JOIN": join_room(player, room_uid, room_password)
    else: 
        return_error(player.connection)
        handle_room_connections(player)

# Здесь клиент и сервер коннектятся и инициализируется игрок
def connect_to_server(server):
    server.listen()
    connection, adress = server.accept()
    threading.Thread(target=connect_to_server, args=(server,), daemon=False).start()
    data = connection.recv(1024).decode(codec).split(';')
    if len(data) != 2 : return_error(connection, "Don't use ; in your name")
    type = data[0]
    message = data[1]
    if type == "CONNECTION": 
        connection.send(array_to_string(rooms).encode(codec))
        connection.send("You are connected".encode(codec))
        player_connected = Player(connection, adress[0], message)
        handle_room_connections(player_connected)
    else: return_error(connection, "You haven't connected yet")

def start_server(port: int):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    print("Server is listening")
    connect_to_server(server)


if __name__ == "__main__":
    start_server(34543) # port