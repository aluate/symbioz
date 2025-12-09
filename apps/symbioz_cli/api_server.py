"""FastAPI server for Symbioz game API."""
import sys
import os
from typing import Dict, List, Optional, Any
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import json
import os

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from main import Game
from models.character import Character
from models.enemy import Enemy

app = FastAPI(title="Symbioz Game API", version="1.0.0")

# CORS configuration - read from environment or use defaults for local dev
def get_allowed_origins():
    """Get allowed origins from environment or use localhost defaults."""
    env_origins = os.getenv("ALLOWED_ORIGINS", "")
    
    # Default origins for local development
    default_origins = ["http://localhost:3000", "http://localhost:3001"]
    
    if env_origins:
        # Split comma-separated list and strip whitespace
        env_origin_list = [origin.strip() for origin in env_origins.split(",")]
        # Combine with defaults (avoid duplicates)
        combined = list(set(default_origins + env_origin_list))
        return combined
    
    return default_origins

# CORS middleware for web UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Game sessions (in-memory with file persistence)
game_sessions: Dict[str, Game] = {}
SAVE_DIR = os.path.join(os.path.dirname(__file__), "saves")
os.makedirs(SAVE_DIR, exist_ok=True)


def save_game_session(session_id: str, game: Game):
    """Save game session to file."""
    if not game.player:
        return
    
    save_data = {
        "session_id": session_id,
        "character": character_to_dict(game.player),
        "has_active_mission": hasattr(game, "current_mission"),
        "mission_id": game.current_mission.get("id") if hasattr(game, "current_mission") else None
    }
    
    save_path = os.path.join(SAVE_DIR, f"{session_id}.json")
    with open(save_path, 'w') as f:
        json.dump(save_data, f, indent=2)


def load_game_session(session_id: str) -> Optional[Game]:
    """Load game session from file."""
    save_path = os.path.join(SAVE_DIR, f"{session_id}.json")
    if not os.path.exists(save_path):
        return None
    
    try:
        with open(save_path, 'r') as f:
            save_data = json.load(f)
        
        game = Game()
        
        # Recreate character
        char_data = save_data["character"]
        # Find race and class by name
        race = next((r for r in game.races if r.name == char_data["race"]), None)
        clazz = next((c for c in game.classes if c.name == char_data["class"]), None)
        
        if not race or not clazz:
            return None
        
        game.player = Character(char_data["name"], race, clazz, char_data["level"], char_data["xp"])
        game.player.hp = char_data["hp"]
        game.player.max_hp = char_data["max_hp"]
        game.player.credits = char_data["credits"]
        game.player.inventory = char_data["inventory"]
        game.player.status_effects = char_data["status_effects"]
        
        # Restore equipment
        if char_data["weapon"]:
            game.player.weapon = next((w for w in game.weapons if w.name == char_data["weapon"]), None)
        if char_data["armor"]:
            game.player.armor = next((a for a in game.armor_list if a.name == char_data["armor"]), None)
        
        return game
    except Exception as e:
        print(f"Error loading session: {e}")
        return None


# Pydantic models for API
class CharacterCreate(BaseModel):
    name: str
    race_id: int
    class_id: int


class CombatAction(BaseModel):
    action_type: str  # "attack", "ability", "item", "defend"
    target_id: Optional[int] = None  # For targeting abilities/attacks
    ability_name: Optional[str] = None  # For ability actions
    item_name: Optional[str] = None  # For item actions


class StartMissionRequest(BaseModel):
    mission_id: int


@app.get("/")
def root():
    """Health check."""
    return {"status": "ok", "message": "Symbioz Game API"}


@app.get("/api/health")
def health():
    """Health check endpoint for deployment monitoring."""
    return {"status": "ok", "message": "Symbioz Game API"}


@app.post("/api/session/create")
def create_session():
    """Create a new game session."""
    session_id = str(uuid.uuid4())
    
    # Try to load existing session first
    game = load_game_session(session_id)
    if not game:
        game = Game()
    
    game_sessions[session_id] = game
    return {"session_id": session_id}


