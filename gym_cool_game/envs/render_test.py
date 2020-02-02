import pygame
import sys
import os
from game import Game, Bot
from board import Board
from valid_inputs import *

def test_print(grid):
    for i in range(0, len(grid)):
        print(str(grid[i]))



# -----------------
# Prepare pygame - must be done before sprites can be loaded
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


# Setup images
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
spikyBot_img = pygame.image.load(os.path.join(img_folder, 'punkrobot2.png')).convert()
blowTorchBot_img = pygame.image.load(os.path.join(img_folder, 'fireBot.png')).convert()


# ---------------------
# Prepare game for play
# --------------------

# Bots are now initialized with a sprite img
player1 = Bot("mamaBot",spikyBot_img)
player2 = Bot("babyBot",blowTorchBot_img)
player2.weight = 3
player2.ticks_between_moves = 2
player1.ticks_between_moves = 8
myboard = Board(10)

game = Game(myboard, player1, player2)


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

    # Background color
    screen.fill(BLACK)

    # Set size of sprite to the size of one tile
    player1.image = pygame.transform.scale(player1.image, (WIDTH, HEIGHT))
    player2.image = pygame.transform.scale(player2.image, (WIDTH, HEIGHT))

    # Draw the grid
    for row in range(1,len(myboard.grid)-1):
        for column in range(1,len(myboard.grid)-1):
            color = WHITE
            if myboard.grid[row][column] == player1:
                color = BOT_COLOR_A_FADED if player1.is_sleeping() else BOT_COLOR_A
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])
                # I am VERY confident that I'm doing something wrong here, but it does work - sprite is re-rendered at the correct location
                player1.rect = [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN]
                player1sprite = pygame.sprite.Group(player1)

            elif myboard.grid[row][column] == player2:
                color = BOT_COLOR_B_FADED if player2.is_sleeping() else BOT_COLOR_B
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])
                player2.rect = [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN]
                player2sprite = pygame.sprite.Group(player2)

            # All other non-player tiles
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])


    player1sprite.draw(screen)
    player2sprite.draw(screen)

    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()