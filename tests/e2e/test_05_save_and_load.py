import unittest
import os
import json
from tests.e2e.cli_harness import CLIHarness

class TestSaveAndLoad(unittest.TestCase):
    def test_save_and_load_fields(self):
        h = CLIHarness(42, "tests/e2e/transcripts/test_save_load.log")
        
        # We need to change the state significantly.
        # 1. Change room (Gate)
        h.walk_to("Sanctum")
        h.command("take rust_key")
        h.walk_to("East Gate")
        h.clear_combat(h.command("use rust_key")) # Unlock gate
        h.walk_to("Forest Path")
        
        # 2. Get quest
        h.walk_to("Sanctum")
        h.command("talk caretaker")
        h.command("say 6")
        h.command("say 1")
        h.command("say 2")
        # 3. Equip an item
        h.walk_to("Sunken Cellar")
        h.clear_combat(h.command("take torch"))
        h.clear_combat(h.command("take rust_dagger"))
        h.clear_combat(h.command("equip rust_dagger"))
        
        # 4. Save
        o = h.clear_combat(h.command("save"))
        self.assertIn("Game saved", o)
        h.close()
        
        # Load and verify fields
        h2 = CLIHarness(42, "tests/e2e/transcripts/test_save_load_verify.log")
        o = h2.command("load")
        self.assertIn("Game loaded", o)
        
        # Verify Room is Sunken Cellar
        o = h2.command("look")
        self.assertIn("Sunken Cellar", o)
        
        # Verify gate is unlocked (we can walk Path -> Overgrown Verge without key)
        h2.walk_to("Forest Path")
        o = h2.command("e") # Should go to Overgrown Verge
        self.assertIn("Overgrown Verge", o)
        
        # Verify quest is active
        o = h2.command("quests")
        self.assertIn("Heal the Grove - active", o)
        
        # Verify inventory and equipment
        o = h2.command("inv")
        self.assertIn("Rust Dagger", o)
        
        self.assertIn("Old Torch", o)
        
        h2.close()
        
    def test_malformed_save(self):
        h = CLIHarness(42, "tests/e2e/transcripts/test_malformed_save.log")
        
        # Write malformed JSON
        with open("save.json", "w") as f:
            f.write("THIS IS NOT JSON")
            
        o = h.command("load")
        self.assertIn("Failed to load", o)
        
        # Write unsupported version
        with open("save.json", "w") as f:
            json.dump({"save_version": 999, "cur_room": "sanctum"}, f)
            
        o = h.command("load")
        self.assertIn("Failed to load: Unsupported save version.", o)
        
        h.close()
