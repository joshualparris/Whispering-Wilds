import unittest
from tests.e2e.cli_harness import CLIHarness

class TestCombatVictory(unittest.TestCase):
    def test_combat_victory(self):
        h = CLIHarness(42, "tests/e2e/transcripts/test_combat_victory.log")
        
        # Equip weapon
        h.walk_to("Sanctum")
        h.command("take rust_key")
        h.walk_to("East Gate")
        h.clear_combat(h.command("use rust_key"))
        h.walk_to("Sunken Cellar")
        h.clear_combat(h.command("take rust_dagger"))
        h.command("equip rust_dagger")
        
        # We need to fight to death (not flee), assert victory text and reward
        h.walk_to("Northern Grove")
        
        won = False
        for _ in range(50):
            if won: break
            o = h.command("hunt")
            if "appears" in o:
                # Flee if it's too strong (e.g. Bog Shade or Camp Raider)
                if "Bog Shade" in o or "Camp Raider" in o or "Stone Gnaw" in o:
                    h.command("flee")
                    continue
                for _combat in range(20):
                    o = h.command("attack")
                    if "dissipates" in o:
                        won = True
                        break
                    if "collapse" in o:
                        break
            if h.get_current_room() == "Sanctum":
                h.walk_to("Northern Grove")
                
        self.assertTrue(won, "Player died before defeating a creature!")
        self.assertIn("+1 XP", o)
        
        h.close()
