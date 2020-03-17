import numpy as np
from .bots import Bot
from .valid_inputs import *


class Board:

    def __init__(self, board_size):
        self.grid = np.ones((board_size, board_size), dtype=int)
        self.grid[1:-1, 1:-1] = 0
        self.grid = self.grid.tolist()

    def clone(self, replace_dict):
        cpy = Board(len(self.grid))
        for i in range(0, len(self.grid)):
            for j in range(0, len(self.grid)):
                gval = self.grid[i][j]
                if gval in replace_dict:
                    gval = replace_dict[gval]
                cpy.grid[i][j] = gval

        return cpy

    # get cell at (x, y)
    def get(self, x, y):
        try:
            cell = self.grid[x][y]
        except:
            cell = None
        return cell

    # Set the position of bot to (x, y)
    # Must be passed an object of class Bot, of course
    def set(self, entity, x, y):
        # Only attempt to set current position to 0 if entity is already on the board
        # This becomes irrelevant if bots are only ever instantiated in valid locations
        if self.currently_on_board(entity.pos_x, entity.pos_y):
            self.grid[entity.pos_x][entity.pos_y] = 0
            entity.pos_x = x
            entity.pos_y = y
            self.grid[x][y] = entity  # set new tile on grid to occupied
        else:
            entity.pos_x = x
            entity.pos_y = y
            self.grid[x][y] = entity

    # Check if a set of coordinates is on the board
    def currently_on_board(self, x, y):
        return not (x > len(self.grid)-1 or x < 0 or y > len(self.grid)-1 or y < 0)

    # Get a list of valid directional moves for bot
    def get_valid_moves(self, bot):
        valid_moves = []

        if self.grid[bot.pos_y-1][bot.pos_x] == 0:
            valid_moves.append(DIRECTION_LEFT)

        if self.grid[bot.pos_y + 1][bot.pos_x] == 0:
            valid_moves.append(DIRECTION_RIGHT)

        if self.grid[bot.pos_y][bot.pos_x-1] == 0:
            valid_moves.append(DIRECTION_UP)

        if self.grid[bot.pos_y][bot.pos_x + 1] == 0:
            valid_moves.append(DIRECTION_DOWN)

        return valid_moves

    def resolve_moves(self, bot1, direction1, bot2, direction2):
        bot1_move = self.resolve_move(bot1, direction1)
        bot2_move = self.resolve_move(bot2, direction2)

        # If the two spaces where they're moving to is not the same, move them there
        if bot1_move != bot2_move:
            self.set(bot1, bot1_move[0], bot1_move[1])
            self.set(bot2, bot2_move[0], bot2_move[1])

        # If the bots are moving to the same space, move only the one with heavier weight
        else:
            if bot1.weight >= bot2.weight:
                self.set(bot1, bot1_move[0], bot1_move[1])
            else:
                self.set(bot2, bot2_move[0], bot2_move[1])

    def resolve_move(self, bot, direction):

        if direction == DIRECTION_LEFT and bot.pos_y > 1 and self.grid[bot.pos_x][bot.pos_y-1] == 0:  # LEFT
            next_pos = (bot.pos_x, bot.pos_y - 1)
        elif direction == DIRECTION_DOWN and bot.pos_x < len(self.grid) - 2 and self.grid[bot.pos_x+1][bot.pos_y] == 0:  # DOWN
            next_pos = (bot.pos_x + 1, bot.pos_y)
        elif direction == DIRECTION_RIGHT and bot.pos_y < len(self.grid) - 2 and self.grid[bot.pos_x][bot.pos_y+1] == 0:  # RIGHT
            next_pos = (bot.pos_x, bot.pos_y + 1)
        elif direction == DIRECTION_UP and bot.pos_x > 1 and self.grid[bot.pos_x-1][bot.pos_y] == 0:  # UP
            next_pos = (bot.pos_x - 1, bot.pos_y)
        else:
            next_pos = (bot.pos_x, bot.pos_y)

        if direction in DIRECTIONS:
            bot.update_rotation(direction)

        return next_pos

    def clear(self, pos_x, pos_y):
        if not isinstance(self.grid[pos_x][pos_y], Bot):
            self.grid[pos_x][pos_y] = 0

    def __repr__(self):
        grid_rep = ""
        for i in range(0, len(self.grid)):
            grid_rep += str(self.grid[i]) + "\n"
        return grid_rep
