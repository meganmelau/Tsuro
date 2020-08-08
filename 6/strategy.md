Strategy: LessDumbPlayer

This strategy is the same as DumbPlayers strategy with the exception of the select_move method.
select_move chooses a tile that will not result in suicide by trying different rotations.

When selecting the initial move, the player searches the tiles around the board's edges 
in a clockwise direction for a valid move starting from (0,0). If a valid move is found,
it will select that move and return it.

When selecting an intermediate move, the player will try to choose a tile that will not result
in a suicide by trying out different rotations. Starting with the first tile with no rotation,
it first checks to see if that placement is valid. If the move is not valid, the player rotates 
the tile 90 degrees clockwise and checks again. If no rotation of the current tile is valid,
it moves to the next tile and repeats the process.
