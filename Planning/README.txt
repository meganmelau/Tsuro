PROJECT TSURO

Brief Description
This project will produce software to allow automated players to connect to a server
and play a modified version of the game Tsuro. This software will allow for the use 
of different implementations of player clients as long as they interact with the server 
in the software in the same way. The software will generate the board and the tiles
and run a game for the clients, providing each player with a "hand" of tiles on their
turn. Each player is initially given 3 cards for the first turn, then 2 tiles choices 
for any other round. A turn is when the current player placed the chosen tile on the board, 
moves the player tokens, and all players connected to that new placed tile moves. The turn ends
and is repeated with the next player.

Folder Structure
Tsuro\
  1\
    allTiles.py
    tile-1.PNG
    tile-2.PNG
    tile-3.PNG
  Common\
    tile.py
    test_tile.py
    Other\
  Planning\
    board.md
    plan.md
    README.txt
  
