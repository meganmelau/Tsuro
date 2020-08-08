import os
import sys
import inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from Common.board import Board
from Common.position import Position
from Common.tile import Tile


class RuleChecker:

    # Check the validity of initial move
    def valid_initial_move(self, board, target_pos, tile, given_tiles):
        # Check if chosen tile is a valid tile from given tiles
        if not self.is_valid_tile(tile, given_tiles):
            return False

        # Check if target position is actually on the board
        target_tile = board.get_tile(target_pos.get_x(), target_pos.get_y())
        if not target_tile:
            return False

        # Check target position must be on the edge of the board
        if not board.is_on_edge(target_pos):
            return False

        # Check if target position has an empty tile
        if not target_tile.is_empty():
            return False

        # Check if surrounding tiles are empty
        surroundings = board.get_surrounding_tiles(target_pos.get_x(), target_pos.get_y())
        for surrounding in surroundings:
            if not surrounding.is_empty():
                return False

        # Check if connected_port is false, which means target port is out of range
        connected_port = tile.get_path(target_pos.get_port())
        if not connected_port:
            return False

        # Can't be suicidal
        player_pos = Position(target_pos.get_x(), target_pos.get_y(), connected_port)
        try:
            return not self.is_suicidal(board, tile, target_pos.get_x(), target_pos.get_y(), player_pos)
        except Exception:
            # is_suicidal(Board.add_tile) threw exception, invalid target position
            return False

    # Check validity of intermediate moves
    def valid_move(self, board, target_x, target_y, tile, given_tiles, player_pos):
        # Check if chosen tile is a valid tile from given tiles
        if not self.is_valid_tile(tile, given_tiles):
            return False

        # Check if position is actually on the board
        target_tile = board.get_tile(target_x, target_y)
        if not target_tile:
            return False

        # Check if target tile is an empty tile
        if not target_tile.is_empty():
            return False

        # Check if player's current position is valid
        proper_tile_position = board.get_next_tile(player_pos)
        if not proper_tile_position:
            return False

        # Target position must be directly connected to the player's current position
        if target_x != proper_tile_position.get_x() or target_y != proper_tile_position.get_y():
            return False

        # If a suicidal move, check if player has other options
        try:
            if self.is_suicidal(board, tile, target_x, target_y, player_pos):
                return not self.has_other_options(board, target_x, target_y, player_pos, given_tiles)
            else:
                return True
        except Exception:
            # is_suicidal threw exception (from Board.add_tile), invalid target position
            # OR has_other_options threw exception (from is_suicidal), invalid target position
            return False

    # Determine if the given position is off the board
    def is_off_board(self, board, pos):
        return board.is_on_edge(pos)

    # Determine if there is more than one player at the given position
    def has_collided(self, board, pos):
        current_tile = board.get_tile(pos.get_x(), pos.get_y())
        if not current_tile:
            # get_tile returns false if position x y are invalid.
            raise Exception("Invalid player position.")
        occupants = current_tile.get_occupants(pos.get_port())
        return len(occupants) > 1

    # Determine if the given player lost the game
    def has_lost(self, board, avatar):
        avatar_position = board.get_player(avatar)
        if not avatar_position:
            # get_player returned False, avatar doesn't exist on the board
            return True
        try:
            return self.has_collided(board, avatar_position) or \
                   self.is_off_board(board, avatar_position)
        except Exception:
            # has_collided raised exception, invalid player position, remove player
            return True

    # Determine if the attempted move is going to make the player lose
    def is_suicidal(self, board, tile, target_x, target_y, player_pos):
        # Make a copy of the board to test out the attempted move
        temp_board = Board(board.get_grid(), board.get_players())
        temp_tile = Tile(tile.get_paths())
        # Add chosen tile
        temp_board.add_tile(temp_tile, target_x, target_y)
        # Determine where is the end position after adding tile
        end_position = temp_board.get_path(player_pos)
        if not end_position:
            # Invalid player position
            return True
        # Add a placeholder avatar "rulechecker" to the end position
        temp_board.add_player("rulechecker", end_position)
        return self.has_lost(temp_board, "rulechecker")

    # Determine if the player has other option that's not suicidal
    def has_other_options(self, board, target_x, target_y, player_pos, given_tiles):
        for given_tile in given_tiles:
            temp_tile = given_tile
            # Try rotating the tile and check if placing the tile would result in suicide
            # If any tile orientation results in non-suicidal move, then there is other option
            for x in range(0, 4):
                if not self.is_suicidal(board, temp_tile, target_x, target_y, player_pos):
                    return True
                else:
                    temp_tile = temp_tile.rotate_90()
        return False

    # Determine if the tile returned actually is from the list of given tiles
    def is_valid_tile(self, tile, given_tiles):
        for given_tile in given_tiles:
            if tile.compare(given_tile):
                return True
        return False
