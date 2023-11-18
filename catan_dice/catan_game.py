
import os
import sys
yourpath = os.path.dirname(os.path.abspath(__file__))
parentpath = os.path.abspath(os.path.join(yourpath, os.pardir))
sys.path.append(parentpath)

import pygame
import random
from catan_dice.catan_board import *
from catan_dice.catan_player import *

def main():
    pygame.init()

    screen = pygame.display.set_mode((BOARD_WIDTH + PANEL_WIDTH, BOARD_HEIGHT), pygame.RESIZABLE, pygame.SRCALPHA)
    pygame.display.set_caption("Catan Dice")
    clock = pygame.time.Clock()

    catan_board = CatanBoard(initialise_structure_blocks_map(), screen)
    catan_player = CatanPlayer(catan_board)
    catan_board.draw_catan_game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                for structure in catan_board.structure_blocks_map.values():
                    if structure.collision_box.collidepoint(mouse_pos):
                        if (event.button == 1):
                            catan_player.build_structure(structure)
                            catan_player.draw_player_action()
                            break
                        elif (event.button == 3):
                            catan_player.destory_structure(structure)
                            catan_player.draw_player_action()
                            break

                for resource in catan_board.resources:
                    if resource.collision_box.collidepoint(mouse_pos):
                        if (event.button == 1):
                            catan_player.remove_resource(resource)
                            catan_player.draw_player_action()
                            break
                        elif (event.button == 3):
                            catan_player.add_resource(resource)
                            catan_player.draw_player_action()
                            break

                for button in catan_board.control_buttons:
                    if button.handle_event(event) == ActionType.ROLL:
                        catan_player.roll_dice(len(catan_player.resources_to_roll))
                        catan_player.draw_player_action()
                        break
                    elif button.handle_event(event) == ActionType.END_TURN:
                        catan_player.end_turn()
                        catan_player.draw_player_action()
                        break
                    

            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                catan_board.panel_width = min(event.w/3, PANEL_WIDTH)
                catan_player.draw_player_action()

        # Rest of your game loop
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()

