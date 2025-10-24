from project.task4.dice import Dice
from project.task4.game_rules import GameRules
from project.task4.player import Player
from typing import List, Optional


class GameEngine:
    """
    Main game engine for Zonk game.

    Attributes:
        players (List[Player]): List of players in the game
        target_score (int): Score needed to win
        max_rounds (int): Maximum number of rounds
        current_round (int): Current round number
        dice_set (List[Dice]): Set of 6 dice
        active_player_index (int): Index of current active player
    """

    def __init__(
        self, players: List[Player], target_score: int = 5000, max_rounds: int = 50
    ) -> None:
        """
        Initialize game engine.

        Args:
            players: List of players
            target_score: Winning score, defaults to 5000
            max_rounds: Maximum rounds, defaults to 50
        """
        self.players = players
        self.target_score = target_score
        self.max_rounds = max_rounds
        self.current_round = 0
        self.dice_set = [Dice() for _ in range(6)]
        self.active_player_index = 0

    def get_active_player(self) -> Player:
        """
        Get currently active player.

        Returns:
            Current active player
        """
        return self.players[self.active_player_index]

    def next_player(self) -> None:
        """Move to next player in rotation."""
        self.active_player_index = (self.active_player_index + 1) % len(self.players)

    def roll_dice(self, dice_count: int) -> List[int]:
        """
        Roll specified number of dice.

        Args:
            dice_count: Number of dice to roll (1-6)

        Returns:
            List of dice values
        """
        values = []
        for i in range(dice_count):
            values.append(self.dice_set[i].roll())
        return values

    def play_round(self, player: Player) -> bool:
        """
        Play a complete round for one player.

        Args:
            player: Player to play the round

        Returns:
            True if round completed successfully, False if zonk occurred
        """
        print(f"\n move {player.name} ")
        player.reset_round()
        dice_count = 6
        round_ended = False

        while not round_ended and dice_count > 0:
            dice_values = self.roll_dice(dice_count)
            print(f"fell out: {dice_values}")

            combinations = GameRules.get_combinations(dice_values)

            if not combinations:
                print("zonk, points per round are burned")
                player.handle_zonk()
                return False

            selected_combinations = player.select_combinations(combinations)

            if not selected_combinations:
                print("the player did not select any combinations - zonk")
                player.handle_zonk()
                return False

            round_points = sum(combo[1] for combo in selected_combinations)
            player.add_score(round_points)

            used_dice = sum(len(combo[2]) for combo in selected_combinations)
            dice_count -= used_dice

            print(f"selected combinations: {[c[0] for c in selected_combinations]}")
            print(
                f"points per move: {round_points}, Total in the round: {player.round_score}"
            )
            print(f"only bones remain: {dice_count}")

            if dice_count == 0 and GameRules.can_take_bonus_throw(dice_values):
                print("bonus throw")
                dice_count = 6
                continue

            if dice_count > 0:
                continue_playing = player.decide_continue(
                    player.round_score, dice_count
                )
                if not continue_playing:
                    print(f"{player.name} decides to stop")
                    round_ended = True

        if player.round_score > 0:
            round_points = player.round_score
            player.finalize_round()
            print(f"{player.name} earned {round_points} points in this round")
            print(f"total score: {player.total_score}")

        return True

    def check_winner(self) -> Optional[Player]:
        """
        Check if any player has reached target score.

        Returns:
            Winning player or None if no winner
        """
        for player in self.players:
            if player.total_score >= self.target_score:
                return player
        return None

    def play_game(self) -> None:
        """Play complete game until winner or round limit reached."""
        print("start game")
        print(f"Purpose: {self.target_score} points")
        print(f"players: {[str(p) for p in self.players]}")

        winner = None
        self.current_round = 0

        while self.current_round < self.max_rounds and not winner:
            self.current_round += 1
            print(f"\n round {self.current_round} ")

            for i in range(len(self.players)):
                player = self.get_active_player()
                self.play_round(player)

                winner = self.check_winner()
                if winner:
                    break

                self.next_player()

        print("\n game is over")
        if winner:
            print(f"winner: {winner.name} with {winner.total_score} points")
        else:
            print(f"The round limit has been reached ({self.max_rounds})")
            best_player = max(self.players, key=lambda p: p.total_score)

        print("\n final results:")
        for player in sorted(self.players, key=lambda p: p.total_score, reverse=True):
            print(f"{player.name}: {player.total_score} points")
