import random


class Dice:
    """
    Represents a single six-sided dice.

    Attributes:
        value (int): Current face value of the dice (1-6)
    """

    def __init__(self) -> None:
        """Initialize dice with value 1."""
        self.value = 1

    def roll(self) -> int:
        """
        Roll the dice and return random value.

        Returns:
            Random integer between 1 and 6
        """
        self.value = random.randint(1, 6)
        return self.value

    def __str__(self) -> str:
        """
        Return string representation of dice value.

        Returns:
            String representation of current value
        """
        return str(self.value)

    def reset(self) -> "Dice":
        """
        Reset dice value to 1.

        Returns:
            self for method chaining
        """
        self.value = 1
        return self
