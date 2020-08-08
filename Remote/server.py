import sys
import os
import inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from Admin.referee import Referee
from Common.board import Board
from Common.rules import RuleChecker
from Common.tile_conversion import Converter
from Player.playerproxy import PlayerProxy
from signal import signal, SIGINT
import socket
import sys
import time
import json
import logging
import logging.handlers

LOG_FILENAME = "xserver.log"

'''
The server should take two optional parameters: an IP address (or hostname) and a port. The
defaults for these parameters are 127.0.0.1 (localhost) and 8000. 

If only one parameter is given, it is the port. 

The server should listen on the specified hostname/port for player client connections.

The minimum number of players is 3. After the first three players connect, the server should wait
for another 30 seconds for two more players. Once 3 to 5 players connect, the server should refuse
any additional connection and should start-up a Tsuro game between a referee and the connected
players
'''


# Handler for when Ctrl + C is input
def quit_handler(signal_received, frame):
    print("Quitting")
    exit(0)

class TsuroServer:

    EOF = "\x04"

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.player_proxies = []
        self.connections = {}
        self.board = Board()
        self.rule_checker = RuleChecker()
        self.referee = None
        self.colors = ["white", "black", "red", "green", "blue"]
        self.deck = Converter().generate_tile_dictionary()
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((ip, int(port)))
        except Exception as e:
            print("Failed Connection, shutting down.", e)
            return
        enough_players = self.wait_for_players()
        if enough_players:
            result = self.start_game()
            self.send_all_players(json.dumps(["game over", result]))
            print(result)

    # wait until there  are 3 players then 30 seconds until max  5 players
    def wait_for_players(self):
        start_time = time.time()
        end_time = start_time + 5*60
        self.socket.settimeout(0.2)
        self.socket.listen()
        # Wait for at most 5 minutes
        while len(self.connections) < 3 and time.time() < end_time:
            self.accept_player()

        logging.info("First round of waiting for players has finished")
        # If not enough players joined after 5 minutes, stop server
        if len(self.connections) < 3:
            logging.info("Did not get enough players for a game of Tsuro, shutting down server")
            return False

        logging.info("Connected with three players, waiting 30 seconds for more")
        # Wait for 30 more seconds for more players to join before starting the game
        start_time = time.time()
        end_time = start_time + 30
        while len(self.connections) < 5 and time.time() < end_time:
            self.accept_player()
        logging.info("Second round of waiting for players has finished")
        return True

    # Accept tcp connection and verify correct player connection message
    def accept_player(self):
        try:
            conn, addr = self.socket.accept()
            received_msg = self.recv_connect_message(conn)
            conn_msg = json.loads(received_msg)
            name = self.process_connect_message(conn_msg)
            logging.info("Player " + name + " has connected")
        except socket.timeout:
            return False
        except Exception as e:
            logging.exception("Failed to connect player after receiving connect message")
            return False
        color = self.colors[len(self.connections)]
        self.connections[color] = [name, conn, addr]
        conn.sendall(json.dumps(["setup", color]).encode("ascii"))
        logging.info("Player " + name + " has been given color " + color)
        return True

    # Receive and return player's connection message
    def recv_connect_message(self, conn):
        total_data = []
        while True:
            data = conn.recv(1024).decode("ascii")
            if '\n' in data:
                total_data.append(data[:data.find('\n')])
                break
            else:
                total_data.append(data)
        return ''.join(total_data)

    # Process player's connection message and return player's name
    def process_connect_message(self, message):
        if len(message) == 2 and message[0] == "tsuro-connect" and isinstance(message[1], str):
            return message[1]
        else:
            logging.exception("Received bad connection message")
            raise Exception("Bad connect message")

    # Starts the game after players join the game
    def start_game(self):
        player_colors = []
        for color, player_info in self.connections.items():
            player_proxy = PlayerProxy(player_info[0], color, player_info[1], player_info[2])
            self.player_proxies.append(player_proxy)
            player_colors.append(color)
        self.referee = Referee(self.player_proxies, self.board, self.rule_checker, self.deck)
        self.send_all_players(json.dumps(["setup", player_colors]))
        logging.info("Running game . . . ")
        return self.referee.run_game()

    # Sends the message to all connected players
    def send_all_players(self, msg):
        for color, player_info in self.connections.items():
            try:
                player_info[1].sendall(msg.encode("ascii"))
                logging.info("Player " + color + " (" + player_info[0] + ") " + "was sent " + msg)
            except Exception as e:
                logging.info("send all players: " + e)
                logging.info("Failed to send message to player " + player_info[0])

if __name__ == "__main__":
    signal(SIGINT, quit_handler)
    ip = "127.0.0.1"
    port = "8000"
    arguments = len(sys.argv) - 1

    if arguments == 1:
        port = sys.argv[1]
    elif arguments == 2:
        ip = sys.argv[1]
        port = sys.argv[2]

    logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG, format='\n%(asctime)s \n%(message)s')
    logging.info("==========================NEW ROUND STARTED==========================")
    logging.info('Started up server')
    server = TsuroServer(ip, port)
    logging.info("==========================ROUND ENDED==========================\n")
