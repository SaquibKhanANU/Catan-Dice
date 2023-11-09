from catan_dice.catan_structure.structure_type import initialise_structure_resource, initialise_structure_points
import pygame

class CatanStructure:
    def __init__(self, structure_type, coordinate):
        self.structure_type = structure_type
        self.coordinate = coordinate
        self.resource_costs = initialise_structure_resource(structure_type=structure_type)
        self.is_built = False
        self.points = initialise_structure_points(structure_type=structure_type)
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
