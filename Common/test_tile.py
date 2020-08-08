import unittest
tile = __import__("tile")

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.tile1 = tile.Tile([[0, 1], [2, 3], [4, 5], [6, 7]])
        self.tile2 = tile.Tile([[1, 6], [0, 2], [3, 7], [4, 5]])
        # Same orientation with connections in different order
        self.tile3 = tile.Tile([[4, 5], [6, 1], [2, 0], [7, 3]])
        # Same tile rotated 90 degree
        self.tile4 = tile.Tile([[3, 0], [2, 4], [5, 1], [6, 7]])
        # Same tile rotated 180 degree
        self.tile5 = tile.Tile([[5, 2], [4, 6], [7, 3], [0, 1]])
        # Rotated 270
        self.tile6 = tile.Tile([[7, 4], [6, 0], [1, 5], [2, 3]])
        
    def test_create_tile(self):
        self.assertEqual(self.tile1.get_path(0), 1)
        self.assertEqual(self.tile1.get_path(1), 0)
        self.assertEqual(self.tile1.get_path(4), 5)
        self.assertEqual(self.tile1.get_path(7), 6)

    def test_add_avatar(self):
        white = self.tile1.add_avatar("white", 5)
        black = self.tile1.add_avatar("black", 4)
        red = self.tile1.add_avatar("red", 4)
        self.assertEqual(white, True)
        self.assertEqual(black, True)
        self.assertEqual(red, True)
        self.assertEqual(self.tile1.is_occupied(5), True)
        self.assertEqual(self.tile1.is_occupied(4), True)
        self.assertEqual(self.tile1.is_occupied(2), False)
        
    def test_remove_avatar(self):
        white = self.tile1.add_avatar("white", 5)
        black = self.tile1.add_avatar("black", 4)
        red = self.tile1.add_avatar("red", 4)
        remove_white = self.tile1.remove_avatar("white")
        remove_black = self.tile1.remove_avatar("black")
        remove_red = self.tile1.remove_avatar("red")
        remove_black_again = self.tile1.remove_avatar("black")
        self.assertEqual(self.tile1.is_occupied(5), False)
        self.assertEqual(self.tile1.is_occupied(4), False)
        self.assertEqual(remove_white, True)
        self.assertEqual(remove_black, True)
        self.assertEqual(remove_red, True)
        self.assertEqual(remove_black_again, False)

    def test_is_equal_connection(self):
        conn1 = [1, 2]
        conn2 = [2, 1]
        conn3 = [4, 7]
        conn4 = [7, 3]
        conn5 = [4, 7]
        self.assertEqual(self.tile1.is_equal_connection(conn1, conn2), True)
        self.assertEqual(self.tile1.is_equal_connection(conn2, conn1), True)
        self.assertEqual(self.tile1.is_equal_connection(conn3, conn5), True)
        self.assertEqual(self.tile1.is_equal_connection(conn3, conn4), False)
        self.assertEqual(self.tile1.is_equal_connection(conn5, conn4), False)

    def test_rotate(self):
        rotated = self.tile2.rotate_90()
        self.assertEqual(self.tile4.is_equal_paths(rotated.get_paths()), True)
        rotated = rotated.rotate_90()
        self.assertEqual(self.tile5.is_equal_paths(rotated.get_paths()), True)
        rotated = rotated.rotate_90()
        self.assertEqual(self.tile6.is_equal_paths(rotated.get_paths()), True)
        rotated = rotated.rotate_90()
        self.assertEqual(self.tile3.is_equal_paths(rotated.get_paths()), True)
        self.assertEqual(self.tile2.is_equal_paths(rotated.get_paths()), True)

    def test_compare(self):
        self.assertEqual(self.tile1.compare(self.tile2), False)
        self.assertEqual(self.tile2.compare(self.tile3), True)
        self.assertEqual(self.tile2.compare(self.tile4), True)
        self.assertEqual(self.tile2.compare(self.tile5), True)
        self.assertEqual(self.tile2.compare(self.tile6), True)
        self.assertEqual(self.tile3.compare(self.tile6), True)
        self.assertEqual(self.tile5.compare(self.tile1), False)

if __name__ == '__main__':
    unittest.main()
