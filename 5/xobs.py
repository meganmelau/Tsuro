import os
import sys
import inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import sys
import json
from tkinter import Tk, Canvas, Frame, BOTH
from Admin.observer import Observer
from Common.board import Board
from Common.tile import Tile
from Common.position import Position

# Tile indices and their corresponding tile configuration
tiles = \
'''[0,[["A","E"],["B","F"],["C","H"],["D","G"]]]
[1,[["A","E"],["B","F"],["C","G"],["D","H"]]]
[2,[["A","F"],["B","E"],["C","H"],["D","G"]]]
[3,[["A","E"],["B","D"],["C","G"],["F","H"]]]
[4,[["A","H"],["B","C"],["D","E"],["F","G"]]]
[5,[["A","E"],["B","C"],["D","H"],["F","G"]]]
[6,[["A","E"],["B","C"],["D","G"],["F","H"]]]
[7,[["A","D"],["B","G"],["C","F"],["E","H"]]]
[8,[["A","D"],["B","F"],["C","G"],["E","H"]]]
[9,[["A","D"],["B","E"],["C","H"],["F","G"]]]
[10,[["A","D"],["B","E"],["C","G"],["F","H"]]]
[11,[["A","D"],["B","C"],["E","H"],["F","G"]]]
[12,[["A","C"],["B","H"],["D","F"],["E","G"]]]
[13,[["A","C"],["B","H"],["D","E"],["F","G"]]]
[14,[["A","C"],["B","G"],["D","F"],["E","H"]]]
[15,[["A","C"],["B","G"],["D","E"],["F","H"]]]
[16,[["A","C"],["B","F"],["D","H"],["E","G"]]]
[17,[["A","C"],["B","F"],["D","G"],["E","H"]]]
[18,[["A","C"],["B","E"],["D","H"],["F","G"]]]
[19,[["A","C"],["B","E"],["D","G"],["F","H"]]]
[20,[["A","C"],["B","D"],["E","H"],["F","G"]]]
[21,[["A","C"],["B","D"],["E","G"],["F","H"]]]
[22,[["A","B"],["C","H"],["D","G"],["E","F"]]]
[23,[["A","B"],["C","H"],["D","F"],["E","G"]]]
[24,[["A","B"],["C","H"],["D","E"],["F","G"]]]
[25,[["A","B"],["C","G"],["D","H"],["E","F"]]]
[26,[["A","B"],["C","G"],["D","F"],["E","H"]]]
[27,[["A","B"],["C","G"],["D","E"],["F","H"]]]
[28,[["A","B"],["C","F"],["D","H"],["E","G"]]]
[29,[["A","B"],["C","F"],["D","G"],["E","H"]]]
[30,[["A","B"],["C","E"],["D","H"],["F","G"]]]
[31,[["A","B"],["C","E"],["D","G"],["F","H"]]]
[32,[["A","B"],["C","D"],["E","H"],["F","G"]]]
[33,[["A","B"],["C","D"],["E","G"],["F","H"]]]
[34,[["A","B"],["C","D"],["E","F"],["G","H"]]]
'''

valid_colors = ["white", "black", "red", "green", "blue"]

# Map from letter port to integer port representation
letter_int_port = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4,
    "F": 5,
    "G": 6,
    "H": 7
}


# Convert from letter port to integer port
def convert_letter_to_int(letter):
    if letter not in letter_int_port:
        raise Exception("Invalid letter port.")
    else:
        return letter_int_port[letter]


# Convert from integer port to letter port
def convert_int_to_letter(integer):
    if integer not in list(letter_int_port.values()):
        raise Exception("Invalid integer port.")
    return list(letter_int_port.keys())[list(letter_int_port.values()).index(integer)]


# Determines whether given degree is a valid rotation
def valid_rotation(degree):
    return (degree == 0) or (degree == 90) or (degree == 180) or (degree == 270)


# Return the tile configuration for given tile index
def get_representation(index):
    tiles_list = tiles.splitlines()
    representation = json.loads(tiles_list[index])
    return representation[1]


# Convert letter representation to integer representation of tile config
def convert_representation(other_representation):
    converted_representation = []
    for path in other_representation:
        converted_path = [convert_letter_to_int(path[0]), convert_letter_to_int(path[1])]
        converted_representation.append(converted_path)
    return converted_representation


