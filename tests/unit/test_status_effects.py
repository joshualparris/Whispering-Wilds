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
