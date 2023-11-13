import pygame
import random
from catan_dice.catan_board import *

BOARD_HEIGHT = 1000
BOARD_WIDTH = 1000

def main():
    catan_board = CatanBoard(initialise_structure_blocks_map())
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Catan Dice")
    clock = pygame.time.Clock()

    screen.fill(Colors.OCEAN_BLUE)
    catan_board.create_board(screen)

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
                        if (event.button == 1):
                        # The click was within this structure's bounds
                        # You can now access the structure's properties
                            structure.build([10, 10, 10, 10, 10, 10])
                            print(structure.resource_costs)
                        elif (event.button == 3):
                            structure.destroy()
                        catan_board.create_board(screen)

            elif event.type == pygame.VIDEORESIZE:
                # Handle window resize event
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                catan_board.create_board(screen)

        # Rest of your game loop
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()

