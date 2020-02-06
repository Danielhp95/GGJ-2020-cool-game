# Pygame specific classes.
import pygame
from .bots import *


class SpriteBot(Bot, pygame.sprite.Sprite):

    def __init__(self, image = None):
        pygame.sprite.Sprite.__init__(self)
        screen = pygame.display.get_surface()
        self.image = image
        self.rect = image.get_rect()
        self.flipped_vert = False
        self.flipped_horiz = False

    def update_rotation(self, direction):
        target_angle = self.to_angle(direction)
        current_angle = self.to_angle(self.curr_rotation)

        self.image = pygame.transform.rotate(self.image, target_angle - current_angle)

        # So that the sprite does not appear upside down
        if self.flipped_horiz == True:
            self.image = pygame.transform.flip(self.image, True, False)
            self.flipped_horiz = False

        self.rect = self.image.get_rect()

        Bot.update_rotation(self, direction)


    def to_angle(self, direction):
        return 90 * (direction - 1)


class NailBotPyg(NailBot, SpriteBot):
	def __init__(self, image, params):
		SpriteBot.__init__(self, image)
		NailBot.__init__(self, params)


class SawBotPyg(SawBot, SpriteBot):
	def __init__(self, image, params):
		SpriteBot.__init__(self, image)
		SawBot.__init__(self, params)


class TorchBotPyg(TorchBot, SpriteBot):
	def __init__(self, image, params):
		SpriteBot.__init__(self, image)
		TorchBot.__init__(self, params)
