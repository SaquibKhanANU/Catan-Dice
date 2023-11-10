class CatanPlayer:
    def __init__(self):
        self.resources = [0, 0, 0, 0, 0, 0]
        self.score = 0
        self.structures = []
    
    def increase_score(self, amount):
        self.score += amount

    def decrease_score(self, amount):
        self.pscore -= amount

    def decrease_resources(self, resource_costs):
        self.resources -= resource_costs
    
    def append_structure(self, structure):
        self.structures.append(structure)
    
    def remove_structure(self, structure):
        self.structures.remove(structure)