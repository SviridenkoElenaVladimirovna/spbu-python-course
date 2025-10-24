from project.task4.player import Player
from typing import List, Tuple


class AggressiveBot(Player):
    """
    Aggressive bot that takes high risks for high rewards.

    Strategy:
    - Continues with many dice and low scores
    - Selects all available combinations
    """

    def __init__(self, name: str = "Aggressive Bot") -> None:
        """
        Initialize aggressive bot.

        Args:
            name: Bot name, defaults to "Aggressive Bot"
        """
        super().__init__(name)

    def decide_continue(self, current_round_score: int, dice_count: int) -> bool:
        """
        Decide to continue if many dice remain and score is low.

        Args:
            current_round_score: Current round score
            dice_count: Number of dice remaining

        Returns:
            True if should continue, False to stop
        """
        return dice_count > 2 and current_round_score < 1000

    def select_combinations(
        self, combinations: List[Tuple[str, int, List[int]]]
    ) -> List[Tuple[str, int, List[int]]]:
        """
        Select all available combinations (aggressive strategy).

        Args:
            combinations: Available scoring combinations

        Returns:
            All available combinations
        """
        if not combinations:
            return []
        return combinations
