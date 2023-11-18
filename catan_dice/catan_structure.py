import pygame
import os
from catan_dice.catan_enum import *
import catan_dice.assets.colors as Colors

class CatanStructure:
    def __init__(self, structure_type, coordinate, points, id, connections):
        self.structure_type = structure_type
        self.coordinate = coordinate
        self.resource_costs = initialise_structure_resource(structure_type)
        self.id = id
        self.is_built = False
        self.points = points
        self._collision_box = None
        self.connections = connections

        # FIX ASSIGNING THSE
        self.point = None
        self.screen = None

    @property
    def collision_box(self):
        return self._collision_box
    
    @collision_box.setter
    def collision_box(self, collision_box):
        if isinstance(collision_box, pygame.Rect):
            self._collision_box = collision_box

    def can_build(self, player_resources):
        if self.is_built:
            return False
        for required, available in zip(self.resource_costs, player_resources):
            if required > available:
                self.is_built = False
                return False
        self.is_built = True
        return True
    
    def destroy(self):
        if (self.is_built):
            self.is_built = False
            print(f"Destroyed a {self.structure_type} at position {self.coordinate}.")

    def draw_structure(self):
        pass
    
    def draw_hit_box(self):
        size = min(self.screen.get_width(), self.screen.get_height())
        hit_box_size = size / 14
        shift_hit_box = hit_box_size / 2
        self.collision_box = pygame.Rect(self.point[0]-shift_hit_box, self.point[1]-shift_hit_box, hit_box_size, hit_box_size)

    def draw_label(self):
        size = min(self.screen.get_width(), self.screen.get_height())
        font = pygame.font.Font(None, size//50)
        text = font.render(self.id, True, Colors.CATAN_GREEN)
        text_rect = text.get_rect()
        text_rect.center = (self.point[0], self.point[1] - size/25)
        text_rect.center = (self.point[0], self.point[1] + size/100)
        text_rect.center = self.point 
        self.screen.blit(text, text_rect)

    def initialise_structure(self):
        self.draw_structure()
        self.draw_hit_box()
        self.draw_label()

    def check_build_constraints(self, structure_blocks_map):
        check = True
        for connection in self.connections[0]:
            if (not structure_blocks_map[connection].is_built):
                check = False
        return check

    def check_destory_constraints(self, structure_blocks_map):
        check = True
        for connection in self.connections[1]:
            if (structure_blocks_map[connection].is_built):
                check = False
        return check
        

class ROAD(CatanStructure):
    def __init__(self, coordinate, id, connections):
        super().__init__(StructureType.ROAD, coordinate, 1, id, connections)
        self.surface = None

    def draw_structure(self):
        size = min(self.screen.get_width(), self.screen.get_height())
        self.surface = pygame.Surface((size/50 , size/14.5), pygame.SRCALPHA)
        self.surface.fill(Colors.WHITE)
        if (self.id == "RI"):
            self.surface.fill(Colors.PURPLE)
            self.is_built = True
        elif (self.is_built):
            self.surface.fill(Colors.CATAN_BROWN)
        rotated_surface = self.surface
        rect = self.surface.get_rect()
        if (self.coordinate[1] == 0 or self.coordinate[1] == 3):
            rotated_surface = pygame.transform.rotate(self.surface, 30)
        elif (self.coordinate[1] == 1 or self.coordinate[1] == 4):
            rotated_surface = pygame.transform.rotate(self.surface, -30)
        elif (self.coordinate[1] == 2 or self.coordinate[1] == 5):
            rotated_surface = pygame.transform.rotate(self.surface, 90)
        rect = rotated_surface.get_rect(center = (100, 100))
        rect.center = self.point
        border_size = (rotated_surface.get_width() + 6, rotated_surface.get_height() + 6)
        rect_border= pygame.transform.scale(rotated_surface, border_size)
        rect_border.fill(Colors.BLACK, special_flags=pygame.BLEND_RGBA_MULT)
        self.screen.blit(rect_border, (rect.x-3, rect.y-3))
        self.screen.blit(rotated_surface, (rect.x, rect.y))


class CITY(CatanStructure):
    def __init__(self, coordinate, points, id, connections):
        super().__init__(StructureType.CITY, coordinate, points, id, connections)

    def draw_structure(self):
        x, y = self.point
        house_width = min(self.screen.get_width(), self.screen.get_height()) // 20
        house_height = min(self.screen.get_width(), self.screen.get_height()) // 50
        vertices = [
            # Top-left corner
            (x - house_width // 2, y),
            # Bottom-left corner
            (x - house_width // 2, y + house_height),
            # Bottom-right corner
            (x + house_width // 2, y + house_height),
            # Top-right corner
            (x + house_width // 2, y),
            # extend top right corner
            (x + house_width // 2, y-house_height/4),
            #shift roof outwards right side
            ((x + house_width // 2)+house_width/12.5, y-house_height/4),
            # roof peak
            ((x + house_width // 4)+house_width/25, y-1.5*house_height),
            # extend top left roof corner
            (x, y-house_height/4),
            # shift roof inwards left side
            (x+house_width/12.5, y-house_height/4),
            # bring back roof back to center
            (x+house_width/12.5, y),
        ]
        if (self.is_built):
            color = Colors.CATAN_BROWN
        else:
            color = Colors.WHITE
        pygame.draw.polygon(self.screen, color, vertices)
        pygame.draw.polygon(self.screen, Colors.BLACK, vertices, 3)

    def draw_label(self):
        size = min(self.screen.get_width(), self.screen.get_height())
        font = pygame.font.Font(None, size//50)
        text = font.render(self.id, True, Colors.CATAN_GREEN)
        text_rect = text.get_rect()
        text_rect.center = (self.point[0], self.point[1] - size/25)
        text_rect.center = (self.point[0], self.point[1] + size/100)
        self.screen.blit(text, text_rect)

class SETTLEMENT(CatanStructure):
    def __init__(self, coordinate, points, id, connections):
        super().__init__(StructureType.SETTLEMENT, coordinate, points, id, connections)

    def draw_structure(self):
        x, y = self.point
        house_width = min(self.screen.get_width(), self.screen.get_height()) // 30
        house_height = min(self.screen.get_width(), self.screen.get_height()) // 40
        vertices = [
            # Top-left corner
            (x - house_width // 2, y),
            # Bottom-left corner
            (x - house_width // 2, y + house_height),
            # Bottom-right corner
            (x + house_width // 2, y + house_height),
            # Top-right corner
            (x + house_width // 2, y),
            # extend top right corner
            ((x + house_width // 2)+house_width/16.5, y),
            # Roof peak (top center)
            (x, y - house_height),
            ((x - house_width // 2) - house_width/16.5, y),
        ]
        if (self.is_built):
            color = Colors.CATAN_BROWN
        else:
            color = Colors.WHITE
        pygame.draw.polygon(self.screen, color, vertices)
        pygame.draw.polygon(self.screen, Colors.BLACK, vertices, 3)

class JOKER(CatanStructure):
    def __init__(self, coordinate, points, resource_type, id, connections):
        super().__init__(StructureType.JOKER, coordinate, points, id, connections)
        self.resource_type = resource_type
        self.is_knight = False
        self.size = None

    def draw_structure(self):
        self.size = min(self.screen.get_width(), self.screen.get_height())
        x, y = self.point
        if (self.is_built):
            color = Colors.YELLOW
        else:
            color = Colors.WHITE
        pygame.draw.circle(self.screen, Colors.BLACK, (x,y-self.size/33), self.size/45)
        pygame.draw.circle(self.screen, Colors.BLACK, self.point, self.size/30)
        pygame.draw.circle(self.screen, color, self.point, self.size/33) 
        folder = "catan_dice"
        filename = "Resource" + str(self.id[1]) + ".png"
        image_path = os.path.join(folder, "assets", "Resources", filename)
        image = pygame.image.load(image_path)        
        image_size = self.size//25
        scaled_image = pygame.transform.scale(image, (image_size, image_size))
        self.screen.blit(scaled_image, (x-image_size/2, y-image_size/2))

    def draw_label(self):
        size = min(self.screen.get_width(), self.screen.get_height())
        font = pygame.font.Font(None, size//50)
        text = font.render(self.id, True, Colors.CATAN_GREEN)
        text_rect = text.get_rect()
        text_rect.center = (self.point[0], self.point[1] - size/25)
        self.screen.blit(text, text_rect)

def initialise_structure_resource(structure_type):
    resource_costs = {
        StructureType.CITY: [3, 2, 0, 0, 0, 0],
        StructureType.SETTLEMENT: [0, 1, 1, 1, 1, 0],
        StructureType.ROAD: [0, 0, 0, 1, 1, 0],
        StructureType.JOKER: [1, 1, 1, 0, 0, 0]
    }
    return resource_costs.get(structure_type)