from tile import Tile
import copy


class Board:

    def __init__(self, *args):
        if len(args) == 0:
            self.width = 10
            self.height = 10
            self.grid = [[0 for x in range(self.width)] for y in range(self.height)]
            self.player_positions = {}
            for x in range(0, self.width):
                for y in range(0, self.height):
                    self.grid[x][y] = Tile([])
        elif len(args) == 2:
            grid = args[0]
            player_positions = args[1]
            if len(grid) > 0 and len(grid[0]) > 0:
                self.grid = grid
                self.height = len(grid)
                self.width = len(grid[0])
                self.player_positions = {}
                for key in player_positions:
                    self.add_player(key, player_positions[key][0], player_positions[key][1], player_positions[key][2])
            else:
                raise Exception("Given bad grid")
    '''
    def __init__(self, grid, player_positions):
        if len(grid) > 0 and len(grid[0]) > 0:
            self.grid = grid
            self.height = len(grid)
            self.width = len(grid[0])
            self.player_positions = {}
            for key in player_positions:
                self.add_player(key, player_positions[key][0], player_positions[key][1], player_positions[key][2])
        else:
            raise Exception("Given bad grid")
    '''

    def get_tile(self, x, y):
        if x in range(0, self.width) and y in range(0, self.width):
            return self.grid[x][y]
        else:
            raise Exception("Bad index")

    def get_surrounding_tiles(self, x, y):
        surrounding = []
        try:
            surrounding.append(self.get_tile(x - 1, y))
        except:
            pass
        try:
            surrounding.append(self.get_tile(x, y - 1))
        except:
            pass
        try:
            surrounding.append(self.get_tile(x + 1, y))
        except:
            pass
        try:
            surrounding.append(self.get_tile(x, y + 1))
        except:
            pass
        return surrounding

    def add_tile(self, tile, x, y):
        if len(self.get_tile(x, y).get_paths()) == 0:
            self.grid[x][y] = tile
        else:
            raise Exception("Tile already exists at given position")

    def is_on_edge(self, x, y, port):
        acceptable_ports = []
        if x == 0:
            acceptable_ports.extend([6, 7])
        if x == (self.width - 1):
            acceptable_ports.extend([2, 3])
        if y == 0:
            acceptable_ports.extend([0, 1])
        if y == (self.height - 1):
            acceptable_ports.extend([4, 5])
        return port in acceptable_ports

    def add_initial_tile(self, tile, x, y, port):
        if len(self.get_tile(x, y).get_paths()) == 0:
            surroundings = self.get_surrounding_tiles(x, y)
            for surrounding in surroundings:
                if len(surrounding.get_paths()) != 0:
                    raise Exception("Initial Tile cannot be placed near existing Tile")
            if self.is_on_edge(x, y, port):
                self.add_tile(tile, x, y)
                return True

        raise Exception("Invalid initial tile placement")

    def add_player(self, token, x, y, port):
        if self.get_tile(x, y).add_avatar(token, port):
            self.player_positions[token] = [x, y, port]

    def remove_player(self, token, x, y):
        if self.get_tile(x, y).remove_avatar(token):
            del self.player_positions[token]

    def get_player(self, token):
        return self.player_positions[token]

    def get_players(self):
        return copy.deepcopy(self.player_positions)

    def get_next_tile(self, x, y, port):
        if port == 0 or port == 1:
            return [x, y - 1, 5 - port]
        elif port == 2 or port == 3:
            return [x + 1, y, 9 - port]
        elif port == 4 or port == 5:
            return [x, y + 1, 5 - port]
        elif port == 6 or port == 7:
            return [x - 1, y, 9 - port]

    def get_path(self, x, y, port):
        # If current port is already occupied, has collided, stop moving
        current_tile = self.get_tile(x, y)
        if current_tile.is_occupied(port):
            return [x, y, port]
        # Move avatar to connect port on current tile
        connected_port = current_tile.get_path(port)
        if not connected_port:
            raise Exception("Invalid port given")
        current_end = [x, y, connected_port]
        # Check if port is occupied by more than 1 avatar
        if current_tile.is_occupied(connected_port):
            return current_end
        # Check if possible to move to another tile
        next_step = self.get_next_tile(current_end[0], current_end[1], current_end[2])
        if (not next_step[0] in range(0, self.width)) or (not next_step[1] in range(0, self.height)):
            return current_end
        elif len(self.get_tile(next_step[0], next_step[1]).get_paths()) == 0:
            return current_end
        else:
            return self.get_path(next_step[0], next_step[1], next_step[2])

    def get_grid(self):
        return_grid = [[0 for x in range(self.width)] for y in range(self.height)]
        for x in range(0, self.width):
            for y in range(0, self.height):
                return_grid[x][y] = Tile(self.get_tile(x, y).get_paths())
        return return_grid
