import unittest
from tests.e2e.cli_harness import CLIHarness

class TestEndingGate(unittest.TestCase):
    def test_ending_gate(self):
        h = CLIHarness(42, "tests/e2e/transcripts/test_ending_gate.log")
        
        h.walk_to("Sanctum")
        h.command("take rust_key")
        h.walk_to("East Gate")
        h.clear_combat(h.command("use rust_key"))
        
        o = h.do_action("Old Watchtower", "ascend")
        self.assertIn("magical seal", o)
        
        # Caretaker
        h.walk_to("Sanctum")
        h.command("talk caretaker")
        h.command("say 6")
        h.command("say 1")
        h.command("say 2")
        h.do_action("Northern Grove", "forage", "1 herb", 2)
        h.walk_to("Sanctum")
        h.command("talk caretaker")
        h.command("say 4")
        h.command("say 1")
        
        # Trader
        h.walk_to("Trader's Post")
        h.command("talk trader")
        h.command("say 2")
        h.command("say 1")
        h.command("say 2")
        h.do_action("Moonlit Lake", "fish", "catch a fish", 2)
        h.walk_to("Trader's Post")
        h.command("talk trader")
        h.command("say 3")
        h.command("say 1")
        
        # Ranger
        h.walk_to("Ranger Camp")
        h.command("talk ranger")
        h.command("say 2")
        h.command("say 1")
        h.command("say 2")
        h.do_action("Abandoned Mine", "mine", "mine some ore", 2)
        h.walk_to("Ranger Camp")
        h.command("talk ranger")
        h.command("say 3")
        h.command("say 1")
        
        # Hermit
        h.walk_to("Hermit's Hut")
        h.command("talk hermit")
        h.command("say 2")
        h.command("say 1")
        h.command("say 2")
        h.do_action("Hermit's Hut", "harvest", "harvested a glowcap", 3)
        h.command("talk hermit")
        h.command("say 3")
        h.command("say 1")
        
        o = h.do_action("Old Watchtower", "ascend")
        self.assertIn("GAME COMPLETED", o)
        
        o = h.command("save")
        self.assertIn("Game saved.", o)
        h.close()
        
        h2 = CLIHarness(42, "tests/e2e/transcripts/test_ending_gate_load.log")
        o = h2.clear_combat(h2.command("load"))
        self.assertIn("Game loaded.", o)
        o = h2.do_action("Old Watchtower", "ascend")
        self.assertIn("already restored", o)
        h2.close()