# Return the exit port letter given the entry port letter
def get_exit_port(index, rotate_degree, entry_port):
    tile_config = convert_representation(get_representation(index))
    target_tile = Tile(tile_config)
    rotation_time = rotate_degree // 90
    for i in range(rotation_time):
        target_tile = target_tile.rotate_90()
    exit_port = target_tile.get_path(convert_letter_to_int(entry_port))
    return convert_int_to_letter(exit_port)


def generate_tile_dictionary():
    tile_dict = {}
    tiles_list = tiles.splitlines()
    for i in range(len(tiles_list)):
        tile_letter_representation = json.loads(tiles_list[i])[1]
        tile_int_representation = convert_representation(tile_letter_representation)
        current_tile = Tile(tile_int_representation)
        tile_dict[i] = current_tile
    return tile_dict


# Dictionary mapping index to a tile class representation
tiles_dict = generate_tile_dictionary()


# Return the index of the chosen tile
def get_equivalent_tile_index(chosen_tile):
    for key, val in tiles_dict.items():
        if chosen_tile.compare(val):
            return key
    return False


# Return the degree of rotation needed to obtain the chosen tile
def get_rotation(tile_index, chosen_tile):
    tile_to_rotate = tiles_dict[tile_index]
    rotation = 0
    while not tile_to_rotate.is_equal_paths(chosen_tile.get_paths()):
        rotation += 1
        tile_to_rotate = tile_to_rotate.rotate_90()
    return rotation * 90


# Get the index and rotation for the given tile
def get_index_rotation(chosen_tile):
    tile_index = get_equivalent_tile_index(chosen_tile)
    rotation = get_rotation(tile_index, chosen_tile)
    return tile_index, rotation

def parse_move(board, placement_json):
    if (len(placement_json) == 6):
        return execute_initial_placement(board, placement_json)
    elif (len(placement_json) == 5):
        return execute_inter_placement(board, placement_json)
    else:
        return False

def execute_initial_placement(board, initial_placement):
    rotated_tile = tiles_dict[initial_placement[0]]
    rotation = initial_placement[1]
    color = initial_placement[2]
    port = convert_letter_to_int(initial_placement[3])
    x = initial_placement[4]
    y = initial_placement[5]
    for i in range(rotation // 90):
        rotated_tile = rotated_tile.rotate_90()
    try:
        board.add_initial_tile(rotated_tile, Position(x, y, port))
        connected_port = rotated_tile.get_path(port)
        board.add_player(color, Position(x, y, connected_port))
        return True
    except Exception as e:
        print(e)
        return False

def execute_inter_placement(board, inter_placement):
    color = inter_placement[0]
    rotated_tile = tiles_dict[inter_placement[1]]
    rotation = inter_placement[2]
    x = inter_placement[3]
    y = inter_placement[4]
    for i in range(rotation // 90):
        rotated_tile = rotated_tile.rotate_90()
    try:
        board.add_tile(rotated_tile, x, y)
        player_current_position = board.get_player(color)
        end_position = board.get_path(player_current_position)
        board.remove_player(color, player_current_position.get_x(), player_current_position.get_y())
        board.add_player(color, end_position)
        return True
    except:
        return False


if __name__ == "__main__":
    game_board = Board()
    root = Tk()
    observer = Observer()
    input_content = ''.join(sys.stdin.readlines())
    json_array = json.loads(input_content)
    for placement_json in json_array[:-1]:
        if not parse_move(game_board, placement_json):
            raise Exception("Invalid placement.")

    player_final_move = json_array[-1]

    if len(player_final_move) != 4 and len(player_final_move) != 3:
        parse_move(game_board, player_final_move)
        observer.render_observer(game_board, "jack", list(), False, 0, list())
    else:
        given_tiles = player_final_move[1:]
        index = given_tiles.index(player_final_move[0][1])

        hand = list()

        for tile in given_tiles:
            temp_tile = Tile(convert_representation(get_representation(tile)))
            hand.append(temp_tile)


        if len(player_final_move) == 4:
            player_port = player_final_move[0][5]
        elif len(player_final_move) == 3:
            player_port = 0

        placement = Position(player_final_move[0][3], player_final_move[0][4], player_port)

        observer.render_observer(game_board, player_final_move[0][0], [placement, player_final_move[0][2]],
                                 len(player_final_move) == 4, index, hand)

    root.geometry("750x500+100+100")
    while True:
        try:
            root.update_idletasks()
            root.update()
        except:
            break