"""
Game balance constants for Whispering Wilds.
Edit values here to tune difficulty and pacing without touching game logic.
"""

BALANCE = {
    # --- Combat ---
    "spawn_rate": 0.35,           # chance of encounter per wild-area move
    "player_hit_chance": 0.70,    # base probability player hits a foe
    "evasive_hit_penalty": 0.20,  # subtracted from hit chance vs evasive foes
    "player_dmg_min": 1,          # minimum base player damage per hit
    "player_dmg_max": 3,          # maximum base player damage per hit
    "enemy_hit_chance": 0.50,     # chance the enemy attacks this turn
    "enemy_dmg_min": 1,           # minimum enemy damage
    "enemy_dmg_max": 2,           # maximum enemy damage

    # --- Status effects ---
    "bleed_chance": 0.35,
    "bleed_turns": 3,
    "bleed_dmg": 1,
    "poison_chance": 0.30,
    "poison_turns": 3,
    "poison_dmg": 1,
    "chill_chance": 0.30,
    "chill_turns": 2,
    "chill_dmg": 2,

    # --- Loot ---
    "mat_drop_chance": 0.30,      # chance to drop herb/fiber on creature kill

    # --- Progression ---
    "xp_per_level": 5,            # XP required per level-up
    "hp_per_level": 2,            # max HP gained on each level-up
    "max_level": 10,              # hard cap on player level

    # --- Inventory ---
    "max_carry": 10,              # base item carry limit (does not count gear slots)

    # --- Time ---
    "day_length": 10,             # player-action turns per day/night phase

    # --- Flee ---
    "flee_chance": 0.50,          # base probability of a successful flee attempt

    # --- Boss ---
    "boss_min_kills": 5,          # creature kills required before the Bog Tyrant can appear
}
