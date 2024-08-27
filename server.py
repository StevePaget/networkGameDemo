import socket
import pickle, time
from _thread import *

class Game:
    def __init__(self):
        board = [["","",""],
                 ["","",""],
                 ["","",""]]
        currentPlayer = 0
        status = 0

game = Game()

# wait for connections, send a player number
server = "192.168.178.23"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

def threaded_client(conn, game,pnum):
    reply = ""
    while game.status != -1:
            conn.send(pickle.dumps(game))
            try:
                 receivedgame = pickle.loads(conn.recv(2048*4))
            except:
                 print("connection failed")
                 game.status = -1
            if not receivedgame:
                print("Disconnected")
                game.status = -1
            else:
                if game.currentPlayerNum == pnum:
                    if receivedgame.status == 4: # turn taken
                        # check for win
                        
                        # update local game board
                        # swap players
                        game.currentPlayerNum = (game.currentPlayerNum+1)%2
    print("Lost connection")
    conn.close()

s.listen(2)
connections = []
print("Waiting for a connection, Server Started")
pnum = 0
while pnum<2:
    conn, addr = s.accept()
    connections.append(conn)
    print("Connected to:", addr)
    conn.send(str.encode(str(pnum)))
    start_new_thread(threaded_client, (conn, game,pnum))
    pnum += 1
print("both players connected")

while game.status not in [-1,5]:
    print("Game running")
    time.sleep(1)

print("Ended")