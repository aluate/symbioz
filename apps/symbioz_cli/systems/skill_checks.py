"""Skill check system for narrative choices."""
import random
import sys
import os
from typing import Tuple

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.character import Character


class SkillCheckSystem:
    """Handles skill/attribute checks."""
    
    def roll_check(
        self,
        character: Character,
        attribute: str,
        difficulty_class: int = 15
    ) -> Tuple[bool, int]:
        """
        Roll a skill check: d20 + attribute modifier vs DC.
        Returns (success, roll_total).
        """
        attr_mod = character.get_attribute_modifier(attribute)
        roll = random.randint(1, 20)
        total = roll + attr_mod
        
        # Apply status effects
        if character.has_status_effect("Focused"):
            total += 1
        
        success = total >= difficulty_class
        return success, total
    
    def check_str(self, character: Character, dc: int = 15) -> Tuple[bool, int]:
        """STR check (force, lift, break)."""
        return self.roll_check(character, "STR", dc)
    
    def check_dex(self, character: Character, dc: int = 15) -> Tuple[bool, int]:
        """DEX check (sneak, dodge, pick locks)."""
        return self.roll_check(character, "DEX", dc)
    
    def check_int(self, character: Character, dc: int = 15) -> Tuple[bool, int]:
        """INT check (hack, analyze, solve)."""
        return self.roll_check(character, "INT", dc)
    
    def check_wis(self, character: Character, dc: int = 15) -> Tuple[bool, int]:
        """WIS check (detect, read people, survival)."""
        return self.roll_check(character, "WIS", dc)
    
    def check_cha(self, character: Character, dc: int = 15) -> Tuple[bool, int]:
        """CHA check (persuade, intimidate, negotiate)."""
        return self.roll_check(character, "CHA", dc)

