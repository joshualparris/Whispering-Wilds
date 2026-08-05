import unittest
import os
from engine.game import GameEngine

class TestStatusEffectsIntegration(unittest.TestCase):
    def setUp(self):
        # 1. Start with no stale test save
        if os.path.exists("save.json"):
            os.remove("save.json")
            
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        content_dir = os.path.join(base_dir, "tests", "e2e", "content_status")
        
        # Use the same content directory when saving and loading
        self.engine = GameEngine(content_dir=content_dir)
        self.engine.state.hp = 10
        self.engine.state.max_hp = 10

    def tearDown(self):
        if os.path.exists("save.json"):
            os.remove("save.json")

    def test_save_load_persistence_roundtrip(self):
        # 2. Apply a status effect with enough duration remaining
        # (Since we are in an integration test, we can directly apply the status without combat)
        self.engine.apply_status("poison")
        self.engine.state.status["poison"] = 5  # Give it plenty of duration
        
        # 3. Leave combat successfully or use an existing supported non-combat test setup.
        # We are out of combat already!
        
        # 4. Record the exact remaining duration and HP.
        self.assertEqual(self.engine.state.status["poison"], 5)
        self.assertEqual(self.engine.state.hp, 10)
        
        # 5. Save successfully.
        self.engine.process_input("save")
        self.assertTrue(os.path.exists("save.json"))
        
        # 6. Consume one valid turn and show the effect changes.
        # 'rest' consumes a turn and is valid outside combat.
        # Wait, if we 'rest', we might heal 2 HP. Let's use a movement command like 'n' which might fail but still consume a turn, or 'take something'.
        # Let's use 'drop nonexistent_item' - wait, does that consume a turn? 
        # Actually 'move n' will work. We are in sanctum. Sanctum exits 'n' to 'wilds'.
        self.engine.process_input("n")
        self.assertEqual(self.engine.state.status["poison"], 4)
        self.assertEqual(self.engine.state.hp, 9)
        
        # 7. Load the saved state.
        # We instantiate a fresh engine just to be perfectly sure.
        fresh_engine = GameEngine(content_dir=self.engine.loader.content_dir)
        fresh_engine.process_input("load")
        
        # 8. Show that HP, effect and remaining duration return to their saved values.
        self.assertEqual(fresh_engine.state.status["poison"], 5)
        self.assertEqual(fresh_engine.state.hp, 10)
        
        # 9. Consume the next valid turn and confirm the expected tick.
        fresh_engine.process_input("n")
        self.assertEqual(fresh_engine.state.status["poison"], 4)
        self.assertEqual(fresh_engine.state.hp, 9)
