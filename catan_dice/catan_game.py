import pygame
import random
from catan_dice.catan_gui import *


def main():
    catan_board = CatanBoard()
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((catan_board.BOARD_WIDTH + SIDE_PANEL_WIDTH, catan_board.BOARD_HEIGHT))
    pygame.display.set_caption("Catan Dice")
    clock = pygame.time.Clock()

    screen.fill(Colors.OCEAN_BLUE)
    create_board(catan_board, screen)
    draw_side_panel(screen)
    control_buttons = draw_control_buttons(screen)

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
                        print(structure.resource_costs)

            for button in control_buttons:
                button.handle_event(event)

        # Rest of your game loop
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()

