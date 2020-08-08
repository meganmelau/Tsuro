import os
import sys
import inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import json
from Common.tile import Tile


# Convert from tile index to actual tile class object
class Converter:

    # Tile indices and their corresponding tile configuration provided by professor
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
    [34,[["A","B"],["C","D"],["E","F"],["G","H"]]]'''

    tile_dict = {}
    tiles_list = tiles.splitlines()
    for i in range(len(tiles_list)):
        tile_letter_representation = json.loads(tiles_list[i])[1]
        tile_dict[i] = tile_letter_representation

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
    def convert_letter_to_int(self, letter):
        if letter not in self.letter_int_port:
            raise Exception("Invalid letter port.")
        else:
            return self.letter_int_port[letter]

    # Convert from integer port to letter port
    def convert_int_to_letter(self, integer):
        if integer not in list(self.letter_int_port.values()):
            raise Exception("Invalid integer port.")
        return list(self.letter_int_port.keys())[list(self.letter_int_port.values()).index(integer)]

    # Determines whether given degree is a valid rotation
    def valid_rotation(degree):
        return (degree == 0) or (degree == 90) or (degree == 180) or (degree == 270)

    # Return the tile configuration for given tile index
    def get_representation(self, index):
        tiles_list = self.tiles.splitlines()
        representation = json.loads(tiles_list[index])
        return representation[1]

    # Convert letter representation to integer representation of tile config
    def convert_representation(self, other_representation):
        converted_representation = []
        for path in other_representation:
            converted_path = [self.convert_letter_to_int(path[0]), self.convert_letter_to_int(path[1])]
            converted_representation.append(converted_path)
        return converted_representation

    # Return actual tile object given tile index
    def create_tile(self, tile_index, rotation):
        result = Tile(self.convert_representation(self.get_representation(tile_index)))
        return result.rotate_tile(rotation)

    # Generate a dictionary mapping from tile index to actual tile class object
    def generate_tile_dictionary(self):
        tile_dict = {}
        tiles_list = self.tiles.splitlines()
        for i in range(len(tiles_list)):
            tile_letter_representation = json.loads(tiles_list[i])[1]
            tile_int_representation = self.convert_representation(tile_letter_representation)
            current_tile = Tile(tile_int_representation)
            tile_dict[i] = current_tile
        return tile_dict

    # Return the index of the chosen tile in the given tile dictionary
    def get_equivalent_tile_index(self, chosen_tile):
        for index in range(35):
            if chosen_tile.compare(self.create_tile(index, 0)):
                return index
        return None

    # Return the degree of rotation needed to obtain the chosen tile from the selected tile index
    def get_rotation(self, tile_index, chosen_tile):
        tile_to_rotate = self.create_tile(tile_index, 0)
        rotation = 0
        while not tile_to_rotate.is_equal_paths(chosen_tile.get_paths()):
            rotation += 1
            tile_to_rotate = tile_to_rotate.rotate_90()
        return rotation * 90

    # Get the index and rotation for the given tile
    def get_index_rotation(self, chosen_tile):
        tile_index = self.get_equivalent_tile_index(chosen_tile)
        rotation = self.get_rotation(tile_index, chosen_tile)
        return tile_index, rotation