@app.get("/api/session/load")
def load_session(session_id: Optional[str] = Query(None)):
    """Load an existing game session."""
    if not session_id:
        raise HTTPException(status_code=400, detail="session_id required")
    
    if session_id not in game_sessions:
        game = load_game_session(session_id)
        if game:
            game_sessions[session_id] = game
            return {"status": "loaded", "session_id": session_id, "has_character": game.player is not None}
        else:
            raise HTTPException(status_code=404, detail="Session not found")
    else:
        game = game_sessions[session_id]
        return {"status": "active", "session_id": session_id, "has_character": game.player is not None}


@app.post("/api/session/save")
def save_session(session_id: Optional[str] = Query(None)):
    """Save current game session."""
    if not session_id:
        raise HTTPException(status_code=400, detail="session_id required")
    
    if session_id not in game_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    game = game_sessions[session_id]
    save_game_session(session_id, game)
    return {"status": "saved", "session_id": session_id}


@app.post("/api/character/create")
def create_character(character: CharacterCreate, session_id: Optional[str] = Query(None)):
    """Create a character in a session."""
    # Get session_id from query param or create new session
    if not session_id:
        session_id = str(uuid.uuid4())
        game = Game()
        game_sessions[session_id] = game
    elif session_id not in game_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    game = game_sessions[session_id]
    
    # Get race and class
    if character.race_id < 1 or character.race_id > len(game.races):
        raise HTTPException(status_code=400, detail="Invalid race_id")
    if character.class_id < 1 or character.class_id > len(game.classes):
        raise HTTPException(status_code=400, detail="Invalid class_id")
    
    selected_race = game.races[character.race_id - 1]
    selected_class = game.classes[character.class_id - 1]
    
    # Create character
    game.player = Character(character.name, selected_race, selected_class)
    
    # Give starting equipment
    if selected_class.name in ["Vanguard"]:
        game.player.weapon = next(w for w in game.weapons if w.name == "Basic Sword")
    else:
        game.player.weapon = next(w for w in game.weapons if w.name == "Basic Pistol")
    game.player.armor = game.starting_armor
    
    # Auto-save after character creation
    save_game_session(session_id, game)
    
    return {"status": "ok", "character": character_to_dict(game.player), "session_id": session_id}


@app.get("/api/character")
def get_character(session_id: str):
    """Get current character state."""
    if session_id not in game_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    game = game_sessions[session_id]
    if not game.player:
        raise HTTPException(status_code=404, detail="Character not created")
    
    return character_to_dict(game.player)


@app.get("/api/missions")
def get_missions(session_id: str):
    """Get available missions."""
    if session_id not in game_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    game = game_sessions[session_id]
    missions = []
    for i, mission in enumerate(game.missions):
        missions.append({
            "id": i,
            "name": mission["name"],
            "description": mission["description"],
            "type": mission["type"],
            "xp_reward": mission.get("xp_reward", 50)
        })
    return {"missions": missions}


@app.get("/api/races")
def get_races(session_id: str):
    """Get available races."""
    if session_id not in game_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    game = game_sessions[session_id]
    races = []
    for i, race in enumerate(game.races):
        races.append({
            "id": i + 1,
            "name": race.name,
            "description": race.description
        })
    return {"races": races}


@app.get("/api/classes")
def get_classes(session_id: str):
    """Get available classes."""
    if session_id not in game_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    game = game_sessions[session_id]
    classes = []
    for i, clazz in enumerate(game.classes):
        classes.append({
            "id": i + 1,
            "name": clazz.name,
            "description": clazz.description,
            "abilities": clazz.abilities
        })
    return {"classes": classes}


