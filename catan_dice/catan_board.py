from catan_dice.catan_structure import *
from catan_dice.catan_enum import *
import math
import os

BOARD_HEIGHT = 1000
BOARD_WIDTH = 1000
PANEL_WIDTH = BOARD_WIDTH / 3

class CatanBoard:
    def __init__(self, structure_blocks_map, screen):
        self.catanBoard = [[[None for _ in range(3)] for _ in range(6)] for _ in range(6)]
        self.structure_blocks_map = structure_blocks_map
        self.screen = screen
        self.board_width = BOARD_WIDTH
        self.board_height = BOARD_HEIGHT
        self.panel_width = PANEL_WIDTH
        self.panel_border_width = 10
        self.resource_size = (self.panel_width)/6
        self.control_buttons = [
            Button((self.board_width+self.panel_width/8, self.board_height/20, self.panel_width*0.75, self.board_height/10), self.screen, Colors.BLACK,
                    "ROLL DICE",
                    lambda: print("NULL")),
            ]
    
    def draw_board(self):
        self.screen.fill(Colors.OCEAN_BLUE)
        self.board_width = self.screen.get_width() - self.panel_width
        self.board_height = self.screen.get_height()
        self.hexagon_size = min(self.board_height, self.board_width) / 6
        center_x = self.board_width/2
        center_y = self.board_height/2
        # Create multiple hexagons in a circle
        num_hexagons = 6
        self.hexagons = []
        for i in range(num_hexagons):
            angle = math.radians(240 + 60 * i)  # Counter-clockwise, starting from the top-left
            x = center_x + 1.80 * self.hexagon_size * math.sin(angle)
            y = center_y + 1.80 * self.hexagon_size * math.cos(angle)
            self.hexagons.append(Hexagon((x, y), self.hexagon_size))

        hexagons = self.hexagons
        for order_index in range(6):
            hexagon = hexagons[order_index]
            vertices = hexagon.vertices
            pygame.draw.polygon(self.screen, Colors.DARK_BROWN, vertices, 10)
            pygame.draw.polygon(self.screen, Colors.SANDY_BROWN, vertices)
            folder = "catan_dice"
            filename = "Hex" + str(order_index) + ".png"
            image_path = os.path.join(folder, "assets", "HexagonTiles", filename)
            image = pygame.image.load(image_path)
            x, y = hexagon.calculate_center()
            if (order_index == 5):
                scaled_image = pygame.transform.scale(image, (2.3*hexagon.size, 2.3*hexagon.size))
                self.screen.blit(scaled_image, (hexagon.center[0]-scaled_image.get_width()/2,hexagon.center[1]-scaled_image.get_height()/2))
            else:
                scaled_image = pygame.transform.scale(image, (2.8*hexagon.size, 2.8*hexagon.size))
                self.screen.blit(scaled_image, (hexagon.center[0]-scaled_image.get_width()/2,hexagon.center[1]-scaled_image.get_height()/2))

        for structure in self.structure_blocks_map.values():
            structure.screen = self.screen
            self.initialise_structure_at_coordinate(structure)
            structure.initialise_structure()
        
    def initialise_structure_at_coordinate(self, structure):
        coordinate = structure.coordinate
        hexagon, point, point_type = coordinate
        # structure_type = structure.structure_type
        # self.catanBoard[hexagon][point][point_type] = CatanStructure(structure_type, coordinate, structure.points, structure.id)
        if (point_type == 0):
            structure.point = self.hexagons[hexagon].edge_midpoints[point]
        elif(point_type == 1):
            structure.point = self.hexagons[hexagon].vertices[point]
        elif(point_type == 2):
            structure.point = self.hexagons[hexagon].calculate_center()

    def get_structure_at_coordinate(self, coordinate):
        hexagon, point, point_type = coordinate
        return self.catanBoard[hexagon][point][point_type]
    
    def draw_panel(self):
        # border
        panel_border = pygame.Surface((self.panel_width+10, self.board_height))
        panel_border.fill(Colors.BLACK)
        self.screen.blit(panel_border, (self.board_width, 0))

        panel = pygame.Surface((self.panel_width-self.panel_border_width, self.board_height-self.panel_border_width))
        panel.fill(Colors.CATAN_GREEN)
        self.screen.blit(panel, (self.board_width+self.panel_border_width//2, self.panel_border_width//2))
    
    def draw_resources(self):
        self.resource_size = (self.panel_width)/9
        resouces_box_border = pygame.Surface((self.panel_width, self.board_height/2.5))
        resouces_box_border.fill(Colors.BLACK)
        self.screen.blit(resouces_box_border, (self.board_width, self.board_height/5))
        resouces_box = pygame.Surface((self.panel_width-self.panel_border_width,self.board_height/2.5-self.panel_border_width))
        resouces_box.fill(Colors.WHITE)
        self.screen.blit(resouces_box, (self.board_width+self.panel_border_width//2, self.board_height/5+self.panel_border_width//2))
        pygame.draw.line(self.screen, Colors.BLACK, (self.board_width,self.board_height/5+1.25*self.resource_size),
                          (self.board_width+self.panel_width, self.board_height/5+1.25*self.resource_size), 4)
        margin = self.panel_width / 6
        for i in range(len(DICE)):
            resource_image = pygame.image.load(r"catan_dice\assets\Resources\Resource" + str(i) + ".png")
            resource_image = pygame.transform.scale(resource_image, (self.resource_size, self.resource_size))
            col = i % len(DICE)
            x = col * (margin)
            self.screen.blit(resource_image, (self.board_width + x+self.panel_border_width, self.board_height/5+self.panel_border_width/2))

    def draw_dice_roll(self, resource_state):
        margin = self.panel_width / 6
        resource_display = pygame.Surface((self.panel_width-self.panel_border_width,(self.board_height/2.5-self.panel_border_width)-1.25*self.resource_size))
        resource_display.fill(Colors.YELLOW)
        for i, count in enumerate(resource_state):
            row = i // len(DICE)
            col = i % len(DICE)
            x = col * (margin) 
            y = row * (margin)
            resource_image = pygame.image.load(r"catan_dice\assets\Resources\Resource" + str(i) + ".png")
            resource_image = pygame.transform.scale(resource_image, (self.resource_size, self.resource_size))
            for _ in range(count):
                resource_display.blit(resource_image, (x, y))
                y +=margin  
        self.screen.blit(resource_display, (self.board_width+self.panel_border_width//2, self.board_height/5+self.panel_border_width//2+1.25*self.resource_size))

    def draw_buttons(self):
        self.control_buttons = [
            Button((self.board_width+self.panel_width/8, self.board_height/20, self.panel_width*0.75, self.board_height/10), self.screen, Colors.BLACK,
                    "ROLL DICE",
                    ActionType.ROLL),
            ]
        for button in self.control_buttons:
            button.draw()
        
    def draw_catan_game(self):
        self.draw_board()
        self.draw_panel()
        self.draw_resources()
        self.draw_buttons()

class Hexagon:
    def __init__(self, center, size):
        self.center = center
        self.size = size
        self.vertices = self.calculate_vertices()
        self.edges = self.calculate_edges()
        self.edge_midpoints = self.calculate_edge_midpoints()

    def calculate_vertices(self):
        vertices = []
        for i in range(6):
            angle = math.radians(60 * i)  # 60 degrees between each vertex
            x = self.center[0] + self.size * math.cos(angle)
            y = self.center[1] + self.size * math.sin(angle)
            vertices.append((x, y))
        return vertices

    def calculate_edges(self):
        edges = []
        for i in range(6):
            start_vertex = self.vertices[i]
            end_vertex = self.vertices[(i - 1) % 6]  # Wrap around to the first vertex
            edges.append((start_vertex, end_vertex))
        return edges
    
    def calculate_edge_midpoints(self):
        midpoints = []
        for edge in self.edges:
            x1, y1 = edge[0]
            x2, y2 = edge[1]
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            midpoints.append((mid_x, mid_y))
        return midpoints
    
    def calculate_center(self):
        x_sum = 0
        y_sum = 0

        for vertex in self.vertices:
            x, y = vertex
            x_sum += x
            y_sum += y

        center_x = x_sum / len(self.vertices)
        center_y = y_sum / len(self.vertices)

        return (center_x, center_y)
    
class Button:
    def __init__(self, rect, screen, color, label, action_type):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.label = label
        self.screen = screen
        self.button_font_size = 36
        self.action_type = action_type

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        font = pygame.font.Font(None, self.button_font_size)
        text_surface = font.render(self.label, True, Colors.WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return self.action_type

    
def initialise_structure_blocks_map():
    structure_blocks_map = {
        "RI": ROAD([0, 0, 0], "RI", [[], []]),
        "R0": ROAD([0, 1, 0], "R0", [["RI"], ["R1", "R2"]]),
        "R1": ROAD([0, 2, 0], "R1", [["R0"], ["C0"]]),
        "R2": ROAD([1, 0, 0], "R2", [["R0"], ["S1", "R3"]]),
        "R3": ROAD([1, 1, 0], "R3", [["R2"], ["R4", "R5"]]),
        "R4": ROAD([1, 2, 0], "R4", [["R3"], ["C1"]]),
        "R5": ROAD([2, 3, 0], "R5", [["R3"], ["S2", "R6"]]),
        "R6": ROAD([2, 2, 0], "R6", [["R5"], ["R7"]]),
        "R7": ROAD([2, 1, 0], "R7", [["R6"], ["S3", "R8", "R12"]]),
        "R8": ROAD([2, 0, 0], "R8", [["R7"], ["R9"]]),
        "R9": ROAD([3, 4, 0], "R9", [["R8"], ["S4", "R10"]]),
        "R10": ROAD([4, 3, 0], "R10", [["R9"], ["R11"]]),
        "R11": ROAD([4, 4, 0], "R11", [["R11"], ["S5"]]),
        "R12": ROAD([3, 2, 0], "R12", [["R7"], ["R13"]]),
        "R13": ROAD([3, 1, 0], "R13", [["R12"], ["C2", "R14"]]),
        "R14": ROAD([3, 0, 0], "R14", [["R13"], ["R15"]]),
        "R15": ROAD([4, 1, 0], "R15", [["R15"], ["C3"]]),

        "C0": CITY([0, 2, 1], 7, "C0", [["R1"], ["C1"]]),
        "C1": CITY([1, 2, 1], 12, "C1", [["C0", "R4"], ["C2"]]),
        "C2": CITY([3, 0, 1], 20, "C2", [["C1", "R13"], ["C3"]]),
        "C3": CITY([4, 0, 1], 30, "C3", [["C2", "R15"], []]),

        "S0": SETTLEMENT([0, 0, 1], 3, "S0", [["RI"], ["S1"]]),
        "S1": SETTLEMENT([1, 0, 1], 4, "S1", [["S0", "R2"], ["S2"]]),
        "S2": SETTLEMENT([2, 2, 1], 5, "S2", [["S1", "R5"], ["S3"]]),
        "S3": SETTLEMENT([2, 0, 1], 7, "S3", [["S2", "R7"], ["S4"]]),
        "S4": SETTLEMENT([4, 2, 1], 9, "S4", [["S3", "R9"], ["S5"]]),
        "S5": SETTLEMENT([4, 4, 1], 11, "S5", [["S4", "R11"], []]),

        "J0": JOKER([0, 0, 2], 1, ResourceType.ORE, "J0", [[], ["J1"]]),
        "J1": JOKER([1, 0, 2], 2, ResourceType.GRAIN, "J1", [["J0"], ["J2"]]),
        "J2": JOKER([2, 0, 2], 3, ResourceType.WOOL, "J2", [["J1"], ["J3"]]),
        "J3": JOKER([3, 0, 2], 4, ResourceType.TIMBER, "J3", [["J2"], ["J4"]]),
        "J4": JOKER([4, 0, 2], 5, ResourceType.BRICK, "J4", [["J3"], ["J5"]]),
        "J5": JOKER([5, 0, 2], 6, ResourceType.GOLD, "J5", [["J4"], []]),
    }
    return structure_blocks_map
