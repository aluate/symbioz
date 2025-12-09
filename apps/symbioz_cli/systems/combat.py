"""Combat system implementing COMBAT_SYSTEM.md rules."""
import random
import sys
import os
from typing import List, Tuple

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.character import Character
from models.enemy import Enemy


class CombatSystem:
    """Handles turn-based combat."""
    
    def __init__(self):
        self.turn_order: List[Character] = []
        self.current_turn = 0
    
    def roll_initiative(self, character: Character) -> int:
        """Roll initiative: d20 + DEX mod."""
        dex_mod = character.get_attribute_modifier("DEX")
        roll = random.randint(1, 20)
        return roll + dex_mod
    
    def start_combat(self, player: Character, enemies: List[Enemy]) -> List[Character]:
        """Initialize combat and determine turn order."""
        all_combatants = [player] + enemies
        
        # Roll initiative for all
        initiatives = []
        for combatant in all_combatants:
            init = self.roll_initiative(combatant)
            initiatives.append((init, combatant))
        
        # Sort by initiative (highest first)
        initiatives.sort(key=lambda x: x[0], reverse=True)
        self.turn_order = [combatant for _, combatant in initiatives]
        self.current_turn = 0
        
        return self.turn_order
    
    def get_current_actor(self) -> Character:
        """Get the character whose turn it is."""
        return self.turn_order[self.current_turn]
    
    def next_turn(self):
        """Advance to next turn."""
        self.current_turn = (self.current_turn + 1) % len(self.turn_order)
    
    def attack(self, attacker: Character, target: Character) -> Tuple[bool, int, str]:
        """
        Perform an attack roll and return (hit, damage, message).
        Returns "hit", "graze", or "miss".
        """
        attack_roll = random.randint(1, 20)
        attack_bonus = attacker.get_attack_bonus()
        total_attack = attack_roll + attack_bonus
        
        defense = target.get_defense()
        
        # Apply status effects
        if attacker.has_status_effect("Staggered"):
            total_attack -= 2
        if target.has_status_effect("Staggered"):
            defense -= 2
        if target.has_status_effect("Guarded"):
            defense += 4  # Brace/Dodge bonus
        if target.has_status_effect("Systems Disrupted"):
            defense -= 2  # Overload Systems debuff
        if attacker.has_status_effect("Focused"):
            total_attack += 2  # Survival Instinct bonus
        if attacker.has_status_effect("Power Strike Active"):
            total_attack += 2  # Power Strike accuracy bonus
        
        # Check for graze (within 2-3 points below defense)
        graze_threshold = defense - 3
        is_graze = graze_threshold <= total_attack < defense
        
        hit = total_attack >= defense
        damage = 0
        result_type = "miss"
        
        if hit or attack_roll == 20:  # Critical hit on natural 20
            damage = attacker.weapon.roll_damage() if attacker.weapon else 1
            attr_mod = attacker.get_attribute_modifier("STR" if attacker.weapon and attacker.weapon.weapon_type == "melee" else "DEX")
            damage += attr_mod
            
            # Power Strike damage bonus
            if attacker.has_status_effect("Power Strike Active"):
                damage += 2
                attacker.remove_status_effect("Power Strike Active")
            
            # Sneak Attack bonus (if enemy hasn't acted - simplified for MVP)
            if attacker.has_status_effect("Sneak Attack Ready"):
                damage += 3
                attacker.remove_status_effect("Sneak Attack Ready")
            
            # Critical hit doubles damage
            if attack_roll == 20:
                damage *= 2
                # Apply bleeding on crit (if weapon allows)
                target.add_status_effect("Bleeding", duration=3)
            
            actual_damage = target.take_damage(damage)
            result_type = "hit"
            return True, actual_damage, result_type
        
        elif is_graze:
            # Graze: half damage, no status effects, no ability bonuses
            damage = attacker.weapon.roll_damage() if attacker.weapon else 1
            attr_mod = attacker.get_attribute_modifier("STR" if attacker.weapon and attacker.weapon.weapon_type == "melee" else "DEX")
            damage = (damage + attr_mod + 1) // 2  # Half damage, rounded up
            actual_damage = target.take_damage(damage)
            result_type = "graze"
            return True, actual_damage, result_type
        
        return False, 0, result_type
    
    def use_ability(self, character: Character, ability_name: str, target: Character = None) -> str:
        """Use a class ability (simplified for MVP)."""
        if ability_name not in character.clazz.abilities:
            return f"{character.name} doesn't have that ability."
        
        # Enhanced ability implementations for Round 2
        if ability_name == "Power Strike":
            # Power Strike: +2 to hit and +2 damage on next attack
            character.add_status_effect("Power Strike Active", duration=1)
            return f"{character.name} uses Power Strike! Next attack gains +2 to hit and +2 damage."
        
        elif ability_name == "Brace":
            # Brace: +4 Defense for 1 turn
            character.add_status_effect("Guarded", duration=1)
            # Store the defense bonus in a way we can check
            return f"{character.name} braces for impact! Defense increased by 4 this turn."
        
        elif ability_name == "Sneak Attack":
            # Sneak Attack: +3 damage if enemy hasn't acted
            character.add_status_effect("Sneak Attack Ready", duration=1)
            return f"{character.name} uses Sneak Attack! Next attack deals +3 damage if enemy hasn't acted."
        
        elif ability_name == "Dodge":
            # Dodge: +4 Defense for 1 turn
            character.add_status_effect("Guarded", duration=1)
            return f"{character.name} dodges! Defense increased by 4 this turn."
        
        elif ability_name == "Hack":
            # Disable enemy for 1 turn (INT check)
            if not target:
                return f"{character.name} needs a target to hack!"
            int_mod = character.get_attribute_modifier("INT")
            roll = random.randint(1, 20) + int_mod
            if roll >= target.get_defense():
                target.add_status_effect("Stunned", duration=1)
                return f"{character.name} hacks {target.name}! {target.name} is stunned for 1 turn."
            return f"{character.name}'s hack failed! (Roll: {roll} vs Defense: {target.get_defense()})"
        
        elif ability_name == "Repair":
            # Repair: MVP - self-only, no enemy targeting
            int_mod = character.get_attribute_modifier("INT")
            heal_amount = random.randint(1, 4) + int_mod
            heal_amount = max(1, heal_amount)  # Minimum 1 HP
            character.heal(heal_amount)
            return f"{character.name} reroutes power and stabilizes systems, restoring {heal_amount} HP."
        
        elif ability_name == "Overload Systems":
            # Overload Systems: Tech Specialist offensive ability
            if not target:
                return f"{character.name} needs a target to overload systems!"
            int_mod = character.get_attribute_modifier("INT")
            roll = random.randint(1, 20) + int_mod + 2  # +2 ability bonus
            defense = target.get_defense()
            
            if roll >= defense:
                # Hit: deal energy damage and apply debuff
                damage = random.randint(1, 6) + int_mod
                actual_damage = target.take_damage(damage)
                target.add_status_effect("Systems Disrupted", duration=2)
                return f"{character.name} overloads enemy systems! The overload hits {target.name} for {actual_damage} energy damage and disrupts their defenses! (-2 Defense for 2 turns)"
            else:
                return f"{character.name}'s overload fizzles against {target.name}'s shielding. (Roll: {roll} vs Defense: {defense})"
        
        elif ability_name == "First Aid":
            # First Aid: MVP - self-only, no target prompt
            heal_amount = random.randint(2, 8) + 2
            character.heal(heal_amount)
            return f"{character.name} applies first aid! You restore {heal_amount} HP."
        
        elif ability_name == "Survival Instinct":
            # Survival Instinct: +2 Attack, +1 to skill checks, lasts 3 turns
            character.add_status_effect("Focused", duration=3)
            return f"{character.name} taps into survival instinct! +2 Attack and +1 to skill checks for 3 turns."
        
        return f"{character.name} uses {ability_name}!"
    
    def apply_status_effects(self, character: Character):
        """Apply status effect damage/effects at start of turn."""
        if character.has_status_effect("Bleeding"):
            damage = character.take_damage(1)
            return f"{character.name} takes 1 bleeding damage! ({character.hp}/{character.max_hp} HP)"
        return None
    
    def is_combat_over(self, player: Character, enemies: List[Enemy]) -> Tuple[bool, str]:
        """Check if combat is over. Returns (is_over, result)."""
        if not player.is_alive():
            return True, "defeat"
        if all(not enemy.is_alive() for enemy in enemies):
            return True, "victory"
        return False, "ongoing"

