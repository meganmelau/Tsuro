import os
import sys
import inspect
import socket
import json
import argparse
import logging
from signal import signal, SIGINT
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from Common.tile import Tile
from Common.tile_conversion import Converter
from Player.player import DumbPlayer, LessDumbPlayer
from Common.position import Position

# Handler for when Ctrl + C is input
def quit_handler(signal_received, frame):
    print("Quitting")
    exit(0)

class TsuroClient:

    def __init__(self, name, strategy, address, port):
        self.player = None
        self.name = name
        self.strategy = strategy
        self.address = address
        self.port = port
        self.color = None
        self.other_colors = None
        self.converter = Converter()
        self.connection = None

    # function to determine what to do with json from the server
    def parse_json(self, json):
        message_type = json[0]
        if message_type == "setup":
            return self.handle_setup(json)
        elif message_type == "initial move request":
            return self.handle_initial_move_request(json)
        elif message_type == "intermediate move request":
            return self.handle_intermediate_move_request(json)
        elif message_type == "board update":
            if len(json) == 2:
                return self.handle_board_position_update(json)
            else:
                return self.handle_board_placement_update(json)
        elif message_type == "game over":
            return self.handle_game_over(json)
        else:
            raise Exception("Not a valid request")

    def handle_setup(self, setup_message):
        logging.info("CLIENT for " + self.name + " handle set up")
        if len(setup_message) != 2:
            raise Exception("bad setup message")
        if isinstance(setup_message[1], str):
            self.create_player(setup_message[1])
        elif isinstance(setup_message[1], list):
            self.other_colors = setup_message[1]
        return

    def create_player(self, color):
        logging.info("CLIENT for " + self.name + " create player")
        if self.strategy == "dumb":
            self.player = DumbPlayer(self.name, color)
        elif self.strategy == "less_dumb":
            self.player = LessDumbPlayer(self.name, color)
        else:
            raise Exception("strategy not supported")

    def handle_game_over(self, game_over_message):
        logging.info("CLIENT for " + self.name + " handle game over")
        return game_over_message[1]

    # Called by parse_json to handle an initial move request
    def handle_initial_move_request(self, init_move_request):
        logging.info("CLIENT for " + self.name + " handle initial move request " + json.dumps(init_move_request))
        if len(init_move_request) != 4:
            raise Exception("invalid initial move request")
        tiles = list()
        for tile in init_move_request[1:]:
            if not isinstance(tile, int):
                raise Exception("invalid initial move request")
            tiles.append(self.converter.create_tile(tile, 0))
        player_move = ["initial move respond"]
        player_move.extend(self.player.select_initial_move(tiles))
        return player_move

    # Called by parse_json to handle an intermediate move request
    def handle_intermediate_move_request(self, intermediate_move_request):
        logging.info("CLIENT for " + self.name + " handle intermediate move request "
                     + json.dumps(intermediate_move_request))
        if len(intermediate_move_request) != 3:
            raise Exception("invalid intermediate move request")
        tiles = list()
        for tile in intermediate_move_request[1:]:
            if not isinstance(tile, int):
                raise Exception("invalid intermediate move request")
            tiles.append(self.converter.create_tile(tile, 0))
        player_move = ["intermediate move respond"]
        player_move.extend(self.player.select_move(tiles))
        return player_move

    # Called by parse_json to handle a board placement update
    def handle_board_placement_update(self, board_placement_update):
        logging.info("CLIENT for " + self.name + " handle board placement update")
        if not self.is_valid_board_placement_update(board_placement_update):
            raise Exception("invalid board placement update")
        update_tile = self.converter.create_tile(board_placement_update[2], board_placement_update[3])
        self.player.update_board_placement(board_placement_update[1], update_tile, board_placement_update[4], board_placement_update[5])
        return None

    # Called by parse_json to handle a board position update
    def handle_board_position_update(self, board_position_update):
        logging.info("CLIENT for " + self.name + " handle board position update")
        if not (len(board_position_update) == 2 and isinstance(board_position_update[1], list)):
            raise Exception("invalid board position update")
        new_positions = {}
        for new_position in board_position_update[1]:
            new_positions[new_position["color"]] = Position(new_position["position"][0], new_position["position"][1], new_position["position"][2])
        self.player.update_board_positions(new_positions)
        return None

    def is_valid_board_placement_update(self, board_placement_update):
        if len(board_placement_update) != 6:
            return False
        elif not (isinstance(board_placement_update[2], int) and board_placement_update[2] in range(0, 35)):
            return False
        elif not isinstance(board_placement_update[3], int):
            return False
        elif not isinstance(board_placement_update[4], int):
            return False
        elif not isinstance(board_placement_update[5], int):
            return False
        else:
            return True

    # Called to send a connect message to the server at the given address over the given port
    def start_up(self):
        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((self.address, self.port))
        except socket.timeout:
            raise Exception("Not able to connect on given address and port")
        connect_message = ["tsuro-connect", self.name]
        send_message = json.dumps(connect_message) + "\n"
        self.connection.send(send_message.encode("ascii"))

    # Called to listen for a message from the server
    def listen_for_server(self):
        try:
            server_message = json.loads(self.connection.recv(1024).decode("ascii"))
            logging.info("CLIENT for " + self.name + " received from server " + json.dumps(server_message))
            response = self.parse_json(server_message)
            if response:
                logging.info("CLIENT for " + self.name + " will send " + json.dumps(response))
                if isinstance(response[0], str):
                    logging.info("CLIENT for " + self.name + " sent to server " + json.dumps(response))
                    self.connection.sendall(json.dumps(response).encode("ascii"))
                    return None
                else:
                    return response
        except socket.timeout:
            pass


if __name__ == "__main__":
    signal(SIGINT, quit_handler)

    parser = argparse.ArgumentParser()
    parser.add_argument("address", help="The IP address of the Tsuro server")
    parser.add_argument("port", type=int, help="The port number to connect to on the Tsuro server")
    parser.add_argument("name", help="The player's name")
    parser.add_argument("strategy", help="The player's strategy")

    args = parser.parse_args()

    logging.basicConfig(filename="xclient.log", level=logging.DEBUG, format='\n%(asctime)s \n%(message)s')

    client = TsuroClient(args.name, args.strategy, args.address, args.port)
    client.start_up()
    game_going = True
    while game_going:
        status = client.listen_for_server()
        if status:
            print(status)
            game_going = False
