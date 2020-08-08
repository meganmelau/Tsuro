from Common.board import Board
from Common.tile import Tile
import unittest

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.b = Board()
        self.tile1 = Tile([[0, 1], [2, 3], [4, 5], [6, 7]])
        self.tile2 = Tile([[1, 6], [0, 2], [3, 7], [4, 5]])
        # Same orientation with connections in different order
        self.tile3 = Tile([[4, 5], [6, 1], [2, 0], [7, 3]])
        # Same tile rotated 90 degree
        self.tile4 = Tile([[3, 0], [2, 4], [5, 1], [6, 7]])
        # Same tile rotated 180 degree
        self.tile5 = Tile([[5, 2], [4, 6], [7, 3], [0, 1]])
        # Rotated 270
        self.tile6 = Tile([[7, 4], [6, 0], [1, 5], [2, 3]])

    def test_initial_tile_add(self):
        print(self.b.get_tile(0, 1).get_paths())
        self.b.add_initial_tile(self.tile1, 0, 1, 6)
        print(self.b.get_tile(0, 1).get_paths())

    def test_initial_tile_add_multiple(self):
        print(self.b.get_tile(0, 1).get_paths())
        print(self.b.get_tile(0, 3).get_paths())
        self.b.add_initial_tile(self.tile1, 0, 1, 6)
        self.b.add_initial_tile(self.tile3, 0, 3, 6)
        print(self.b.get_tile(0, 1).get_paths())
        print(self.b.get_tile(0, 3).get_paths())


if __name__ == '__main__':
    unittest.main()

