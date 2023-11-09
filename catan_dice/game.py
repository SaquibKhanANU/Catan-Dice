import pygame
from catan_dice.catan_board.board import CatanBoard
from catan_dice.catan_structure.structure_type import StructureType

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE =  (128, 0, 128)
YELLOW = (255, 255, 0)
BROWN = (165, 42, 42)
OCEAN_BLUE =  (51, 153, 255)
SANDY_BROWN = (244, 164, 96)
DARK_BROWN = (101, 67, 33)

def main():
    catan_board = CatanBoard()
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((catan_board.BOARD_WIDTH, catan_board.BOARD_HEIGHT))
    pygame.display.set_caption("Hexagon Layout")
    clock = pygame.time.Clock()

    screen.fill(OCEAN_BLUE)

    hexagons = catan_board.hexagons
    for order_index in range(6):
        hexagon = hexagons[order_index]
        vertices = hexagon.vertices
        pygame.draw.polygon(screen, DARK_BROWN, vertices, 10)
        pygame.draw.polygon(screen, SANDY_BROWN, vertices)
        image = pygame.image.load("catan_dice\\assets\HexagonTiles\Hex" + str(order_index) + ".png")
        x, y = hexagon.calculate_center()
        if (order_index == 5):
            size = 218
            scaled_image = pygame.transform.scale(image, (hexagon.size + size, hexagon.size + size))
            screen.blit(scaled_image, (x-hexagon.size//2-size//2 +3, y-hexagon.size//2-size//2 + 2 ))
        else:
            size = 305
            scaled_image = pygame.transform.scale(image, (hexagon.size + size, hexagon.size + size))
            screen.blit(scaled_image, (x-hexagon.size//2-size//2 , y-hexagon.size//2 - size//2 ))

        
    catan_board.initialise_basic_board(catan_board)
    structure_hit_box = 70
    shift_hit_box = structure_hit_box // 2
    for id, structure in catan_board.structure_blocks_map.items():
        point = catan_board.initialise_structure_at_coordinate(structure.structure_type, structure.coordinate)
        structure.collision_box = pygame.Rect(point[0]-shift_hit_box, point[1]-shift_hit_box, structure_hit_box, structure_hit_box)
        if (structure.structure_type == StructureType.ROAD):
            draw_road(structure, point, screen, id)
        elif(structure.structure_type == StructureType.CITY):
            draw_city(point, screen)
        elif(structure.structure_type == StructureType.SETTLEMENT):
            draw_settlement(point, screen)
        elif(structure.structure_type == StructureType.JOKER):
            draw_joker(point, screen, id)
        font = pygame.font.Font(None, 20)
        text = font.render(id, True, WHITE)
        text_rect = text.get_rect()
        text_rect.center = point if structure.structure_type != StructureType.JOKER else (point[0], point[1] - 40)
        screen.blit(text, text_rect)
            
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                # Check each structure to see if the click was within its bounds
                for structure in catan_board.structure_blocks_map.values():
                    if structure.collision_box.collidepoint(mouse_pos):
                        # The click was within this structure's bounds
                        # You can now access the structure's properties
                        print(structure.structure_type)


        # Rest of your game loop
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def draw_road(structure, point, screen, id):
    surface = pygame.Surface((26 , 76), pygame.SRCALPHA)
    surface.fill(BLACK)
    rotated_surface = surface
    rect = surface.get_rect()
    if (structure.coordinate[1] == 0 or structure.coordinate[1] == 3):
        rotated_surface = pygame.transform.rotate(surface, 30)
    elif (structure.coordinate[1] == 1 or structure.coordinate[1] == 4):
        rotated_surface = pygame.transform.rotate(surface, -30)
    elif (structure.coordinate[1] == 2 or structure.coordinate[1] == 5):
        rotated_surface = pygame.transform.rotate(surface, 90)
    rect = rotated_surface.get_rect(center = (100, 100))
    rect.center = point
    screen.blit(rotated_surface, (rect.x, rect.y))

    surface = pygame.Surface((20 , 70), pygame.SRCALPHA)
    surface.fill(WHITE)
    if (id == "RI"):
        surface.fill(PURPLE)
    rotated_surface = surface
    rect = surface.get_rect()
    if (structure.coordinate[1] == 0 or structure.coordinate[1] == 3):
        rotated_surface = pygame.transform.rotate(surface, 30)
    elif (structure.coordinate[1] == 1 or structure.coordinate[1] == 4):
        rotated_surface = pygame.transform.rotate(surface, -30)
    elif (structure.coordinate[1] == 2 or structure.coordinate[1] == 5):
        rotated_surface = pygame.transform.rotate(surface, 90)
    rect = rotated_surface.get_rect(center = (100, 100))
    rect.center = point
    screen.blit(rotated_surface, (rect.x, rect.y))


def draw_city(point, screen):
    x, y = point
    y -= 10
    house_width = 55
    house_height = 20

    # Define the vertices of the house with a roof
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
        (x + house_width // 2, y-5),
        #shift roof outwards right side
        ((x + house_width // 2)+4, y-5),
        # roof peak
        ((x + house_width // 4)+2, y-30),
        # extend top left roof corner
        (x, y-5),
        # shift roof inwards left side
        (x+4, y-5),
        # bring back roof back to center
        (x+4, y),
    ]

    # Draw the house with a roof
    pygame.draw.polygon(screen, WHITE, vertices)
    pygame.draw.polygon(screen, BLACK, vertices, 3)


def draw_settlement(point, screen):
    x, y = point
    y -= 10
    house_width = 35
    house_height = 25

    # Define the vertices of the house with a roof
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
        ((x + house_width // 2)+2, y),
        # Roof peak (top center)
        (x, y - house_height),
        ((x - house_width // 2) - 2, y),
    ]

    # Draw the house with a roof
    pygame.draw.polygon(screen, WHITE, vertices)
    pygame.draw.polygon(screen, BLACK, vertices, 3)

def draw_joker(point, screen, id):
    x, y = point
    y -= 30
    pygame.draw.circle(screen, BLACK, (x,y), 23)
    pygame.draw.circle(screen, BLACK, point, 33)
    pygame.draw.circle(screen, WHITE, point, 30)
    image = pygame.image.load("catan_dice\\assets\Resources\Resource" + str(id[1]) + ".png")
    size = 40
    scaled_image = pygame.transform.scale(image, (size, size))
    screen.blit(scaled_image, (x-size//2, y+30-size//2))
    
if __name__ == "__main__":
    main()
    