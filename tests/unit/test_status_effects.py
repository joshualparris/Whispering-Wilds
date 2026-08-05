import unittest
from engine.game import GameEngine
from engine.state import GameState
import os

class TestStatusEffects(unittest.TestCase):
    def setUp(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        content_dir = os.path.join(base_dir, "src", "content")
        self.engine = GameEngine(content_dir=content_dir)
        # reset state
        self.engine.state = GameState()
        self.engine.state.hp = 10
        self.engine.state.max_hp = 10

    def test_apply_and_tick_damage_effect(self):
        # apply bleed
        self.engine.apply_status("bleed")
        self.assertIn("bleed", self.engine.state.status)
        self.assertEqual(self.engine.state.status["bleed"], 3) # duration
        
        # tick
        self.engine.tick()
        self.assertEqual(self.engine.state.hp, 9)
        self.assertEqual(self.engine.state.status["bleed"], 2)
        
        # tick until expire
        self.engine.tick()
        self.engine.tick()
        self.assertNotIn("bleed", self.engine.state.status)

    def test_immunity(self):
        self.engine.state.equipment["armor"] = "reed_cloak"
        self.engine.apply_status("chill")
        self.assertNotIn("chill", self.engine.state.status)

    def test_multiple_simultaneous_effects_and_refresh(self):
        self.engine.apply_status("bleed")
        self.engine.apply_status("poison")
        self.assertEqual(len(self.engine.state.status), 2)
        
        self.engine.tick()
        self.assertEqual(self.engine.state.hp, 8) # takes both damage ticks
        
        self.engine.apply_status("bleed") # refresh
        self.assertEqual(self.engine.state.status["bleed"], 3)
        self.assertEqual(self.engine.state.status["poison"], 4)
        
    def test_zero_health_handling(self):
        self.engine.state.hp = 1
        self.engine.apply_status("bleed")
        self.engine.tick()
        # Takes damage, drops to 0, resets to max hp at sanctum, clears status
        self.assertEqual(self.engine.state.hp, self.engine.state.max_hp)
        self.assertEqual(self.engine.state.cur_room, "sanctum")
        self.assertNotIn("bleed", self.engine.state.status)

    def test_save_load_persistence(self):
        # 1. Applies a status with known remaining duration
        self.engine.apply_status("poison")
        self.engine.tick()
        self.assertEqual(self.engine.state.status["poison"], 4)
        self.assertEqual(self.engine.state.hp, 9)
        
        # 2. Saves the game
        state_dict = self.engine.state.to_dict()
        
        # 3. Loads the game into a fresh engine instance
        fresh_engine = GameEngine(content_dir=self.engine.loader.content_dir)
        fresh_engine.state = GameState.from_dict(state_dict)
        
        # 4. Confirms status, duration, relevant state preserved
        self.assertIn("poison", fresh_engine.state.status)
        self.assertEqual(fresh_engine.state.status["poison"], 4)
        self.assertEqual(fresh_engine.state.hp, 9)
        
        # 5. Confirms next tick behaves exactly as it would have before saving
        fresh_engine.tick()
        self.assertEqual(fresh_engine.state.status["poison"], 3)
        self.assertEqual(fresh_engine.state.hp, 8)
        
    def test_load_older_save_no_status_data(self):
        older_save = {
            "save_version": 2,
            "cur_room": "sanctum",
            "hp": 10,
            "max_hp": 10,
            # no "status" field like an older save might have before the dict change
        }
        state = GameState.from_dict(older_save)
        self.assertEqual(state.status, {})

