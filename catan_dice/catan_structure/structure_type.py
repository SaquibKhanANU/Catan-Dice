from enum import Enum

class StructureType(Enum):
    CITY = 1
    SETTLEMENT = 2
    ROAD = 3
    JOKER = 4

def initialise_structure_resource(structure_type):
    resource_costs = {
        StructureType.CITY: [3, 2, 0, 0, 0, 0],
        StructureType.SETTLEMENT: [0, 1, 1, 1, 1, 0],
        StructureType.ROAD: [0, 0, 0, 1, 1, 0],
        StructureType.JOKER: [1, 1, 1, 0, 0, 0]
    }
    return resource_costs.get(structure_type)

def initialise_structure_points(structure_type):
    points = {
        StructureType.CITY: 3,
        StructureType.SETTLEMENT: 5,
        StructureType.ROAD: 1,
        StructureType.JOKER: 2
    }
    return points.get(structure_type)