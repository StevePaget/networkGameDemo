from pygame_functions import *
import random, pickle
from network import Network

screenSize(900,900)
setBackgroundColour("#3C047C")
setAutoUpdate(False)

class Game:
    def __init__(self):
        self.thisPlayerNum = None
        self.board = [["x","o",""],
                 ["","x",""],
                 ["","","o"]]
        self.playerLabel = makeLabel("Player: ",42,10,700,"white")
        showLabel(self.playerLabel)
        self.infoLabel = makeLabel("Info here",42,10,750,"white")
        showLabel(self.infoLabel)
        self.displayBoard()

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
                if symbol == "x":
                    drawLine(x-75,y-75,x+75,y+75,"white",5)
                    drawLine(x-75,y+75,x+75,y-75,"white",5)
                elif symbol == "o":
                    drawEllipse(x,y,150,150,"white",5)
                x += 200
            x=150
            y+=200
        if self.thisPlayerNum == 0:
            changeLabel(self.playerLabel, "You are Noughts")
        elif self.thisPlayerNum == 1:
            changeLabel(self.playerLabel, "You are Crosses")
        updateDisplay()

    def playerTurn(self):
        # player makes their go
        changeLabel(self.infoLabel, "It it your turn - click a square")
        validMoveMade = False
        while not validMoveMade:
            # keep checking the mouse to see where they click
            

    def houseKeeping(self):
            # receive game state
            self.receivedState = self.n.receive()
            print("HS received player num", self.receivedState.currentPlayerNum)
            if self.thisPlayerNum == self.receivedState.currentPlayerNum:
                print("updating")
                self.receivedState.status = self.status
                if self.status == 4:
                     # send the updated gamestate to the server
                    self.receivedState.pile = [ (t.value, t.colourcode, t.colour, t.x,t.y, t.id) for t in self.pile]
                    self.receivedState.table = []
                    for group in self.table:
                        self.receivedState.table.append([])
                        self.receivedState.table[-1] = [(t.value, t.colourcode, t.colour, t.x,t.y, t.id) for t in group]
                    self.receivedState.playerHands[self.currentPlayerNum] = [ (t.value, t.colourcode, t.colour, t.x,t.y, t.id) for t in self.thisPlayer.hand]
                    self.status = 0
            result = self.n.send(self.receivedState)
            print(result, "sent", self.receivedState.status )
            changeLabel(self.playerNumLabel,"Player " + str(self.thisPlayerNum+1))
            changeLabel(self.tileCountLabel,"Tiles left: " + str(len(self.pile)))
            updateDisplay()
            tick(100)

main = Game()

print("Ended")

endWait()