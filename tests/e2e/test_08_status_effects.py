import unittest
from tests.e2e.cli_harness import CLIHarness

class TestStatusEffects(unittest.TestCase):
    def test_poison_and_chill(self):
        h = CLIHarness(12345, "tests/e2e/transcripts/test_status_effects.log")
        
        # Go to a dangerous area
        h.walk_to("Sanctum")
        h.command("take rust_key")
        h.walk_to("East Gate")
        h.clear_combat(h.command("use rust_key"))
        h.walk_to("Overgrown Verge")
        
        seen_poison = False
        seen_chill = False
        seen_bleed = False
        
        for _ in range(100):
            if seen_poison and seen_chill and seen_bleed:
                break
            o = h.command("hunt")
            if "appears" in o:
                for _combat in range(20):
                    o = h.command("attack")
                    if "poisoned" in o or "poison" in o:
                        seen_poison = True
                    if "chilled" in o or "chill" in o or "stiffens" in o:
                        seen_chill = True
                    if "bleeding" in o or "bleed" in o:
                        seen_bleed = True
                    if "collapse" in o:
                        break
            if h.get_current_room() == "Sanctum":
                h.walk_to("Overgrown Verge")
                        
        self.assertTrue(seen_poison, "Never received poison")
        self.assertTrue(seen_chill, "Never received chill")
        self.assertTrue(seen_bleed, "Never received bleed")
        
        h.close()
