import pytest
from project.task4.game_rules import GameRules
from project.task4.balanced_bot import BalancedBot
from project.task4.aggressive_bot import AggressiveBot
from project.task4.cautious_bot import CautiousBot

class TestBotStrategies:
    """Bot strategy tests"""
    
    def test_cautious_bot_decisions(self, cautious_bot):
        """Testing cautious bot decisions"""
        assert cautious_bot.decide_continue(100, 4) == True
        
        assert cautious_bot.decide_continue(400, 4) == False
        
        assert cautious_bot.decide_continue(350, 3) == False
    
    def test_aggressive_bot_decisions(self, aggressive_bot):
        """Aggressive bot solution test"""
        assert aggressive_bot.decide_continue(800, 3) == True
        assert aggressive_bot.decide_continue(50, 6) == True
        
        assert aggressive_bot.decide_continue(100, 2) == False
    
    def test_balanced_bot_decisions(self, balanced_bot):
        """Balanced bot solution test"""
        assert balanced_bot.decide_continue(500, 4) == False
        
        assert balanced_bot.decide_continue(250, 2) == False
        
        assert balanced_bot.decide_continue(300, 4) == True
    
    def test_bot_combination_selection(self, sample_combinations):
        """Bot combination selection test"""
        cautious = CautiousBot()
        aggressive = AggressiveBot()
        balanced = BalancedBot()
        
        cautious_choice = cautious.select_combinations(sample_combinations)
        assert len(cautious_choice) <= 2
        
        aggressive_choice = aggressive.select_combinations(sample_combinations)
        assert len(aggressive_choice) == 4
        
        balanced_choice = balanced.select_combinations(sample_combinations)
        assert all(combo[1] >= 100 for combo in balanced_choice)
        assert len(balanced_choice) <= 3
    
    def test_bots_with_real_combinations(self):
        """Testing bots with real combinations from GameRules"""
        combinations = GameRules.get_combinations([1, 1, 1, 5, 2, 3])
        
        cautious = CautiousBot()
        aggressive = AggressiveBot()
        balanced = BalancedBot()
        
        cautious_choice = cautious.select_combinations(combinations)
        aggressive_choice = aggressive.select_combinations(combinations)
        balanced_choice = balanced.select_combinations(combinations)
        
        assert len(cautious_choice) > 0
        assert len(aggressive_choice) > 0
        assert len(balanced_choice) > 0
        
        assert len(cautious_choice) <= 2
        assert len(aggressive_choice) >= len(cautious_choice)
    
    def test_minimum_score_threshold(self):
        """Minimum threshold test of 300 points to stop"""
        bot = CautiousBot()
    
        assert bot.decide_continue(250, 3) == True
    
        assert bot.decide_continue(300, 3) == False

    def test_combination_conflicts(self):
        """Conflict combination selection test"""
        combinations = [
            ('3 1', 1000, [1, 1, 1]),
            ('1', 100, [1]),  
            ('5', 50, [5])
        ]
    
        bot = BalancedBot()
        selected = bot.select_combinations(combinations)
        assert len(selected) > 0
        assert all(combo[1] >= 100 for combo in selected)