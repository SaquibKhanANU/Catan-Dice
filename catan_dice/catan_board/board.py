from catan_dice.catan_structure.structure import CatanStructure
from catan_dice.catan_structure.structure_type import StructureType
import math

# Hexagonal Grid
NUM_HEXAGONS = 6
NUM_POINTS = 6
POINT_TYPES = 3 # 1 = vertex, 0 = edge # 2 = center
SIZE_SCALING = 5.6
class CatanBoard:
    def __init__(self):
        hexagon_size = 160
        self.BOARD_HEIGHT = hexagon_size * SIZE_SCALING
        self.BOARD_WIDTH = hexagon_size * SIZE_SCALING
        self.catanBoard = [[[None for _ in range(POINT_TYPES)] for _ in range(NUM_POINTS)] for _ in range(NUM_HEXAGONS)]
        self.structure_blocks_map = {}

        center_x = self.BOARD_WIDTH/2
        center_y = self.BOARD_HEIGHT/2
        # Create multiple hexagons in a circle
        num_hexagons = 6
        self.hexagons = []
        for i in range(num_hexagons):
            angle = math.radians(240 + 60 * i)  # Counter-clockwise, starting from the top-left
            x = center_x + 1.80 * hexagon_size * math.sin(angle)
            y = center_y + 1.80 * hexagon_size * math.cos(angle)
            self.hexagons.append(Hexagon((x, y), hexagon_size))

    def initialise_structure_at_coordinate(self, structure_type, coordinate):
        hexagon, point, point_type = coordinate
        if (self.catanBoard[hexagon][point][point_type] != None):
            raise Exception("Structure already built")
        elif (hexagon < 0 or hexagon >= NUM_HEXAGONS):
            raise Exception("Hexagon out of bounds")
        elif (point < 0 or point >= NUM_POINTS):
            raise Exception("Point out of bounds")
        elif (point_type < 0 or point_type >= POINT_TYPES):
            raise Exception("Point type out of bounds")
        self.catanBoard[hexagon][point][point_type] = CatanStructure(structure_type, coordinate)
        if (point_type == 0):
            return self.hexagons[hexagon].edge_midpoints[point]
        elif(point_type == 1):
            return self.hexagons[hexagon].vertices[point]
        elif(point_type == 2):
            return self.hexagons[hexagon].calculate_center()

    def get_structure_at_coordinate(self, coordinate):
        hexagon, point, point_type = coordinate
        return self.catanBoard[hexagon][point][point_type]
    
    @staticmethod
    def initialise_basic_board(self):
        self.structure_blocks_map["RI"] = CatanStructure(StructureType.ROAD, [0,0,0])
        self.structure_blocks_map["R0"] = CatanStructure(StructureType.ROAD, [0,1,0])
        self.structure_blocks_map["R1"] = CatanStructure(StructureType.ROAD, [0,2,0])
        self.structure_blocks_map["R2"] = CatanStructure(StructureType.ROAD, [1,0,0])
        self.structure_blocks_map["R3"] = CatanStructure(StructureType.ROAD, [1,1,0])
        self.structure_blocks_map["R4"] = CatanStructure(StructureType.ROAD, [1,2,0])
        self.structure_blocks_map["R5"] = CatanStructure(StructureType.ROAD, [2,3,0])
        self.structure_blocks_map["R6"] = CatanStructure(StructureType.ROAD, [2,2,0])
        self.structure_blocks_map["R7"] = CatanStructure(StructureType.ROAD, [2,1,0])
        self.structure_blocks_map["R8"] = CatanStructure(StructureType.ROAD, [2,0,0])
        self.structure_blocks_map["R9"] = CatanStructure(StructureType.ROAD, [3,4,0])
        self.structure_blocks_map["R10"] = CatanStructure(StructureType.ROAD, [4,3,0])
        self.structure_blocks_map["R11"] = CatanStructure(StructureType.ROAD, [4,4,0])
        self.structure_blocks_map["R12"] = CatanStructure(StructureType.ROAD, [3,2,0])
        self.structure_blocks_map["R13"] = CatanStructure(StructureType.ROAD, [3,1,0])
        self.structure_blocks_map["R14"] = CatanStructure(StructureType.ROAD, [3,0,0])
        self.structure_blocks_map["R15"] = CatanStructure(StructureType.ROAD, [4,1,0])

        self.structure_blocks_map["C7"] = CatanStructure(StructureType.CITY, [0,2,1])
        self.structure_blocks_map["C12"] = CatanStructure(StructureType.CITY, [1,2,1])
        self.structure_blocks_map["C20"] = CatanStructure(StructureType.CITY, [3,0,1])
        self.structure_blocks_map["C30"] = CatanStructure(StructureType.CITY, [4,0,1])

        self.structure_blocks_map["S3"] = CatanStructure(StructureType.SETTLEMENT, [0,0,1])
        self.structure_blocks_map["S4"] = CatanStructure(StructureType.SETTLEMENT, [1,0,1])
        self.structure_blocks_map["S5"] = CatanStructure(StructureType.SETTLEMENT, [2,2,1])
        self.structure_blocks_map["S7"] = CatanStructure(StructureType.SETTLEMENT, [2,0,1])
        self.structure_blocks_map["S9"] = CatanStructure(StructureType.SETTLEMENT, [4,2,1])
        self.structure_blocks_map["S11"] = CatanStructure(StructureType.SETTLEMENT, [4,4,1])


        self.structure_blocks_map["J1"] = CatanStructure(StructureType.JOKER, [0,0,2])
        self.structure_blocks_map["J2"] = CatanStructure(StructureType.JOKER, [1,0,2])
        self.structure_blocks_map["J3"] = CatanStructure(StructureType.JOKER, [2,0,2])
        self.structure_blocks_map["J4"] = CatanStructure(StructureType.JOKER, [3,0,2])
        self.structure_blocks_map["J5"] = CatanStructure(StructureType.JOKER, [4,0,2])
        self.structure_blocks_map["J6"] = CatanStructure(StructureType.JOKER, [5,0,2])


    
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
    
