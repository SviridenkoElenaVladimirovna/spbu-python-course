import pytest
from project.task4.game_rules import GameRules
from project.task4.balanced_bot import BalancedBot
from project.task4.aggressive_bot import AggressiveBot
from project.task4.cautious_bot import CautiousBot
from project.task4.game_engine import GameEngine


class TestIntegration:
    """Integration tests"""

    def test_full_game_flow(self, game_with_bots):
        """Full game flow test"""
        game = game_with_bots
        bots = game.players

        assert all(bot.total_score == 0 for bot in bots)
        assert game.current_round == 0

        game.current_round = 1
        bots[0].add_score(100)
        bots[0].finalize_round()

        game.current_round = 2
        bots[1].add_score(400)
        bots[1].finalize_round()

        assert bots[0].total_score == 100
        assert bots[1].total_score == 400
        assert game.current_round == 2

    def test_bot_strategy_integration(self):
        """Testing the integration of bot strategies with the game"""
        cautious = CautiousBot()
        aggressive = AggressiveBot()

        test_combos = GameRules.get_combinations([1, 1, 1, 5, 2, 3])

        cautious_choice = cautious.select_combinations(test_combos)
        aggressive_choice = aggressive.select_combinations(test_combos)

        assert len(cautious_choice) > 0
        assert len(aggressive_choice) > 0

        assert len(cautious_choice) <= 2
        assert len(aggressive_choice) >= len(cautious_choice)

    def test_game_rules_with_bot_decisions(self):
        """Testing the interaction between game rules and bot decisions"""
        dice_values = [1, 2, 3, 4, 5, 6]
        combinations = GameRules.get_combinations(dice_values)

        cautious = CautiousBot()
        aggressive = AggressiveBot()
        balanced = BalancedBot()

        cautious_decision = cautious.decide_continue(1500, 6)
        aggressive_decision = aggressive.decide_continue(1500, 6)
        balanced_decision = balanced.decide_continue(1500, 6)

        assert cautious_decision in [True, False]
        assert aggressive_decision in [True, False]
        assert balanced_decision in [True, False]

    def test_complete_game_simulation(self):
        """Full simulation test of the game until victory"""
        game = GameEngine([CautiousBot(), AggressiveBot()], target_score=1000)
        game.play_game()
        assert game.check_winner() is not None
