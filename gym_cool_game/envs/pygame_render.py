import pygame
import os
import numpy as np
from .bots import *


class BotSprite(pygame.sprite.Sprite):

    def __init__(self, image = None):
        pygame.sprite.Sprite.__init__(self)
        screen = pygame.display.get_surface()
        self.image = image
        self.rect = image.get_rect()

class PygameRender():

    def __init__(self, environment):
        pygame.init()
        screen = pygame.display.set_mode((640,480))
        self.game_folder = os.path.dirname(__file__)
        img_folder = os.path.join(self.game_folder, 'images')
        self.spikyBot_img = pygame.image.load(os.path.join(img_folder, 'punkrobot2.png')).convert_alpha()
        self.blowTorchBot_img = pygame.image.load(os.path.join(img_folder, 'fireBot.png')).convert_alpha()
        # self.nailBot_img = pygame.image.load(os.path.join(img_folder, 'nailBot.png')).convert_alpha()

        self.env = environment
        self.game = environment.current_state


    def get_sprite(self, player_index):
        if player_index == 0:
            return self.get_bot(self.env.botA_type)
        else:
            return self.get_bot(self.env.botB_type)


    def get_bot(self, bot_type):
        if bot_type == BOT_TYPE_SPIKE:
            return BotSprite(self.spikyBot_img)
        elif bot_type == BOT_TYPE_TORCH:
            return BotSprite(self.blowTorchBot_img)
        else:
            raise ValueError("ERROR: Invalid Bot Type")


    def render(self):
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
        WIDTH = 80
        HEIGHT = 80

        # This sets the margin between each cell
        MARGIN = 5

        # Set the HEIGHT and WIDTH of the screen
        WINDOW_SIZE = [1000, 1000]
        screen = pygame.display.set_mode(WINDOW_SIZE)

        # Set title of screen
        pygame.display.set_caption("Bot Game")

        # Setup font
        fonts_folder = os.path.join(self.game_folder,'fonts')
        font = pygame.font.Font(os.path.join(fonts_folder, 'SigmarOne.ttf'), 32)

        player1name = font.render('Player 1', True, BLUE)
        player2name = font.render('Player 2', True, GREEN)

        # create a rectangular object for the
        # text surface object
        player1_text_rect = player1name.get_rect()
        player2_text_rect = player2name.get_rect()

        # set the center of the rectangular object.
        player1_text_rect.center = (100, 20)
        player2_text_rect.center = (800,20)

        player1 = self.game.player1
        player2 = self.game.player2

        # Background color
        screen.fill(BLACK)

        # Set size of sprite to the size of one tile
        player1_sprite = self.get_sprite(0)
        player2_sprite = self.get_sprite(1)
        player1_sprite.image = pygame.transform.scale(player1_sprite.image, (WIDTH, HEIGHT))
        player2_sprite.image = pygame.transform.scale(player1_sprite.image, (WIDTH, HEIGHT))

        # Draw the grid
        for row in range(1,len(self.game.board.grid)-1):
            for column in range(1,len(self.game.board.grid)-1):
                color = WHITE
                if self.game.board.grid[row][column] == player1:
                    color = BOT_COLOR_A_FADED if player1.is_sleeping() else BOT_COLOR_A
                    pygame.draw.rect(screen,
                                     color,
                                     [(MARGIN + WIDTH) * column + MARGIN,
                                      (MARGIN + HEIGHT) * row + MARGIN,
                                      WIDTH,
                                      HEIGHT])
                    # I am VERY confident that I'm doing something wrong here, but it does work - sprite is re-rendered at the correct location
                    player1_sprite.rect = [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN]
                    player1sprite = pygame.sprite.Group(player1_sprite)

                elif self.game.board.grid[row][column] == player2:
                    color = BOT_COLOR_B_FADED if player2.is_sleeping() else BOT_COLOR_B
                    pygame.draw.rect(screen,
                                     color,
                                     [(MARGIN + WIDTH) * column + MARGIN,
                                      (MARGIN + HEIGHT) * row + MARGIN,
                                      WIDTH,
                                      HEIGHT])
                    player2_sprite.rect = [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN]
                    player2sprite = pygame.sprite.Group(player2_sprite)

                # All other non-player tiles
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])

        # Render players
        player1sprite.draw(screen)
        player2sprite.draw(screen)

        # Render player names and scoreboard

        # Player 1
        pygame.draw.rect(screen, (255, 0, 0), (10,40, (300/player1.max_health)*player1.max_health, 30))
        pygame.draw.rect(screen, (0, 128, 0), (10,40, (300/player1.max_health)*player1.health, 30))
        screen.blit(player1name, player1_text_rect)

        # Player 2
        pygame.draw.rect(screen, (255, 0, 0), (600,40, (300/player2.max_health)*player2.max_health, 30))
        pygame.draw.rect(screen, (0, 128, 0), (600,40, (300/player2.health)*player2.health, 30))
        screen.blit(player2name, player2_text_rect)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()



    def draw(self):
        self.render()
        return pygame.surfarray.array3d(pygame.display.get_surface()).astype(np.uint8)
