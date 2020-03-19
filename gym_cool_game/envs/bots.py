from .valid_inputs import DIRECTION_LEFT, DIRECTION_DOWN, DIRECTION_RIGHT, DIRECTION_UP, ACTION, NONE_ACTION, DIRECTIONS
from .game_params import NailBotParams, SawBotParams, TorchParams
from colorama import Fore

BOT_TYPE_SPIKE = 0
BOT_TYPE_TORCH = 1
BOT_TYPE_NAIL = 2

class Bot():

    def __init__(self, name: str, ticks_between_moves: int,
                 weight: int, cooldown: int, health: int):
        self.ticks_between_moves = ticks_between_moves
        self.sleep = 0
        self.weight = 1
        self.pos_x = -100
        self.pos_y = -100
        self.name = str(name)
        self.curr_rotation = DIRECTION_UP
        self.health = health
        self.max_health = health

        self.ticks_till_action_available = 0
        self.cooldown = cooldown

        # To be set outside of __init__ 
        self.player_index = None

    def copy_to(self, cpy):
        cpy.ticks_between_moves = self.ticks_between_moves
        cpy.sleep = self.sleep
        cpy.weight = self.weight
        cpy.pos_x = self.pos_x
        cpy.pos_y = self.pos_y
        cpy.name = self.name
        cpy.curr_rotation = self.curr_rotation
        cpy.health = self.health
        cpy.max_health = self.max_health
        cpy.ticks_till_action_available = self.ticks_till_action_available
        cpy.cooldown = self.cooldown
        cpy.player_index = self.player_index

    def tick(self, state):
        if self.sleep > 0:
            self.sleep -= 1

        self.tick_bot(state)

    def update_rotation(self, direction):
        self.curr_rotation = direction

    def is_sleeping(self):
        return self.sleep > 0

    def get_valid_moves(self, state):
        moves = [NONE_ACTION]
        if not self.is_sleeping():
            moves += self.get_moves_bot(state) + self.get_actions_bot(state)
        return moves

    def get_moves_bot(self, state):
        return state.board.get_valid_moves(self)

    def after_move(self):
        self.sleep = self.ticks_between_moves

    def act(self, state):
        pass

    def tick_bot(self, state):
        if self.ticks_till_action_available > 0:
            self.ticks_till_action_available -= 1

    def __repr__(self):
        color = Fore.GREEN if self.player_index == 0 else Fore.BLUE
        return color + self.name[0] + Fore.RESET

    def get_actions_bot(self, state):
        if self.ticks_till_action_available == 0: return [ACTION]
        else: return []


class SawBot(Bot):

    def __init__(self, params: SawBotParams):
        Bot.__init__(self, 'SawBot', params.ticks_between_moves, params.weight,
                     params.cooldown, params.health)
        self.params = params
        self.dmg_min = params.dmg_min
        self.dmg_max = params.dmg_max
        self.duration = params.duration

        self.dmg = self.dmg_min
        self.active_time = 0

    def act(self, state):
        if self.ticks_till_action_available <= 0:
            self.active_time = self.duration + self.cooldown
            self.dmg = self.dmg_max
            self.ticks_till_action_available = self.duration + self.cooldown

    def tick_bot(self, state):
        self.active_time -= 1
        # get adjacent cells
        for x, y in [(self.pos_x + i, self.pos_y + j)
		     for i in (-1, 0, 1) for j in (-1, 0, 1)
		     if i != 0 or j != 0]:
	    # check if bot exists
            cell = state.board.get(x, y)
            if hasattr(cell, 'health'):
                # apply damage
                cell.health -= self.dmg
                break
        super(SawBot, self).tick_bot(state)

    def clone(self):
        cpy = SawBot(self.params)
        self.copy_to(cpy)
        cpy.dmg = self.dmg
        cpy.active_time = self.active_time
        return cpy


