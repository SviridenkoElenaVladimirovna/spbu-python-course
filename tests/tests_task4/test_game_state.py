import pytest

class TestGameStateProgression:
    """Game state progression tests"""
    
    def test_score_progression(self, balanced_bot):
        """Test of point progression during the game"""
        initial_score = balanced_bot.total_score
        balanced_bot.add_score(200)
        balanced_bot.finalize_round()
        
        mid_score = balanced_bot.total_score
        balanced_bot.add_score(300)
        balanced_bot.finalize_round()
        
        final_score = balanced_bot.total_score
        
        assert initial_score == 0
        assert mid_score == 200
        assert final_score == 500
        assert final_score > initial_score
    
    def test_round_progression(self, game_with_bots):
        """Round progression test"""
        game = game_with_bots
        
        game.current_round = 1
        assert game.current_round == 1
        
        game.current_round = 2
        assert game.current_round == 2
        
        game.current_round = 3
        assert game.current_round == 3
    
    def test_zonk_counter_progression(self, cautious_bot):
        """Zone counter progression test"""
        assert cautious_bot.consecutive_zonks == 0
        cautious_bot.handle_zonk()
        assert cautious_bot.consecutive_zonks == 1
        cautious_bot.handle_zonk()
        assert cautious_bot.consecutive_zonks == 2
        cautious_bot.handle_zonk()
        assert cautious_bot.consecutive_zonks == 3
        
        cautious_bot.finalize_round()
        assert cautious_bot.consecutive_zonks == 0
    
    def test_player_state_persistence(self, aggressive_bot):
        """Testing player state preservation between rounds"""
        aggressive_bot.add_score(250)
        aggressive_bot.finalize_round()
        assert aggressive_bot.total_score == 250
        assert aggressive_bot.round_score == 0
        
        aggressive_bot.add_score(350)
        aggressive_bot.finalize_round()
        assert aggressive_bot.total_score == 600
        assert aggressive_bot.round_score == 0