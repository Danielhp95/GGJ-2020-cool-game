import numpy as np


class Board:
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

    def __init__(self, board_size, bot1, bot2):
        # self.grid = [[1 for x in range(int(board_size))] for y in range(int(board_size))]
        # self.grid[1:-1][1:-1] = 0
        self.grid = np.ones((board_size, board_size), dtype=int)
        self.grid[1:-1, 1:-1] = 0
        # todo - make board boundaries 1s
        # make occupied tiles occupied by object itself
        self.bot1 = bot1
        self.bot2 = bot2

    # Set the position of bot to (x, y)
    # Must be passed an object of class Bot, of course
    def set(self, bot, x, y):
        try: # In case the current location is off the grid
            self.grid[bot.pos_x][bot.pos_y] = 0
        except:
            None

        bot.pos_x = x
        bot.pos_y = y
        self.grid[x][y] = 2  # set new tile on grid to occupied

    # Get a list of valid directional moves for bot
    def get_valid_moves(self, bot):

        # begin with all possible directional moves
        valid_moves = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if self.grid[bot.pos_x + i][bot.pos_y + j] == 0:
                    valid_moves.append(
                        [bot.pos_x + i, bot.pos_y + j])  # note: this allows for staying put as a valid move

        return valid_moves

    # Move bot in direction
    def move(self, bot, direction):
        if direction == 1 and bot.pos_y > 1:  # UP
            self.grid[bot.pos_x][bot.pos_y] = 0
            bot.pos_y -= 1
            self.grid[bot.pos_x][bot.pos_y] = 2
        elif direction == 2 and bot.pos_x < len(self.grid - 2):  # RIGHT
            self.grid[bot.pos_x][bot.pos_y] = 0
            bot.pos_x += 1
            self.grid[bot.pos_x][bot.pos_y] = 2
        elif direction == 3 and bot.pos_y < len(self.grid - 2):  # DOWN
            self.grid[bot.pos_x][bot.pos_y] = 0
            bot.pos_y += 1
            self.grid[bot.pos_x][bot.pos_y] = 2
        elif direction == 4 and bot.pos_x > 1:  # LEFT
            self.grid[bot.pos_x][bot.pos_y] = 0
            bot.pos_x -= 1
            self.grid[bot.pos_x][bot.pos_y] = 2
