class CatanPlayer: # Equivalent to a gameState class 
    def __init__(self, catan_board):
        self.resource_state = [10,10,10,10,10,10]
        self.structures_built = {} # dictionary containing Round, With Structures built in that round
        self.victory_points_per_round = {} # dictionary containing Round, With points gained that round
        self.catan_board = catan_board
        self.current_round_number = 0
    
    def build_structure(self, structure):
        if (check_build_constraints(self.catan_board.structure_blocks_map, structure)):
            structure.build(self.resource_state)
            if self.current_round_number not in self.structures_built:
                self.structures_built[self.current_round_number] = []
            if (structure.is_built):
                self.structures_built[self.current_round_number].append(structure)

    def destory_structure(self, structure):
        if (structure in self.structures_built[self.current_round_number]):
            structure.destroy()
            for i in range(len(self.resource_state)):
                self.resource_state[i] += structure.resource_costs[i]
            self.structures_built[self.current_round_number].remove(structure)

    def roll_dice():
        pass

    def swap():
        pass

    def trade():
        pass

    def end_turn():
        pass


def check_build_constraints(structure_blocks_map, structure):
    for connection in structure.connections:
        if (structure_blocks_map[connection].is_built):
            return True
    return False

def check_destory_constraints(structure_blocks_map, structure):
    pass