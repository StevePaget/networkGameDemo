import socket
import pickle, time, random
import threading

class GameState:
    def __init__(self):
        self.board = [[None,None,None],
                 [None,None,None],
                 [None,None,None]]
        self.currentPlayerNum = 0
        self.running = [True,True]
        self.turntaken = False
        self.winner = None

# wait for connections, send a player number
server = "192.168.178.23"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

def threaded_client(conn, game,pnum):
    while game.running == [True,True]:
            try:
                conn.send(pickle.dumps(game))
                receivedgame = pickle.loads(conn.recv(2048*4))
                if not receivedgame:
                    print("Disconnected")
                    game.running[pnum] = False
                else:
                    if game.currentPlayerNum == pnum: # it's this player
                        if receivedgame.turntaken: # turn taken
                            # check for win
                            print("move made")
                            # update local game board
                            game.board = receivedgame.board[:]
                            winner = checkWin(game.board)
                            if winner is not None:
                                print(winner, "wins")
                                game.winner = winner
                                game.running[pnum] = False
                                conn.send(pickle.dumps(game))
                            else:
                                # swap players
                                game.currentPlayerNum = (game.currentPlayerNum+1)%2
                    elif game.winner is not None:
                        game.running[pnum] = False
                        conn.send(pickle.dumps(game))

            except Exception as e:
                print(e)
                print("connection failed")
                game.running[pnum] = False
    print("Ended", pnum)
    if game.running[pnum]:
        game.currentPlayerNum = -1               
        conn.send(pickle.dumps(game))    

def checkWin(board):
    spaces = 0
    for i in range(3):
        if board[i][0] == board[i][1] and board[i][1] == board[i][2]:
            return board[i][0]
        if board[0][i] == board[1][i] and board[1][i] == board[2][i]:
            return board[0][i]
        spaces += board[i].count(None)
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
            return board[0][0]
    if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
            return board[1][1]
    if spaces == 0:
         return 99
    return None

while True:
    # this keeps running, waiting for 2 players to join
    # when the game ends, it repeats
    print("New Game")
    game = GameState()
    players = [0,1]
    random.shuffle(players) # randomise who gets x or o
    s.listen(2)
    print("Waiting for a connection, Server Started")
    for i in range(2):
        pnum = players[i]
        conn, addr = s.accept()
        print("Connected to:", addr)
        conn.send(str.encode(str(pnum)))  # send them their player number, 0 or 1
        # now start a thread which will handle this player's network connection
        threading.Thread(target=threaded_client, args = (conn, game,pnum)).start()
    print("both players connected")

    while game is not None and game.running == [True, True]:
        # keep going while the players are still playing
        print("Game running")
    print("player disconnected")          
            

print("Ended")