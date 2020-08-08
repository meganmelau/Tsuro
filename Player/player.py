import os
import sys
import inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from Common.board import Board
from Common.rules import RuleChecker
from Common.tile import Tile
from Common.position import Position
import json


class DumbPlayer:

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.board = Board()
        self.rule_checker = RuleChecker()

    # Returns the color of the player
    def get_color(self):
        return self.color

    def get_name(self):
        return self.name

    # takes in a list of tiles and the current state of the board and then selects an initial move.
    # An initial move is a tile index in the given hand, rotation, x,  y, and port
    # 00, 20, 40, 60, 80 --> only 5 characters because a set of colors
    def select_initial_move(self, tiles):
        # start at position (0,0)
        start_x = 0
        start_y = 0
        state = 0
        # Goes clockwise around the board's edge searching for a valid move
        while not self.check_valid_initial_move(start_x, start_y, state, tiles[0], tiles):
            if state == 0:
                if start_x == 9:
                    state = 2
                    start_y += 1
                else:
                    start_x += 1
            elif state == 2:
                if start_y == 9:
                    state = 4
                    start_x -= 1
                else:
                    start_y += 1
            elif state == 4:
                if start_x == 0:
                    state = 6
                    start_y -= 1
                else:
                    start_x -= 1
            elif state == 6:
                if start_y == 0:
                    # no valid moves exist, return an invalid one
                    return [2, 0, start_x, start_y, state]
                else:
                    start_y -= 1
        return [2, 0, start_x, start_y, state]

    # takes in a list of tiles and the current state of the board and then selects a move. A move is a
    # tile index in the given hand, rotation, x, and y
    def select_move(self, tiles):
        curr_pos = self.board.get_player(self.get_color())

        if not curr_pos:
            return None
        
        x = curr_pos.get_x()
        y = curr_pos.get_y()
        port = curr_pos.get_port()
        if port == 0 or port == 1:
            next_move = [x, y - 1]
        elif port == 2 or port == 3:
            next_move = [x + 1, y]
        elif port == 4 or port == 5:
            next_move = [x, y + 1]
        elif port == 6 or port == 7:
            next_move = [x - 1, y]
        return [0, 0, next_move[0], next_move[1]]

    # asks the rule-checker if a given initial move is valid
    def check_valid_initial_move(self, x, y, port, tile, tiles):
        return self.rule_checker.valid_initial_move(Board(self.board.get_grid(), self.board.get_players()),
                                                    Position(x, y, port), tile, tiles)

    # checks if the player's move is valid based on the rules of the game. Takes in the current state of the board,
    # a rule_checker with the implementation of the rules of the game, a tile, a rotation, an x, and a y to determine
    # whether the given move is valid
    def check_valid_move(self, x, y, tile, tiles):
        curr_pos = self.board.get_player(self.get_color())
        return self.rule_checker.valid_move(Board(self.board.get_grid(), self.board.get_players()), x, y, tile, tiles,
                                            Position(curr_pos[0], curr_pos[1], curr_pos[2]))

    def update_board_placement(self, color, tile, x, y):
        self.board.add_tile(tile, x, y)

    def update_board_positions(self, positions):
        old_positions = self.board.get_players()
        for key,val in old_positions.items():
            self.board.remove_player(key, val.get_x(), val.get_y())
        for key,val in positions.items():
            self.board.add_player(key, val)

class LessDumbPlayer(DumbPlayer):

    # Overwrites Player's intermediate move selection
    # Chooses a tile that will not result in suicide by trying different rotation
    # tile index in the given hand, rotation, x, and y
    def select_move(self, tiles):
        curr_pos = self.board.get_player(self.get_color())

        if not curr_pos:
            return None
        
        x = curr_pos.get_x()
        y = curr_pos.get_y()
        port = curr_pos.get_port()
        if port == 0 or port == 1:
            next_move = [x, y - 1]
        elif port == 2 or port == 3:
            next_move = [x + 1, y]
            next_move = [x + 1, y]
        elif port == 4 or port == 5:
            next_move = [x, y + 1]
        elif port == 6 or port == 7:
            next_move = [x - 1, y]

        for tile_index in range(len(tiles)):
            tile_to_place = tiles[tile_index]
            rotated = 0
            while rotated < 4:
                if self.rule_checker.valid_move(Board(self.board.get_grid(), self.board.get_players()), next_move[0], next_move[1], tile_to_place, tiles, curr_pos):
                    return [tile_index, rotated*90, next_move[0], next_move[1]]
                else:
                    tile_to_place = tile_to_place.rotate_90()
                    rotated += 1
        # impossible to not have returned at this point
