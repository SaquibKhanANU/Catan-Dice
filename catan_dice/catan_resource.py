from enum import Enum

# Create the DICE. 0 = Ore, 1 = Grain, 2 = Wool, 3 = Timber, 4 = Brick, 5 = Gold.
DICE = [0, 1, 2, 3, 4, 5]

class ResourceType(Enum):
    ORE = 0
    WOOL = 1
    GRAIN = 2
    TIMBER = 3
    BRICK = 4
    GOLD = 5

