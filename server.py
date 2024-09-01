import socket
import pickle, random, sys
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
    # This procedure keeps running as long as both players are still running.
    # There are two copies of this thread running simultaneously.
    # Each thread handles the communication with a single player.
    while game.running == [True,True]:
            try:
                # first, we send the current game state to the player client
                conn.send(pickle.dumps(game))
                # we receive back a response from the player client
                receivedgame = pickle.loads(conn.recv(256))
                # if we got back a None object, they must have disconnected
                if not receivedgame:
                    print("Disconnected")
                    game.running[pnum] = False
                else:
                    # we check the currentPlayerNum attribute of the game object
                    if game.currentPlayerNum == pnum: # it's this player
                        # We check to see if the player client has completed their turn
                        # and they're ready to pass to the next player
                        if receivedgame.turntaken: 
                            # Copy the board state in the received gamestate
                            # and update local game board.
                            game.board = receivedgame.board[:]
                            # check to see if either player has won the game
                            winner = checkWin(game.board)
                            if winner is not None:
                                print(winner, "wins")
                                game.winner = winner
                                game.running[pnum] = False
                                conn.send(pickle.dumps(game))
                            else:
                                # There's no winner, so swap players
                                game.currentPlayerNum = (game.currentPlayerNum+1)%2
                    elif game.winner is not None:
                        # In this case, it is not this player's turn
                        # but either someone has won the game or it's a draw
                        game.running[pnum] = False
                        # we will send them the updated gamestate to confirm the
                        # end of the game
                        conn.send(pickle.dumps(game))

            except Exception as e: # Probably some sort of network error
                print(e)
                print("connection failed")
                game.running[pnum] = False
    print("Ended", pnum)
    # The next section occurs if this player is still connected, but the other player
    # has disconnected. In which case we tell this player to shut down mid-game
    if game.running[pnum]:
        game.currentPlayerNum = -1               
        conn.send(pickle.dumps(game))    

def checkWin(board):
    # This is specific to noughts and crosses.
    # The server determines if someone has won the game
    spaces = 0
    for i in range(3):
        #check the three columns for matching symbols
        if board[i][0] is not None and board[i][0] == board[i][1] and board[i][1] == board[i][2]:
            return board[i][0]
        #check the three rows for matching symbols
        if board[0][i] is not None and board[0][i] == board[1][i] and board[1][i] == board[2][i]:
            return board[0][i]
        spaces += board[i].count(None) # count how many spaces are on this row
    # check the two diagonals
    if board[0][0] is not None and board[0][0] == board[1][1] and board[1][1] == board[2][2]:
            return board[0][0]
    if board[0][2] is not None and board[0][2] == board[1][1] and board[1][1] == board[2][0]:
            return board[1][1]
    # there are no remaining spaces in the board, so it's a draw
    if spaces == 0:
         return 99
    return None

while True:
    # this keeps running, waiting for 2 players to join
    # when the game ends, it repeats
    print("New Game")
    game = GameState()
    print("A gamestate is", sys.getsizeof(game), "bytes")
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