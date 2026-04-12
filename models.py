"""
Core data models for Whispering Wilds.
Extracted from the monolithic code.py to improve navigability.
"""
from __future__ import annotations
from typing import Dict, List, Optional


class Item:
    def __init__(
        self,
        id: str,
        name: str,
        desc: str,
        usable: bool = False,
        slot: Optional[str] = None,   # "weapon" | "armor" | "trinket" | None
        atk: int = 0,
        df: int = 0,
    ):
        self.id = id
        self.name = name
        self.desc = desc
        self.usable = usable
        self.slot = slot
        self.atk = atk
        self.df = df

    def __repr__(self) -> str:
        return f"Item({self.id})"


class Room:
    def __init__(self, id: str, name: str, desc: str):
        self.id = id
        self.name = name
        self.desc = desc
        self.items: List[Item] = []
        self.neighbors: Dict[str, str] = {}
        self.npcs: List[str] = []
        self.tag: Optional[str] = None
        self.seen: bool = False

    def link(self, direction: str, other_room_id: str) -> None:
        self.neighbors[direction] = other_room_id


class Player:
    def __init__(self):
        self.inv: Dict[str, Item] = {}
        self.hp: int = 10
        self.max_hp: int = 10
        self.equipment: Dict[str, Optional[Item]] = {
            "weapon": None,
            "armor": None,
            "trinket": None,
        }

    def add_item(self, item: Item) -> None:
        self.inv[item.id] = item

    def remove_item(self, item_id: str) -> Optional[Item]:
        return self.inv.pop(item_id, None)

    def get_atk(self) -> int:
        total = 0
        for it in self.equipment.values():
            if it:
                total += getattr(it, "atk", 0)
        return total

    def get_def(self) -> int:
        total = 0
        for it in self.equipment.values():
            if it:
                total += getattr(it, "df", 0)
        return total


class World:
    def __init__(self):
        self.rooms: Dict[str, Room] = {}
        self.start_room: str = ""

    def add_room(self, room: Room) -> None:
        self.rooms[room.id] = room

    def get(self, room_id: str) -> Room:
        return self.rooms[room_id]
