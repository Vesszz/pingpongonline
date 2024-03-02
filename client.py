import socket
import threading
import time
import json

host = "0.0.0.0"

'''
Packets
CONNECTION;name
CREATE;uid;password
JOIN;uid;password
'''


def receive(client):
    while True:
        data = client.recv(1024).decode("utf-8")
        print(data)
        

def start_client(host: str, port: int):
    
    name = input().replace(';',"")
    packet = "CONNECTION;"+str(name)
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((host, port))
    client.send(packet.encode("utf-8"))
    rooms = client.recv(1024).decode("utf-8")
    if rooms == "": print("No rooms available")
    else: print(rooms)
    threading.Thread(target=receive, args=(client,), daemon=False).start()
    #print(client.recv(1024).decode("utf-8"))
    while True:
        packet=input()
        client.send(packet.encode("utf-8"))
    #packet = "CREATE;"
    #client.send(packet.encode("utf-8"))
    #while True:
    #    client.send(input().encode("utf-8"))


    



if __name__ == "__main__":
    start_client("127.0.0.1", 34543)