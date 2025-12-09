"""Symbioz CLI - Main game entry point."""
import sys
import os

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from models.character import Character
from models.enemy import Enemy
from models.weapon import Weapon
from models.armor import Armor
from systems.combat import CombatSystem
from systems.skill_checks import SkillCheckSystem
from systems.progression import ProgressionSystem
from systems.hub import Hub
import data_loader


class Game:
    """Main game controller."""
    
    def __init__(self):
        self.player: Character = None
        self.hub = Hub()
        self.combat_system = CombatSystem()
        self.skill_system = SkillCheckSystem()
        self.progression = ProgressionSystem()
        
        # Load game data
        self.races = data_loader.load_races()
        self.classes = data_loader.load_classes()
        self.weapons = data_loader.load_weapons()
        self.armor_list = data_loader.load_armor()
        self.missions = data_loader.load_missions()
        
        # Give player starting equipment
        self.starting_weapon = self.weapons[0]  # Basic Pistol or Basic Sword
        self.starting_armor = self.armor_list[0]  # Light Armor
    
    def print_separator(self):
        """Print a visual separator."""
        print("\n" + "=" * 60 + "\n")
    
    def get_input(self, prompt: str) -> str:
        """Get user input with error handling."""
        try:
            return input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nGame exited.")
            sys.exit(0)
    
    def character_creation(self):
        """Create a new character."""
        self.print_separator()
        print("=== CHARACTER CREATION ===\n")
        
        # Get name
        name = self.get_input("Enter your character's name: ")
        if not name:
            name = "Player"
        
        # Choose race
        print("\nChoose your race:")
        for i, race in enumerate(self.races, 1):
            print(f"{i}) {race.name} - {race.description}")
        
        while True:
            choice = self.get_input("\nEnter choice (1-3): ")
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(self.races):
                    selected_race = self.races[idx]
                    break
                else:
                    print("Invalid choice. Please enter 1-3.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        # Choose class
        print("\nChoose your class:")
        for i, clazz in enumerate(self.classes, 1):
            print(f"{i}) {clazz.name} - {clazz.description}")
        
        while True:
            choice = self.get_input("\nEnter choice (1-4): ")
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(self.classes):
                    selected_class = self.classes[idx]
                    break
                else:
                    print("Invalid choice. Please enter 1-4.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        # Create character
        self.player = Character(name, selected_race, selected_class)
        
        # Give starting equipment based on class
        if selected_class.name in ["Vanguard"]:
            # Melee class gets sword
            self.player.weapon = next(w for w in self.weapons if w.name == "Basic Sword")
        else:
            # Others get pistol
            self.player.weapon = next(w for w in self.weapons if w.name == "Basic Pistol")
        
        self.player.armor = self.starting_armor
        
        # Show character summary
        self.print_separator()
        print(f"Character created: {self.player.name}")
        print(f"Race: {self.player.race.name}")
        print(f"Class: {self.player.clazz.name}")
        print(f"Level: {self.player.level}")
        print(f"HP: {self.player.hp}/{self.player.max_hp}")
        print(f"\nAttributes:")
        for attr, value in self.player.attributes.items():
            mod = self.player.get_attribute_modifier(attr)
            print(f"  {attr}: {value} ({mod:+d})")
        print(f"\nWeapon: {self.player.weapon.name}")
        print(f"Armor: {self.player.armor.name}")
        input("\nPress Enter to continue...")
    
    def run_combat_mission(self, mission_data: dict):
        """Run a combat-based mission."""
        print(f"\n=== {mission_data['name']} ===\n")
        print(mission_data['description'])
        print("\nCombat begins!\n")
        
        # Create enemies
        enemies = []
        for enemy_data in mission_data['enemies']:
            # Find weapon/armor objects
            weapon = None
            armor = None
            if enemy_data.get('weapon'):
                weapon = next((w for w in self.weapons if w.name == enemy_data['weapon']), None)
            if enemy_data.get('armor'):
                armor = next((a for a in self.armor_list if a.name == enemy_data['armor']), None)
            
            enemy = Enemy(
                name=enemy_data['name'],
                level=enemy_data['level'],
                attributes=enemy_data['attributes'],
                max_hp=enemy_data['max_hp'],
                weapon=weapon,
                armor=armor
            )
            enemies.append(enemy)
        
        # Start combat
        turn_order = self.combat_system.start_combat(self.player, enemies)
        print("Initiative rolled. Turn order:")
        for i, combatant in enumerate(turn_order, 1):
            print(f"  {i}. {combatant.name}")
        input("\nPress Enter to begin combat...")
        
        # Combat loop
        round_num = 1
        while True:
            self.print_separator()
            print(f"=== ROUND {round_num} ===\n")
            
            # Check status effects
            for combatant in [self.player] + enemies:
                if combatant.is_alive():
                    status_msg = self.combat_system.apply_status_effects(combatant)
                    if status_msg:
                        print(status_msg)
            
            # Check if combat is over
            is_over, result = self.combat_system.is_combat_over(self.player, enemies)
            if is_over:
                break
            
            # Process each turn
            for actor in turn_order:
                if not actor.is_alive():
                    continue
                
                if actor == self.player:
                    # Player turn
                    print(f"\n--- {self.player.name}'s Turn ---")
                    print(f"HP: {self.player.hp}/{self.player.max_hp}")
                    if self.player.status_effects:
                        print(f"Status: {', '.join(self.player.status_effects)}")
                    
                    # Show alive enemies
                    alive_enemies = [e for e in enemies if e.is_alive()]
                    print("\nEnemies:")
                    for i, enemy in enumerate(alive_enemies, 1):
                        print(f"  {i}) {enemy.name} - HP: {enemy.hp}/{enemy.max_hp}")
                    
                    # Player action menu
                    print("\nActions:")
                    print("  1) Attack")
                    print("  2) Use Ability")
                    print("  3) Use Item")
                    print("  4) Defend")
                    
                    while True:
                        choice = self.get_input("\nChoose action (1-4): ")
                        if choice == "1":
                            # Attack
                            if not alive_enemies:
                                break
                            target_choice = self.get_input(f"Target (1-{len(alive_enemies)}): ")
                            try:
                                target_idx = int(target_choice) - 1
                                if 0 <= target_idx < len(alive_enemies):
                                    target = alive_enemies[target_idx]
                                    hit, damage, result_type = self.combat_system.attack(self.player, target)
                                    if hit:
                                        if result_type == "graze":
                                            print(f"{self.player.name} grazes {target.name} for {damage} damage!")
                                        else:
                                            print(f"{self.player.name} hits {target.name} for {damage} damage!")
                                        if target.hp <= 0:
                                            print(f"{target.name} is defeated!")
                                    else:
                                        print(f"{self.player.name} misses {target.name}!")
                                    break
                                else:
                                    print("Invalid target.")
                            except ValueError:
                                print("Invalid input.")
                        
                        elif choice == "2":
                            # Use ability
                            print("\nAbilities:")
                            for i, ability in enumerate(self.player.clazz.abilities, 1):
                                print(f"  {i}) {ability}")
                            ability_choice = self.get_input("\nChoose ability: ")
                            try:
                                ability_idx = int(ability_choice) - 1
                                if 0 <= ability_idx < len(self.player.clazz.abilities):
                                    ability = self.player.clazz.abilities[ability_idx]
                                    # Self-only abilities
                                    if ability in ["First Aid", "Repair", "Survival Instinct"]:
                                        target = None  # Self-only
                                    elif ability in ["Hack", "Overload Systems"]:
                                        # Need target - show menu
                                        if not alive_enemies:
                                            print("No enemies to target!")
                                            break
                                        print("\nTarget:")
                                        for i, enemy in enumerate(alive_enemies, 1):
                                            print(f"  {i}) {enemy.name} - HP: {enemy.hp}/{enemy.max_hp}")
                                        target_choice = self.get_input("Choose target (1-{}): ".format(len(alive_enemies)))
                                        try:
                                            target_idx = int(target_choice) - 1
                                            if 0 <= target_idx < len(alive_enemies):
                                                target = alive_enemies[target_idx]
                                            else:
                                                print("Invalid target.")
                                                continue
                                        except ValueError:
                                            print("Invalid input.")
                                            continue
                                    else:
                                        # Other abilities (Power Strike, Brace, etc.) don't need targets
                                        target = None
                                    msg = self.combat_system.use_ability(self.player, ability, target)
                                    print(msg)
                                    break
                                else:
                                    print("Invalid choice.")
                            except ValueError:
                                print("Invalid input.")
                        
                        elif choice == "3":
                            # Use item (Honey)
                            # Check if player has items
                            if not self.player.inventory:
                                print("You have no items to use!")
                                break
                            
                            # For MVP, just use Vital Honey if available
                            has_honey = any("Honey" in str(item) for item in self.player.inventory)
                            if has_honey:
                                import random
                                con_mod = self.player.get_attribute_modifier("CON")
                                heal_amount = random.randint(1, 6) + con_mod
                                heal_amount = max(3, heal_amount)  # Minimum 3 HP
                                old_hp = self.player.hp
                                self.player.heal(heal_amount)
                                actual_heal = self.player.hp - old_hp
                                # Remove one honey from inventory (simplified)
                                honey_items = [item for item in self.player.inventory if "Honey" in str(item)]
                                if honey_items:
                                    self.player.inventory.remove(honey_items[0])
                                print(f"You consume Vital Honey and restore {actual_heal} HP! ({self.player.hp}/{self.player.max_hp} HP)")
                            else:
                                print("You have no consumable items!")
                            break
                        
                        elif choice == "4":
                            # Defend
                            msg = self.combat_system.use_ability(self.player, "Brace")
                            print(msg)
                            break
                        
                        else:
                            print("Invalid choice.")
                
                else:
                    # Enemy turn
                    if actor.is_alive():
                        print(f"\n--- {actor.name}'s Turn ---")
                        action = actor.choose_action(self.player)
                        if action == "attack":
                            hit, damage, result_type = self.combat_system.attack(actor, self.player)
                            if hit:
                                if result_type == "graze":
                                    print(f"{actor.name} grazes {self.player.name} for {damage} damage!")
                                else:
                                    print(f"{actor.name} hits {self.player.name} for {damage} damage!")
                                if self.player.hp <= 0:
                                    print(f"{self.player.name} is defeated!")
                            else:
                                print(f"{actor.name} misses {self.player.name}!")
            
            round_num += 1
            input("\nPress Enter to continue...")
        
        # Combat result
        self.print_separator()
        if result == "victory":
            print("=== VICTORY! ===\n")
            xp = mission_data.get('xp_reward', 50)
            leveled_up = self.player.add_xp(xp)
            print(f"XP Gained: {xp}")
            if leveled_up:
                print(f"\n*** LEVEL UP! ***")
                print(f"You are now level {self.player.level}!")
                print(f"Max HP increased to {self.player.max_hp}")
            
            # Loot
            loot = mission_data.get('loot', {})
            if loot.get('credits'):
                self.player.credits += loot['credits']
                print(f"\nCredits: +{loot['credits']} (Total: {self.player.credits})")
            if loot.get('items'):
                for item in loot['items']:
                    self.player.inventory.append(item)
                print(f"Items found: {', '.join(loot['items'])}")
                if "Vital Honey" in loot.get('items', []):
                    print(f"\nHint: You can use Vital Honey during combat via 'Use Item' to restore HP.")
                else:
                    print(f"(Added to inventory. Use 'Use Item' in combat to consume.)")
            
            print("\nMission complete!")
        else:
            print("=== DEFEAT ===\n")
            print("You have been defeated. Returning to hub...")
            self.player.hp = 1  # Revive with 1 HP
        
        input("\nPress Enter to continue...")
    
    def run_skill_mission(self, mission_data: dict):
        """Run a skill-check-based mission."""
        print(f"\n=== {mission_data['name']} ===\n")
        print(mission_data['description'])
        print("\n")
        
        success = True
        for check in mission_data.get('skill_checks', []):
            attr = check['attribute']
            dc = check['dc']
            desc = check['description']
            
            print(f"Skill Check: {desc}")
            print(f"Rolling {attr} check (DC {dc})...")
            input("Press Enter to roll...")
            
            passed, total = self.skill_system.roll_check(self.player, attr, dc)
            print(f"Roll: {total} (need {dc})")
            
            if passed:
                print("Success!")
            else:
                print("Failure!")
                success = False
                break
            
            print()
        
        self.print_separator()
        if success:
            print("=== MISSION SUCCESS ===\n")
            xp = mission_data.get('xp_reward', 50)
            leveled_up = self.player.add_xp(xp)
            print(f"XP Gained: {xp}")
            if leveled_up:
                print(f"\n*** LEVEL UP! ***")
                print(f"You are now level {self.player.level}!")
            
            loot = mission_data.get('loot', {})
            if loot.get('credits'):
                self.player.credits += loot['credits']
                print(f"\nCredits: +{loot['credits']} (Total: {self.player.credits})")
            if loot.get('items'):
                for item in loot['items']:
                    self.player.inventory.append(item)
                print(f"Items found: {', '.join(loot['items'])}")
        else:
            print("=== MISSION FAILED ===\n")
            full_xp = mission_data.get('xp_reward', 50)
            xp = full_xp // 2
            self.player.add_xp(xp)
            print(f"You failed the mission. Reduced rewards...")
            print(f"XP Gained: {xp} (would have been {full_xp} on success)")
            print("No items or credits earned.")
        
        input("\nPress Enter to continue...")
    
    def hub_menu(self):
        """Display and handle hub menu."""
        while True:
            self.print_separator()
            print(f"=== {self.hub.name} ===\n")
            print("What would you like to do?")
            for option in self.hub.show_menu():
                print(f"  {option}")
            
            choice = self.get_input("\nEnter choice (1-6): ")
            
            if choice == "1":
                # View Missions
                self.print_separator()
                print("=== AVAILABLE MISSIONS ===\n")
                for i, mission in enumerate(self.missions, 1):
                    print(f"{i}) {mission['name']}")
                    print(f"   {mission['description']}")
                    print(f"   XP Reward: {mission.get('xp_reward', 50)}")
                    print()
                
                mission_choice = self.get_input("Choose mission (or 0 to cancel): ")
                try:
                    idx = int(mission_choice) - 1
                    if 0 <= idx < len(self.missions):
                        mission = self.missions[idx]
                        if mission['type'] == 'combat':
                            self.run_combat_mission(mission)
                        elif mission['type'] == 'skill':
                            self.run_skill_mission(mission)
                    elif mission_choice == "0":
                        continue
                    else:
                        print("Invalid choice.")
                except ValueError:
                    print("Invalid input.")
            
            elif choice == "2":
                # Visit Vendor
                self.visit_vendor()
            
            elif choice == "3":
                # Rest/Recover
                msg = self.hub.rest(self.player)
                print(f"\n{msg}")
                input("\nPress Enter to continue...")
            
            elif choice == "4":
                # Character Sheet
                sheet = self.hub.show_character_sheet(self.player)
                print(sheet)
                input("\nPress Enter to continue...")
            
            elif choice == "5":
                # Talk
                print("\nYou chat with the locals. They have nothing interesting to say.")
                print("(NPC dialogue coming in Phase 2!)")
                input("\nPress Enter to continue...")
            
            elif choice == "6":
                # Exit
                print("\nThanks for playing! Exiting...")
                return False
            
            else:
                print("Invalid choice.")
        
        return True
    
    def visit_vendor(self):
        """Handle vendor shopping."""
        self.print_separator()
        print("=== VENDOR ===\n")
        print(f"Your Credits: {self.player.credits}\n")
        print("Available Items:\n")
        
        vendor_items = [
            {"name": "Improved Pistol", "price": 80, "type": "weapon", "weapon_name": "Improved Pistol"},
            {"name": "Improved Sword", "price": 80, "type": "weapon", "weapon_name": "Improved Sword"},
            {"name": "Reinforced Light Armor", "price": 70, "type": "armor", "armor_name": "Reinforced Light Armor"},
            {"name": "Vital Honey", "price": 25, "type": "item", "item_name": "Vital Honey"}
        ]
        
        for i, item in enumerate(vendor_items, 1):
            print(f"{i}) {item['name']} - {item['price']} credits")
        
        print("\n0) Exit Vendor")
        
        while True:
            choice = self.get_input("\nWhat would you like to buy? (0-4): ")
            if choice == "0":
                break
            
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(vendor_items):
                    item = vendor_items[idx]
                    if self.player.credits >= item['price']:
                        self.player.credits -= item['price']
                        
                        if item['type'] == "weapon":
                            # Find and equip weapon
                            weapon = next((w for w in self.weapons if w.name == item['weapon_name']), None)
                            if weapon:
                                old_weapon = self.player.weapon.name if self.player.weapon else "None"
                                self.player.weapon = weapon
                                print(f"\nPurchased {item['name']}!")
                                print(f"Replaced {old_weapon} with {weapon.name}.")
                            else:
                                print(f"\nError: {item['weapon_name']} not found in weapons list.")
                                self.player.credits += item['price']  # Refund
                        
                        elif item['type'] == "armor":
                            # Find and equip armor
                            armor = next((a for a in self.armor_list if a.name == item['armor_name']), None)
                            if armor:
                                old_armor = self.player.armor.name if self.player.armor else "None"
                                self.player.armor = armor
                                print(f"\nPurchased {item['name']}!")
                                print(f"Replaced {old_armor} with {armor.name}.")
                            else:
                                # Create Reinforced Light Armor if it doesn't exist
                                from models.armor import Armor
                                armor = Armor(
                                    name="Reinforced Light Armor",
                                    armor_type="light",
                                    defense_bonus=2,  # +1 over Light Armor
                                    damage_reduction=1
                                )
                                old_armor = self.player.armor.name if self.player.armor else "None"
                                self.player.armor = armor
                                print(f"\nPurchased {item['name']}!")
                                print(f"Replaced {old_armor} with {armor.name}.")
                        
                        elif item['type'] == "item":
                            self.player.inventory.append(item['item_name'])
                            print(f"\nPurchased {item['name']}! Added to inventory.")
                        
                        print(f"Remaining credits: {self.player.credits}")
                        input("\nPress Enter to continue...")
                        break
                    else:
                        print(f"\nNot enough credits! You need {item['price']} but only have {self.player.credits}.")
                        input("\nPress Enter to continue...")
                        break
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input.")
    
    def run(self):
        """Main game loop."""
        print("\n" + "=" * 60)
        print("  SYMBIOZ - CLI Prototype MVP")
        print("=" * 60)
        
        # Character creation
        self.character_creation()
        
        # Hub loop
        while True:
            if not self.hub_menu():
                break


if __name__ == "__main__":
    game = Game()
    game.run()

