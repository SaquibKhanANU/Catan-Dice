from catan_dice.catan_structure import *
from catan_dice.catan_resource import *
import math

# Hexagonal Grid

NUM_HEXAGONS = 6
NUM_POINTS = 6 # number of vertciees and edges around a hexagon
POINT_TYPES = 3 # 1 = vertex, 0 = edge # 2 = center

BOARD_HEIGHT = 1000
BOARD_WIDTH = 1000

class CatanBoard:
    def __init__(self, structure_blocks_map):
        self.catanBoard = [[[None for _ in range(POINT_TYPES)] for _ in range(NUM_POINTS)] for _ in range(NUM_HEXAGONS)]
        self.structure_blocks_map = structure_blocks_map
        self.board_width = BOARD_WIDTH
        self.board_height = BOARD_HEIGHT
    
    def create_board(self, screen):
        screen.fill(Colors.OCEAN_BLUE)
        self.board_width = screen.get_width()
        self.board_height = screen.get_height()
        self.hexagon_size = min(self.board_height, self.board_width) // 6
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
            pygame.draw.polygon(screen, Colors.DARK_BROWN, vertices, 10)
            pygame.draw.polygon(screen, Colors.SANDY_BROWN, vertices)
            image = pygame.image.load(r"catan_dice\assets\HexagonTiles\Hex" + str(order_index) + ".png")
            x, y = hexagon.calculate_center()
            if (order_index == 5):
                scaled_image = pygame.transform.scale(image, (2.3*hexagon.size, 2.3*hexagon.size))
                screen.blit(scaled_image, (hexagon.center[0]-scaled_image.get_width()/2,hexagon.center[1]-scaled_image.get_height()/2))
            else:
                scaled_image = pygame.transform.scale(image, (2.8*hexagon.size, 2.8*hexagon.size))
                screen.blit(scaled_image, (hexagon.center[0]-scaled_image.get_width()/2,hexagon.center[1]-scaled_image.get_height()/2))

        for structure in self.structure_blocks_map.values():
            structure.screen = screen
            self.initialise_structure_at_coordinate(structure)
            structure.initialise_structure()
        
    def initialise_structure_at_coordinate(self, structure):
        coordinate = structure.coordinate
        hexagon, point, point_type = coordinate
        if (self.catanBoard[hexagon][point][point_type] != None):
            print("Structure already built")
        elif (hexagon < 0 or hexagon >= NUM_HEXAGONS):
            print("Hexagon out of bounds")
        elif (point < 0 or point >= NUM_POINTS):
            print("Point out of bounds")
        elif (point_type < 0 or point_type >= POINT_TYPES):
            print("Point type out of bounds")
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
    
@staticmethod
def initialise_structure_blocks_map():
    structure_blocks_map = {
        "RI": ROAD([0, 0, 0], "RI", [[], ["R0"]]),
        "R0": ROAD([0, 1, 0], "R0", [["RI"], ["R1", "R2"]]),
        "R1": ROAD([0, 2, 0], "R1", [["R0"], ["C0"]]),
        "R2": ROAD([1, 0, 0], "R2", [["R0"], [""]]),
        "R3": ROAD([1, 1, 0], "R3", [["R2"], []]),
        "R4": ROAD([1, 2, 0], "R4", [["R3"], []]),
        "R5": ROAD([2, 3, 0], "R5", [["R3"], []]),
        "R6": ROAD([2, 2, 0], "R6", [["R5"], []]),
        "R7": ROAD([2, 1, 0], "R7", [["R6"], []]),
        "R8": ROAD([2, 0, 0], "R8", [["R7"], []]),
        "R9": ROAD([3, 4, 0], "R9", [["R8"], []]),
        "R10": ROAD([4, 3, 0], "R10", [["R10"], []]),
        "R11": ROAD([4, 4, 0], "R11", [["R11"], []]),
        "R12": ROAD([3, 2, 0], "R12", [["R7"], []]),
        "R13": ROAD([3, 1, 0], "R13", [["R12"], []]),
        "R14": ROAD([3, 0, 0], "R14", [["R13"], []]),
        "R15": ROAD([4, 1, 0], "R15", [["R15"], []]),

        "C0": CITY([0, 2, 1], 7, "C0", ["R1"]),
        "C1": CITY([1, 2, 1], 12, "C1", ["R1"]),
        "C2": CITY([3, 0, 1], 20, "C2", ["R1"]),
        "C3": CITY([4, 0, 1], 30, "C3", ["R1"]),

        "S0": SETTLEMENT([0, 0, 1], 3, "S0", ["R1"]),
        "S1": SETTLEMENT([1, 0, 1], 4, "S1", ["R1"]),
        "S2": SETTLEMENT([2, 2, 1], 5, "S2", ["R1"]),
        "S3": SETTLEMENT([2, 0, 1], 7, "S3", ["R1"]),
        "S4": SETTLEMENT([4, 2, 1], 9, "S4", ["R1"]),
        "S5": SETTLEMENT([4, 4, 1], 11, "S5", ["R1"]),

        "J0": JOKER([0, 0, 2], 1, ResourceType.ORE, "J0", ["R1"]),
        "J1": JOKER([1, 0, 2], 2, ResourceType.GRAIN, "J1", ["R1"]),
        "J2": JOKER([2, 0, 2], 3, ResourceType.WOOL, "J2", ["R1"]),
        "J3": JOKER([3, 0, 2], 4, ResourceType.TIMBER, "J3", ["R1"]),
        "J4": JOKER([4, 0, 2], 5, ResourceType.BRICK, "J4", ["R1"]),
        "J5": JOKER([5, 0, 2], 6, ResourceType.GOLD, "J5", ["R1"]),
    }
    return structure_blocks_map
