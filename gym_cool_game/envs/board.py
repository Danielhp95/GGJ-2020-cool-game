import numpy as np
from valid_inputs import *
import pygame

class Board:

    def __init__(self, board_size):
        self.grid = np.ones((board_size, board_size), dtype=int)
        self.grid[1:-1, 1:-1] = 0
        self.grid = self.grid.tolist()

    # Set the position of bot to (x, y)
    # Must be passed an object of class Bot, of course
    def set(self, bot, x, y):
        # Only attempt to set current position to 0 if bot is already on the board
        # This becomes irrelevant if bots are only ever instantiated in valid locations
        if self.currently_on_board(bot.pos_x, bot.pos_y) == True:
            self.grid[bot.pos_x][bot.pos_y] = 0
            bot.pos_x = x
            bot.pos_y = y
            self.grid[x][y] = bot  # set new tile on grid to occupied
        else:
            bot.pos_x = x
            bot.pos_y = y
            self.grid[x][y] = bot

    # Check if a set of coordinates is on the board
    def currently_on_board(self, x, y):
        if x > len(self.grid)-1 or x < 0 or y > len(self.grid)-1 or y < 0:
            return False
        else:
            return True

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


    def resolve_moves(self, bot1, direction1, bot2, direction2):

        # ------------------------------------
        # Figure out where bot1 is moving to
        # ------------------------------------
        if direction1 == DIRECTION_LEFT and bot1.pos_y > 1 and self.grid[bot1.pos_x][bot1.pos_y-1] == 0:  # LEFT
            bot1.next_move_y = bot1.pos_y - 1
            bot1.next_move_x = bot1.pos_x
            bot1.image = pygame.transform.rotate(bot1.image, 0-bot1.curr_rotation)

            # So that the sprite does not appear upside down
            if bot1.flipped_vert == True:
                bot1.image = pygame.transform.flip(bot1.image,False,True)
                bot1.flipped_vert = False

            bot1.rect = bot1.image.get_rect()
            bot1.curr_rotation = 0

        elif direction1 == DIRECTION_DOWN and bot1.pos_x < len(self.grid) - 2 and self.grid[bot1.pos_x+1][bot1.pos_y] == 0:  # DOWN
            bot1.next_move_x = bot1.pos_x + 1
            bot1.next_move_y = bot1.pos_y
            bot1.image = pygame.transform.rotate(bot1.image, 90-bot1.curr_rotation)

            # So that the sprite does not appear upside down
            if bot1.flipped_horiz == True:
                bot1.image = pygame.transform.flip(bot1.image,True,False)
                bot1.flipped_horiz = False

            bot1.rect = bot1.image.get_rect()
            bot1.curr_rotation = 90

        elif direction1 == DIRECTION_RIGHT and bot1.pos_y < len(self.grid) - 2 and self.grid[bot1.pos_x][bot1.pos_y+1] == 0:  # RIGHT
            bot1.next_move_y = bot1.pos_y + 1
            bot1.next_move_x = bot1.pos_x
            bot1.image = pygame.transform.rotate(bot1.image, 180-bot1.curr_rotation)

            # So that the sprite does not appear upside down
            if bot1.flipped_vert == False:
                bot1.image = pygame.transform.flip(bot1.image,False,True)
                bot1.flipped_vert = True

            bot1.rect = bot1.image.get_rect()
            bot1.curr_rotation = 180


        elif direction1 == DIRECTION_UP and bot1.pos_x > 1 and self.grid[bot1.pos_x-1][bot1.pos_y] == 0:  # UP
            bot1.next_move_x = bot1.pos_x - 1
            bot1.next_move_y = bot1.pos_y
            bot1.image = pygame.transform.rotate(bot1.image, 270-bot1.curr_rotation)

            # So that the sprite does not appear upside down
            if bot1.flipped_horiz == True:
                bot1.image = pygame.transform.flip(bot1.image,True,False)
                bot1.flipped_horiz = False

            bot1.rect = bot1.image.get_rect()
            bot1.curr_rotation = 270
        else:
            bot1.next_move_x = bot1.pos_x
            bot1.next_move_y = bot1.pos_y

        # ------------------------------
        # Figure out where bot2 is moving to
        # ------------------------------
        if direction2 == DIRECTION_LEFT and bot2.pos_y > 1 and self.grid[bot2.pos_x][bot2.pos_y-1] == 0:  # LEFT
            bot2.next_move_y = bot2.pos_y - 1
            bot2.next_move_x = bot2.pos_x
            bot2.image = pygame.transform.rotate(bot2.image, 0-bot2.curr_rotation)

            # So that the sprite does not appear upside down
            if bot2.flipped_vert == True:
                bot2.image = pygame.transform.flip(bot2.image,False,True)
                bot2.flipped_vert = False

            bot2.rect = bot2.image.get_rect()
            bot2.curr_rotation = 0

        elif direction2 == DIRECTION_DOWN and bot2.pos_x < len(self.grid) - 2 and self.grid[bot2.pos_x+1][bot2.pos_y] == 0:  # DOWN
            bot2.next_move_x = bot2.pos_x + 1
            bot2.next_move_y = bot2.pos_y
            bot2.image = pygame.transform.rotate(bot2.image, 90-bot2.curr_rotation)

            # So that the sprite does not appear upside down
            if bot2.flipped_horiz == True:
                bot2.image = pygame.transform.flip(bot1.image,True,False)
                bot2.flipped_horiz = False

            bot2.rect = bot2.image.get_rect()
            bot2.curr_rotation = 90

        elif direction2 == DIRECTION_RIGHT and bot2.pos_y < len(self.grid) - 2 and self.grid[bot2.pos_x][bot2.pos_y+1] == 0:  # RIGHT
            bot2.next_move_y = bot2.pos_y + 1
            bot2.next_move_x = bot2.pos_x
            bot2.image = pygame.transform.rotate(bot2.image, 180-bot2.curr_rotation)

            # So that the sprite does not appear upside down
            if bot2.flipped_vert == False:
                bot2.image = pygame.transform.flip(bot2.image,False,True)
                bot2.flipped_vert = True

            bot2.rect = bot2.image.get_rect()
            bot2.curr_rotation = 180

        elif direction2 == DIRECTION_UP and bot2.pos_x > 1 and self.grid[bot2.pos_x-1][bot2.pos_y] == 0:  # UP
            bot2.next_move_x = bot2.pos_x - 1
            bot2.next_move_y = bot2.pos_y
            bot2.image = pygame.transform.rotate(bot2.image, 270-bot2.curr_rotation)

            # So that the sprite does not appear upside down
            if bot2.flipped_horiz == True:
                bot2.image = pygame.transform.flip(bot2.image,True,False)
                bot2.flipped_horiz = False

            bot2.rect = bot2.image.get_rect()
            bot2.curr_rotation = 270

        else:
            bot2.next_move_x = bot2.pos_x
            bot2.next_move_y = bot2.pos_y

        # If the two spaces where they're moving to is not the same, move them there
        if [bot1.next_move_x, bot1.next_move_y] != [bot2.next_move_x, bot2.next_move_y]:
            self.set(bot1, bot1.next_move_x, bot1.next_move_y)
            self.set(bot2, bot2.next_move_x, bot2.next_move_y)

        # If the bots are moving to the same space, move only the one with heavier weight
        elif [bot1.next_move_x, bot1.next_move_y] == [bot2.next_move_x, bot2.next_move_y]:

            if bot1.weight >= bot2.weight:
                print("*************** COLLISION, bot 1 is heavier *********************")
                self.set(bot1, bot1.next_move_x, bot1.next_move_y)
            else:
                print("*************** COLLISION, bot 2 is heavier *********************")
                self.set(bot2, bot2.next_move_x, bot2.next_move_y)

