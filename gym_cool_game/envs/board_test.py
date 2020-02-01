"""
 Example program to show using an array to back a grid on-screen.

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

 Explanation video: http://youtu.be/mdTeqiWyFnc


 #TODO
    - list of valid moves


"""
import pygame

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

# Create a 2D array
grid_size = 10
grid = [[0 for x in range(grid_size)] for y in range(grid_size)]

# Set starting position here
current_pos = [5,5]
grid[current_pos[0]][current_pos[1]] = 1

# Initialize pygame
pygame.init()

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [255, 255]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("Array Backed Grid")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

def get_available_moves(the_grid, curr_pos):
    col = curr_pos[0]
    row = curr_pos[1]

    available_moves = []

# -------- Main Program Loop -----------
while not done:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:

            curr_column = current_pos[0]
            curr_row = current_pos[1]

            keys_pressed = pygame.key.get_pressed()

            if keys_pressed[pygame.K_LEFT] and curr_column > 0:
                pygame.key.set_repeat(10, 10)
                grid[curr_row][curr_column] = 0
                current_pos[0] -= 1
            if keys_pressed[pygame.K_RIGHT] and curr_column < 9:
                pygame.key.set_repeat(10, 10)
                grid[curr_row][curr_column] = 0
                current_pos[0] += 1
            if keys_pressed[pygame.K_UP] and curr_row > 0:
                pygame.key.set_repeat(10, 10)
                grid[curr_row][curr_column] = 0
                current_pos[1] -= 1
            if keys_pressed[pygame.K_DOWN] and curr_column < 9:
                pygame.key.set_repeat(10, 10)
                grid[curr_row][curr_column] = 0
                current_pos[1] += 1

            new_column = current_pos[0]
            new_row = current_pos[1]

            # Set that location to one
            grid[new_row][new_column] = 1
            print("Click ", current_pos, "Grid coordinates: ", row, column)

    screen.fill(BLACK)

    # Draw the grid
    for row in range(10):
        for column in range(10):
            color = WHITE
            if grid[row][column] == 1:
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