@app.post("/api/mission/start")
def start_mission(session_id: str, request: StartMissionRequest):
    """Start a mission and initialize combat if needed."""
    if session_id not in game_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    game = game_sessions[session_id]
    if not game.player:
        raise HTTPException(status_code=404, detail="Character not created")
    
    if request.mission_id < 0 or request.mission_id >= len(game.missions):
        raise HTTPException(status_code=400, detail="Invalid mission_id")
    
    mission = game.missions[request.mission_id]
    
    # Initialize combat if combat mission
    if mission["type"] == "combat":
        # Create enemies
        enemies = []
        for enemy_data in mission["enemies"]:
            weapon = None
            armor = None
            if enemy_data.get("weapon"):
                weapon = next((w for w in game.weapons if w.name == enemy_data["weapon"]), None)
            if enemy_data.get("armor"):
                armor = next((a for a in game.armor_list if a.name == enemy_data["armor"]), None)
            
            enemy = Enemy(
                name=enemy_data["name"],
                level=enemy_data["level"],
                attributes=enemy_data["attributes"],
                max_hp=enemy_data["max_hp"],
                weapon=weapon,
                armor=armor
            )
            enemies.append(enemy)
        
        # Start combat
        turn_order = game.combat_system.start_combat(game.player, enemies)
        
        # Store combat state
        game.current_mission = mission
        game.current_enemies = enemies
        game.combat_round = 1
        
        return {
            "status": "combat_started",
            "mission": {
                "name": mission["name"],
                "description": mission["description"]
            },
            "enemies": [enemy_to_dict(e) for e in enemies],
            "turn_order": [c.name for c in turn_order],
            "combat_state": get_combat_state(game)
        }
    else:
        # Skill mission - store mission state and return data
        game.current_mission = mission
        return {
            "status": "mission_started",
            "mission": mission,
            "skill_checks": mission.get("skill_checks", [])
        }


@app.get("/api/combat/state")
def get_combat_state_endpoint(session_id: str):
    """Get current combat state."""
    if session_id not in game_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    game = game_sessions[session_id]
    if not hasattr(game, "current_enemies") or not game.current_enemies:
        raise HTTPException(status_code=404, detail="No active combat")
    
    return get_combat_state(game)


