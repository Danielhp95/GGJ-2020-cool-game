from .valid_inputs import DIRECTION_LEFT, DIRECTION_DOWN, DIRECTION_RIGHT, DIRECTION_UP, ACTION, NONE_ACTION
from .game_params import NailBotParams, SawBotParams, TorchParams

BOT_TYPE_SPIKE = 0
BOT_TYPE_TORCH = 1
BOT_TYPE_NAIL = 2

class Bot():

    def __init__(self, name: str, ticks_between_moves: int, weight: int):
        self.ticks_between_moves = ticks_between_moves
        self.sleep = 0
        self.weight = 1
        self.pos_x = -100
        self.pos_y = -100
        self.name = str(name)
        self.curr_rotation = DIRECTION_UP
        self.health = 10
        self.max_health = 10

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

    def get_actions_bot(self, state):
        return [ACTION]

    def after_move(self):
        self.sleep = self.ticks_between_moves

    def act(self, state):
        pass

    def tick_bot(self, state):
        pass

    def __repr__(self):
        return self.name[0]

class SawBot(Bot):

    def __init__(self, params: SawBotParams):
        Bot.__init__(self, 'SawBot', params.ticks_between_moves, params.weight)
        self.dmg_min = params.dmg_min
        self.dmg_max = params.dmg_max
        self.duration = params.duration
        self.cooldown = params.cooldown

        self.dmg = self.dmg_min
        self.active_time = 0

    def act(self, state):
        if self.active_time < self.cooldown:
            self.active_time = self.duration + self.cooldown
            self.dmg = self.dmg_max

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


class NailBot(Bot):

    def __init__(self, params: NailBotParams):
        super(NailBot, self).__init__('NailBot', params.ticks_between_moves, params.weight)

        self.dmg = params.dmg
        self.cooldown = params.cooldown

        self.ability_counter = 0
        self.active_bullets = []

    def act(self, state):
        # spawn bullet, moves in direction self.curr_rotation at speed self.bullet_speed
        self.ability_counter = self.cooldown
        if self.active_time > self.cooldown:
            if self.curr_rotation == DIRECTION_UP: bullet_x, bullet_y = self.pos_x - 1, self.pos_y 
            if self.curr_rotation == DIRECTION_DOWN: bullet_x, bullet_y = self.pos_x + 1, self.pos_y
            if self.curr_rotation == DIRECTION_LEFT: bullet_x, bullet_y = self.pos_x, self.pos_y - 1
            if self.curr_rotation == DIRECTION_RIGHT: bullet_x, bullet_y = self.pos_x, self.pos_y + 1
            new_bullet = Bullet(bullet_x, bullet_y, self.curr_rotation)
            self.active_bullets.append(new_bullet)

    def tick_bot(self, state):
        if self.ability_counter > 0:
            self.ability_counter -= 1
        for b in self.active_bullets: b.tick(state)


class Bullet:

    def __init__(self, pos_x, pos_y, direction):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.direction = direction

    def tick(self, state):
        cell = state.board.get(self.pos_x, self.pos_y)

        # Check for destruction conditions
        if hasattr(cell, 'health'):
            cell.health -= self.dmg
            del self
            return
        if cell == 1:  # 1 refers to boundaries
            del self
            return

        # Move to direction
        if self.direction == DIRECTION_UP:
            self.pos_x -= 1
        if self.direction == DIRECTION_DOWN:
            self.pos_x += 1
        if self.direction == DIRECTION_LEFT:
            self.pos_y -= 1
        if self.direction == DIRECTION_RIGHT:
            self.pos_y += 1


class TorchBot(Bot):

    def __init__(self, params: TorchParams):
        Bot.__init__(self, 'TorchBot', params.ticks_between_moves, params.weight)

        self.dmg = params.dmg
        self.torch_range = params.torch_range
        self.duration = params.duration
        self.cooldown = params.cooldown

        self.active_time = 0
        self.torch_cells = []

    def act(self, state):
        if self.active_time < self.cooldown:
            self.active_time = self.duration + self.cooldown

    def tick_bot(self, state):
        self.active_time -= 1
        # if ability is active spawn flame in direction of current rotation with range of torch_range
        if self.active_time > self.cooldown:
            if self.curr_rotation == DIRECTION_LEFT:  # Left
                self.torch_cells = [(self.pos_x, self.pos_y - i) for i in range(1, self.torch_range+1)]
            elif self.curr_rotation == DIRECTION_UP:  # Up
                self.torch_cells = [(self.pos_x - i, self.pos_y ) for i in range(1, self.torch_range+1)]
            elif self.curr_rotation == DIRECTION_RIGHT:  # Right
                self.torch_cells = [(self.pos_x, self.pos_y + i) for i in range(1, self.torch_range+1)]
            elif self.curr_rotation == DIRECTION_DOWN:  # Down
                self.torch_cells = [(self.pos_x + i, self.pos_y) for i in range(1, self.torch_range+1)]
            for cell in self.torch_cells:
                cell = state.board.get(cell[0], cell[1])
                if hasattr(cell, 'health'):
                    # apply damage to opponent if they are in torch_cells
                    cell.health -= self.dmg
                    break
        else:
            self.torch_cells = []
