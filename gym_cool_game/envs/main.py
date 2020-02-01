from game import Bot
from game import Game
from board import Board
import pygame

player1 = Bot("A")
player2 = Bot("B")

board = Board(10)

game = Game(board, player1, player2)

def test_print(grid):
    for i in range(0, len(grid)):
        print(str(grid[i]))


while not game.winner:
    # step forward the game until input is needed
    test_print(game.board.grid)
    game.step()
    # get input
    inp = input("Enter Actions in the form 'Player1,Player2' where valid actions are Null(0)|Up(1)|Down(2)|Left(3)|Right(4)|Action(5)|RotR(6)|RotL(7)\n")
    actions = inp.split(',')

    playerA = int(actions[0].strip())
    playerB = int(actions[1].strip())
    print("You entered: %s, %s" % (playerA, playerB))
    game.make_moves(playerA, playerB)


'''

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# This sets the margin between each cell
MARGIN = 5

# Initialize pygame
pygame.init()

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [255, 255]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("Bot Battle")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

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
'''
