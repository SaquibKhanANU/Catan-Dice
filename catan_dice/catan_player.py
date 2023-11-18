import random
from catan_dice.catan_enum import DICE

class CatanPlayer: # Equivalent to a gameState class 
    def __init__(self, catan_board):
        self.resource_state = [0,0,0,0,0,0]
        self.structures_built = {} # dictionary containing Round, With Structures built in that round
        self.victory_points_per_round = {} # dictionary containing Round, With points gained that round
        self.catan_board = catan_board
        self.current_round_number = 0
        self.current_round_victory_points = 0

        self.num_dice_rolled = 0
        self.resources_to_roll = [None, None, None, None, None, None]
        self.structures_built[self.current_round_number] = []
        self.victory_points_per_round[self.current_round_number] = []
        
    def build_structure(self, structure):
        if (structure.check_build_constraints(self.catan_board.structure_blocks_map)):
            if (structure.can_build(self.resource_state)):
                for i in range(len(self.resource_state)):
                    self.resource_state[i] -= structure.resource_costs[i]
                self.structures_built[self.current_round_number].append(structure)
                self.current_round_victory_points += structure.victory_points

    def destory_structure(self, structure):
        if (structure.check_destory_constraints(self.catan_board.structure_blocks_map)):
            if (structure in self.structures_built[self.current_round_number]):
                structure.destroy()
                for i in range(len(self.resource_state)):
                    self.resource_state[i] += structure.resource_costs[i]
                self.structures_built[self.current_round_number].remove(structure)
                self.current_round_victory_points -= structure.victory_points

    def roll_dice(self, n_dice):
        if (self.num_dice_rolled <= 2 and n_dice > 0):
            for _ in range(n_dice):
                roll_value = random.choice(DICE)
                resource_count = self.resource_state[roll_value]
                resource_count += 1  
                self.resource_state[roll_value] = resource_count
            self.num_dice_rolled += 1
            self.resources_to_roll = []

    def remove_resource(self, resource):
        if (self.num_dice_rolled <= 2 and resource.rolled == False):
            resource.rolled = True
            self.resources_to_roll.append(resource)
            self.resource_state[resource.resource_type] -= 1

    def add_resource(self, resource):
        if (self.num_dice_rolled <= 2 and resource.rolled == True):
            resource.rolled = False
            self.resources_to_roll.remove(resource)
            self.resource_state[resource.resource_type] += 1

    def end_turn(self):
        self.victory_points_per_round[self.current_round_number].append(self.current_round_victory_points)
        self.current_round_number += 1
        self.current_round_victory_points = 0
        self.num_dice_rolled = 0
        self.resource_state = [0,0,0,0,0,0]
        self.resources_to_roll = [None, None, None, None, None, None]
        if self.current_round_number not in self.structures_built:
                self.structures_built[self.current_round_number] = []
                self.victory_points_per_round[self.current_round_number] = []

    def draw_player_action(self):
        self.catan_board.draw_catan_game()
        self.catan_board.draw_dice_roll(self.resource_state)
        self.catan_board.draw_saved_dice(self.resources_to_roll)

class CatanAI(CatanPlayer):
    def __init__(self, catan_board) -> None:
        super().__init__(catan_board)
        pass

    def get_legal_actions(self):
        pass

    def take_action(self):
        pass

    def simulate(self):
        pass

