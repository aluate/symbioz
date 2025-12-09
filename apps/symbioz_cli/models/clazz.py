"""Class model for character classes."""
from typing import Dict, List


class Class:
    """Represents a character class."""
    
    def __init__(
        self,
        name: str,
        description: str,
        base_hp: int,
        hp_per_level: int,
        attribute_bonuses: Dict[str, int],
        abilities: List[str] = None
    ):
        self.name = name
        self.description = description
        self.base_hp = base_hp
        self.hp_per_level = hp_per_level
        self.attribute_bonuses = attribute_bonuses  # Bonuses to attributes
        self.abilities = abilities or []  # List of ability names
    
    def __str__(self) -> str:
        return self.name

