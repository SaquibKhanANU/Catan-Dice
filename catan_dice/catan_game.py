
import os
import sys

yourpath = os.path.dirname(os.path.abspath(__file__)) #current filepath

parentpath = os.path.abspath(os.path.join(yourpath, os.pardir))
sys.path.append(parentpath)

import pygame
import random
from catan_dice.catan_board import *
from catan_dice.catan_player import *


def main():
    catan_board = CatanBoard(initialise_structure_blocks_map())
    catan_player = CatanPlayer(catan_board)
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((catan_board.board_width, catan_board.board_height), pygame.RESIZABLE, pygame.SRCALPHA)
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
                            catan_player.build_structure(structure)
                            print(catan_player.resource_state)
                        elif (event.button == 3):
                            catan_player.destory_structure(structure)
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

