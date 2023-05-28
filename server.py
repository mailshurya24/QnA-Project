import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "192.0.0.1"
port = 5000
server.bind((ip, port))
server.listen()

clients = []

questions = [
    "What is the Italian word for Pie: \n a.Pasta \n b.Pizza",
    "Water boils at what temperature: \n a.100C \n b.500C",
    "Who is Loki: \n a.God of Mischief \n b.God of Thunder"
]

answers  = ["b.", "a.", "a."]

def randomQA(conn):
    randIndex = random.randint(0, len(questions) - 1)
    randQ = questions[randIndex]
    randA = answers[randIndex]
    conn.send(randQ.encode("utf-8"))
    return randIndex, randQ, randA

def removeQ(index):
    questions.pop(index)
    answers.pop(index)

def removeClients(c):
    if c in clients:
        clients.remove(c)

def broadcast(m, c):
    for i in clients:
        if i != c:
            try:
                i.send(m.encode("utf-8"))
            except:
                removeClients(i)

def clientThread(conn):
    score = 0
    conn.send("Welcome to the quiz!".encode("utf-8"))
    conn.send("You will receive a question. Choose the correct option!".encode("utf-8"))
    conn.send("Good Luck!\n\n".encode("utf-8"))
    
    index, question, answer = randomQA(conn)

    while True:
        try:
            message = conn.recv(2048).encode("utf-8")

            if message:
                if message.lower() == answer:
                    score += 1
                    conn.send(f"Bravo, your current score is {score}\n\n!".encode("utf-8"))
                else:
                    conn.send("Incorrect answer, better luck next time! \n\n".encode("utf-8"))
                
                removeQ(index)
                index, question, answer = randomQA(conn)
            else:
                clients.remove(conn)
        except:
                continue
        
while True:
    conn, addr = server.accept()
    conn.send(addr)
    clients.append(conn)
    msg = addr + " joined."
    print(msg)
    broadcast(msg, conn)

    thread1 = Thread(target = clientThread(), args = (conn, addr))
    thread1.start()