import pygame
import os
import numpy as np
from .bots import *


class BotSprite(pygame.sprite.Sprite):

    def __init__(self, image = None):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()


class FlameSprite(pygame.sprite.Sprite):

    def __init__(self, image = None):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()


class NailSprite(pygame.sprite.Sprite):

    def __init__(self, image = None):
        pygame.sprite.Sprite.__init__(self)
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
        self.nailBot_img = pygame.image.load(os.path.join(img_folder, 'nailBot.png')).convert_alpha()
        # self.nailBot_img = pygame.image.load(os.path.join(img_folder, 'nailBot.png')).convert_alpha()
        self.flame_img = pygame.image.load(os.path.join(img_folder, 'flame.png')).convert_alpha()
        self.nail_img = pygame.image.load(os.path.join(img_folder, 'nailBullet.png')).convert_alpha()

        self.env = environment
        self.game = environment.current_state

        # This sets the WIDTH and HEIGHT of each grid location
        self.WIDTH = 80
        self.HEIGHT = 80

        # This sets the margin between each cell
        self.MARGIN = 5

    def crate_flame_sprite(self) -> FlameSprite:
        sprite = FlameSprite(self.flame_img)
        sprite.image = pygame.transform.scale(sprite.image, (self.WIDTH, self.HEIGHT))
        return sprite

    def create_nail_sprite(self) -> NailSprite:
        sprite = NailSprite(self.nail_img)
        sprite.image = pygame.transform.scale(sprite.image, (self.WIDTH, self.HEIGHT))
        return sprite

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
        elif bot_type == BOT_TYPE_NAIL:
            return BotSprite(self.nailBot_img)
        else:
            return ValueError('Unknown Bot Type')

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

        # Set the WIDTH and HEIGHT of the screen
        WINDOW_SIZE = [900, 650]
        screen = pygame.display.set_mode(WINDOW_SIZE)

        # Background color
        screen.fill(BLACK)

        player1 = self.game.player1
        player2 = self.game.player2

        # Set title of screen
        pygame.display.set_caption("Cool Bot Game")

        # Setup font
        fonts_folder = os.path.join(self.game_folder,'fonts')
        font = pygame.font.Font(os.path.join(fonts_folder, 'SigmarOne.ttf'), 28)

        p1_sleeping_text = 'Sleeping' if player1.is_sleeping() else 'READY'
        p2_sleeping_text = 'Sleeping' if player2.is_sleeping() else 'READY'
        player1name = font.render(f'Player 1: {player1.health} HP. {p1_sleeping_text}', True, GREEN)
        player2name = font.render(f'Player 2: {player2.health} HP. {p2_sleeping_text}', True, BLUE)

        # create a rectangular object for the
        # text surface object
        player1_text_rect = player1name.get_rect()
        player2_text_rect = player2name.get_rect()

        # set the center of the rectangular object.
        player1_text_rect.center = (200, 20)
        player2_text_rect.center = (700, 20)

        # Render player names and scoreboard

        # Player 1
        pygame.draw.rect(screen, (255, 0, 0), (10,40, (250/player1.max_health)*player1.max_health, 30))
        pygame.draw.rect(screen, (0, 128, 0), (10,40, (250/player1.max_health)*player1.health, 30))
        screen.blit(player1name, player1_text_rect)

        # Player 2
        pygame.draw.rect(screen, (255, 0, 0), (520,40, (250/player2.max_health)*player2.max_health, 30))
        pygame.draw.rect(screen, (0, 128, 0), (520,40, (250/player2.max_health)*player2.health, 30))
        screen.blit(player2name, player2_text_rect)

        # Set size of sprite to the size of one tile
        player1_sprite = self.get_sprite(0)
        player2_sprite = self.get_sprite(1)
        player1_sprite.image = pygame.transform.scale(player1_sprite.image, (self.WIDTH, self.HEIGHT))
        player2_sprite.image = pygame.transform.scale(player2_sprite.image, (self.WIDTH, self.HEIGHT))

        # Draw the grid
        for row in range(1,len(self.game.board.grid)-1):
            for column in range(1,len(self.game.board.grid)-1):
                color = WHITE
                if isinstance(self.game.board.grid[row][column], Bullet):
                    bullet_sprite = self.create_nail_sprite()
                    bullet_sprite.rect = [(self.MARGIN + self.WIDTH) * column + self.MARGIN, (self.MARGIN + self.HEIGHT) * row + self.MARGIN]
                    bullet_sprite_group = pygame.sprite.Group(bullet_sprite)
                    bullet_sprite_group.draw(screen)
                if self.game.board.grid[row][column] == player1:
                    color = BOT_COLOR_A_FADED if player1.is_sleeping() else BOT_COLOR_A
                    pygame.draw.rect(screen,
                                     color,
                                     [(self.MARGIN + self.WIDTH) * column + self.MARGIN,
                                      (self.MARGIN + self.HEIGHT) * row + self.MARGIN,
                                      self.WIDTH,
                                      self.HEIGHT])
                    # I am VERY confident that I'm doing something wrong here, but it does work - sprite is re-rendered at the correct location
                    player1_sprite.rect = [(self.MARGIN + self.WIDTH) * column + self.MARGIN, (self.MARGIN + self.HEIGHT) * row + self.MARGIN]
                    player1sprite = pygame.sprite.Group(player1_sprite)

                elif self.game.board.grid[row][column] == player2:
                    color = BOT_COLOR_B_FADED if player2.is_sleeping() else BOT_COLOR_B
                    pygame.draw.rect(screen,
                                     color,
                                     [(self.MARGIN + self.WIDTH) * column + self.MARGIN,
                                      (self.MARGIN + self.HEIGHT) * row + self.MARGIN,
                                      self.WIDTH,
                                      self.HEIGHT])
                    player2_sprite.rect = [(self.MARGIN + self.WIDTH) * column + self.MARGIN, (self.MARGIN + self.HEIGHT) * row + self.MARGIN]
                    player2sprite = pygame.sprite.Group(player2_sprite)

                # All other non-player tiles
                pygame.draw.rect(screen,
                                 color,
                                 [(self.MARGIN + self.WIDTH) * column + self.MARGIN,
                                  (self.MARGIN + self.HEIGHT) * row + self.MARGIN,
                                  self.WIDTH,
                                  self.HEIGHT])

        # Render players
        player1sprite.draw(screen)
        player2sprite.draw(screen)

        # Render Special bot actions
        for p in [player1, player2]:
            # Render Flames from torch bot
            if isinstance(p, TorchBot):
                for row, column in p.torch_cells:
                    flame_sprite = self.crate_flame_sprite()
                    flame_sprite.rect = [(self.MARGIN + self.WIDTH) * column + self.MARGIN, (self.MARGIN + self.HEIGHT) * row + self.MARGIN]
                    flame_sprite_group = pygame.sprite.Group(flame_sprite)
                    flame_sprite_group.draw(screen)
            # Render Nails from nail bots
            if isinstance(p, NailBot):
                for b in p.active_bullets:
                    bullet_sprite = self.create_nail_sprite()
                    bullet_sprite.rect = [(self.MARGIN + self.WIDTH) * b.pos_y + self.MARGIN, (self.MARGIN + self.HEIGHT) * b.pos_x + self.MARGIN]
                    bullet_sprite_group = pygame.sprite.Group(bullet_sprite)
                    bullet_sprite_group.draw(screen)

        pygame.display.flip()

    def draw(self):
        self.render()
        rgb_array = pygame.surfarray.array3d(pygame.display.get_surface()).astype(np.uint8)
        rgb_array = np.rot90(rgb_array, k=3)  # Rotate 270 degrees
        rgb_array = np.fliplr(rgb_array)
        return rgb_array
