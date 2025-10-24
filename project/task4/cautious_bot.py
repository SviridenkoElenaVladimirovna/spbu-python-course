from project.task4.player import Player
from typing import List, Tuple

class CautiousBot(Player):
    """
    Cautious bot that prioritizes safety over high scores.
    
    Strategy:
    - Stops early with decent scores
    - Selects only the best combinations
    - Very risk-averse
    """
    
    def __init__(self, name: str = "Cautious Bot") -> None:
        """
        Initialize cautious bot.
        
        Args:
            name: Bot name, defaults to "Cautious Bot"
        """
        super().__init__(name)
    
    def decide_continue(self, current_round_score: int, dice_count: int) -> bool:
        """
        Very conservative decision logic.
        
        Args:
            current_round_score: Current round score
            dice_count: Number of dice remaining
            
        Returns:
            True if should continue, False to stop
        """
        if current_round_score >= 300 and dice_count < 4:
            return False
        return current_round_score < 400
    
    def select_combinations(
        self, 
        combinations: List[Tuple[str, int, List[int]]]
    ) -> List[Tuple[str, int, List[int]]]:
        """
        Select only top combinations (70% of max value), limited to 2.
        
        Args:
            combinations: Available scoring combinations
            
        Returns:
            Selected top combinations (max 2)
        """
        if not combinations:
            return []
        
        selected = []
        max_points = max(c[1] for c in combinations) if combinations else 0
        
        for combo in combinations:
            if combo[1] >= max_points * 0.7:
                selected.append(combo)
        
        return selected[:2]