import socket
from threading import Thread

nickname = input("Enter your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "192.0.0.1"
port = 5000
client.connect((ip, port))

print("Connected with the server")

def receive():
    while True:
        try:
            msg = client.recv(2048).decode("utf-8")
            if msg == "nickname":
                client.send(nickname.encode("utf-8"))
            else:
                print(msg)
        except:
            print("error")
            client.close()
            
            break

def write():
    while True:
        msg = nickname + ": " + input("")
        client.send(msg.encode("utf-8"))

thread1 = Thread(target = receive)
thread1.start()
thread2 = Thread(target = write)
thread2.start()