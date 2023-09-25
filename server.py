import socket, sys
from _thread import *
from framework import * 
import pickle

server = "192.168.100.58"
port = 4445 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try: 
    s.bind((server, port))
except Exception as e:
    print(str(e))

s.listen(2)
print("Waiting for connection, Server started at ", server, ":", str(port))


DEFAULT = [Player(SCREEN_SIZE[0]/4, SCREEN_SIZE[1]/2, "res/robot.png"), Player(SCREEN_SIZE[0]/4 + SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2, "res/robot_two.png")]
players = [Player(SCREEN_SIZE[0]/4, SCREEN_SIZE[1]/2, "res/robot.png"), Player(SCREEN_SIZE[0]/4 + SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2, "res/robot_two.png")]

def threaded_client(client, current_player):
    client.send(pickle.dumps(players[current_player]))
    reply = ""
    while 1:
        try:
            data = pickle.loads(client.recv(4096*20))
            players[current_player] = data

            if not data:
                print("Diconnected")
                break
            else:
                if current_player == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                # print("Received: ", data)
                # print("Sending: ", reply)
            client.sendall(pickle.dumps(reply))
        except Exception as e:
            print(str(e))
            break
    print("Lost connect")
    client.close()

current_player = 0
while 1:
    client, addr = s.accept() 
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (client, current_player))
    current_player += 1

