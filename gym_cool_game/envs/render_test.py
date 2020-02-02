import pygame
import sys
from game import Game, Bot
from board import Board
from valid_inputs import *

def test_print(grid):
    for i in range(0, len(grid)):
        print(str(grid[i]))


# ---------------------
# Prepare game for play
# --------------------

player1 = Bot()
player2 = Bot()
player2.weight = 3
player2.ticks_between_moves = 2
player1.ticks_between_moves = 8
myboard = Board(10)

game = Game(myboard, player1, player2)


# -----------------
# Prepare pygame
# -----------------

pygame.init()
screen = pygame.display.set_mode((640,480))

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

BOT_COLOR_A = (0, 255, 0)
BOT_COLOR_A_FADED = (60, 100, 60)
BOT_COLOR_B = (0, 0, 255)
BOT_COLOR_B_FADED = (60, 60, 100)



# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20

# This sets the margin between each cell
MARGIN = 5

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [255, 255]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("Bot Games")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()


# ------------------------
# Main Program Loop
# ------------------------

bot1Input = None
bot2Input = None

while not done:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            keys_pressed = pygame.key.get_pressed()

            if keys_pressed[pygame.K_LEFT]:
                bot1Input = DIRECTION_LEFT

            if keys_pressed[pygame.K_RIGHT]:
                bot1Input = DIRECTION_RIGHT

            if keys_pressed[pygame.K_UP]:
                bot1Input = DIRECTION_UP

            if keys_pressed[pygame.K_DOWN]:
                bot1Input = DIRECTION_DOWN

            if keys_pressed[pygame.K_RETURN]:
                bot1Input = ACTION

            if keys_pressed[pygame.K_a]:
                bot2Input = DIRECTION_LEFT

            if keys_pressed[pygame.K_d]:
                bot2Input = DIRECTION_RIGHT

            if keys_pressed[pygame.K_w]:
                bot2Input = DIRECTION_UP

            if keys_pressed[pygame.K_s]:
                bot2Input = DIRECTION_DOWN

            if keys_pressed[pygame.K_SPACE]:
                bot2Input = ACTION



    if (not game.is_waiting_for(player1) or bot1Input) and (not game.is_waiting_for(player2) or bot2Input):
        if not game.is_valid_for(player1, bot1Input):
            bot1Input = None

        if not game.is_valid_for(player2, bot2Input):
            bot2Input = None

        game.handle_input(bot1Input, bot2Input)

        bot1Input = None
        bot2Input = None

    # TODO: This will advance the game state all the way to the next input choice
    #   which could be far in the future. We ideally want to render each tick rather than
    #   rendering only the states in which the players can take actions.
    game.step()
 
    screen.fill(BLACK)

    # Draw the grid
    for row in range(1,len(myboard.grid)-1):
        for column in range(1,len(myboard.grid)-1):
            color = WHITE
            if myboard.grid[row][column] == player1:
                color = BOT_COLOR_A_FADED if player1.is_sleeping() else BOT_COLOR_A
            elif myboard.grid[row][column] == player2:
                color = BOT_COLOR_B_FADED if player2.is_sleeping() else BOT_COLOR_B
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()

