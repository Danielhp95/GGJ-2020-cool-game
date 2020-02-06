from typing import List
from copy import deepcopy
import numpy as np
import gym
from gym.spaces import Discrete, Box, Tuple
import pygame
import os

from .pygame_bots import *

from .game import Game
from .board import Board

from .bots import SawBot, TorchBot, NailBot
from .game_params import (GameParams, TorchParams, SawBotParams, NailBotParams,
                          construct_game_params)

BOT_TYPE_SPIKE = 0
BOT_TYPE_TORCH = 1
BOT_TYPE_NAIL = 1

class CoolGameEnv(gym.Env):

    def __init__(self,
                 with_pygame: bool=False,
                 botA_type: int = 0, botB_type: int = 0,
                 board_size: int = 10,
                 p1_starting_position: List = [2,2],
                 p2_starting_position: List = [7,7],
                 # TorchBot parameters
                 torch_dmg=2,
                 torch_weight=2,
                 torch_torch_range=2,
                 torch_duration=2,
                 torch_cooldown=3,
                 torch_ticks_between_moves=2,
                 # SawBot parameters 
                 saw_dmg_min=1,
                 saw_dmg_max=5,
                 saw_weight=3,
                 saw_duration=3,
                 saw_cooldown=5,
                 saw_ticks_between_moves=1,
                 # NaileBot parameters
                 nail_dmg=1,
                 nail_weight=1,
                 nail_bullet_speed=3,
                 nail_cooldown=2,
                 nail_ticks_between_moves=3):
        # Each player has 5 actions. Directional moves: UP / DOWN/ LEFT / RIGHT
        # And a 5th "Action", which is bot dependant
        self.action_space = Tuple([Discrete(5), Discrete(5)])
        single_agent_observation = Box(shape=(board_size, board_size),
                                       low=0, high=5, dtype=int) # TODO: find maximum number of values
        self.observation_space = Tuple([single_agent_observation,
                                        single_agent_observation])

        # Game params
        self.p1_starting_position = p1_starting_position
        self.p2_starting_position = p2_starting_position

        # Bot params
        self.game_params = construct_game_params(
                torch_dmg, torch_weight, torch_torch_range, torch_duration,
                torch_cooldown, torch_ticks_between_moves,
                saw_dmg_min, saw_dmg_max, saw_weight, saw_duration,
                saw_cooldown, saw_ticks_between_moves,
                nail_dmg, nail_weight, nail_bullet_speed,
                nail_cooldown, nail_ticks_between_moves)

        self.botA_type = botA_type
        self.botB_type = botB_type
        self.board_size = board_size

        self.with_pygame = with_pygame
        if self.with_pygame:
            pygame.init()
            screen = pygame.display.set_mode((640,480))
            self.game_folder = os.path.dirname(__file__)
            img_folder = os.path.join(self.game_folder, 'images')
            self.spikyBot_img = pygame.image.load(os.path.join(img_folder, 'punkrobot2.png')).convert_alpha()
            self.blowTorchBot_img = pygame.image.load(os.path.join(img_folder, 'fireBot.png')).convert_alpha()
            # self.nailBot_img = pygame.image.load(os.path.join(img_folder, 'nailBot.png')).convert_alpha()
        self.reset()

    def reset(self):
        self.winner = -1 # Values: [-1, 0, 1]
        self.player1 = self.get_bot(self.botA_type)
        self.player2 = self.get_bot(self.botB_type)
        self.board = Board(self.board_size)
        self.current_state = Game(self.board, self.player1, self.player2,
                                  self.p1_starting_position, self.p2_starting_position)
        return np.array([[],[]]) # TODO: must return observation for each agent

    def get_bot(self, bot_type):
        if bot_type == BOT_TYPE_SPIKE:
            return SawBot(self.game_params.saw_params) if not self.with_pygame else SawBotPyg(self.spikyBot_img, self.game_params.saw_params)
        elif bot_type == BOT_TYPE_TORCH:
            return TorchBot(self.game_params.torch_params) if not self.with_pygame else TorchBotPyg(self.blowTorchBot_img, self.game_params.torch_params)
        elif bot_type == BOT_TYPE_NAIL:
            return NailBot(self.game_params.nail_params)
        else:
            raise ValueError("ERROR: Invalid Bot Type")

    def clone(self):
        """
        Creates a deep copy of the game state.
        NOTE: it is _really_ important that a copy is used during simulations
              Because otherwise MCTS would be operating on the real game board.
        :returns: deep copy of this GameState
        """

        return deepcopy(self)


    def step(self, actions: List):
        """
        returns: (obsvervations: List, rewards: List, done: bool)
        :param actions: List of two elements, containing one action for each player
        """

        self.current_state.handle_input(actions[0], actions[1])
        self.current_state.step()

        reward_vector = [self.current_state.get_score(self.player1),
                         self.current_state.get_score(self.player2)]

        # TODO: find if a player has won
        if self.current_state.is_gameover():
            self.winner = 0 if self.player1 == self.current_state.winner else 1

        # info should be kept empty
        info = {}
        return [[], []], reward_vector, \
               self.winner != -1, info

    def get_moves(self, player: int):
        """
        :param player: (int) player for whom we wish to generate moves
        :returns: array with all possible moves, index of columns which aren't full
        TODO: figure out what are the valid moves an agent can take.
        (i.e figure ability cooldowns / collision against map borders)
        """
        available_moves = (self.player1 if player == 0 else self.player2).get_valid_moves(self.current_state)

        if self.winner != -1:
            return []

        return available_moves

    def is_over(self):
        return self.winner != -1

    def get_result(self, player):
        """
        :param player: (int) player which we want to see if he / she is a winner
        :returns: winner from the perspective of the param player
        """
        return self.current_state.get_score(self.player1 if player == 0 else self.player2)

    def render(self, mode='string'):
        # TODO: Here's where we would show the screen based on the game state
        if mode == 'rgb':
            # This might be useful
            self.draw_game()
            return pygame.surfarray.array3d(
                    pygame.display.get_surface()).astype(np.uint8)
        elif mode == 'string':
            return self.current_state.board.test_print()


    def draw_game(self):

        if not self.with_pygame:
            print("WARNING: Game not initialized with pygame flag (with_pygame=True) and cannot draw.")
            return
        else:
            print("Drawing...")

        game = self.current_state

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

        # Setup images
        self.game_folder = os.path.dirname(__file__)

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

        player1 = game.player1
        player2 = game.player2

        # Background color
        screen.fill(BLACK)

        # Set size of sprite to the size of one tile
        player1.image = pygame.transform.scale(player1.image, (WIDTH, HEIGHT))
        player2.image = pygame.transform.scale(player2.image, (WIDTH, HEIGHT))

        # Draw the grid
        for row in range(1,len(game.board.grid)-1):
            for column in range(1,len(game.board.grid)-1):
                color = WHITE
                if game.board.grid[row][column] == player1:
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

                elif game.board.grid[row][column] == player2:
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
