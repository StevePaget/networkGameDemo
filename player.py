from pygame_functions import *
from network import Network
import threading

screenSize(900,900)
setBackgroundColour("#3C047C")
setAutoUpdate(False)
playerLabel = makeLabel("Player: ",42,10,700,"white")
showLabel(playerLabel)
infoLabel = makeLabel("Waiting for your turn",42,10,750,"white")
showLabel(infoLabel)

class GameState:
    def __init__(self):
        self.board = [[None,None,None],
                 [None,None,None],
                 [None,None,None]]
        self.currentPlayerNum = 0
        self.running = [True,True]
        self.turntaken = False
        self.winner = None

class Game:
    def __init__(self):
        self.board = [[None,None,None],
                 [None,None,None],
                 [None,None,None]]
        #  status values:  0=wait,  1=playing, 2=start of turn, 9=done
        self.status = 2
        self.running = True
        self.connect() # connects to network and fires up houseKeeping thread
        self.displayBoard()
        self.playGame()

    
    def playGame(self):
        changeLabel(infoLabel,"Waiting for your turn")
        while self.running:
            updateDisplay()
            if self.status == 1:
                self.playerTurn()
            elif self.status == 8:
                self.displayBoard()
                updateDisplay()
                pause(1000)
                self.running = False
            elif self.status == -1:
                print("Shutdown signal received")
                pygame.quit()
                sys.exit()
            
            tick(100)
        updateDisplay()


    def displayBoard(self):
        clearShapes()
        # draw lines for the grid
        drawLine(250,50,250,650,"white",5)
        drawLine(450,50,450,650,"white",5)
        drawLine(50,250,650,250,"white",5)
        drawLine(50,450,650,450,"white",5)
        x = 150
        y = 150
        # go through each row of the board array
        for row in self.board:
            for symbol in row:
                if symbol == 1: # draw a cross
                    drawLine(x-75,y-75,x+75,y+75,"white",5)
                    drawLine(x-75,y+75,x+75,y-75,"white",5)
                elif symbol == 0: # draw a circle
                    drawEllipse(x,y,150,150,"white",5)
                x += 200
            x=150
            y+=200
        if self.thisPlayerNum == 0:
            changeLabel(playerLabel, "You are Noughts")
        elif self.thisPlayerNum == 1:
            changeLabel(playerLabel, "You are Crosses")



    def playerTurn(self):
        # player makes their go
        changeLabel(infoLabel, "It's your turn - click a square")
        updateDisplay()
        validMoveMade = False
        while not validMoveMade and self.status != -1:
            # keep checking the mouse to see where they click
            if mousePressed():
                xpos = (mouseX()-50)//200 # work out which column they clicked in
                ypos = (mouseY()-50)//200 # work out which row they clicked in
                # if they have clicked outside of the grid
                if xpos < 0 or xpos > 2 or ypos < 0 or ypos > 2:
                    changeLabel(infoLabel, "Click inside the grid")
                else:
                    currentContents = self.board[ypos][xpos]
                    if currentContents is not None:
                        changeLabel(infoLabel, "That cell is occupied")
                    else:
                        # a valid move
                        validMoveMade = True
                        # put a 1 or 0 in the array for this player's symbol
                        self.board[ypos][xpos] = self.thisPlayerNum
                        self.status = 9   # we have completed our turn
                        self.displayBoard()
                        updateDisplay()
                # wait until mouse released
                while mousePressed():
                    updateDisplay()
                    # if you don't have a tick command in your while loops,
                    # pygame can lock up.
                    tick(100)
            tick(100)

    def connect(self):
        self.n = Network()  # this connects to the server using the Network Library
        self.thisPlayerNum = self.n.getP()  # The server sends us our player number
        # now we fire up a separate concurrent thread which will run in the background
        self.thread = threading.Thread(target=self.houseKeeping).start()

    def houseKeeping(self):
        # this thread sits in the background, communicating with the server,
        # keeping it up to date with our current status, and waiting until
        # it tells us that it's our turn.
        while True:
            # receive game state
            receivedState = self.n.receive()
            print(receivedState.currentPlayerNum, receivedState.winner)
            if receivedState.currentPlayerNum == -1:
                # shutdown signal has been sent
                self.status = -1
                break
            # check the gamestate to see if anyone has won the game (or it's a draw)
            if receivedState.winner is not None:
                self.board = receivedState.board[:]
                if receivedState.winner == self.thisPlayerNum:
                    changeLabel(infoLabel, "You win!")
                elif receivedState.winner == 99:
                    changeLabel(infoLabel, "Bah, draw")
                else:
                    changeLabel(infoLabel, "You lose!")
                self.status = 8
                break
            if self.thisPlayerNum == receivedState.currentPlayerNum:
                # it's our turn.
                # Is this the start of our turn? If so, update our local board
                # so it matches the one from the server
                if self.status == 2:
                    self.board = receivedState.board[:]
                    self.displayBoard()
                    self.status = 1 # now start the actual player turn

                elif self.status == 9: # we have finished our move, so send it
                    receivedState.board = self.board[:] # copy the board over
                    receivedState.turntaken = True
                    # now we go into Start of Turn mode, waiting for
                    # our next turn
                    self.status = 2 
            else:
                # CurrentPlayerNum does not match our player number
                changeLabel(infoLabel, "Waiting for your turn")

            # having possibly made some changes to the received state,
            # send it back to the server
            self.n.send(receivedState)


while True:
    pause(1000)
    print("New game")
    game = Game()

endWait()