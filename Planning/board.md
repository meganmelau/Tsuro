# Board

A Board represents the board of a Tsuro game. It contains Tiles and has functions to get and add Tiles. The Player will interact with the Board through Referee, which is  the rule keeper of the game. It will randomly deal a hand of Tiles to the Player, and get back a Tile that the Player chose. Then the Referee will add the chosen Tile to the Board, and move Player avatar(s) according to the rule. At the end of the round, the Referee will also determine whether the game has ended or not.

#### Class variables
Grid: a 10 x 10 two-dimensional array of Tiles, initially populated with empty Tiles. Position [0,0] is at the upper left portion of the board.

#### Class methods
new_board(): a method to fill the Board with empty Tiles with no connections. This will cause the board to render them as blank spaces with ports

add_tile(Tile t, int x, int y): a method for the Referee to add a Tile to the given x and y location on the grid. This function throws an error if the position given is out of bounds or contains a Tile already.

get_tile(x, y): this method returns the Tile at the given x and y location. This method should return the Tile even if it is an empty Tile, but throw an error if the position given is out of bounds.

render_board(): this method renders the board by rendering a backdrop for the board, and then looping through Grid and rendering each Tile in the proper position, based on its place in the grid.

# Tile
A data representation of a Tile for a Tsuro game.

#### Class variables
position: The x,y position of the border. This is set to 30 and cannot be changed by interacting with Tile.

paths: an array of two-element integer arrays that represent connections between ports. A Tile is made by passing an array like this into the constructor.

occupied_ports: A dictionary that contains the ports, represented by integers, matched to the color of the Player token that occupies it. If no ports are occupied, this dictionary is empty.

Ports_coordinates: An array of two-element arrays that represent the position that ports should be drawn at when rendering the board.



#### Class methods
get_paths(self): A method to return the connections of this Tile

compare(self, other_tile): A method to compare this Tile with some other Tile. Returns True only if this Tile is equivalent to the given Tile. Tests equivalency by rotating the given Tile 3 times.

is_equal_paths(self, other_paths): A method to test if the connections between ports on this Tile are the same as the given connections

is_equal_connection(self, first_connect, second_connect): A method to test if a given connection between ports is the same.

get_path(self, port): A method to return the port that the given port connects to.

is_occupied(port): checks if the port is occupied by using the occupied_ports class variable

rotate_90(paths): A method that returns a new Tile with the ports and connections rotated 90 degrees to the right.

add_avatar(self, avatar, port): adds an avatar, string of color, to the given port

remove_avatar(self, avatar): removes an avatar, color of string, from the given port

draw_ports(self, canvas): this method draws the 8 ports around the edges of the Tile. There are two ports on each edge of the Tile equally spaced by 50 pixels.

draw_paths(self, canvas): for each path in the list of paths in the Tile class, draw a curved line from the position of the start of the path to the position of the end of the path.

draw_players(self, canvas): for each player, draw a triangle over the port the player occupies. The color of each triangle matches the color string given to the player.

render_tile(self): draws a square, then draw the ports, paths, and players on the tile.
