import pygame
import sys
from game import Game,Bot
from board import Board

def test_print(grid):
    for i in range(0, len(grid)):
        print(str(grid[i]))


# ---------------------
# Prepare game for play
# --------------------

babyBot = Bot()
mamaBot = Bot()
myboard = Board(10)

game = Game(myboard, babyBot, mamaBot)



# -----------------
# Prepare pygame
# -----------------

pygame.init()
screen = pygame.display.set_mode((640,480))

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20

# This sets the margin between each cell
MARGIN = 5

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [255, 255]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("If this works, it's a miracle")

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
                bot1Input = 3

            if keys_pressed[pygame.K_RIGHT]:
                bot1Input = 4

            if keys_pressed[pygame.K_UP]:
                bot1Input = 1

            if keys_pressed[pygame.K_DOWN]:
                bot1Input = 2

            if keys_pressed[pygame.K_a]:
                bot2Input = 3

            if keys_pressed[pygame.K_d]:
                bot2Input = 4

            if keys_pressed[pygame.K_w]:
                bot2Input = 1

            if keys_pressed[pygame.K_s]:
                bot2Input = 2

    if bot1Input and bot2Input:
        game.make_moves(bot1Input, bot2Input)
        bot1Input = None
        bot2Input = None
 
    screen.fill(BLACK)

    # Draw the grid
    for row in range(1,len(myboard.grid)-1):
        for column in range(1,len(myboard.grid)-1):
            color = WHITE
            if myboard.grid[row][column] == babyBot:
                # print(str(babyBot.pos_x) + "," + str(babyBot.pos_y))
                color = GREEN
            elif myboard.grid[row][column] == mamaBot:
                color = RED
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

