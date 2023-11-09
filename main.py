import pygame
import math

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class HexagonLayout:
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

def main():
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Hexagon Layout")

    clock = pygame.time.Clock()

    hexagon_size = 100
    center_x = 400
    center_y = 300

    # Create multiple hexagons in a circle
    num_hexagons = 6
    hexagons = []
    for i in range(num_hexagons):
        angle = math.radians(240 + 60 * i)  # Counter-clockwise, starting from the top-left
        x = center_x + 1.80 * hexagon_size * math.sin(angle)
        y = center_y + 1.80 * hexagon_size * math.cos(angle)
        hexagons.append(HexagonLayout((x, y), hexagon_size))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)

        # Create a list to define the order of hexagons
        hexagon_order = [0, 1, 2, 3, 4, 5]

        for order_index in hexagon_order:
            hexagon = hexagons[order_index]
            vertices = hexagon.vertices
            for i in range(len(vertices)):
                start_point = vertices[i]
                end_point = vertices[(i + 1) % len(vertices)]
                pygame.draw.line(screen, WHITE, start_point, end_point, 2)

        edge_to_place = 0  # You can change this to place it on a different edge
        edge_midpoint = hexagons[0].edge_midpoints[edge_to_place]
        pygame.draw.circle(screen, RED, edge_midpoint, 10)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
