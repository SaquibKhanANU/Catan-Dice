from enum import Enum

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
    KNIGHT = 4

def initialise_structure_resource(structure_type):
    resource_costs = {
        StructureType.CITY: [3, 2, 0, 0, 0, 0],
        StructureType.SETTLEMENT: [0, 1, 1, 1, 1, 0],
        StructureType.ROAD: [0, 0, 0, 1, 1, 0],
        StructureType.JOKER: [1, 1, 1, 0, 0, 0]
    }
    return resource_costs.get(structure_type)