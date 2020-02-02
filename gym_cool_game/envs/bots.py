from gym_cool_game.envs.game import Bot


class SawBot(Bot):

	def __init__(self,
				 dmg_min=1,
				 dmg_max=5,
				 weight=3,
				 duration=3,
				 cooldown=5):
		super().__init__('SawBot')

		self.dmg_min = dmg_min
		self.dmg = dmg_min
		self.dmg_max = dmg_max
		self.weight = weight
		self.duration = duration
		self.cooldown = cooldown
		self.active_time = 0

	def act(self):

		if self.active_time < self.cooldown:
			self.active_time = self.duration + self.cooldown
			self.dmg = self.dmg_max

	def tick_bot(self, state):

		self.active_time -= 1
		# if ability is active, get adjacent cells
		if self.active_time > self.cooldown:
			for x, y in [(self.pos_x + i, self.pos_y + j)
						 for i in (-1, 0, 1) for j in (-1, 0, 1)
						 if i != 0 or j != 0]:
				# check if bot exists
				cell = state.board.get(x, y)
				if hasattr(cell, 'health'):
					# apply damage if the saw ability is active
					cell.health -= self.dmg
					break


class NailBot(Bot):

	def __init__(self,
				 dmg=1,
				 weight=1,
				 bullet_speed=3,
				 cooldown=2):
		super().__init__('NailBot')

		self.dmg = dmg
		self.weight = weight
		self.bullet_speed = bullet_speed
		self.cooldown = cooldown
		self.ability_counter = 0

	def act(self):
		# spawn bullet, moves in direction self.curr_rotation at speed self.bullet_speed
		self.ability_counter = self.cooldown

	def tick_bot(self, state):

		if self.ability_counter > 0:
			self.ability_counter -= 1


class BlowTorch(Bot):

	def __init__(self,
				 dmg=2,
				 weight=2,
				 torch_range=2,
				 duration=2,
				 cooldown=3):
		super().__init__('BlowTorch')

		self.dmg = dmg
		self.weight = weight
		self.torch_range = torch_range
		self.duration = duration
		self.cooldown = cooldown

	def act(self):

		if self.active_time < self.cooldown:
			self.active_time = self.duration + self.cooldown

	def tick_bot(self, state):

		self.active_time -= 1
		# if ability is active spawn flame in direction of current rotation with range of torch_range
		if self.active_time > self.cooldown:
			if self.curr_rotation == 0:
				torch_cells = [(self.pos_x, self.pos_y - i) for i in range(1, self.torch_range+1)]
			elif self.curr_rotation == 90:
				torch_cells = [(self.pos_x + i, self.pos_y) for i in range(1, self.torch_range+1)]
			elif self.curr_rotation == 180:
				torch_cells = [(self.pos_x, self.pos_y + i) for i in range(1, self.torch_range+1)]
			else:
				torch_cells = [(self.pos_x - i, self.pos_y ) for i in range(1, self.torch_range+1)]
			for cell in torch_cells:
				cell = state.board.get(cell[0], cell[1])
				if hasattr(cell, 'health'):
					# apply damage to opponent if they are in torch_cells
					cell.health -= self.dmg
					break
