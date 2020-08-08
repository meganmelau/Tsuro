# Referee

A referee represents the board the enforcer of moves that are accepted
to update the board. It contains a dictionary of session-id and players,
rule checker, board, last round of players, a deck of 35 unique titles,
the current turn, and socket object. The referee will interact with
the player by dealing a hand of tiles to the player, the player returns
the move they want to make, and the referee checks the rule checker
to see if it's valid. Next, it updates the board to reflect the newly
placed tile by updating the board and moving the players to the
respective locations. If the player did not give a valid move, they
are kicked out of the game. A turn is when one player goes and a round
is when all the players go. This continues until a game is finished.
A game is finished if there is one person left or if there are multiple
players based on extenuating circumstances.


#### Class variables
player_sessions: Is a map of session id to player to keep track of 
which session to player.

board: A 10x10 board that holds the tiles and players.

rule_checker: A list of rules that dictate where initially players can 
move, whether a player can move to the location, 
if they are kicked out of the game, and who won.

last_round_players: Keeps track of the players who are active from 
last round if we have joint winners

current_turn: Current turn represents how many turns have occurred
since the start of the game. It is initialized to 1. 

deck: The list of 35 unique tiles that is generated for usage of the game

socket_obj: The channel in which to communicate to the player 


#### Class methods
send_tiles(tiles, player): Sends the list of tile options to the player.

draw_tiles(num_tiles): Takes in a number of tiles to return in a list
from the deck. 

receive_tile(): Listens for a response from the player about what tile
they would like to place and move.  

check_valid_move(next_x, next_y, next_tile, player): checks if the 
next x,y and tile the player wants to move is valid within
the rules of the rule checker.

place_tile(next_x, next_y, next_tile, player): Places the tile in the 
board base on the x,y,tiles.

move_players(): Updates all the players after a turn if they are 
affected by the newly placed tile.

send_board_state(): Sends the representation of the board to the player.

remove_losers(): After each turn, checks to see which player lost and 
remove them.

run_turn(): Runs a single turn that takes one player's move and update
the state of the game.

run_round(): Runs a turn for every player in the game and update 
the state of the game.

run_game(): Runs rounds until there is a winner(s). Returns a list of
winners.
