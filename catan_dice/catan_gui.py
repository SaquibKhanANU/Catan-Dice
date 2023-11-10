import pygame
from catan_dice.catan_game_logic import *
import catan_dice.assets.colors as Colors

SIDE_PANEL_WIDTH = BOARD_WIDTH // 2.5
SIDE_PANEL_HEIGHT = BOARD_HEIGHT
SIDE_PANEL_SHIFT = 40

BUTTON_FONT_SIZE = 36
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 40
BUTTON_COLOR = Colors.WHITE

class Button:
    def __init__(self, rect, screen, color, label, callback):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.label = label
        self.callback = callback
        self.screen = screen

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        font = pygame.font.Font(None, BUTTON_FONT_SIZE)
        text_surface = font.render(self.label, True, Colors.WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()


def create_board(catan_board, screen):
    hexagons = catan_board.hexagons
    for order_index in range(6):
        hexagon = hexagons[order_index]
        vertices = hexagon.vertices
        pygame.draw.polygon(screen, Colors.DARK_BROWN, vertices, 10)
        pygame.draw.polygon(screen, Colors.SANDY_BROWN, vertices)
        image = pygame.image.load(r"catan_dice\assets\HexagonTiles\Hex" + str(order_index) + ".png")
        x, y = hexagon.calculate_center()
        if (order_index == 5):
            size = 218
            scaled_image = pygame.transform.scale(image, (hexagon.size + size, hexagon.size + size))
            screen.blit(scaled_image, (x-hexagon.size//2-size//2 +3, y-hexagon.size//2-size//2 + 2 ))
        else:
            size = 305
            scaled_image = pygame.transform.scale(image, (hexagon.size + size, hexagon.size + size))
            screen.blit(scaled_image, (x-hexagon.size//2-size//2 , y-hexagon.size//2 - size//2 ))

    initialise_basic_board(catan_board.structure_blocks_map)
    structure_hit_box = 70
    shift_hit_box = structure_hit_box // 2
    for id, structure in catan_board.structure_blocks_map.items():
        point = catan_board.initialise_structure_at_coordinate(structure)
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
        text = font.render(id, True, Colors.WHITE)
        text_rect = text.get_rect()
        text_rect.center = point if structure.structure_type != StructureType.JOKER else (point[0], point[1] - 40)
        screen.blit(text, text_rect)

def draw_side_panel(screen):
    shift_panel = SIDE_PANEL_SHIFT
    shift_border = shift_panel - 10
    side_panel_border = pygame.Surface((SIDE_PANEL_WIDTH-shift_border, SIDE_PANEL_HEIGHT))
    side_panel_border.fill(Colors.BLACK)
    screen.blit(side_panel_border, (BOARD_WIDTH+shift_border, 0))
    side_panel = pygame.Surface((SIDE_PANEL_WIDTH-shift_panel, SIDE_PANEL_HEIGHT-10))
    side_panel.fill(Colors.CATAN_GREEN)
    screen.blit(side_panel, (BOARD_WIDTH+shift_panel-5, 5))

def draw_control_buttons(screen):
    control_button_x = BOARD_WIDTH+BUTTON_WIDTH-SIDE_PANEL_SHIFT+5
    control_buttons = [
        Button((control_button_x, SIDE_PANEL_SHIFT, BUTTON_WIDTH, BUTTON_HEIGHT), screen, Colors.BLACK,
                "ROLL DICE",
                  lambda: roll_dice(6, [0,0,0,0,0,0])),
        Button((control_button_x, SIDE_PANEL_SHIFT+BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT), screen, Colors.BLACK,
                "Button 2",
                  lambda: print("Button 2 clicked")),
    ]
    for button in control_buttons:
        button.draw()
    return control_buttons

def draw_road(structure, point, screen, id):
    surface = pygame.Surface((20 , 70), pygame.SRCALPHA)
    surface.fill(Colors.WHITE)
    if (id == "RI"):
        surface.fill(Colors.PURPLE)
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
    border_size = (rotated_surface.get_width() + 6, rotated_surface.get_height() + 6)
    rect_border= pygame.transform.scale(rotated_surface, border_size)
    rect_border.fill(Colors.BLACK, special_flags=pygame.BLEND_RGBA_MULT)
    screen.blit(rect_border, (rect.x-3, rect.y-3))
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
    pygame.draw.polygon(screen, Colors.WHITE, vertices)
    pygame.draw.polygon(screen, Colors.BLACK, vertices, 3)


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
    pygame.draw.polygon(screen, Colors.WHITE, vertices)
    pygame.draw.polygon(screen, Colors.BLACK, vertices, 3)

def draw_joker(point, screen, id):
    x, y = point
    y -= 30
    pygame.draw.circle(screen, Colors.BLACK, (x,y), 23)
    pygame.draw.circle(screen, Colors.BLACK, point, 33)
    pygame.draw.circle(screen, Colors.WHITE, point, 30)
    image = pygame.image.load(r"catan_dice\assets\Resources\Resource" + str(id[1]) + ".png")
    size = 40
    scaled_image = pygame.transform.scale(image, (size, size))
    screen.blit(scaled_image, (x-size//2, y+30-size//2))