# networkGameDemo
 
This is a demo game of Noughts and Crosses (Tic Tac Toe), which has been designed to aid students creating a network game for multiple players.
This example allows two players on different computers to play against each other.

I have tried to structure the game and provide comments so that you could adapt the network communication elements to apply to a variety of different games.
It will work best with games which have a turn-based structure, rather than where both players act simultaneously. Examples would include simple card games, board games etc.

The example game uses a library called pygame_functions. This is my own library which takes care of drawing on a graphical screen and mouse inputs, simplifying the process of drawing in standard pygame. You can find out more about pygame_functions here: https://github.com/StevePaget/Pygame_Functions/wiki

## Installation

Your server computer needs to have server.py running. You need to change line 16 to reflect the server computer's IP local address  (Look up how to find this out on your specific operating system - in most cases it involves running ifconfig in a command prompt)

This IP address also needs to be entered into the relevant line of network.py

Each player needs to have network.py, player.py and pygame_functions.py in the same folder.

Fire up server.py on the server computer, then have the players run their player.py

They should communicate with the server, and the server will confirm this with console output.
