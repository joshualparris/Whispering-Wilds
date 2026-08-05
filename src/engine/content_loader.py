import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from pathlib import Path

@dataclass
class ItemDef:
    id: str
    name: str
    desc: str
    usable: bool = False
    slot: Optional[str] = None
    atk: int = 0
    df: int = 0
    tags: List[str] = field(default_factory=list)

@dataclass
class StatusEffectDef:
    id: str
    name: str
    type: str
    duration: int
    damage_per_turn: int = 0
    heal_per_turn: int = 0
    stat_mod_atk: int = 0
    message_apply: str = ""
    message_tick: str = ""
    message_expire: str = ""
    immunity_armor: Optional[str] = None


@dataclass
class RoomDef:
    id: str
    name: str
    desc: str
    exits: Dict[str, str] = field(default_factory=dict)
    items: List[str] = field(default_factory=list)
    npcs: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    map_pos: List[int] = field(default_factory=list)

@dataclass
class CreatureDef:
    id: str
    name: str
    hp: List[int]
    lore: str
    tags: List[str] = field(default_factory=list)

@dataclass
class QuestDef:
    id: str
    title: str
    need: Dict[str, int]
    reward: Dict[str, int]
    npc: str
    room: str

class ContentLoader:
    def __init__(self, content_dir: str):
        self.content_dir = Path(content_dir)
        self.rooms: Dict[str, RoomDef] = {}
        self.items: Dict[str, ItemDef] = {}
        self.bestiary: Dict[str, CreatureDef] = {}
        self.quests: Dict[str, QuestDef] = {}
        self.status_effects: Dict[str, StatusEffectDef] = {}
        
    def load_all(self):
        self._load_items()
        self._load_rooms()
        self._load_bestiary()
        self._load_quests()
        self._load_status_effects()
        self.validate_all()
        
    def _load_items(self):
        items_path = self.content_dir / "items.json"
        if not items_path.exists():
            return
        with open(items_path, 'r') as f:
            data = json.load(f)
            for item_data in data:
                if item_data["id"] in self.items:
                    raise ValueError(f"Duplicate item ID: {item_data['id']}")
                self.items[item_data["id"]] = ItemDef(**item_data)
                
    def _load_rooms(self):
        rooms_path = self.content_dir / "rooms.json"
        if not rooms_path.exists():
            return
        with open(rooms_path, 'r') as f:
            data = json.load(f)
            seen_coords = set()
            for room_data in data:
                if room_data["id"] in self.rooms:
                    raise ValueError(f"Duplicate room ID: {room_data['id']}")
                    
                pos = room_data.get("map_pos", [])
                if pos:
                    if len(pos) != 2 or not all(isinstance(x, (int, float)) for x in pos):
                        raise ValueError(f"Room {room_data['id']} has invalid map_pos: {pos}")
                    coord = tuple(pos)
                    if coord in seen_coords:
                        raise ValueError(f"Room {room_data['id']} has duplicate map_pos: {pos}")
                    seen_coords.add(coord)
                    
                self.rooms[room_data["id"]] = RoomDef(**room_data)

    def _load_bestiary(self):
        bestiary_path = self.content_dir / "bestiary.json"
        if not bestiary_path.exists():
            return
        with open(bestiary_path, 'r') as f:
            data = json.load(f)
            # bestiary.json keys are display names, let's derive id or use it as is
            for key, val in data.items():
                c_id = key.lower().replace(" ", "_")
                if c_id in self.bestiary:
                    raise ValueError(f"Duplicate creature ID: {c_id}")
                self.bestiary[c_id] = CreatureDef(
                    id=c_id,
                    name=key,
                    hp=val.get("hp", [1,1]),
                    lore=val.get("lore", ""),
                    tags=val.get("tags", [])
                )

    def _load_quests(self):
        quests_path = self.content_dir / "quests.json"
        if not quests_path.exists():
            return
        with open(quests_path, 'r') as f:
            data = json.load(f)
            for q_id, val in data.items():
                if q_id in self.quests:
                    raise ValueError(f"Duplicate quest ID: {q_id}")
                self.quests[q_id] = QuestDef(
                    id=q_id,
                    title=val.get("title", ""),
                    need=val.get("need", {}),
                    reward=val.get("reward", {}),
                    npc=val.get("npc", ""),
                    room=val.get("room", "")
                )

    def _load_status_effects(self):
        status_path = self.content_dir / "status_effects.json"
        if not status_path.exists():
            return
        with open(status_path, 'r') as f:
            data = json.load(f)
            for eff_id, val in data.items():
                if eff_id in self.status_effects:
                    raise ValueError(f"Duplicate status effect ID: {eff_id}")
                self.status_effects[eff_id] = StatusEffectDef(**val)


    def validate_all(self):
        # 1. Check room exits and items
        for r_id, room in self.rooms.items():
            for d, target in room.exits.items():
                if target not in self.rooms:
                    raise ValueError(f"Room {r_id} has exit {d} to unknown room {target}")
            for item in room.items:
                if item not in self.items:
                    raise ValueError(f"Room {r_id} contains unknown item {item}")
        
        # 2. Check item slots
        valid_slots = {None, "weapon", "armor", "trinket"}
        for i_id, item in self.items.items():
            if item.slot not in valid_slots:
                raise ValueError(f"Item {i_id} has invalid slot {item.slot}")

    def get_room(self, room_id: str) -> Optional[RoomDef]:
        return self.rooms.get(room_id)

    def get_item(self, item_id: str) -> Optional[ItemDef]:
        return self.items.get(item_id)
