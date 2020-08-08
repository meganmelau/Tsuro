#!/usr/bin/env python3


# A class to represent a tile on Tsuro board game
class Tile:

    def __init__(self, paths):
        # Check for valid port
        flatten_list_of_ports = [port for conn in paths for port in conn]
        for port in flatten_list_of_ports:
            if port < 0 or port > 7:
                raise Exception("Invalid port number out of range [0, 7].")
        if len(flatten_list_of_ports) != len(set(flatten_list_of_ports)):
            raise Exception("Duplicated port number found.")
        # All paths on the tile
        self.paths = paths
        # Maps port number to an Avatar (string color)
        self.occupied_ports = {}

    # Returns all paths on this tile
    def get_paths(self):
        return self.paths

    # Returns the map occupied_ports
    def get_occupied_ports(self):
        return self.occupied_ports

    # Compare if the given tile is equivalent to this tile
    def compare(self, other_tile):
        tile_to_compare = other_tile
        for x in range(4):
            if self.is_equal_paths(tile_to_compare.get_paths()):
                return True
            tile_to_compare = tile_to_compare.rotate_90()
        return False

    # Determines if the given paths are equivalent to the paths on this tile
    def is_equal_paths(self, other_paths):
        for connection in self.paths:
            is_same_connection = False
            for path in other_paths:
                if self.is_equal_connection(connection, path):
                    is_same_connection = True
            if not is_same_connection:
                return False
        return True

    # Determines if the two connections are equivalent
    def is_equal_connection(self, first_connect, second_connect):
        return (first_connect[0] == second_connect[0] and first_connect[1] == second_connect[1]) \
            or (first_connect[0] == second_connect[1] and first_connect[1] == second_connect[0])

    # get the connected port
    def get_path(self, port):
        if port not in range(0, 8):
            return None
        for connection in self.paths:
            if port == connection[0]:
                return connection[1]
            elif port == connection[1]:
                return connection[0]

    # Determines whether a port is occupied by an avatar
    def is_occupied(self, port):
        return (port in self.occupied_ports) and (len(self.occupied_ports[port]) > 0)

    # Return all occupants in given port
    def get_occupants(self, port):
        if self.is_occupied(port):
            return self.occupied_ports[port]
        else:
            return []

    # Creates a new tile with same paths as this tile rotated clockwise 90 degrees
    def rotate_90(self):
        new_path = []
        for connection in self.paths:
            new_connection = [(connection[0] + 2) % 8, (connection[1] + 2) % 8]
            new_path.append(new_connection)
        return Tile(new_path)

    # Rotate tile with given degree
    def rotate_tile(self, degree):
        temp_tile = self
        if degree not in [0, 90, 180, 270]:
            raise Exception("Invalid degree of rotation")
        for i in range(degree//90):
            temp_tile = temp_tile.rotate_90()
        return temp_tile

    # Adds an avatar to the given port if it's not yet occupied
    # Returns true if avatar was added successfully, false if not
    def add_avatar(self, avatar, port):
        if port in range(0, 8):
            if not self.is_occupied(port):
                self.occupied_ports[port] = [avatar]
            else:
                self.occupied_ports[port].append(avatar)
            return True
        else:
            return None

    # Remove the given avatar from this tile if it exists
    # Returns true if avatar was removed successfully, false if not
    def remove_avatar(self, avatar):
        for key in self.occupied_ports.keys():
            if avatar in self.occupied_ports[key]:
                self.occupied_ports[key].remove(avatar)
                return True
        return None

    # Determine if this tile if empty
    def is_empty(self):
        return len(self.get_paths()) == 0
