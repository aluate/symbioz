"""Character model for player and NPCs."""
import sys
import os
from typing import Dict, List, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.race import Race
from models.clazz import Class
from models.weapon import Weapon
from models.armor import Armor


class Character:
    """Represents a playable character or NPC."""
    
    def __init__(
        self,
        name: str,
        race: Race,
        clazz: Class,
        level: int = 1,
        xp: int = 0
    ):
        self.name = name
        self.race = race
        self.clazz = clazz
        self.level = level
        self.xp = xp
        self.credits = 0  # Starting credits
        
        # Attributes (D&D style: STR, DEX, CON, INT, WIS, CHA)
        # Base attributes from race + class
        self.attributes = self._calculate_base_attributes()
        
        # Derived stats
        self.max_hp = self._calculate_max_hp()
        self.hp = self.max_hp
        
        # Equipment
        self.weapon: Optional[Weapon] = None
        self.armor: Optional[Armor] = None
        self.inventory: List[Dict] = []  # List of items (honey, etc.)
        
        # Status effects
        self.status_effects: List[str] = []  # e.g., "Staggered", "Bleeding"
        
    def _calculate_base_attributes(self) -> Dict[str, int]:
        """Calculate base attributes from race and class."""
        # Start with race base attributes
        attrs = self.race.base_attributes.copy()
        
        # Add class bonuses
        for attr, bonus in self.clazz.attribute_bonuses.items():
            attrs[attr] = attrs.get(attr, 10) + bonus
        
        # Add level-based increases (simple: +1 to one stat per level after 1)
        # For MVP, we'll keep it simple
        return attrs
    
    def _calculate_max_hp(self) -> int:
        """Calculate max HP from CON and class."""
        base_hp = self.clazz.base_hp
        con_mod = self.get_attribute_modifier("CON")
        level_bonus = (self.level - 1) * self.clazz.hp_per_level
        return base_hp + (con_mod * self.level) + level_bonus
    
    def get_attribute_modifier(self, attr: str) -> int:
        """Get D&D-style attribute modifier (e.g., 16 = +3, 10 = +0)."""
        value = self.attributes.get(attr, 10)
        return (value - 10) // 2
    
    def get_attack_bonus(self) -> int:
        """Calculate attack bonus for equipped weapon."""
        base = self.level  # Simple: level = base attack bonus
        if self.weapon:
            if self.weapon.weapon_type == "melee":
                attr_mod = self.get_attribute_modifier("STR")
            else:  # ranged
                attr_mod = self.get_attribute_modifier("DEX")
            weapon_bonus = self.weapon.attack_bonus
            return base + attr_mod + weapon_bonus
        return base
    
    def get_defense(self) -> int:
        """Calculate defense (AC)."""
        base = 10
        dex_mod = self.get_attribute_modifier("DEX")
        armor_bonus = self.armor.defense_bonus if self.armor else 0
        return base + dex_mod + armor_bonus
    
    def get_damage_reduction(self) -> int:
        """Get damage reduction from armor."""
        return self.armor.damage_reduction if self.armor else 0
    
    def take_damage(self, damage: int) -> int:
        """Apply damage, accounting for armor reduction."""
        reduction = self.get_damage_reduction()
        actual_damage = max(1, damage - reduction)  # Minimum 1 damage
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage
    
    def heal(self, amount: int):
        """Restore HP."""
        self.hp = min(self.max_hp, self.hp + amount)
    
    def add_xp(self, amount: int) -> bool:
        """Add XP and return True if leveled up."""
        self.xp += amount
        xp_for_next = self._xp_for_level(self.level + 1)
        if self.xp >= xp_for_next:
            self.level_up()
            return True
        return False
    
    def level_up(self):
        """Level up: increase level, recalculate stats."""
        self.level += 1
        # Increase one attribute (simple MVP: player chooses, NPC gets CON)
        # For MVP, we'll just increase CON automatically
        self.attributes["CON"] += 1
        old_max_hp = self.max_hp
        self.max_hp = self._calculate_max_hp()
        # Heal by the difference
        self.hp += (self.max_hp - old_max_hp)
    
    def _xp_for_level(self, level: int) -> int:
        """Calculate XP needed for a given level (tuned for MVP)."""
        # Level 2 at 75 XP, then scale up
        if level == 2:
            return 75
        elif level == 3:
            return 150
        elif level == 4:
            return 250
        elif level == 5:
            return 400
        else:
            # Fallback for higher levels
            return 100 * (level ** 2)
    
    def is_alive(self) -> bool:
        """Check if character is alive."""
        return self.hp > 0
    
    def add_status_effect(self, effect: str, duration: int = 1):
        """Add a status effect."""
        if effect not in self.status_effects:
            self.status_effects.append(effect)
    
    def remove_status_effect(self, effect: str):
        """Remove a status effect."""
        if effect in self.status_effects:
            self.status_effects.remove(effect)
    
    def has_status_effect(self, effect: str) -> bool:
        """Check if character has a status effect."""
        return effect in self.status_effects
    
    def __str__(self) -> str:
        """String representation for display."""
        return f"{self.name} ({self.race.name} {self.clazz.name}) - Level {self.level} - HP: {self.hp}/{self.max_hp}"

