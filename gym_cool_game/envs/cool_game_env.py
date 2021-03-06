import warnings
from typing import List
from copy import deepcopy
import numpy as np
import gym
from gym.spaces import Discrete, Box, Tuple

from .game import Game
from .board import Board
from .pygame_render import PygameRender
from .bots import *
from .valid_inputs import *
from .game_params import (GameParams, TorchParams, SawBotParams, NailBotParams,
                          construct_game_params)

class CoolGameEnv(gym.Env):

    def __init__(self,
                 botA_type: int = 0, botB_type: int = 0,
                 board_size: int = 7,
                 max_game_ticks: int = 500,
                 p1_starting_position: List = [2,2],
                 p2_starting_position: List = [4,4],
                 # TorchBot parameters
                 torch_health=7,
                 torch_dmg=3,
                 torch_weight=2,
                 torch_torch_range=3,
                 torch_duration=2,
                 torch_cooldown=5,
                 torch_ticks_between_moves=4,
                 # SawBot parameters 
                 saw_health=4,
                 saw_dmg_min=6,
                 saw_dmg_max=6,
                 saw_weight=3,
                 saw_duration=3,
                 saw_cooldown=3,
                 saw_ticks_between_moves=5,
                 # NaileBot parameters
                 nail_health=3,
                 nail_dmg=9,
                 nail_weight=1,
                 nail_cooldown=1,
                 nail_ticks_between_moves=2, omit_construction = False):
        # Each player has 5 actions. Directional moves: UP / DOWN/ LEFT / RIGHT
        # And a 5th "Action", which is bot dependant
        if not omit_construction:
          self.action_space = Tuple([Discrete(5), Discrete(5)])
          single_agent_observation = Box(shape=(board_size, board_size),
                                         low=0, high=5, dtype=int) # TODO: find maximum number of values
          self.observation_space = Tuple([single_agent_observation,
                                          single_agent_observation])

          # Game params
          self.max_game_ticks = max_game_ticks
          self.p1_starting_position = p1_starting_position
          self.p2_starting_position = p2_starting_position

          # Bot params
          self.game_params = construct_game_params(
                  torch_health, torch_dmg, torch_weight,
                  torch_torch_range, torch_duration,
                  torch_cooldown, torch_ticks_between_moves,
                  saw_health,saw_dmg_min, saw_dmg_max,
                  saw_weight, saw_duration,
                  saw_cooldown, saw_ticks_between_moves,
                  nail_health, nail_dmg, nail_weight,
                  nail_cooldown, nail_ticks_between_moves)

          self.botA_type = botA_type
          self.botB_type = botB_type
          self.board_size = board_size       
          self.reset()


    def clone(self):
        """
        Creates a deep copy of the game state.
        NOTE: it is _really_ important that a copy is used during simulations
              Because otherwise MCTS would be operating on the real game board.
        :returns: deep copy of this GameState
        """
        
        cpy = CoolGameEnv(omit_construction=True)
        cpy.action_space = self.action_space
        cpy.observation_space = self.observation_space
        cpy.max_game_ticks = self.max_game_ticks
        cpy.p1_starting_position = self.p1_starting_position
        cpy.p2_starting_position = self.p2_starting_position
        cpy.game_params = self.game_params
        cpy.botA_type = self.botA_type
        cpy.botB_type = self.botB_type
        cpy.board_size = self.board_size
        cpy.winner = self.winner
        cpy.current_state = self.current_state.clone()
        cpy.player1 = cpy.current_state.player1
        cpy.player2 = cpy.current_state.player2
        cpy.board = cpy.current_state.board

        return cpy


    def reset(self):
        self.winner = -1 # Values: [-1, 0, 1]
        self.player1 = self.get_bot(self.botA_type, player_index=0)
        self.player2 = self.get_bot(self.botB_type, player_index=1)
        self.board = Board(self.board_size)
        self.current_state = Game(self.board, self.player1, self.player2,
                                  self.p1_starting_position, self.p2_starting_position,
                                  self.max_game_ticks)
        state = np.array([self.player1.health, self.player2.health,
                          self.player1.is_sleeping(), self.player2.is_sleeping()])
        # TODO: Currently incomplete
        return np.array([deepcopy(state), deepcopy(state)])

    def get_bot(self, bot_type, player_index):
        if bot_type == BOT_TYPE_SPIKE:
            bot = SawBot(self.game_params.saw_params)
        elif bot_type == BOT_TYPE_TORCH:
            bot = TorchBot(self.game_params.torch_params)
        elif bot_type == BOT_TYPE_NAIL:
            bot = NailBot(self.game_params.nail_params)
        bot.player_index = player_index
        return bot

    def step(self, actions: List):
        """
        returns: (obsvervations: List, rewards: List, done: bool)
        :param actions: List of two elements, containing one action for each player
        """
        # Check input validity
        for i, (p, action) in enumerate(zip([self.player1, self.player2], actions)):
            if action not in p.get_valid_moves(self.current_state):
                warnings.warn(f'Player {i} took invalid action {action}. Valid actions: {p.get_valid_moves(self.current_state)}. None action taken instead')
                actions[i] = NONE_ACTION

        self.current_state.handle_input(self.current_state, actions[0], actions[1])
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
        if self.winner != -1:
            return []
        available_moves = (self.player1 if player == 0 else self.player2).get_valid_moves(self.current_state)
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
        if mode == 'rgb':
            return PygameRender(self).draw()
        elif mode == 'string':
            game_stats = f'Current tick: {self.current_state.ticks}'
            p1_health = self.player1.health
            p2_health = self.player2.health
            p1_sleeping = self.player1.is_sleeping()
            p2_sleeping = self.player2.is_sleeping()
            p1_moves = self.player1.get_valid_moves(self.current_state)
            p2_moves = self.player2.get_valid_moves(self.current_state)
            player1_stats = f'P1: health={p1_health}, sleeping={p1_sleeping}. Moves: {p1_moves}'
            player2_stats = f'P2: health={p2_health}, sleeping={p2_sleeping}. Moves: {p2_moves}'
            player_stats = player1_stats + '\n' + player2_stats
            board_state = str(self.current_state.board)
            return game_stats + '\n' + player_stats + '\n' + board_state