class TorchBot(Bot):

    def __init__(self, params: TorchParams):
        Bot.__init__(self, 'TorchBot', params.ticks_between_moves,
                     params.weight, params.cooldown, params.health)

        self.params = params
        self.dmg = params.dmg
        self.torch_range = params.torch_range
        self.duration = params.duration

        self.active_time = 0
        self.torch_cells = []

    def act(self, state):
        if self.active_time < self.cooldown:
            self.ticks_till_action_available = self.duration + self.cooldown
            self.active_time = self.duration + self.cooldown

    def tick_bot(self, state):
        self.active_time -= 1
        # if ability is active spawn flame in direction of current rotation with range of torch_range
        # Understand why this is the opposite as saw bot
        if self.ticks_till_action_available > self.cooldown: # Hacky way to say '
            self.update_torch_cells(state)
        else:
            self.torch_cells = []
        super(TorchBot, self).tick_bot(state)

    def update_torch_cells(self, state):
        self.torch_cells = [(self.pos_x, self.pos_y - i) for i in range(1, self.torch_range+1)] + \
                            [(self.pos_x - i, self.pos_y ) for i in range(1, self.torch_range+1)] + \
                            [(self.pos_x, self.pos_y + i) for i in range(1, self.torch_range+1)] + \
                            [(self.pos_x + i, self.pos_y) for i in range(1, self.torch_range+1)]

        self.torch_cells = [cell for cell in self.torch_cells if state.board.currently_on_board(*cell) and state.board.get(*cell) != 1]
        for cell in self.torch_cells:
            cell = state.board.get(cell[0], cell[1])
            if hasattr(cell, 'health'):
                cell.health -= self.dmg
                break

    def clone(self):
        cpy = TorchBot(self.params)
        self.copy_to(cpy)
        cpy.active_time = self.active_time
        cpy.torch_cells = self.torch_cells.copy()

        return cpy


class NailBot(Bot):

    def __init__(self, params: NailBotParams):
        super(NailBot, self).__init__('NailBot', params.ticks_between_moves,
                                      params.weight, params.cooldown, params.health)
        self.params = params
        self.dmg = params.dmg
        self.active_bullets = []

    def act(self, state):
        if self.ticks_till_action_available <= 0:
            self.ticks_till_action_available = self.cooldown
            for direction in DIRECTIONS:
                new_bullet = Bullet(self, direction, state)
                self.active_bullets.append(new_bullet)

    def tick_bot(self, state):
        super(NailBot, self).tick_bot(state)

        for b in self.active_bullets:
            b.tick(state)
        
        self.active_bullets = [b for b in self.active_bullets if b.is_alive]


    def clone(self):
        cpy = NailBot(self.params)
        self.copy_to(cpy)
        cpy.active_bullets = [b.clone() for b in self.active_bullets]
        return cpy



class Bullet:

    def __init__(self, creator, direction, state):
        self.creator = creator
        self.dmg = creator.dmg
        self.pos_x = creator.pos_x
        self.pos_y = creator.pos_y
        self.direction = direction
        self.is_alive = True

    def clone(self):
        cpy = Bullet(self.creator, self.direction, None)
        cpy.is_alive = self.is_alive
        cpy.pos_x = self.pos_x
        cpy.pos_y = self.pos_y
        return cpy

    def tick(self, state):
        self.collide(state)
        self.move()
        self.collide(state)

    def move(self):
        if self.direction == DIRECTION_UP:
            self.pos_x -= 1
        if self.direction == DIRECTION_DOWN:
            self.pos_x += 1
        if self.direction == DIRECTION_LEFT:
            self.pos_y -= 1
        if self.direction == DIRECTION_RIGHT:
            self.pos_y += 1

    def collide(self, state):
        cell = state.board.get(self.pos_x, self.pos_y)

        # Check for destruction conditions
        if self.is_alive and hasattr(cell, 'health') and (cell != self.creator): # bot occupies area
            cell.health -= self.dmg
            self.is_alive = False

        self.is_alive = self.is_alive and not self.reached_boundary(cell)

    def reached_boundary(self, cell):
        return cell == 1

    def __repr__(self):
        return Fore.YELLOW + 'n' + Fore.RESET  # 'n' for nail. Lowercase to differentiate from bots
