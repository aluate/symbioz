"""Data loader for JSON game data."""
import json
import os
import sys
from typing import List, Dict

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.race import Race
from models.clazz import Class
from models.weapon import Weapon
from models.armor import Armor


def load_json(filepath: str) -> List[Dict]:
    """Load JSON file and return list/dict."""
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    full_path = os.path.join(data_dir, filepath)
    with open(full_path, 'r') as f:
        return json.load(f)


def load_races() -> List[Race]:
    """Load all races from data/races.json."""
    data = load_json("races.json")
    races = []
    for race_data in data:
        race = Race(
            name=race_data["name"],
            description=race_data["description"],
            base_attributes=race_data["base_attributes"],
            racial_traits=race_data.get("racial_traits", {})
        )
        races.append(race)
    return races


def load_classes() -> List[Class]:
    """Load all classes from data/classes.json."""
    data = load_json("classes.json")
    classes = []
    for class_data in data:
        clazz = Class(
            name=class_data["name"],
            description=class_data["description"],
            base_hp=class_data["base_hp"],
            hp_per_level=class_data["hp_per_level"],
            attribute_bonuses=class_data["attribute_bonuses"],
            abilities=class_data.get("abilities", [])
        )
        classes.append(clazz)
    return classes


def load_weapons() -> List[Weapon]:
    """Load all weapons from data/weapons.json."""
    data = load_json("weapons.json")
    weapons = []
    for weapon_data in data:
        weapon = Weapon(
            name=weapon_data["name"],
            weapon_type=weapon_data["weapon_type"],
            base_damage=weapon_data["base_damage"],
            attack_bonus=weapon_data.get("attack_bonus", 0),
            upgrades=weapon_data.get("upgrades", {})
        )
        weapons.append(weapon)
    return weapons


def load_armor() -> List[Armor]:
    """Load all armor from data/armor.json."""
    data = load_json("armor.json")
    armor_list = []
    for armor_data in data:
        armor = Armor(
            name=armor_data["name"],
            armor_type=armor_data["armor_type"],
            defense_bonus=armor_data["defense_bonus"],
            damage_reduction=armor_data["damage_reduction"]
        )
        armor_list.append(armor)
    return armor_list


def load_missions() -> List[Dict]:
    """Load all missions from data/missions.json."""
    return load_json("missions.json")

