import unittest
from tests.e2e.cli_harness import CLIHarness

class TestDeath(unittest.TestCase):
    def test_death_and_respawn(self):
        h = CLIHarness(999, "tests/e2e/transcripts/test_death.log")
        h.walk_to("Sanctum")
        h.command("take rust_key")
        h.walk_to("East Gate")
        h.clear_combat(h.command("use rust_key"))
        h.walk_to("Overgrown Verge")
        
        # Turn hardmode on to take more damage
        h.command("hardmode on")
        
        o = ""
        died = False
        for _ in range(50):
            if died: break
            o = h.command("hunt")
            if "appears" in o:
                for _combat in range(20):
                    o = h.command("attack")
                    if "collapse and awaken at the Sanctum" in o:
                        died = True
                        break
                    if "dissipates" in o:
                        break
        self.assertTrue(died, "Player did not die")
        
        curr = h.get_current_room()
        self.assertEqual(curr, "Sanctum")
        
        # Ending blocked in combat
        h.walk_to("Old Watchtower")
        o = h.command("hunt")
        if "appears" in o:
            o2 = h.command("ascend")
            self.assertIn("You cannot ascend while fighting!", o2)
        h.close()
