#!/usr/bin/env python3
import time
from tkinter import Tk, Canvas, Frame, BOTH


# A class to represent a tile on Tsuro board game
class Tile(Frame):
    # Canvas offset
    position = 30
    # All paths on the tile
    paths = []
    # Maps port number to an Avatar (string color)
    occupied_ports = {}
    # Coordinates to graphically draw each port
    ports_coordinates = []

    def __init__(self, paths):
        # Check for valid port
        flatten_list_of_ports = [port for conn in paths for port in conn]
        for port in flatten_list_of_ports:
            if port < 0 or port > 7:
                raise Exception("Invalid port number out of range [0, 7].")
        if len(flatten_list_of_ports) != len(set(flatten_list_of_ports)):
            raise Exception("Duplicated port number found.")
        super().__init__()
        self.position = 30
        self.paths = paths
        self.occupied_ports = {}
        self.ports_coordinates = [[self.position + 50, self.position],\
                                  [self.position + 150, self.position],\
                                  [self.position + 200, self.position + 50],\
                                  [self.position + 200, self.position + 150],\
                                  [self.position + 150, self.position + 200],\
                                  [self.position + 50, self.position + 200],\
                                  [self.position, self.position + 150],\
                                  [self.position, self.position + 50]]
        self.initUI()

    # Initialize graphical display
    def initUI(self):
        self.master.title("Lines")
        self.pack(fill=BOTH, expand=1)

    # Returns all paths on this tile
    def get_paths(self):
        return self.paths

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
        if port not in range(0,8):
            return False
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

    # Adds an avatar to the given port if it's not yet occupied
    def add_avatar(self, avatar, port):
        if port in range(0,8):
            if not self.is_occupied(port):
                self.occupied_ports[port] = [avatar]
            else:
                self.occupied_ports[port].append(avatar)
            return True
        else:
            return False

    # Remove the given avatar from this tile if it exists
    def remove_avatar(self, avatar):
        for key in self.occupied_ports.keys():
            if avatar in self.occupied_ports[key]:
                self.occupied_ports[key].remove(avatar)
                return True
        return False

    # Draw each port graphically
    def draw_ports(self, canvas):
        x = self.position
        y = self.position
        
        canvas.create_oval(x + 45, y - 5, x + 55, y + 5)
        canvas.create_oval(x + 145, y - 5, x + 155, y + 5)

        canvas.create_oval(x + 195, y + 45, x + 205, y + 55)
        canvas.create_oval(x + 195, y + 145, x + 205, y + 155)

        canvas.create_oval(x + 45, y + 195, x + 55, y + 205)
        canvas.create_oval(x + 145, y + 195, x + 155, y + 205)

        canvas.create_oval(x - 5, y + 45, x + 5, y + 55)
        canvas.create_oval(x - 5, y + 145, x + 5, y + 155)

    # Draw paths between ports
    def draw_paths(self, canvas):
        midpoint = [self.position + 100, self.position + 100]

        for path in self.paths:
            start_x = self.ports_coordinates[path[0]][0]
            start_y = self.ports_coordinates[path[0]][1]
            end_x = self.ports_coordinates[path[1]][0]
            end_y = self.ports_coordinates[path[1]][1]
            
            canvas.create_line(start_x, start_y, midpoint[0], midpoint[1], end_x, end_y, smooth="true")

    # Draw avatar on corresponding port
    def draw_players(self, canvas):
        for port in self.occupied_ports:
            start_x = self.ports_coordinates[port][0]
            start_y = self.ports_coordinates[port][1]
            
            canvas.create_polygon(start_x - 10, start_y + 10, start_x, start_y - 10, start_x + 10, start_y + 10, fill=self.occupied_ports[port])

    # Graphically render the tile
    def render_tile(self):
        canvas = Canvas(self)
        
        canvas.create_rectangle(self.position, self.position, self.position + 200, self.position + 200)

        self.draw_ports(canvas)
        self.draw_paths(canvas)
        self.draw_players(canvas)

        canvas.pack(fill=BOTH, expand=1)


# Given list of port numbers on a tile, creates a generator for all possible tile configurations
def all_tile_config(list_of_ports):
    if len(list_of_ports) < 2:
        yield []
        return
    else:
        a = list_of_ports[0]
        for i in range(1, len(list_of_ports)):
            pair = (a, list_of_ports[i])
            for rest in all_tile_config(list_of_ports[1:i] + list_of_ports[i + 1:]):
                yield [pair] + rest


# Creates a list of all unique tiles
def generate_unique_tiles():
    unique_tiles = []
    for x in all_tile_config([0, 1, 2, 3, 4, 5, 6, 7]):
        temp_tile = Tile(x)
        is_unique = True
        for tile in unique_tiles:
            if temp_tile.compare(tile):
                is_unique = False
        if is_unique:
            unique_tiles.append(temp_tile)
    return unique_tiles


def main():
    # example render
    root = Tk()
    tile = Tile([[0, 1], [2, 3], [4, 5], [6, 7]])
    tile.add_avatar("blue", 3)
    tile.render_tile()
    root.geometry("250x250+300+300")
    root.mainloop()

    # Generates all unique tile configuration
    unique_tiles = generate_unique_tiles()
    for x in unique_tiles:
        print(x.get_paths())


if __name__ == '__main__':
    main()


