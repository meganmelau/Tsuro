# Player

A Player is represented as a person who can receive tiles and dictate
what their next move is. They can look at the board representation,
optionally check if their move is valid, and send it to the referee.

#### Class variables
color: This is unique to each player

time_connected: The time the player is connected to the client

session_id: The session the player is on

#### Class methods
get_color(): Returns the color of the player

get_time(): Returns the time connected

get_session(): Returns the session the player is connected to

select_initial_move(board, tiles): takes in a list of tiles and the current state of the board and then selects an initial move. An initial move is a tile, rotation, x, y, and port

select_move(board, tiles): takes in a list of tiles and the current state of the board and then selects a move. A move is a tile, rotation, x, and y

check_valid_move(board, rulechecker, x, y, tile, rotation): checks if the player's move is valid based on the rules of the game. Takes in the current state of the board, a rulechecker with the implementation of the rules of the game, a tile, a rotation, an x, and a y to determine whether the given move is valid
