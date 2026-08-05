import unittest
from engine.game import GameEngine

class TestSnapshot(unittest.TestCase):
    def setUp(self):
        self.engine = GameEngine("src/content")
        self.engine.look()
        
    def test_snapshot_after_movement(self):
        self.engine.process_input("move n")
        snap = self.engine.get_snapshot()
        self.assertEqual(snap["room_name"], "Northern Grove")
        
    def test_snapshot_combat_damage(self):
        self.engine.state.hp = 10
        self.engine.start_encounter("goblin") # Assuming this exists or similar
        self.engine.state.active_encounter = {"id": "goblin", "name": "Goblin", "hp": 5, "max_hp": 5, "tags": []}
        
        snap = self.engine.get_snapshot()
        self.assertEqual(snap["encounter"]["name"], "Goblin")
        self.assertEqual(snap["encounter"]["hp"], 5)
        
        self.engine.state.hp = 5
        snap2 = self.engine.get_snapshot()
        self.assertEqual(snap2["hp"], 5)
        
    def test_snapshot_equipment_inventory(self):
        # taking item
        self.engine.process_input("take rust_key")
        snap = self.engine.get_snapshot()
        self.assertIn("Rusty Key", snap["inventory"])
        
        # equip (cheat item into inv)
        self.engine.state.inventory.append("rust_dagger")
        self.engine.process_input("equip rust_dagger")
        snap2 = self.engine.get_snapshot()
        self.assertEqual(snap2["equipment"]["weapon"], "Rust Dagger")
        
        # drop
        self.engine.process_input("drop rust_key")
        snap3 = self.engine.get_snapshot()
        self.assertNotIn("Rusty Key", snap3["inventory"])
        
    def test_snapshot_status(self):
        self.engine.apply_status("poison")
        snap = self.engine.get_snapshot()
        # The exact string may differ based on capitalization/duration.
        self.assertTrue(any("Poison" in s for s in snap["status"]))
        
        # expire
        self.engine.state.status["poison"] = 1
        self.engine.tick()
        snap2 = self.engine.get_snapshot()
        self.assertFalse(any("Poison" in s for s in snap2["status"]))

    def test_snapshot_save_load(self):
        self.engine.apply_status("chill")
        self.engine.process_input("save")
        self.engine.state.status = {}
        
        self.engine.process_input("load")
        snap = self.engine.get_snapshot()
        self.assertTrue(any("Chill" in s for s in snap["status"]))
        
    def test_snapshot_death(self):
        self.engine.process_input("move e") # east to gate
        self.engine.state.hp = 0
        self.engine.tick() # processes death
        snap = self.engine.get_snapshot()
        self.assertEqual(snap["room_name"], "Sanctum")
        self.assertEqual(snap["hp"], 10)
