"""Progression system: XP, leveling, upgrades."""
import sys
import os
from typing import Tuple

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.character import Character


class ProgressionSystem:
    """Handles character progression."""
    
    def __init__(self):
        pass
    
    def award_xp(self, character: Character, amount: int) -> bool:
        """Award XP and return True if leveled up."""
        return character.add_xp(amount)
    
    def xp_for_level(self, level: int) -> int:
        """Calculate XP needed for a level."""
        return 100 * (level ** 2)
    
    def get_xp_progress(self, character: Character) -> Tuple[int, int]:
        """Get (current_xp, xp_needed_for_next_level)."""
        current_xp = character.xp
        next_level_xp = self.xp_for_level(character.level + 1)
        return current_xp, next_level_xp

