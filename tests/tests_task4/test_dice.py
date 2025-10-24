import pytest

class TestDice:
    """Tests for the Dice class"""
    
    def test_dice_initialization(self, dice):
        """Dice initialization test"""
        assert dice.value == 1
        assert str(dice) == "1"
    
    def test_dice_roll_range(self, dice):
        """Range test when throwing"""
        for _ in range(100):
            value = dice.roll()
            assert 1 <= value <= 6
    
    def test_dice_state_change(self, dice):
        """Dice state change test"""
        initial_value = dice.value
        new_value = dice.roll()
        assert new_value != initial_value or new_value == initial_value == 1
    
    def test_dice_reset(self, dice):
        """Dice reset test"""
        dice.roll()
        dice.reset()
        assert dice.value == 1
    
    def test_multiple_dice_rolls_produce_variety(self, dice):
        """Test that multiple throws produce different values"""
        values = set()
        for _ in range(50):
            values.add(dice.roll())
        
        assert len(values) >= 2