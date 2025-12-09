"""Enemy model - simplified NPC for combat."""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.character import Character
from models.race import Race
from models.clazz import Class


class Enemy(Character):
    """Represents an enemy in combat."""
    
    def __init__(
        self,
        name: str,
        level: int,
        attributes: dict,
        max_hp: int,
        weapon=None,
        armor=None
    ):
        # Create minimal race/class for enemy
        race = Race(name="Generic", description="", base_attributes=attributes)
        clazz = Class(
            name="Enemy",
            description="",
            base_hp=max_hp,
            hp_per_level=0,
            attribute_bonuses={}
        )
        
        super().__init__(name, race, clazz, level=level)
        self.max_hp = max_hp
        self.hp = max_hp
        self.weapon = weapon
        self.armor = armor
        
        # Override attributes
        self.attributes = attributes
    
    def choose_action(self, player: Character) -> str:
        """Simple AI: choose action (MVP: always attack)."""
        return "attack"

