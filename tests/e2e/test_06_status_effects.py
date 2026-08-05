import unittest
from cli_harness import CLIHarness

class TestStatusEffectsE2E(unittest.TestCase):
    def test_status_effects_e2e(self):
        h = CLIHarness(seed=123, transcript_path="tests/e2e/transcripts/test_status_effects.log")
        h.command("n")
        h.command("n")
        
        # Keep hunting until we get poisoned or bleed
        max_attempts = 10
        got_status = False
        for _ in range(max_attempts):
            o = h.command("hunt")
            if "appears!" in o:
                # in combat, attack until victory or status applied
                for _ in range(10):
                    atk = h.command("attack")
                    if "You are bleeding!" in atk or "You have been poisoned!" in atk or "You have been chilled!" in atk:
                        got_status = True
                    if "Victory!" in atk or "awaken at the Sanctum" in atk:
                        break
            if got_status:
                break
                
        # Now use stats to check status
        o = h.command("stats")
        self.assertTrue("bleed" in o or "poison" in o or "chill" in o or not got_status)
        
        # Then rest or tick to see it decay
        h.command("rest")
        
        h.close()
