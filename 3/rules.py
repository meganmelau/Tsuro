from board import Board


class RuleChecker:

    # Check the validity of initial move
    def valid_initial_move(self, board, target_x, target_y, target_port, tile, given_tiles):
        if not self.is_valid_tile(tile, given_tiles):
            return False
        try:
            current_tile = board.get_tile(target_x, target_y)
        except:
            return False
        if len(current_tile.get_paths()) == 0:
            surroundings = board.get_surrounding_tiles(target_x, target_y)
            for surrounding in surroundings :
                if len(surrounding.get_paths()) != 0:
                    return False

            if self.is_on_edge(target_x, target_y, target_port):
                if self.is_suicidal(board, tile, given_tiles, target_x, target_y, target_x, target_y, target_port):
                    return not self.has_other_options(board, target_x, target_y, target_x, target_y, target_port, given_tiles)
                else:
                    return True
        return False

    # Check validity of intermediate moves
    def valid_move(self, board, target_x, target_y, tile, given_tiles, player_x, player_y, player_port):
        if not self.is_valid_tile(tile, given_tiles):
            return False
        try:
            current_tile = board.get_tile(target_x, target_y)
        except:
            return False
        if not len(current_tile.get_paths()) == 0:
            return False
        proper_tile_position = board.get_next_tile(player_x, player_y, player_port)
        if target_x == proper_tile_position[0] and target_y == proper_tile_position[1]:
            if self.is_suicidal(board, tile, target_x, target_y, player_x, player_y, player_port):
                return not self.has_other_options(board, target_x, target_y, player_x, player_y, player_port, given_tiles)
            else:
                return True
        return False

    # Determine if any players have won the game (allow joint winners)
    def who_won(self, previous_players, current_players):
        if len(current_players) == 1:
            return list(current_players[0])
        elif len(current_players) == 0:
            return previous_players
        else:
            return False

    # Determine if the given position is off the board
    def is_off_board(self, board, x, y, port):
        return board.is_on_edge(x, y, port)

    # Determine if there is more than one player at the given position
    def has_collided(self, board, x, y, port):
        return len(board.get_tile(x, y).get_occupants(port)) > 1

    # Determine if the given player lost the game
    def has_lost(self, board, avatar):
        avatar_position = board.get_player(avatar)
        return self.has_collided(board, avatar_position[0], avatar_position[1], avatar_position[2]) or \
               self.is_off_board(board, avatar_position[0], avatar_position[1], avatar_position[2])

    # Determine if the attempted move is going to make the player lose
    def is_suicidal(self, board, tile, target_x, target_y, player_x, player_y, player_port):
        temp_board = Board(board.get_grid(), board.get_players())
        temp_board.add_tile(tile, target_x, target_y)
        end_position = temp_board.get_path(player_x, player_y, player_port)
        if not end_position:
            raise Exception("Invalid port given")
        temp_board.add_player("rulechecker", end_position[0], end_position[1], end_position[2])
        return self.has_lost(temp_board, "rulechecker")

    # Determine if the player has other option that's not suicidal
    def has_other_options(self, board, target_x, target_y, player_x, player_y, player_port, given_tiles):
        for given_tile in given_tiles:
            temp_tile = given_tile
            for x in range(0, 4):
                if not self.is_suicidal(board, temp_tile, target_x, target_y, player_x, player_y, player_port):
                    return True
                else:
                    temp_tile = temp_tile.rotate90()
        return False

    # Determine if the tile returned actually is from the list of given tiles
    def is_valid_tile(self, tile, given_tiles):
        for given_tile in given_tiles:
            if tile.compare(given_tile):
                return True
        return False