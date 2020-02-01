import pygame
import sys
from gym_cool_game.envs.game import Game,Bot
from gym_cool_game.envs.board import Board

# ---------------------
# Prepare game for play
# --------------------

babyBot = Bot(20)
mamaBot = Bot(30)
myboard = Board(10)

myboard.set(babyBot, 1, 1)
myboard.set(mamaBot, 1, 5)

myboard.test_print()
print()

myboard.resolve_moves(babyBot, "RIGHT", mamaBot,  "LEFT")
print()

myboard.resolve_moves(babyBot, "RIGHT", mamaBot,  "LEFT")


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

def get_available_moves(the_grid, curr_pos):
    col = curr_pos[0]
    row = curr_pos[1]

    available_moves = []

# ------------------------
# Main Program Loop
# ------------------------
while not done:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:

            keys_pressed = pygame.key.get_pressed()

            if keys_pressed[pygame.K_LEFT]:
                myboard.resolve_moves(babyBot, "LEFT", mamaBot, "None")
            # if keys_pressed[pygame.K_RIGHT]:
            #
            # if keys_pressed[pygame.K_UP]:
            #
            # if keys_pressed[pygame.K_DOWN]:

    screen.fill(BLACK)

    # Draw the grid
    for row in range(10):
        for column in range(10):
            color = WHITE
            if grid[row][column] != 1:
                color = GREEN
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