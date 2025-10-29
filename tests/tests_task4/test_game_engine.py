import pytest
from project.task4.balanced_bot import BalancedBot
from project.task4.aggressive_bot import AggressiveBot
from project.task4.cautious_bot import CautiousBot
from project.task4.game_engine import GameEngine


class TestGameEngine:
    """Game engine tests"""

    def test_game_engine_initialization(self, game_with_bots):
        """Game engine initialization test"""
        game = game_with_bots
        assert len(game.players) == 3
        assert game.target_score == 1000
        assert game.max_rounds == 5
        assert game.current_round == 0
        assert game.active_player_index == 0
        assert len(game.dice_set) == 6

    def test_player_rotation(self, game_with_bots):
        """Player rotation test"""
        game = game_with_bots

        first_player = game.get_active_player()
        game.next_player()
        second_player = game.get_active_player()
        game.next_player()
        third_player = game.get_active_player()
        game.next_player()
        back_to_first = game.get_active_player()

        assert first_player != second_player
        assert second_player != third_player
        assert third_player != back_to_first
        assert first_player == back_to_first

    def test_dice_rolling(self, game_with_bots):
        """Dice roll test"""
        game = game_with_bots

        for dice_count in [1, 3, 6]:
            values = game.roll_dice(dice_count)
            assert len(values) == dice_count
            assert all(1 <= v <= 6 for v in values)

    def test_winner_detection(self):
        """Winner determination test"""
        bot1 = CautiousBot("Bot1")
        bot2 = AggressiveBot("Bot2")

        bot1.total_score = 1500
        bot2.total_score = 800

        game = GameEngine(players=[bot1, bot2], target_score=1000)
        winner = game.check_winner()

        assert winner == bot1
        assert winner.total_score >= game.target_score

    def test_no_winner_scenario(self):
        """Test scenario without a winner"""
        bot1 = CautiousBot("Bot1")
        bot2 = AggressiveBot("Bot2")

        bot1.total_score = 800
        bot2.total_score = 900

        game = GameEngine(players=[bot1, bot2], target_score=1000)
        winner = game.check_winner()

        assert winner is None

    def test_boundary_values(self):
        """Limit value tests"""

        game = GameEngine([CautiousBot()], target_score=5000)

        game.players[0].total_score = 4999
        assert game.check_winner() is None

        game.players[0].total_score = 5000
        assert game.check_winner() is not None

        game.players[0].total_score = 5001
        assert game.check_winner() is not None

    def test_win_conditions(self):
        """Testing different victory conditions"""
        game = GameEngine([CautiousBot()], target_score=5000)

        game.players[0].total_score = 5000
        assert game.check_winner() is not None

        game.players[0].total_score = 5001
        assert game.check_winner() is not None

        game.players[0].total_score = 4999
        assert game.check_winner() is None

    def test_exact_target_score_scenario(self):
        """Accurate goal achievement scenario test"""
        game = GameEngine([CautiousBot()], target_score=1000)

        game.players[0].total_score = 1000
        winner = game.check_winner()
        assert winner is not None
        assert winner.total_score == game.target_score
