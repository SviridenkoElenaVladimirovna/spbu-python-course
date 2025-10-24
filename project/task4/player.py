from abc import ABC, abstractmethod
from typing import List, Tuple, Optional


class Player(ABC):
    """
    Abstract base class representing a player in the Zonk game.

    Attributes:
        name (str): Player's name
        total_score (int): Total accumulated score across all rounds
        round_score (int): Score accumulated in the current round
        consecutive_zonks (int): Number of consecutive zonks
        is_active (bool): Whether the player is active in the game
    """

    def __init__(self, name: str) -> None:
        """
        Initialize a new player.

        Args:
            name: Player's name
        """
        self.name = name
        self.total_score = 0
        self.round_score = 0
        self.consecutive_zonks = 0
        self.is_active = True

    @abstractmethod
    def decide_continue(self, current_round_score: int, dice_count: int) -> bool:
        """
        Decide whether to continue rolling or stop the round.

        Args:
            current_round_score: Points accumulated in current round
            dice_count: Number of dice remaining to roll

        Returns:
            True if player wants to continue, False to stop
        """
        pass

    @abstractmethod
    def select_combinations(
        self, combinations: List[Tuple[str, int, List[int]]]
    ) -> List[Tuple[str, int, List[int]]]:
        """
        Select scoring combinations from available options.

        Args:
            combinations: List of available combinations, each as
                         (name, points, dice_values)

        Returns:
            List of selected combinations
        """
        pass

    def reset_round(self) -> None:
        """Reset round-specific state while preserving total score."""
        self.round_score = 0
        self.consecutive_zonks = 0

    def add_score(self, points: int) -> None:
        """
        Add points to current round score.

        Args:
            points: Points to add to round score
        """
        self.round_score += points

    def finalize_round(self) -> None:
        """Finalize the round by adding round score to total and resetting round state."""
        if self.round_score > 0:
            self.total_score += self.round_score
        self.round_score = 0
        self.consecutive_zonks = 0

    def handle_zonk(self) -> None:
        """Handle a zonk (no scoring combinations) by resetting round score and applying penalties."""
        self.consecutive_zonks += 1
        self.round_score = 0
        if self.consecutive_zonks >= 3:
            self.total_score = max(0, self.total_score - 500)

    def __str__(self) -> str:
        """
        Return string representation of player.

        Returns:
            String in format "Name (Points: score)"
        """
        return f"{self.name} (Points: {self.total_score})"
