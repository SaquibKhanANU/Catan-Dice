from enum import Enum

DICE = [0, 1, 2, 3, 4, 5]

class ResourceType(Enum):
    ORE = 0
    WOOL = 1
    GRAIN = 2
    TIMBER = 3
    BRICK = 4
    GOLD = 5

class StructureType(Enum):
    CITY = 0
    SETTLEMENT = 1
    ROAD = 2
    JOKER = 3
    # KNIGHT = 4

class ActionType(Enum):
    ROLL = 0
    SWAP = 1
    TRADE = 2
    END_TURN = 3

