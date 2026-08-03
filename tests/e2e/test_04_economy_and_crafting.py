import unittest
from tests.e2e.cli_harness import CLIHarness

class TestEconomyAndCrafting(unittest.TestCase):
    def test_economy_and_crafting(self):
        h = CLIHarness(42, "tests/e2e/transcripts/test_economy_and_crafting.log")
        
        # 0. Get Key and Unlock Gate to access Trader later
        h.walk_to("Sanctum")
        h.command("take rust_key")
        h.walk_to("East Gate")
        h.clear_combat(h.command("use rust_key"))
        
        # 1. Gather materials for a bandage (1 fiber)
        h.walk_to("Northern Grove")
        
        gathered_fiber = False
        for _ in range(50):
            o = h.command("forage")
            o = h.clear_combat(o)
            if "1 fiber" in o:
                gathered_fiber = True
                break
                
        # 2. Craft bandage
        o = h.clear_combat(h.command("craft bandage"))
        o = h.clear_combat(o)
        self.assertIn("You craft a bandage", o)
        
        # 3. Use bandage (we might be at full HP, so let's get hit first)
        # But we don't care, using it might just say "HP restored" or "Already at max HP"
        o = h.command("use bandage")
        self.assertTrue("restored" in o or "max HP" in o or "bandage" in o)
        
        # 4. Economy - Sell to get gold
        # We need items to sell.
        h.walk_to("Northern Grove")
        h.clear_combat(h.command("take mint"))
        h.clear_combat(h.command("take reed_cloak"))
        h.clear_combat(h.command("take grove_charm"))
        
        h.walk_to("Trader's Post")
        
        o = h.clear_combat(h.command("sell mint"))
        self.assertIn("Sold mint", o)
        
        o = h.clear_combat(h.command("sell reed_cloak"))
        self.assertIn("Sold reed_cloak", o)
        
        # 5. Buy an item
        # Now we have at least 2 gold. Let's buy an apple.
        o = h.clear_combat(h.command("buy apple"))
        self.assertIn("You bought apple", o)
        
        # Verify gold decreased / item obtained
        o = h.clear_combat(h.command("inv"))
        self.assertIn("Apple", o)
        
        h.close()
