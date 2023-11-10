from catan_dice.catan_game import roll_dice, DICE
import unittest
from scipy.stats import chisquare

class TestRollDice(unittest.TestCase):
    def test_sum_of_resource_counts(self):
        resource_state = [0, 0, 0, 0, 0, 0]
        n_dice = len(DICE)
        roll_dice(n_dice, resource_state)
        self.assertEqual(sum(resource_state), 6, "The sum of resource counts should be 6.")

class TestDiceRandomness(unittest.TestCase):
    def test_dice_randomness(self):
        n_simulations = 10000
        n_dice = len(DICE)
        observed_frequency = [0] * len(DICE)

        for _ in range(n_simulations):
            resource_state = [0, 0, 0, 0, 0, 0]
            roll_dice(n_dice, resource_state)
            for i in range(len(DICE)):
                observed_frequency[i] += resource_state[i]

        _, p_value = chisquare(observed_frequency)

        # (0.05) to determine if the distribution is significantly different from uniform.
        significance_level = 0.05
        self.assertGreater(p_value, significance_level)

if __name__ == '__main__':
    unittest.main()