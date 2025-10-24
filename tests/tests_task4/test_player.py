import pytest
from project.task4.cautious_bot import CautiousBot

class TestPlayer:
    """Basic Player Class Tests"""
    
    def test_player_initialization(self, cautious_bot):
        """Player initialization test"""
        assert cautious_bot.name == "TestCautious"
        assert cautious_bot.total_score == 0
        assert cautious_bot.round_score == 0
        assert cautious_bot.consecutive_zonks == 0
        assert cautious_bot.is_active == True
    
    def test_score_management(self, aggressive_bot):
        """Points  control test"""
        aggressive_bot.add_score(100)
        aggressive_bot.add_score(50)
        assert aggressive_bot.round_score == 150
        assert aggressive_bot.total_score == 0
        
        aggressive_bot.finalize_round()
        assert aggressive_bot.round_score == 0
        assert aggressive_bot.total_score == 150
    
    def test_zonk_handling(self, balanced_bot):
        """Zone processing test"""
        balanced_bot.total_score = 1000
        
        balanced_bot.handle_zonk()
        assert balanced_bot.consecutive_zonks == 1
        assert balanced_bot.round_score == 0
        assert balanced_bot.total_score == 1000
        
        balanced_bot.handle_zonk()
        assert balanced_bot.consecutive_zonks == 2
        
        balanced_bot.handle_zonk()
        assert balanced_bot.consecutive_zonks == 3
        assert balanced_bot.total_score == 500
    
    def test_reset_round(self, cautious_bot):
        """Round reset test"""
        cautious_bot.round_score = 300
        cautious_bot.consecutive_zonks = 2
        
        cautious_bot.reset_round()
        assert cautious_bot.round_score == 0
        assert cautious_bot.consecutive_zonks == 0
    
    def test_player_string_representation(self, aggressive_bot):
        """Player string representation test"""
        aggressive_bot.total_score = 500
        expected_str = "TestAggressive (Points: 500)"
        assert str(aggressive_bot) == expected_str
    
    def test_consecutive_zonk_penalty(self):
        """Penalty test for three consecutive zones"""
        bot = CautiousBot()
        bot.total_score = 1000
    
        bot.handle_zonk()  
        bot.handle_zonk()  
        bot.handle_zonk()  
    
        assert bot.total_score == 500 