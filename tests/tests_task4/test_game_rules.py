import pytest
from project.task4.game_rules import GameRules

class TestGameRules:
    """Tests for the GameRules class"""
    
    def test_has_scoring_combinations_positive(self):
        """Test for the presence of scoring combinations (positive case)"""
        assert GameRules.has_scoring_combinations([1, 1, 1, 2, 3, 4]) == True
        assert GameRules.has_scoring_combinations([1, 5, 2, 3, 4, 6]) == True
        assert GameRules.has_scoring_combinations([2, 2, 4, 4, 6, 6]) == True
    
    def test_has_scoring_combinations_negative(self):
        """Test for the presence of scoring combinations (negative case)"""
        assert GameRules.has_scoring_combinations([2, 3, 4, 6, 2, 3]) == False
    
    def test_three_ones_combination(self):
        """Three-unit combination test"""
        combinations = GameRules.get_combinations([1, 1, 1, 2, 3, 4])
        triple_ones = [c for c in combinations if '3 1' in c[0]]
        assert len(triple_ones) > 0
        assert triple_ones[0][1] == 1000
    
    def test_single_ones_and_fives(self):
        """Testing of individual units and groups of five"""
        combinations = GameRules.get_combinations([1, 5, 2, 3, 4, 4])
        ones = [c for c in combinations if '1' in c[0] and '3' not in c[0]]
        fives = [c for c in combinations if '5' in c[0] and '3' not in c[0]]
        assert len(ones) > 0
        assert len(fives) > 0
        assert ones[0][1] == 100
        assert fives[0][1] == 50
    
    def test_six_different_combination(self):
        """Test of six different combinations"""
        combinations = GameRules.get_combinations([1, 2, 3, 4, 5, 6])
        six_diff = [c for c in combinations if 'Six different' in c[0]]
        assert len(six_diff) > 0
        assert six_diff[0][1] == 1500
        assert six_diff[0][3] == True
    
    def test_three_pairs_combination(self):
        """Three pairs combination test"""
        combinations = GameRules.get_combinations([1, 1, 2, 2, 3, 3])
        three_pairs = [c for c in combinations if 'Three pairs' in c[0]]
        assert len(three_pairs) > 0
        assert three_pairs[0][1] == 750
        assert three_pairs[0][3] == True
    
    def test_bonus_throw_detection(self):
        """Bonus roll determination test"""
        assert GameRules.can_take_bonus_throw([1, 2, 3, 4, 5, 6]) == True
        assert GameRules.can_take_bonus_throw([1, 1, 2, 2, 3, 3]) == True
        assert GameRules.can_take_bonus_throw([1, 1, 1, 2, 3, 4]) == False
    
    def test_four_of_a_kind_points(self):
        """Test of points for four identical dice"""
        combinations = GameRules.get_combinations([2, 2, 2, 2, 3, 4])
        four_twos = [c for c in combinations if '4 2' in c[0]]
        assert len(four_twos) > 0
        assert four_twos[0][1] == 400 
    
    def test_calculate_possible_combinations(self):
        """Test of the calculate_possible_combinations method"""
        combinations = GameRules.calculate_possible_combinations([1, 1, 1, 2, 3, 4])
        assert len(combinations) > 0
        assert any('3 1' in c[0] for c in combinations)
    
    def test_all_combination_types(self):
        """Test all possible types of combinations"""
        test_cases = [
            ([1, 1, 1, 1, 1, 1], "6 единиц"),  
            ([2, 2, 2, 2, 2, 2], "6 двоек"),   
            ([1, 1, 1, 1, 2, 3], "4 единицы"), 
            ([1, 1, 1, 2, 2, 2], "две тройки"), 
        ]
    
        for dice_values, description in test_cases:
            combinations = GameRules.get_combinations(dice_values)
            assert len(combinations) > 0, f"No combinations for {description}"