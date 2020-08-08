import sys
import json
import tile
import board
import rules

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

rule_checker = rules.RuleChecker()

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
    target_tile = tile.Tile(tile_config)
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
        current_tile = tile.Tile(tile_int_representation)
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


# Verify initial placement JSON
def is_valid_initial_placement(placement_json):
    tile_index = placement_json[0]
    rotation = placement_json[1]
    color = placement_json[2]
    port = placement_json[3]
    x = placement_json[4]
    y = placement_json[5]
    return (tile_index in range(35)) and (valid_rotation(rotation)) and (color in valid_colors) and\
           (port in letter_int_port.keys()) and (x in range(10)) and (y in range(10))


# Verify intermediate placement JSON
def is_valid_inter_placement(placement_json):
    color = placement_json[0]
    tile_index = placement_json[1]
    rotation = placement_json[2]
    x = placement_json[3]
    y = placement_json[4]
    return (tile_index in range(35)) and (valid_rotation(rotation)) and (color in valid_colors) and \
           (x in range(10)) and (y in range(10))

def parse_move(board, placement_json):
    if (len(placement_json) == 6) and (is_valid_initial_placement(placement_json)):
        return execute_initial_placement(board, placement_json)
    elif (len(placement_json) == 5) and (is_valid_inter_placement(placement_json)):
        return execute_inter_placement(board, placement_json)
    else:
        return False

def execute_initial_placement(board, initial_placement):
    # Check valid with rulechecker???
    rotated_tile = tiles_dict[initial_placement[0]]
    rotation = initial_placement[1]
    color = initial_placement[2]
    port = convert_letter_to_int(initial_placement[3])
    x = initial_placement[4]
    y = initial_placement[5]
    for i in range(rotation // 90):
        rotated_tile = rotated_tile.rotate_90()
    try:
        board.add_initial_tile(rotated_tile, x, y, port)
        #board.add_player(color, x, y, port)
        end_position = board.get_path(x, y, port)
        #board.remove_player(color, x, y)
        board.add_player(color, end_position[0], end_position[1], end_position[2])
        return True
    except Exception as e:
        return False

def execute_inter_placement(board, inter_placement):
    # Check valid with rulechecker???
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
        # First need to move player to tile just placed
        player_next_position = board.get_next_tile(player_current_position[0],
                                                   player_current_position[1], player_current_position[2])
        end_position = board.get_path(player_next_position[0], player_next_position[1], player_next_position[2])
        board.remove_player(color, player_current_position[0], player_current_position[1])
        board.add_player(color, end_position[0], end_position[1], end_position[2])
        return True
    except:
        return False


def get_result(board):
    player_positions = board.get_players()
    results = []
    for color in valid_colors:
        if color not in player_positions.keys():
            results.append([color, " never played"])
        else:
            position = player_positions[color]
            if rule_checker.is_off_board(board, position[0], position[1], position[2]):
                results.append([color, " exited"])
            elif rule_checker.has_collided(board, position[0], position[1], position[2]):
                results.append([color, " collided"])
            else:
                end_position = board.get_player(color)
                tile_at = board.get_tile(end_position[0], end_position[1])
                tile_index, tile_rotation = get_index_rotation(tile_at)
                letter_port = convert_int_to_letter(end_position[2])
                results.append([color, tile_index, tile_rotation, letter_port, end_position[0], end_position[1]])
    return results


if __name__ == "__main__":
    game_board = board.Board()
    json_inputs = sys.stdin.readlines()
    json_array = json.loads(''.join(json_inputs))
    json_outputs = []
    for placement_json in json_array:
        if not parse_move(game_board, placement_json):
            raise Exception("Invalid placement.")
        else:
            json_outputs.extend(get_result(game_board))
    print(json.dumps(json_outputs))
