import pygame
from enum import Enum

class StructureType(Enum):
    CITY = 0
    SETTLEMENT = 1
    ROAD = 2
    JOKER = 3

def initialise_structure_resource(structure_type):
    resource_costs = {
        StructureType.CITY: [3, 2, 0, 0, 0, 0],
        StructureType.SETTLEMENT: [0, 1, 1, 1, 1, 0],
        StructureType.ROAD: [0, 0, 0, 1, 1, 0],
        StructureType.JOKER: [1, 1, 1, 0, 0, 0]
    }
    return resource_costs.get(structure_type)


class CatanStructure:
    def __init__(self, structure_type, coordinate, points):
        self.structure_type = structure_type
        self.coordinate = coordinate
        self.resource_costs = initialise_structure_resource(structure_type)
        self.is_built = False
        self.points = points
        self._colission_box = None

    @property
    def collision_box(self):
        return self._colission_box
    
    @collision_box.setter
    def collision_box(self, collision_box):
        if isinstance(collision_box, pygame.Rect):
            self._colission_box = collision_box
        
    def build(self, player_resources):
        if self.can_build(player_resources):
            print(f"Building a {self.structure_type} at position {self.coordinate}.")
            for i in range(len(player_resources)):
                player_resources[i] -= self.resource_costs[i]
            self.is_built = True
        else:
            print(f"Cannot build {self.structure_type} at position {self.coordinate}. Insufficient resources.")

    def can_build(self, player_resources):
        if self.is_built:
            raise Exception("Structure already built")
        for required, available in zip(self.resource_costs, player_resources):
            if required > available:
                return False
        return True


class JOKER(CatanStructure):
    def __init__(self, coordinate, points, resource_type):
        super().__init__(StructureType.JOKER, coordinate, points)
        self.resource_type = resource_type


