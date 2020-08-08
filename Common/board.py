import os
import sys
import inspect
from builtins import len, Exception

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from Common.tile import Tile
import copy
from Common.position import Position


class Board:

    def __init__(self, grid={}, player={}):
        if len(grid) == 0:
            # need to initialize to 10 x 10 grid
            self.grid = [[0 for x in range(10)] for y in range(10)]
            for x in range(0, 10):
                for y in range(0, 10):
                    self.grid[x][y] = Tile([])
        else:
            self.grid = grid

        self.width = len(self.grid)
        self.height = len(self.grid[0])
        self.player_positions = player

    # Returns the tile on the given x and y
    def get_tile(self, x, y):
        # ensures the x and y are valid
        if x in range(0, self.width) and y in range(0, self.height):
            return self.grid[x][y]
        else:
            return None

    # Returns a list of tiles surrounding the tile at the given x and y
    def get_surrounding_tiles(self, x, y):
        above = self.get_tile(x, y - 1)
        below = self.get_tile(x, y + 1)
        left = self.get_tile(x - 1, y)
        right = self.get_tile(x + 1, y)
        # appends the tiles if they are not False
        surrounding = [t for t in [above, below, left, right] if t]
        return surrounding

    # Adds a tile to the board given the tile, x, y
    def add_tile(self, tile, x, y):
        if self.get_tile(x, y).is_empty():
            self.grid[x][y] = tile
        else:
            raise Exception("Tile already exists at given position")

    # Determines if the player is on the edge given their position
    def is_on_edge(self, pos):
        edge_ports = []
        x = pos.get_x()
        y = pos.get_y()
        port = pos.get_port()
        if x == 0:
            edge_ports.extend([6, 7])
        if x == (self.width - 1):
            edge_ports.extend([2, 3])
        if y == 0:
            edge_ports.extend([0, 1])
        if y == (self.height - 1):
            edge_ports.extend([4, 5])
        return port in edge_ports

    # Adds the initial tile given tile and position
    def add_initial_tile(self, tile, pos):
        x = pos.get_x()
        y = pos.get_y()
        if self.get_tile(x, y).is_empty():
            surroundings = self.get_surrounding_tiles(x, y)
            for surrounding in surroundings:
                if not surrounding.is_empty():
                    raise Exception("Initial Tile cannot be placed near existing Tile")
            if self.is_on_edge(pos):
                self.add_tile(tile, x, y)
                return True

        raise Exception("Invalid initial tile placement")

    # Add a player to the tile given the position and token
    def add_player(self, token, pos):
        if self.get_tile(pos.get_x(), pos.get_y()).add_avatar(token, pos.get_port()):
            self.player_positions[token] = pos
        else:
            return None

    # Remove the player from the tile given the x and y
    def remove_player(self, token, x, y):
        if self.get_tile(x, y).remove_avatar(token):
            del self.player_positions[token]
        else:
            return None

    # Get the player given the color token
    def get_player(self, token):
        if token in self.player_positions.keys():
            return self.player_positions[token]
        else:
            return None

    # Makes a copy of player position map
    def get_players(self):
        return copy.deepcopy(self.player_positions)

    # gets the next tile the player is suppose to move to
    def get_next_tile(self, pos):
        x = pos.get_x()
        y = pos.get_y()
        port = pos.get_port()
        if port == 0 or port == 1:
            return Position(x, y - 1, 5 - port)
        elif port == 2 or port == 3:
            return Position(x + 1, y, 9 - port)
        elif port == 4 or port == 5:
            return Position(x, y + 1, 5 - port)
        elif port == 6 or port == 7:
            return Position(x - 1, y, 9 - port)
        else:
            return None

    # Return the ending position given player's current position
    # given position is current player position before moving to added tile
    # Only used for intermediate placements
    def get_path(self, pos):
        next_step = self.get_next_tile(pos)
        if (not next_step.get_x() in range(0, self.width)) or (not next_step.get_y() in range(0, self.height)):
            # Already on the edge of the board
            return pos
        elif self.get_tile(next_step.get_x(), next_step.get_y()).is_empty():
            # No more tile to continue path
            return pos

        # If port is already occupied, has collided, stop moving
        next_tile = self.get_tile(next_step.get_x(), next_step.get_y())
        if next_tile.is_occupied(next_step.get_port()):
            return next_step

        # "Move" avatar to connecting port on next tile
        connected_port = next_tile.get_path(next_step.get_port())
        next_tile_pos = Position(next_step.get_x(), next_step.get_y(), connected_port)

        # If connecting port is already occupied, has collided, stop moving
        if next_tile.is_occupied(connected_port):
            return next_tile_pos

        # "Moved" player to a new position, recursively call get_path on new position
        return self.get_path(next_tile_pos)

    # Returns a copy of the Board's grid
    def get_grid(self):
        return_grid = [[0 for x in range(self.width)] for y in range(self.height)]
        for x in range(0, self.width):
            for y in range(0, self.height):
                return_grid[x][y] = Tile(self.get_tile(x, y).get_paths())
        return return_grid
