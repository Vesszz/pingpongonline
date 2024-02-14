import socket
import threading
import time

host = "0.0.0.0"

def accessNewClients(server):
    global users
    while True:
        user, adress = server.accept()
        ip = str(adress).replace("(","").replace(")","").replace("'","").split(",")[0]
        users[user] = ip
        user.send( ("Server: Hi "+ip+", we are connected!").encode("utf-8"))
        threading.Thread(target=receive, args=(user,), daemon=True).start()

def receive(user):
    while True:
        data = user.recv(1024)
        

def start_client(host: str, port: int):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((host, port))
    threading.Thread(target=receive, args=(client,), daemon=True).start()
    client.send("I am connected!".encode("utf-8"))
    while True:
        client.send(input().encode("utf-8"))

{
  "packet": {
    "type": "CONNECTION",
    "message": "LOGIN"
  }
}


if __name__ == "__main__":
    start_client(host, 34543)