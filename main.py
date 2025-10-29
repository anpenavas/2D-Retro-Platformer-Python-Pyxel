from board import Board
import pyxel

# Set the board
board = Board()

# The first thing to do is to create the screen
pyxel.init(board.width, board.height, caption="Super Mario Bros")
# Load the assets
pyxel.load("assets/marioassets.pyxres")
# Start the game by calling pyxel.run and passing as parameters the update and draw method of the board
pyxel.run(board.update, board.draw)