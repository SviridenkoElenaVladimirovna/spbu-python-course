import os
import sys

current_dir = os.path.dirname(__file__)
project_path = os.path.join(current_dir, "..")
sys.path.insert(0, os.path.abspath(project_path))

from project.task4.cautious_bot import CautiousBot
from project.task4.aggressive_bot import AggressiveBot
from project.task4.balanced_bot import BalancedBot
from project.task4.game_engine import GameEngine

def main():
    """
    Launching the Zonk game with three bots.
    """
    bots = [
        CautiousBot("Cautious Bot"),
        AggressiveBot("Aggressive Bot"), 
        BalancedBot("Balanced Bot")
    ]
    
    game = GameEngine(players=bots, target_score=5000, max_rounds=30)
    game.play_game()

if __name__ == "__main__":
    main()