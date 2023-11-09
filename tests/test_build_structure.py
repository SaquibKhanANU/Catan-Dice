import unittest
from catan_dice.catan_structure.structure import CatanStructure
from catan_dice.catan_structure.structure_type import StructureType, initialise_structure_resource

structure_types_to_test = [StructureType.CITY, StructureType.ROAD, StructureType.JOKER, StructureType.SETTLEMENT]
coordinate = (0, 0)

class TestBuildStructure(unittest.TestCase):
    def test_can_build_structure_exact_resources(self):
        # Test the can_build method for multiple structure types
        for structure_type in structure_types_to_test:
            structure = CatanStructure(structure_type, coordinate)
            player_resources = initialise_structure_resource(structure_type)
            can_build = structure.can_build(player_resources)
            self.assertTrue(can_build)

    def test_can_build_structure_sufficient_resources(self):
        # Test the can_build method for a structure that can be built
        for structure_type in structure_types_to_test:
            structure = CatanStructure(structure_type, coordinate)
            player_resources = [x + y for x, y in zip(initialise_structure_resource(structure_type), [1, 1, 1, 1, 1, 1])]
            can_build = structure.can_build(player_resources) 
            self.assertTrue(can_build)

    def test_structure_is_built(self):
        # Test the can_build method for multiple structure types
        for structure_type in structure_types_to_test:
            structure = CatanStructure(structure_type, coordinate)
            player_resources = initialise_structure_resource(structure_type)
            can_build = structure.build(player_resources)
            self.assertTrue(structure.is_built)

    def test_cannot_build_structure_insufficient_resources(self):
        # Test the can_build method for a structure that can be built
        for structure_type in structure_types_to_test:
            structure = CatanStructure(structure_type, coordinate)
            player_resources = [x - y for x, y in zip(initialise_structure_resource(structure_type), [1, 1, 1, 1, 1, 1])]
            can_build = structure.can_build(player_resources) 
            self.assertFalse(can_build)

    def test_structure_is_not_built(self):
        # Test the can_build method for multiple structure types
        for structure_type in structure_types_to_test:
            structure = CatanStructure(structure_type, coordinate)
            player_resources = [x - y for x, y in zip(initialise_structure_resource(structure_type), [1, 1, 1, 1, 1, 1])]
            can_build = structure.build(player_resources)
            self.assertFalse(structure.is_built)
    
    def test_multiple_structures_built(self):
        pass


unittest.main()