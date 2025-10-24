import pytest
import sys
import os

current_dir = os.path.dirname(__file__)
project_path = os.path.join(current_dir, "..")
sys.path.insert(0, os.path.abspath(project_path))

from project.task4.dice import Dice
from project.task4.game_rules import GameRules
from project.task4.player import Player
from project.task4.cautious_bot import CautiousBot
from project.task4.aggressive_bot import AggressiveBot
from project.task4.balanced_bot import BalancedBot
from project.task4.game_engine import GameEngine


@pytest.fixture
def dice():
    """Fixture for creating a dice"""
    return Dice()


@pytest.fixture
def cautious_bot():
    """Fixture for creating a cautious bot"""
    return CautiousBot("TestCautious")


@pytest.fixture
def aggressive_bot():
    """Fixture for creating an aggressive bot"""
    return AggressiveBot("TestAggressive")


@pytest.fixture
def balanced_bot():
    """Fixture for creating a balanced bot"""
    return BalancedBot("TestBalanced")


@pytest.fixture
def sample_combinations():
    """Fixture for test combinations"""
    return [
        ("3 1", 1000, [1, 1, 1]),
        ("1", 100, [1]),
        ("5", 50, [5]),
        ("3 2", 200, [2, 2, 2]),
    ]


@pytest.fixture
def game_with_bots():
    """Fixture for playing with bots"""
    bots = [
        CautiousBot("Cautious"),
        AggressiveBot("Aggressive"),
        BalancedBot("Balanced"),
    ]
    return GameEngine(players=bots, target_score=1000, max_rounds=5)
