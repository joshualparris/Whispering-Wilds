from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
import json

@dataclass
class GameState:
    save_version: int = 2
    cur_room: str = "sanctum"
    hp: int = 10
    max_hp: int = 10
    
    # Inventory list to allow duplicates. Stores item def IDs.
    inventory: List[str] = field(default_factory=list) 
    
    # equipment slots -> item def id
    equipment: Dict[str, Optional[str]] = field(default_factory=lambda: {
        "weapon": None,
        "armor": None,
        "trinket": None
    })
    
    gold: int = 0
    xp: int = 0
    materials: Dict[str, int] = field(default_factory=dict)
    bandages: int = 1
    
    status: Dict[str, int] = field(default_factory=dict)
    quests: Dict[str, str] = field(default_factory=dict)
    flags: Dict[str, bool] = field(default_factory=dict)
    
    visited_rooms: Set[str] = field(default_factory=set)
    gate_unlocked: bool = False
    
    active_encounter: Optional[dict] = None
    bestiary: Dict[str, bool] = field(default_factory=dict) # id -> discovered
    
    room_items: Dict[str, List[str]] = field(default_factory=dict) # room_id -> list of item def ids left on ground

    game_completed: bool = False
    journal: List[str] = field(default_factory=list)
    hardmode: bool = False
    
    def get_atk(self, loader) -> int:
        total = 0
        for slot in ["weapon", "armor", "trinket"]:
            it_id = self.equipment.get(slot)
            if it_id:
                it = loader.get_item(it_id)
                if it:
                    total += it.atk
        for eff_id in self.status.keys():
            eff = getattr(loader, "status_effects", {}).get(eff_id)
            if eff:
                total += eff.stat_mod_atk
        return total

    def get_def(self, loader) -> int:
        total = 0
        for slot in ["weapon", "armor", "trinket"]:
            it_id = self.equipment.get(slot)
            if it_id:
                it = loader.get_item(it_id)
                if it:
                    total += it.df
        return total

    def to_dict(self):
        d = {
            "save_version": self.save_version,
            "cur_room": self.cur_room,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "inventory": self.inventory,
            "equipment": self.equipment,
            "gold": self.gold,
            "xp": self.xp,
            "materials": self.materials,
            "bandages": self.bandages,
            "status": self.status,
            "quests": self.quests,
            "flags": self.flags,
            "visited_rooms": list(self.visited_rooms),
            "gate_unlocked": self.gate_unlocked,
            "active_encounter": self.active_encounter,
            "bestiary": self.bestiary,
            "room_items": self.room_items,
            "game_completed": self.game_completed,
            "journal": self.journal,
            "hardmode": self.hardmode,
        }
        return d

    @classmethod
    def from_dict(cls, d: dict):
        if d.get("save_version") != 2:
            raise ValueError("Unsupported save version.")
        state = cls()
        state.cur_room = d.get("cur_room", "sanctum")
        state.hp = d.get("hp", 10)
        state.max_hp = d.get("max_hp", 10)
        state.inventory = d.get("inventory", [])
        state.equipment = d.get("equipment", {"weapon": None, "armor": None, "trinket": None})
        state.gold = d.get("gold", 0)
        state.xp = d.get("xp", 0)
        state.materials = d.get("materials", {})
        state.bandages = d.get("bandages", 1)
        state.status = d.get("status", {})
        state.quests = d.get("quests", {})
        state.flags = d.get("flags", {})
        state.visited_rooms = set(d.get("visited_rooms", []))
        state.gate_unlocked = d.get("gate_unlocked", False)
        state.active_encounter = d.get("active_encounter")
        state.bestiary = d.get("bestiary", {})
        state.room_items = d.get("room_items", {})
        state.game_completed = d.get("game_completed", False)
        state.journal = d.get("journal", [])
        state.hardmode = d.get("hardmode", False)
        return state
