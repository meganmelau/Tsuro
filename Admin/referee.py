import os
import sys
import inspect
from builtins import len, list, set

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from Player.playerproxy import PlayerProxy
from Player.player import DumbPlayer
from Common.position import Position
from Common.board import Board
from Common.rules import RuleChecker
from Common.tile import Tile
import logging


class Referee:

    # Takes in a list of players, a board, a rule_checker, and a deck
    # Creates a list of players that have lost, a list of currently active players,
    # an integer to keep track of the current round, and an integer to keep track of
    # the tile index the deck is currently on
    def __init__(self, players, board, rule_checker, deck):
        self.current_round = 0
        self.current_tile_index = 0
        # players who made invalid moves
        self.disqualified_players = list()
        # the orders at which the players lost
        self.eliminated_players = list()
        # players who have lost or got eliminated
        self.inactive_players = list()
        # list of player objects
        self.players = players
        # an initialized Board object
        self.board = board
        # an initialized rule-checker
        self.rule_checker = rule_checker
        # a list of initialized Tiles
        self.deck = deck

    # Makes a copy of the board object
    def get_board_copy(self):
        return Board(self.board.get_grid(), self.board.get_players())

    # Draws a set amount of tiles in order from the deck
    # Uses current_tile_index to keep track of where in the deck it should draw from
    def draw_tiles(self):
        hand = list()
        # draws three tiles if in initial round
        if self.current_round == 0:
            num_tiles = 3
        # else draws two
        else:
            num_tiles = 2
        for x in range(0, num_tiles):
            # gets a copy of the Tile from the deck
            hand.append(Tile(self.deck[self.current_tile_index].get_paths()))
            self.current_tile_index = (self.current_tile_index + 1) % len(self.deck)
        return hand

    # asks the rule checker if an initial move is valid
    def check_valid_initial_move(self, target_position, next_tile, given_tiles):
        return self.rule_checker.valid_initial_move(self.get_board_copy(), target_position, next_tile, given_tiles)

    # asks the rule checker if the intermediate move is valid
    def check_valid_move(self, next_x, next_y, next_tile, player, given_tiles):
        player_position = self.board.get_player(player.get_color())
        if not player_position:
            return False
        return self.rule_checker.valid_move(self.get_board_copy(), next_x, next_y, next_tile, given_tiles,
                                            player_position)

    # Remove the given player from the game by removing them from the board
    # and adding them to the inactive player list
    def remove_player(self, player):
        player_position = self.board.get_player(player.get_color())
        if player_position:
            self.board.remove_player(player.get_color(), player_position.get_x(), player_position.get_y())
            self.inactive_players.append(player)

    # Places the tile in the board based on the x, y, and tile
    def place_tile(self, next_x, next_y, next_tile):
        self.board.add_tile(next_tile, next_x, next_y)

    # Place the initial tile given target position, tile, and player
    def place_initial_tile(self, target_position, next_tile, player):
        self.board.add_tile(next_tile, target_position.get_x(), target_position.get_y())
        connected_port = next_tile.get_path(target_position.get_port())
        player_position = Position(target_position.get_x(), target_position.get_y(), connected_port)
        self.board.add_player(player.get_color(), player_position)

    # Updates all the players after a turn if they are affected by the newly placed tile.
    def move_players(self):
        for player in self.players:
            if player not in self.inactive_players:
                current_position = self.board.get_player(player.get_color())
                end_position = self.board.get_path(current_position)
                self.board.remove_player(player.get_color(), current_position.get_x(), current_position.get_y())
                self.board.add_player(player.get_color(), end_position)

    # After each turn, checks to see which player lost and remove them.
    def remove_losers(self):
        lost_players = list()
        for player in self.players:
            # Makes sure it only affects players that are on the board
            if (player not in self.inactive_players) and self.board.get_player(player.get_color()) and \
                    (self.rule_checker.has_lost(self.get_board_copy(), player.get_color())):
                lost_players.append(player.get_name())
                logging.info("Player " + player.get_color() + " (" + player.get_name() + ") was knocked out of the game")
                self.remove_player(player)
        if len(lost_players) != 0:
            lost_players.sort()
            self.eliminated_players.insert(0, lost_players)

    # Sends the list of tile indexes as options to the player
    # Player returns tile, rotation, x, y and port if initial
    # Function will return either tile, x, y and port if initial
    # Returns false if it detects an invalid tile selection by index
    def get_player_move(self, tiles, player):
        try:
            # asks a Player for their initial move
            if self.current_round == 0:
                move = player.select_initial_move(tiles)
            # asks a Player for their intermediate move
            else:
                move = player.select_move(tiles)
        except:
            return None
        # gets and rotates given tile if valid
        try:
            tile = tiles[move[0]]
        except IndexError:
            return None
        for x in range(0, move[1] // 90):
            tile = tile.rotate_90()
        # removes tile index and rotation from the response and adds the tile object to the front
        move = move[2:]
        move.insert(0, tile)
        return move

    # Tells all players to update their board with the new tile
    def update_player_board_placement(self, player, player_move):
        for p in self.players:
            if p not in self.inactive_players:
                try:
                    p.update_board_placement(player.get_color(), player_move[0], player_move[1], player_move[2])
                except:
                    pass

    # Tells all players to update their board with the new player positions
    def update_player_board_position(self):
        positions = self.board.get_players()
        if len(positions) == 0:
            return
        for player in self.players:
            if player not in self.inactive_players:
                try:
                    player.update_board_positions(self.board.get_players())
                except:
                    pass

    # Runs a single turn that takes one player's move and updates the state of the game.
    def run_turn(self, player):
        # Draws tiles for the player
        hand = self.draw_tiles()
        # Asks the player for their move
        player_move = self.get_player_move(hand, player)
        # skips the rest of the turn if move is known to be invalid
        if not player_move:
            self.disqualified_players.append(player.get_name())
            logging.info("Player " + player.get_name() + " was disqualified for making an invalid move")
            if self.current_round == 0:
                self.inactive_players.append(player)
            else:
                self.remove_player(player)
            return
        if self.current_round == 0:
            self.run_initial_turn(player, hand, player_move)
        else:
            self.run_intermediate_turn(player, hand, player_move)
        return player_move

    # Runs the initial turn where players plays their first move
    # Checks to see if the given move is valid. If not, the Player is removed from the game
    # Else, the given move is made
    def run_initial_turn(self, player, hand, player_move):
        target_position = Position(player_move[1], player_move[2], player_move[3])
        if self.rule_checker.valid_initial_move(self.get_board_copy(), target_position, player_move[0], hand):
            self.place_initial_tile(target_position, player_move[0], player)
            self.update_player_board_placement(player, player_move)
        else:
            self.disqualified_players.append(player.get_name())
            logging.info("Player " + player.get_name() + " was disqualified for making an invalid move")
            self.inactive_players.append(player)

    # Runs the intermediate turns of the game per player
    # Checks to see if the given move is valid. If not, the Player is removed from the game
    # Else, the given move is made and all players are moved if possible
    def run_intermediate_turn(self, player, hand, player_move):
        player_position = self.board.get_player(player.get_color())
        if self.rule_checker.valid_move(self.get_board_copy(), player_move[1], player_move[2], player_move[0], hand,
                                        player_position):
            self.place_tile(player_move[1], player_move[2], player_move[0])
            self.update_player_board_placement(player, player_move)
            self.move_players()
        else:
            self.disqualified_players.append(player.get_name())
            logging.info("Player " + player.get_name() + " was disqualified for making an invalid move")
            self.remove_player(player)

    # Runs a turn for every active player in the game and update the state of the game.
    def run_round(self):
        for player in self.players:
            # Only runs a turn for players who are not inactive and if there are enough players left
            if player not in self.inactive_players and (len(self.players) - len(self.inactive_players)) > 1:
                player_move = self.run_turn(player)
                # remove any losers after players have been moved and remove losers after move
                self.remove_losers()
                self.update_player_board_position()

    # Runs rounds until there is a winner(s). Returns two lists,
    # one of players who only made valid moves in the order they placed
    # and one of players who made invalid moves, ordered alphabetically
    def run_game(self):
        # run rounds until there is a winner
        while (len(self.players) - len(self.inactive_players)) > 1:
            self.run_round()
            self.current_round += 1
        # If there is only one player left, do some formatting
        if (len(self.players) - len(self.inactive_players)) == 1:
            winner = list(set(self.players) - set(self.inactive_players))
            self.eliminated_players.insert(0, [winner[0].get_name()])

        # sort list of disqualified players
        self.disqualified_players.sort()
        return self.eliminated_players, self.disqualified_players