@app.post("/api/combat/action")
def combat_action(session_id: str, action: CombatAction):
    """Execute a combat action."""
    if session_id not in game_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    game = game_sessions[session_id]
    if not game.player:
        raise HTTPException(status_code=404, detail="Character not created")
    
    if not hasattr(game, "current_enemies") or not game.current_enemies:
        raise HTTPException(status_code=404, detail="No active combat")
    
    combat_log = []
    
    # Check if it's player's turn
    current_actor = game.combat_system.get_current_actor()
    if current_actor != game.player:
        # Process enemy turns until it's player's turn
        while current_actor != game.player and current_actor.is_alive():
            enemy_action = current_actor.choose_action(game.player)
            if enemy_action == "attack":
                hit, damage, result_type = game.combat_system.attack(current_actor, game.player)
                if hit:
                    if result_type == "graze":
                        combat_log.append(f"{current_actor.name} grazes {game.player.name} for {damage} damage!")
                    else:
                        combat_log.append(f"{current_actor.name} hits {game.player.name} for {damage} damage!")
                else:
                    combat_log.append(f"{current_actor.name} misses {game.player.name}!")
            
            game.combat_system.next_turn()
            current_actor = game.combat_system.get_current_actor()
            
            # Check if combat is over
            is_over, result = game.combat_system.is_combat_over(game.player, game.current_enemies)
            if is_over:
                return handle_combat_end(session_id, game, combat_log, result)
    
    # Apply status effects
    for combatant in [game.player] + game.current_enemies:
        if combatant.is_alive():
            status_msg = game.combat_system.apply_status_effects(combatant)
            if status_msg:
                combat_log.append(status_msg)
    
    # Check if combat is over before player action
    is_over, result = game.combat_system.is_combat_over(game.player, game.current_enemies)
    if is_over:
        return handle_combat_end(session_id, game, combat_log, result)
    
    # Execute player action
    alive_enemies = [e for e in game.current_enemies if e.is_alive()]
    
    if action.action_type == "attack":
        if not alive_enemies:
            raise HTTPException(status_code=400, detail="No enemies to attack")
        if action.target_id is None or action.target_id < 0 or action.target_id >= len(alive_enemies):
            raise HTTPException(status_code=400, detail="Invalid target_id")
        
        target = alive_enemies[action.target_id]
        hit, damage, result_type = game.combat_system.attack(game.player, target)
        if hit:
            if result_type == "graze":
                combat_log.append(f"{game.player.name} grazes {target.name} for {damage} damage!")
            else:
                combat_log.append(f"{game.player.name} hits {target.name} for {damage} damage!")
            if target.hp <= 0:
                combat_log.append(f"{target.name} is defeated!")
        else:
            combat_log.append(f"{game.player.name} misses {target.name}!")
    
    elif action.action_type == "ability":
        if not action.ability_name:
            raise HTTPException(status_code=400, detail="ability_name required")
        
        target = None
        if action.ability_name in ["Hack", "Overload Systems"]:
            if action.target_id is None or action.target_id < 0 or action.target_id >= len(alive_enemies):
                raise HTTPException(status_code=400, detail="Invalid target_id for this ability")
            target = alive_enemies[action.target_id]
        
        msg = game.combat_system.use_ability(game.player, action.ability_name, target)
        combat_log.append(msg)
    
    elif action.action_type == "item":
        if not action.item_name:
            raise HTTPException(status_code=400, detail="item_name required")
        
        # Use item (Honey)
        if "Honey" in action.item_name:
            import random
            con_mod = game.player.get_attribute_modifier("CON")
            heal_amount = random.randint(1, 6) + con_mod
            heal_amount = max(3, heal_amount)
            old_hp = game.player.hp
            game.player.heal(heal_amount)
            actual_heal = game.player.hp - old_hp
            
            # Remove honey from inventory
            honey_items = [item for item in game.player.inventory if "Honey" in str(item)]
            if honey_items:
                game.player.inventory.remove(honey_items[0])
            
            combat_log.append(f"You consume {action.item_name} and restore {actual_heal} HP! ({game.player.hp}/{game.player.max_hp} HP)")
        else:
            raise HTTPException(status_code=400, detail="Unknown item")
    
    elif action.action_type == "defend":
        msg = game.combat_system.use_ability(game.player, "Brace", None)
        combat_log.append(msg)
    
    else:
        raise HTTPException(status_code=400, detail="Invalid action_type")
    
    # Advance turn
    game.combat_system.next_turn()
    
    # Process enemy turns
    current_actor = game.combat_system.get_current_actor()
    while current_actor != game.player and current_actor.is_alive():
        enemy_action = current_actor.choose_action(game.player)
        if enemy_action == "attack":
            hit, damage, result_type = game.combat_system.attack(current_actor, game.player)
            if hit:
                if result_type == "graze":
                    combat_log.append(f"{current_actor.name} grazes {game.player.name} for {damage} damage!")
                else:
                    combat_log.append(f"{current_actor.name} hits {game.player.name} for {damage} damage!")
            else:
                combat_log.append(f"{current_actor.name} misses {game.player.name}!")
        
        game.combat_system.next_turn()
        current_actor = game.combat_system.get_current_actor()
        
        # Check if combat is over
        is_over, result = game.combat_system.is_combat_over(game.player, game.current_enemies)
        if is_over:
            return handle_combat_end(session_id, game, combat_log, result)
    
    # Check if combat is over after all turns
    is_over, result = game.combat_system.is_combat_over(game.player, game.current_enemies)
    if is_over:
        return handle_combat_end(session_id, game, combat_log, result)
    
    # Return updated state
    return {
        "status": "action_complete",
        "combat_log": combat_log,
        "combat_state": get_combat_state(game)
    }


@app.get("/api/hub/vendor")
def get_vendor_items(session_id: str):
    """Get vendor items."""
    if session_id not in game_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    game = game_sessions[session_id]
    if not game.player:
        raise HTTPException(status_code=404, detail="Character not created")
    
    vendor_items = [
        {"id": 1, "name": "Improved Pistol", "price": 80, "type": "weapon"},
        {"id": 2, "name": "Improved Sword", "price": 80, "type": "weapon"},
        {"id": 3, "name": "Reinforced Light Armor", "price": 70, "type": "armor"},
        {"id": 4, "name": "Vital Honey", "price": 25, "type": "item"}
    ]
    
    return {"items": vendor_items, "player_credits": game.player.credits}


