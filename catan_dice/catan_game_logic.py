import random
from catan_dice.catan_board import *

class GameState:
    def __init__(self):
        self.catan_board = CatanBoard()
        self.player = CatanPlayer()
        self.dice_rolled = False

def roll_dice(n_dice, resource_state):
    for _ in range(n_dice):
        roll_value = random.choice(DICE)
        resource_count = resource_state[roll_value]
        resource_count += 1  # Increment the number of that resource by 1
        resource_state[roll_value] = resource_count