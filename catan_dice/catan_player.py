import random
from catan_dice.catan_enum import DICE

class CatanPlayer: # Equivalent to a gameState class 
    def __init__(self, catan_board):
        self.resource_state = [0,0,0,0,0,0]
        self.structures_built = {} # dictionary containing Round, With Structures built in that round
        self.victory_points_per_round = {} # dictionary containing Round, With points gained that round
        self.catan_board = catan_board
        self.current_round_number = 0

        if self.current_round_number not in self.structures_built:
                self.structures_built[self.current_round_number] = []
    
    def build_structure(self, structure):
        if (check_build_constraints(self.catan_board.structure_blocks_map, structure)):
            structure.build(self.resource_state)
            if (structure.is_built):
                for i in range(len(self.resource_state)):
                    self.resource_state[i] -= structure.resource_costs[i]
                self.structures_built[self.current_round_number].append(structure)
            self.catan_board.draw_catan_game()
            self.catan_board.draw_dice_roll(self.resource_state)

    def destory_structure(self, structure):
        if (check_destory_constraints(self.catan_board.structure_blocks_map, structure)):
            if (structure in self.structures_built[self.current_round_number]):
                structure.destroy()
                for i in range(len(self.resource_state)):
                    self.resource_state[i] += structure.resource_costs[i]
                self.structures_built[self.current_round_number].remove(structure)
            self.catan_board.draw_catan_game()
            self.catan_board.draw_dice_roll(self.resource_state)

    def roll_dice(self):
        self.resource_state = [0,0,0,0,0,0]
        for _ in range(len(DICE)):
            roll_value = random.choice(DICE)
            resource_count = self.resource_state[roll_value]
            resource_count += 1  
            self.resource_state[roll_value] = resource_count
        self.catan_board.draw_dice_roll(self.resource_state)
        

    def swap():
        pass

    def trade():
        pass

    def end_turn():
        pass


def check_build_constraints(structure_blocks_map, structure):
    check = True
    for connection in structure.connections[0]:
        if (not structure_blocks_map[connection].is_built):
            check = False
    return check

def check_destory_constraints(structure_blocks_map, structure):
    check = True
    for connection in structure.connections[1]:
        if (structure_blocks_map[connection].is_built):
            check = False
    return check