@app.post("/api/hub/vendor/purchase")
def purchase_item(session_id: str, item_id: int):
    """Purchase an item from vendor."""
    if session_id not in game_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    game = game_sessions[session_id]
    if not game.player:
        raise HTTPException(status_code=404, detail="Character not created")
    
    vendor_items = {
        1: {"name": "Improved Pistol", "price": 80, "type": "weapon", "weapon_name": "Improved Pistol"},
        2: {"name": "Improved Sword", "price": 80, "type": "weapon", "weapon_name": "Improved Sword"},
        3: {"name": "Reinforced Light Armor", "price": 70, "type": "armor", "armor_name": "Reinforced Light Armor"},
        4: {"name": "Vital Honey", "price": 25, "type": "item", "item_name": "Vital Honey"}
    }
    
    if item_id not in vendor_items:
        raise HTTPException(status_code=400, detail="Invalid item_id")
    
    item = vendor_items[item_id]
    
    if game.player.credits < item["price"]:
        raise HTTPException(status_code=400, detail="Not enough credits")
    
    game.player.credits -= item["price"]
    
    if item["type"] == "weapon":
        weapon = next((w for w in game.weapons if w.name == item["weapon_name"]), None)
        if weapon:
            game.player.weapon = weapon
    elif item["type"] == "armor":
        armor = next((a for a in game.armor_list if a.name == item["armor_name"]), None)
        if not armor:
            from models.armor import Armor
            armor = Armor(
                name="Reinforced Light Armor",
                armor_type="light",
                defense_bonus=2,
                damage_reduction=1
            )
        game.player.armor = armor
    elif item["type"] == "item":
        game.player.inventory.append(item["item_name"])
    
    # Auto-save after purchase
    save_game_session(session_id, game)
    
    return {"status": "purchased", "character": character_to_dict(game.player)}


@app.post("/api/hub/rest")
def rest(session_id: str):
    """Rest and recover HP."""
    if session_id not in game_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    game = game_sessions[session_id]
    if not game.player:
        raise HTTPException(status_code=404, detail="Character not created")
    
    game.player.hp = game.player.max_hp
    game.player.status_effects = []
    
    # Auto-save after rest
    save_game_session(session_id, game)
    
    return {"status": "rested", "character": character_to_dict(game.player)}


@app.post("/api/skill/check")
def skill_check(session_id: str, skill_check_data: dict):
    """Execute a skill check."""
    if session_id not in game_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    game = game_sessions[session_id]
    if not game.player:
        raise HTTPException(status_code=404, detail="Character not created")
    
    if not hasattr(game, "current_mission") or not game.current_mission:
        raise HTTPException(status_code=404, detail="No active mission")
    
    attribute = skill_check_data.get("attribute")
    dc = skill_check_data.get("dc")
    
    if not attribute or not dc:
        raise HTTPException(status_code=400, detail="attribute and dc required")
    
    passed, total = game.skill_system.roll_check(game.player, attribute, dc)
    
    return {
        "passed": passed,
        "total": total,
        "dc": dc,
        "attribute": attribute,
        "modifier": game.player.get_attribute_modifier(attribute)
    }


