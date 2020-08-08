import sys
import json
import tile

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


if __name__ == "__main__":
    for json_input in sys.stdin:
        try:
            input_list = json.loads(json_input)
        except json.decoder.JSONDecodeError:
            print("Invalid JSON input, terminating.")
            sys.exit(0)

        tile_index = input_list[0]
        rotation_degree = input_list[1]
        port_letter = input_list[2]
        if (len(input_list) != 3) or (not isinstance(tile_index, int)) or (tile_index not in range(0, 35)) or \
                (not isinstance(port_letter, str)) or (port_letter not in letter_int_port.keys()) or \
                (not valid_rotation(rotation_degree)):
            # Allow user to type another json input
            print("Invalid input format. Please provide [tile_index, degrees, port]",
                  "tile_index within range [0, 34]",
                  "degrees is in [0, 90, 180, 270]",
                  "port is in [\"A\",\"B\",\"C\",\"D\",\"E\",\"F\",\"G\",\"H\"]")
        else:
            exit_port_letter = get_exit_port(tile_index, rotation_degree, port_letter)
            print(json.dumps(["if ", port_letter, " is the entrance, ", exit_port_letter, " is the exit."]))






