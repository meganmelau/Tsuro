import os
import sys
import inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import json
from Admin.referee import Referee
from Common.board import Board
import Common.tile
from Common.tile_conversion import Converter
from Player.player import DumbPlayer
from Common.rules import RuleChecker

color = ["white", "black", "red", "green", "blue"]
if __name__ == "__main__":
    input_content = sys.stdin.readline()
    json_array = json.loads(input_content)
    if len(json_array) > 5 or len(json_array) < 3:
        raise Exception("Must have 3 to 5 players.")
    # Construct players
    player_list = []
    for i in range(len(json_array)):
        player_list.append(DumbPlayer(json_array[i], color[i]))
    game_board = Board()
    rule_checker = RuleChecker()
    deck = Converter().generate_tile_dictionary()
    manager = Referee(player_list, game_board, rule_checker, deck)
    win_order, elimination = manager.run_game()
    print(json.dumps({"winners": win_order, "losers": elimination}))