"""Race model for character races."""
from typing import Dict


class Race:
    """Represents a playable race."""
    
    def __init__(
        self,
        name: str,
        description: str,
        base_attributes: Dict[str, int],
        racial_traits: Dict[str, any] = None
    ):
        self.name = name
        self.description = description
        self.base_attributes = base_attributes  # STR, DEX, CON, INT, WIS, CHA
        self.racial_traits = racial_traits or {}
    
    def __str__(self) -> str:
        return self.name

