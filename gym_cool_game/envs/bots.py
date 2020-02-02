from game import Bot


class SawBot(Bot):

	def __init__(self,
				 dmg_min=1,
				 dmg_max=5,
				 weight=3,
				 duration=3,
				 cooldown=5,
				 ticks_between_moves=1):
		Bot.__init__(self, 'SawBot')

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
					# apply damage
					cell.health -= self.dmg
					break


class NailBot(Bot):

	def __init__(self,
				 dmg=1,
				 weight=1,
				 bullet_speed=3,
				 cooldown=2,
				 ticks_between_moves=3):
		Bot.__init__(self, 'NailBot')

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


class TorchBot(Bot):

	def __init__(self,
				 dmg=2,
				 weight=2,
				 torch_range=2,
				 duration=2,
				 cooldown=3,
				 ticks_between_moves=2):
		Bot.__init__(self, 'Torch')

		self.dmg = dmg
		self.weight = weight
		self.torch_range = torch_range
		self.duration = duration
		self.cooldown = cooldown
		self.active_time = 0
		self.torch_cells = []

	def act(self):

		if self.active_time < self.cooldown:
			self.active_time = self.duration + self.cooldown

	def tick_bot(self, state):

		self.active_time -= 1
		# if ability is active spawn flame in direction of current rotation with range of torch_range
		if self.active_time > self.cooldown:
			if self.curr_rotation == 1:
				self.torch_cells = [(self.pos_x, self.pos_y - i) for i in range(1, self.torch_range+1)]
			elif self.curr_rotation == 2:
				self.torch_cells = [(self.pos_x + i, self.pos_y) for i in range(1, self.torch_range+1)]
			elif self.curr_rotation == 3:
				self.torch_cells = [(self.pos_x, self.pos_y + i) for i in range(1, self.torch_range+1)]
			else:
				self.torch_cells = [(self.pos_x - i, self.pos_y ) for i in range(1, self.torch_range+1)]
			for cell in self.torch_cells:
				cell = state.board.get(cell[0], cell[1])
				if hasattr(cell, 'health'):
					# apply damage to opponent if they are in torch_cells
					cell.health -= self.dmg
					break
		else:
			self.torch_cells = []
