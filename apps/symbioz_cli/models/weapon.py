"""Weapon model."""
from typing import Dict, Optional


class Weapon:
    """Represents a weapon."""
    
    def __init__(
        self,
        name: str,
        weapon_type: str,  # "melee" or "ranged"
        base_damage: str,  # e.g., "1d6", "1d8"
        attack_bonus: int = 0,
        upgrades: Dict[str, any] = None
    ):
        self.name = name
        self.weapon_type = weapon_type
        self.base_damage = base_damage  # Dice notation
        self.attack_bonus = attack_bonus
        self.upgrades = upgrades or {}  # Slot upgrades
    
    def roll_damage(self) -> int:
        """Roll damage dice (simple parser for MVP)."""
        # Parse "1d6" or "1d8" format
        parts = self.base_damage.split("d")
        if len(parts) != 2:
            return 1
        num_dice = int(parts[0])
        die_size = int(parts[1])
        
        import random
        total = 0
        for _ in range(num_dice):
            total += random.randint(1, die_size)
        
        # Add upgrade bonuses
        damage_bonus = self.upgrades.get("damage_bonus", 0)
        return total + damage_bonus
    
    def __str__(self) -> str:
        return self.name

