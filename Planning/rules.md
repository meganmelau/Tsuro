# Rulechecker

### Summary
The Rulechecker is in charge of validating Player chosen moves given the current state of the Board. The Referee, before making any moves on behalf of the Player, will check with the Rulechecker to ensure that the Player's move is valid. The Rulechecker uses the current state of the Board, including the current Player's position, to determine if the move is valid. The Referee class will have a Rulechecker as a class variable.

### Class methods

- valid_initial_move(): This method checks to see if an initial move is valid. This function takes in the target x and y coordinates, the target port, and a copy of the current state of the Board. It checks to see if the given position is on the edge of the board, if the given port is on the edge of the board, and if the given position is next to an already placed Tile.
- valid_move(): This method checks to see if a move made after the initial moves is valid. This function takes in the target x and y coordinates, the Player's position, and a copy of the current state of the Board. It checks to see if given position for the Tile placement is appropriate given the Player's position.
- who_won(): This method determines which of the Player's has won the game. It takes in a list of the currently active Players and the Players that were active before the last move.
- is_off_board(): This method determines whether a Player is off the board. It takes in a Player's position and a copy of the current state of the Board.