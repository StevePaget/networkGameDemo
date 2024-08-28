from pygame_functions import *
import random, pickle
from network import Network
import threading

screenSize(900,900)
setBackgroundColour("#3C047C")
setAutoUpdate(False)
playerLabel = makeLabel("Player: ",42,10,700,"white")
showLabel(playerLabel)
infoLabel = makeLabel("Waiting for your turn",42,10,750,"white")
showLabel(infoLabel)

class Game:
    def __init__(self):
        self.board = [[None,None,None],
                 [None,None,None],
                 [None,None,None]]
        #  0=wait,  1=playing, 2=updateScreen, 9=done
        self.status = 2
        self.running = True
        self.connect()
        self.displayBoard()
        self.playGame()

    
    def playGame(self):
        changeLabel(infoLabel,"Waiting for your turn")
        updateDisplay()
        while self.running:
            if self.status == 1:
                self.playerTurn()
            elif self.status == -1:
                break
            tick(100)


    def displayBoard(self):
        clearShapes()
        # draw lines for the grid
        drawLine(250,50,250,650,"white",5)
        drawLine(450,50,450,650,"white",5)
        drawLine(50,250,650,250,"white",5)
        drawLine(50,450,650,450,"white",5)
        x = 150
        y = 150
        for row in self.board:
            for symbol in row:
                if symbol == 1:
                    drawLine(x-75,y-75,x+75,y+75,"white",5)
                    drawLine(x-75,y+75,x+75,y-75,"white",5)
                elif symbol == 0:
                    drawEllipse(x,y,150,150,"white",5)
                x += 200
            x=150
            y+=200
        if self.thisPlayerNum == 0:
            changeLabel(playerLabel, "You are Noughts")
        elif self.thisPlayerNum == 1:
            changeLabel(playerLabel, "You are Crosses")
        updateDisplay()


    def playerTurn(self):
        # player makes their go
        changeLabel(infoLabel, "It's your turn - click a square")
        updateDisplay()
        validMoveMade = False
        while not validMoveMade:
            # keep checking the mouse to see where they click
            if mousePressed():
                print("start")
                xpos = (mouseX()-50)//200
                ypos = (mouseY()-50)//200
                if xpos < 0 or xpos > 2 or ypos < 0 or ypos > 2:
                    changeLabel(infoLabel, "Click inside the grid")
                else:
                    currentContents = self.board[ypos][xpos]
                    if currentContents is not None:
                        changeLabel(infoLabel, "That cell is occupied")
                    else:
                        # a valid move
                        validMoveMade = True
                        self.board[ypos][xpos] = self.thisPlayerNum
                        self.status = 9
                        self.displayBoard()
                        updateDisplay()
                # wait until mouse released
                while mousePressed():
                    print("pausing")
                    updateDisplay()
                    tick(50)
                print("released")
            tick(100)

    def connect(self):
        self.n = Network()
        self.thisPlayerNum = self.n.getP()
        self.thread = threading.Thread(target=self.houseKeeping).start()

    def houseKeeping(self):
        while True:
            # receive game state
            receivedState = self.n.receive()
            print(self.board, receivedState.board)
            print(self.thisPlayerNum, receivedState.currentPlayerNum, self.status, receivedState.winner)
            if receivedState.winner is not None:
                if receivedState.winner == self.thisPlayerNum:
                    changeLabel(infoLabel, "You win!")
                elif receivedState.winner == 99:
                    changeLabel(infoLabel, "Bah, draw")
                else:
                    changeLabel(infoLabel, "You lose!")
                updateDisplay()
                self.running = False
                break
            if self.thisPlayerNum == receivedState.currentPlayerNum:
                if self.status == 2:
                    self.board = receivedState.board[:]
                    self.displayBoard()
                    updateDisplay()
                    self.status = 1 # now our turn
                elif self.status == 9: # we have made our move, so send it
                    receivedState.board = self.board[:] # copy the board over
                    receivedState.turntaken = True
                    self.status = 2
            else:
                changeLabel(infoLabel, "Waiting for your turn")
            result = self.n.send(receivedState)
            tick(100)

while True:
    pause(1000)
    print("New game")
    game = Game()

endWait()