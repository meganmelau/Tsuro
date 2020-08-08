#!/usr/bin/env python3
import time
from tkinter import Tk, Canvas, Frame, BOTH

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from Common.board import Board
from Common.tile import Tile
from Common.position import Position
from Player.player import DumbPlayer


# A class to represent a tile on Tsuro board game
class Observer(Frame):

    def __init__(self):
        self.tile_size = 40
        self.board_offset = 20
        super().__init__()
        #self.initUI()

    # Initialize graphical display
    def initUI(self):
        self.master.title("Tsuro Observer")
        self.pack(fill=BOTH, expand=1)

    # returns coordinates to draw the ports at given the x,y position and port number
    def get_port_coordinate(self, tile, port, x, y):
        ax = self.board_offset + x * self.tile_size
        ay = self.board_offset + y * self.tile_size
        bx = self.board_offset + self.tile_size + (x * self.tile_size)
        by = self.board_offset + self.tile_size + (y * self.tile_size)

        port_offset = self.tile_size / 4
        
        if port == 0:
            return [ax + port_offset, ay]
        if port == 1:
            return [ax + 3*port_offset,ay]
        if port == 2:
            return [bx, ay + port_offset]
        if port == 3:
            return [bx, ay + 3*port_offset]
        if port == 4:
            return [ax + 3*port_offset, by]
        if port == 5:
            return [ax + port_offset, by]
        if port == 6:
            return [ax, ay + 3*port_offset]
        if port == 7:
            return [ax, ay + port_offset]
            
        return [0, 0]

    # renders the given hand of tiles, with the chosen hand outlined in red
    def render_hands(self, canvas, tile_index, hands):
        for x in range(len(hands)):
            if x == tile_index:
                self.render_tile(canvas, hands[x], 12 + (x * 2), 5, "red")
            else:
                self.render_tile(canvas, hands[x], 12 + (x * 2), 5, "black")

    # Show the player's move as text
    def show_placement(self, canvas, player_name, player_move, is_initial):
        initial_string = "Player: " + player_name + "\n" + "wants to place at (" \
                           + str(player_move[0].get_x()) + ", " + str(player_move[0].get_y()) + ")"
        if is_initial:
            initial_string += ", port " + str(player_move[0].get_port())
        
        canvas.create_text(580,160,fill="black",font="Times 15 italic bold", \
                           text=initial_string + "\nwith " + str(player_move[1]) + " degree rotation")

    # Draw each port graphically in given tile
    def draw_ports(self, canvas, x, y):
        ax = self.board_offset + x * self.tile_size
        ay = self.board_offset + y * self.tile_size
        bx = self.board_offset + self.tile_size + (x * self.tile_size)
        by = self.board_offset + self.tile_size + (y * self.tile_size)

        port_offset = self.tile_size / 4
        port_radius = self.tile_size / 15

        canvas.create_oval(ax + port_offset - port_radius, ay - port_radius, ax + port_offset + port_radius, ay +
                           port_radius)
        canvas.create_oval(ax + 3*port_offset - port_radius, ay - port_radius, ax + 3*port_offset + port_radius, ay +
                           port_radius)

        canvas.create_oval(bx - port_radius, ay + port_offset - port_radius, bx + port_radius, ay + port_offset +
                           port_radius)
        canvas.create_oval(bx - port_radius, ay + 3*port_offset - port_radius, bx + port_radius, ay + 3*port_offset +
                           port_radius)

        canvas.create_oval(ax + 3*port_offset - port_radius, by - port_radius, ax + 3*port_offset + port_radius, by +
                           port_radius)
        canvas.create_oval(ax + port_offset - port_radius, by - port_radius, ax + port_offset + port_radius, by +
                           port_radius)

        canvas.create_oval(ax - port_radius, ay + 3*port_offset - port_radius, ax + port_radius, ay + 3*port_offset +
                           port_radius)
        canvas.create_oval(ax - port_radius, ay + port_offset - port_radius, ax + port_radius, ay + port_offset +
                           port_radius)

    # Draw paths between ports in given tile
    def draw_paths(self, canvas, tile, x, y):
        ax = self.board_offset + x * self.tile_size
        ay = self.board_offset + y * self.tile_size
        bx = self.board_offset + self.tile_size + (x * self.tile_size)
        by = self.board_offset + self.tile_size + (y * self.tile_size)
        
        midpoint = [(ax + bx) / 2, (ay + by) / 2]

        port_offset = self.tile_size / 4

        for path in tile.get_paths:
            start_position = self.get_port_coordinate(tile, path[0], x, y)
            end_position = self.get_port_coordinate(tile, path[1], x, y)
            
            canvas.create_line(start_position[0], start_position[1], midpoint[0], midpoint[1], end_position[0],
                               end_position[1], smooth="true")

    # Draw avatar on corresponding port in given tile
    def draw_players(self, canvas, tile, x, y):
        for port in tile.get_occupied_ports:
            center = self.get_port_coordinate(tile, port, x, y)
            size = 6
            
            canvas.create_polygon(center[0] - size, center[1] + size, center[0], center[1] - size, center[0] + size,
                                  center[1] + size, fill=tile.occupied_ports[port])

    # renders the given tile placed on (x,y) on the board
    def render_tile(self, canvas, tile, x, y, color):
        canvas.create_rectangle(self.board_offset + x * self.tile_size, \
                                self.board_offset + y * self.tile_size, \
                                self.board_offset + self.tile_size + (x * self.tile_size), \
                                self.board_offset + self.tile_size + (y * self.tile_size), outline=color)

        self.draw_ports(canvas, x, y)
        self.draw_paths(canvas, tile, x, y)
        self.draw_players(canvas, tile, x, y)

    # Labels the indices around the board
    def render_indices(self, canvas):
        for x in range(0, 10):
            canvas.create_text(self.board_offset + .5 * self.tile_size + self.tile_size * x, self.board_offset / 2, fill="black", font="Times 10", \
                           text=str(x))

        for y in range(0, 10):
            canvas.create_text(self.board_offset / 2, self.board_offset + .5 * self.tile_size + self.tile_size * y, fill="black", font="Times 10", \
                           text=str(y))
        

    # renders the Tsuro board, the tiles, and players
    def render_board(self, canvas, board):
        grid = board.get_grid()

        for x in range(0, len(grid[0])):
            for y in range(0, len(grid)):
                tile = board.get_tile(x, y)
                self.render_tile(canvas, tile, x, y, "black")

        self.render_indices(canvas)
                
    # Renders the state of the current game of Tsuro to the observer
    def render_observer(self, board, player_name, player_move, is_initial, tile_index, hand):
        '''
        boolean is_initial
        tile index 0,1,2 if initial or 0,1 if intermediate
        list of tiles (hand)
        player move = [list of position, rotation]
        port is only printed for initial
        player name
        '''

        self.master.title("Tsuro Observer")
        self.pack(fill=BOTH, expand=1)
        canvas = Canvas(self, width=750, height=500)

        self.render_board(canvas, board)
        if len(hand) > 1:
            self.render_hands(canvas, tile_index, hand)
            self.show_placement(canvas, player_name, player_move, is_initial)
        
        canvas.pack(fill=BOTH, expand=1)


def main():
    # example render
    root = Tk()
    observer = Observer()
    
    grid = [[0 for x in range(10)] for y in range(10)]
    for x in range(0, 10):
                for y in range(0, 10):
                    grid[x][y] = Tile([])

    tile1 = Tile([[0, 1], [2, 3], [4, 5], [6, 7]])
    tile2 = Tile([[0, 5], [1, 4], [2, 3], [6, 7]])
    tile3 = Tile([[0, 3], [2, 1], [4, 5], [6, 7]])
    grid[0][0] = tile1
    grid[1][0] = tile2
    grid[0][1] = tile3
    
    board = Board()
    observer.render_observer(board, "marcos", [Position(0, 2, 1), 90], False, 0, [tile1])
    root.geometry("750x500+100+100")
    root.mainloop()

if __name__ == '__main__':
    main()
