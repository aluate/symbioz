"""Hub system: menu, vendor, rest, missions."""
import sys
import os
from typing import List, Dict

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.character import Character


class Hub:
    """Represents the player's hub/base."""
    
    def __init__(self, name: str = "The Outpost"):
        self.name = name
        self.missions: List[Dict] = []
        self.vendor_items: List[Dict] = []
    
    def show_menu(self) -> List[str]:
        """Return list of hub menu options."""
        return [
            "1) View Missions",
            "2) Visit Vendor",
            "3) Rest/Recover",
            "4) Character Sheet",
            "5) Talk",
            "6) Exit Game"
        ]
    
    def rest(self, character: Character) -> str:
        """Rest: restore HP and remove status effects."""
        character.hp = character.max_hp
        character.status_effects = []
        return f"You rest at {self.name}. HP restored to full, status effects cleared."
    
    def show_character_sheet(self, character: Character) -> str:
        """Display character information."""
        lines = [
            f"\n=== {character.name} ===",
            f"Race: {character.race.name}",
            f"Class: {character.clazz.name}",
            f"Level: {character.level}",
            f"HP: {character.hp}/{character.max_hp}",
            f"XP: {character.xp}",
            "",
            "Attributes:",
            f"  STR: {character.attributes['STR']} ({character.get_attribute_modifier('STR'):+d})",
            f"  DEX: {character.attributes['DEX']} ({character.get_attribute_modifier('DEX'):+d})",
            f"  CON: {character.attributes['CON']} ({character.get_attribute_modifier('CON'):+d})",
            f"  INT: {character.attributes['INT']} ({character.get_attribute_modifier('INT'):+d})",
            f"  WIS: {character.attributes['WIS']} ({character.get_attribute_modifier('WIS'):+d})",
            f"  CHA: {character.attributes['CHA']} ({character.get_attribute_modifier('CHA'):+d})",
            "",
            f"Weapon: {character.weapon.name if character.weapon else 'None'}",
            f"Armor: {character.armor.name if character.armor else 'None'}",
            ""
        ]
        return "\n".join(lines)