@app.post("/api/skill/complete")
def complete_skill_mission(session_id: str, success: bool):
    """Complete a skill mission and award rewards."""
    if session_id not in game_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    game = game_sessions[session_id]
    if not game.player:
        raise HTTPException(status_code=404, detail="Character not created")
    
    if not hasattr(game, "current_mission") or not game.current_mission:
        raise HTTPException(status_code=404, detail="No active mission")
    
    mission = game.current_mission
    
    if success:
        xp = mission.get("xp_reward", 50)
        leveled_up = game.player.add_xp(xp)
        
        loot = mission.get("loot", {})
        if loot.get("credits"):
            game.player.credits += loot["credits"]
        if loot.get("items"):
            for item in loot["items"]:
                game.player.inventory.append(item)
        
        # Clear mission state
        delattr(game, "current_mission")
        
        # Auto-save after skill mission success
        save_game_session(session_id, game)
        
        return {
            "status": "success",
            "xp_gained": xp,
            "leveled_up": leveled_up,
            "new_level": game.player.level if leveled_up else None,
            "credits_gained": loot.get("credits", 0),
            "items_found": loot.get("items", []),
            "character": character_to_dict(game.player)
        }
    else:
        full_xp = mission.get("xp_reward", 50)
        xp = full_xp // 2
        game.player.add_xp(xp)
        
        # Clear mission state
        delattr(game, "current_mission")
        
        # Auto-save after skill mission failure
        save_game_session(session_id, game)
        
        return {
            "status": "failed",
            "xp_gained": xp,
            "character": character_to_dict(game.player)
        }


# Helper functions
def character_to_dict(char: Character) -> Dict[str, Any]:
    """Convert Character to dict."""
    return {
        "name": char.name,
        "race": char.race.name,
        "class": char.clazz.name,
        "level": char.level,
        "hp": char.hp,
        "max_hp": char.max_hp,
        "xp": char.xp,
        "credits": char.credits,
        "attributes": char.attributes,
        "weapon": char.weapon.name if char.weapon else None,
        "armor": char.armor.name if char.armor else None,
        "inventory": char.inventory,
        "abilities": char.clazz.abilities,
        "status_effects": char.status_effects
    }


def enemy_to_dict(enemy: Enemy) -> Dict[str, Any]:
    """Convert Enemy to dict."""
    return {
        "name": enemy.name,
        "level": enemy.level,
        "hp": enemy.hp,
        "max_hp": enemy.max_hp,
        "attributes": enemy.attributes
    }


def get_combat_state(game: Game) -> Dict[str, Any]:
    """Get current combat state."""
    alive_enemies = [e for e in game.current_enemies if e.is_alive()]
    current_actor = game.combat_system.get_current_actor()
    
    return {
        "player": character_to_dict(game.player),
        "enemies": [enemy_to_dict(e) for e in alive_enemies],
        "round": game.combat_round,
        "is_player_turn": current_actor == game.player,
        "current_actor": current_actor.name if current_actor else None
    }


def handle_combat_end(session_id: str, game: Game, combat_log: List[str], result: str) -> Dict[str, Any]:
    """Handle combat end and return results."""
    if result == "victory":
        mission = game.current_mission
        xp = mission.get("xp_reward", 50)
        leveled_up = game.player.add_xp(xp)
        
        # Loot
        loot = mission.get("loot", {})
        if loot.get("credits"):
            game.player.credits += loot["credits"]
        if loot.get("items"):
            for item in loot["items"]:
                game.player.inventory.append(item)
        
        # Clear combat state
        delattr(game, "current_mission")
        delattr(game, "current_enemies")
        delattr(game, "combat_round")
        
        # Auto-save after victory
        save_game_session(session_id, game)
        
        return {
            "status": "victory",
            "combat_log": combat_log,
            "xp_gained": xp,
            "leveled_up": leveled_up,
            "new_level": game.player.level if leveled_up else None,
            "credits_gained": loot.get("credits", 0),
            "items_found": loot.get("items", []),
            "character": character_to_dict(game.player)
        }
    else:
        # Defeat
        game.player.hp = 1
        if hasattr(game, "current_mission"):
            delattr(game, "current_mission")
        if hasattr(game, "current_enemies"):
            delattr(game, "current_enemies")
        if hasattr(game, "combat_round"):
            delattr(game, "combat_round")
        
        # Auto-save after defeat
        save_game_session(session_id, game)
        
        return {
            "status": "defeat",
            "combat_log": combat_log,
            "character": character_to_dict(game.player)
        }


if __name__ == "__main__":
    import uvicorn
    # Use PORT from environment (for Render/Railway) or default to 8002 for local dev
    port = int(os.getenv("PORT", "8002"))
    uvicorn.run(app, host="0.0.0.0", port=port)

