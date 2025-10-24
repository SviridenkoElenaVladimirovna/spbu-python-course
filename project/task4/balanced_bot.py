from project.task4.player import Player
from typing import List, Tuple

class BalancedBot(Player):
    """
    Balanced bot with moderate risk tolerance.
    
    Strategy:
    - Stops at reasonable scores
    - Selects high-value combinations only
    - Limits number of selected combinations
    """
    
    def __init__(self, name: str = "Balanced Bot") -> None:
        """
        Initialize balanced bot.
        
        Args:
            name: Bot name, defaults to "Balanced Bot"
        """
        super().__init__(name)
    
    def decide_continue(self, current_round_score: int, dice_count: int) -> bool:
        """
        Balanced decision based on score and dice count.
        
        Args:
            current_round_score: Current round score
            dice_count: Number of dice remaining
            
        Returns:
            True if should continue, False to stop
        """
        if current_round_score >= 500:
            return False
        if dice_count <= 2 and current_round_score >= 200:
            return False
        return True
    
    def select_combinations(
        self, 
        combinations: List[Tuple[str, int, List[int]]]
    ) -> List[Tuple[str, int, List[int]]]:
        """
        Select high-value combinations (100+ points), limited to 3.
        
        Args:
            combinations: Available scoring combinations
            
        Returns:
            Selected high-value combinations (max 3)
        """
        if not combinations:
            return []
        
        selected = []
        
        for combo in combinations:
            if combo[1] >= 100:
                selected.append(combo)
        
        return selected[:3] if len(selected) > 3 else selected