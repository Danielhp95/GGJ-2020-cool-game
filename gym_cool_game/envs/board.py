class Board:

    def __init__(self, board_size, bot1, bot2):
        self.grid = [[0 for x in range(int(board_size))] for y in range(int(board_size))] # Unoccupied tiles will have value 0

    # Set the position of bot to (x, y)
    # Must be fed an object of class Bot, of course
    def set(self, x, y, bot):
        self.grid[x][y] = 1 #set new tile on grid to occupied
        bot.pos[0] = x
        bot.pos[1] = y

        # why you no work dsjkfldasjlf

    # Get a list of valid directional moves for bot
    def get_valid_moves(self, bot):

        if bot.pos[0]

        bot.pos[0]
        return []


    # Move bot in direction
    def move(self, bot, direction):
        pass

babyBot = Bot()
mamaBot = Bot()
myboard = Board(10, babyBot, mamaBot)
