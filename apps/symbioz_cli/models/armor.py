"""Armor model."""


class Armor:
    """Represents armor."""
    
    def __init__(
        self,
        name: str,
        armor_type: str,  # "light" or "medium"
        defense_bonus: int,
        damage_reduction: int
    ):
        self.name = name
        self.armor_type = armor_type
        self.defense_bonus = defense_bonus
        self.damage_reduction = damage_reduction
    
    def __str__(self) -> str:
        return self.name

