from typing import List, Tuple, Dict
class GameRules:
    """Static class containing Zonk game rules and combination logic."""
    @staticmethod
    def get_combinations(dice_values: List[int]) -> List[Tuple[str, int, List[int]]]:
        """
        Get all valid scoring combinations from dice values.
        
        Args:
            dice_values: List of 6 dice values
            
        Returns:
            List of combinations, each as (name, points, dice_used)
        """
        combinations = []
        counts = {i: dice_values.count(i) for i in range(1, 7)}
        used_dice = []  

        if all(counts[i] >= 1 for i in range(1, 7)):
            combinations.append(('Six different', 1500, list(range(1, 7)), True))
            used_dice = list(range(1, 7))

        if not used_dice:
            pairs = sum(1 for c in counts.values() if c == 2)
            if pairs == 3:
                used_dice = []
                for value, count in counts.items():
                    if count == 2:
                        used_dice.extend([value] * 2)
                combinations.append(('Three pairs', 750, used_dice, True))

        temp_counts = counts.copy()
        
        if used_dice:
            for value in used_dice:
                temp_counts[value] = 0

        for value, count in temp_counts.items():
            if count >= 3:
                base_points = 1000 if value == 1 else (500 if value == 5 else value * 100)
                total_points = base_points + (count - 3) * base_points
                combinations.append((f'{count} {value}', total_points, [value] * count))
            
            elif count > 0 and value in (1, 5):
                points_per_die = 100 if value == 1 else 50
                total_points = count * points_per_die
                combinations.append((f'{count} {value}', total_points, [value] * count))

        return combinations
    
    @staticmethod
    def calculate_possible_combinations(dice_values: List[int]) -> List[Tuple[str, int, List[int]]]:
        """
        Alias for get_combinations for interface consistency.
        
        Args:
            dice_values: List of dice values
            
        Returns:
            List of scoring combinations
        """
        return GameRules.get_combinations(dice_values)

    @staticmethod
    def get_bonus_throw_combinations(dice_values: List[int]) -> List[Tuple[str, int, List[int]]]:
        """
        Get combinations that qualify for bonus throw.
        
        Args:
            dice_values: List of dice values
            
        Returns:
            List of bonus-qualifying combinations
        """
        combinations = GameRules.get_combinations(dice_values)
        return [c for c in combinations if len(c) == 4 and c[3] is True]

    @staticmethod
    def can_take_bonus_throw(dice_values: List[int]) -> bool:
        """
        Check if player qualifies for bonus throw.
        
        Args:
            dice_values: List of dice values
            
        Returns:
            True if bonus throw is available
        """
        return len(GameRules.get_bonus_throw_combinations(dice_values)) > 0
    
    @staticmethod
    def has_scoring_combinations(dice_values: List[int]) -> bool:
        """
        Check if dice values contain any scoring combinations.
        
        Args:
            dice_values: List of dice values
            
        Returns:
            True if scoring combinations exist
        """
        return len(GameRules.get_combinations(dice_values)) > 0