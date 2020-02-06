from game import Bot
from game import Game
from board import Board
import pygame
from cool_game_env import *

print("Attempting to create a cool_game_env instance")

cge = CoolGameEnv(with_pygame=True)

print("Attempting to draw game")

print(cge.render('rgb'))
