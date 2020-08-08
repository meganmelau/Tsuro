import os
import sys
import inspect
import socket
import json
import time
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from Common.board import Board
from Common.rules import RuleChecker
from Common.tile import Tile
from Common.tile_conversion import Converter
import json
import logging


class PlayerProxy:

    def __init__(self, name, color, connection, address):
        logging.basicConfig(filename="server.log", level=logging.DEBUG, format='\n%(asctime)s %(message)s')
        logging.info("Player proxy created for " + name + " with color " + color)
        self.color = color
        self.name = name
        self.connection = connection
        self.address = address
        self.board = Board()
        self.rule_check = RuleChecker()
        self.converter = Converter()
        self.tile_dict = self.converter.generate_tile_dictionary()

    # Returns the color of the player
    def get_color(self):
        return self.color

    # Returns the name of the player
    def get_name(self):
        return self.name

    # takes in a list of tiles and the current state of the board and then selects an initial move.
    # An initial move is a tile index in the given hand, rotation, x,  y, and port
    # 00, 20, 40, 60, 80 --> only 5 characters because a set of colors
    def select_initial_move(self, tiles):
        tile_indices = [self.converter.get_equivalent_tile_index(t) for t in tiles]
        to_send = ["initial move request"]
        to_send.extend(tile_indices)
        response = self.wait_for_response(to_send, 10)
        return self.parse_initial_move(response)

    # Parse initial move response
    # Response format: ["initial move respond", index, rotation, x, y, port]
    def parse_initial_move(self, response):
        if (not response) or (len(response) != 6) or (response[0] != "initial move respond"):
            # Invalid response, return a move with invalid index to eliminate player
            return [-10, 0, 0, 0, 0]
        else:
            return response[1:]


    # takes in a list of tiles and the current state of the board and then selects a move. A move is a
    # tile index in the given hand, rotation, x, and y
    def select_move(self, tiles):
        tile_indices = [self.converter.get_equivalent_tile_index(t) for t in tiles]
        to_send = ["intermediate move request"]
        to_send.extend(tile_indices)
        response = self.wait_for_response(to_send, 10)
        return self.parse_intermediate_move(response)

    # Parse intermediate move response
    # Response format: ["intermediate move respond", index, rotation, x, y]
    def parse_intermediate_move(self, response):
        if (len(response) != 5) or (response[0] != "intermediate move respond"):
            # Invalid response, return a move with invalid index to eliminate player
            return [-10, 0, 0, 0]
        else:
            return response[1:]

    # Send json over socket for remote players to update a new avatar placement on the board
    def update_board_placement(self, color, tile, x, y):
        try:
            tile_index, rotation = self.converter.get_index_rotation(tile)
            to_send = ["board update", color, tile_index, rotation, x, y]
            self.connection.sendall(json.dumps(to_send).encode("ascii"))
        except Exception as e:
            logging.info("update board placement: " + e)

    # Send json over socket for remote players to update each player's position on the board
    def update_board_positions(self, positions):
        try:
            to_send = ["board update"]
            position_list = list()
            for key, val in positions.items():
                player_position = {"color": key, "position": [val.get_x(), val.get_y(), val.get_port()]}
                position_list.append(player_position)
            to_send.append(position_list)
            self.connection.sendall(json.dumps(to_send).encode("ascii"))
        except Exception as e:
            logging.info("board update positions: " + e)

    # Send the json message to remote player and wait for their response
    def wait_for_response(self, to_send, timeout):
        self.connection.settimeout(timeout)
        try:
            self.connection.sendall(json.dumps(to_send).encode("ascii"))
            logging.info("Player " + self.color + " (" + self.name + ") " + " received " + json.dumps(to_send))
            received = self.connection.recv(1024).decode("ascii")
            logging.info("Player " + self.color + " (" + self.name + ") " + " sent " + received + " to the server")
            response = json.loads(received)
            return response
        except Exception as e:
            logging.info("wait for response: " + e)
            return None

