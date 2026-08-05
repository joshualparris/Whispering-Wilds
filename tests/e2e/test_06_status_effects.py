import unittest
import pexpect

class TestStatusEffectsE2E(unittest.TestCase):
    def test_status_effects_e2e(self):
        # We spawn manually because CLIHarness hardcodes its room_exits graph which would break with our custom content
        child = pexpect.spawn("python3 src/main.py --seed 42 --content tests/e2e/content_status", env={"PYTHONPATH": "src"}, encoding="utf-8")
        child.expect("Welcome to the Whispering Wilds")
        child.expect("> ")
        
        # move to wilds
        child.sendline("n")
        child.expect("Wilds")
        child.expect("> ")
        
        # hunt to spawn slime
        child.sendline("hunt")
        child.expect("A wild Poison Slime appears!")
        child.expect("> ")
        
        # enemy attacks immediately after hunt since hunt consumes a turn!
        # we don't know who goes first. Let's attack until poisoned.
        poisoned = False
        for _ in range(10):
            child.sendline("attack")
            child.expect("> ")
            if "You have been poisoned!" in child.before:
                poisoned = True
                break
            
        self.assertTrue(poisoned, "Failed to get poisoned within 10 attacks")
        
        # status ticks exactly once per action
        child.sendline("look") # doesn't consume a turn
        child.expect("Wilds")
        child.expect("> ")
        
        # attack again -> consumes turn -> poison ticks
        child.sendline("attack")
        child.expect("Poison courses through your veins \\(-1 HP\\)")
        child.expect("> ")
        
        # stats -> doesn't tick
        child.sendline("stats")
        child.expect("HP:")
        child.expect("> ")
        
        # let's flee until it expires
        expired = False
        for _ in range(5):
            child.sendline("flee")
            child.expect("> ")
            if "The poison runs its course." in child.before:
                expired = True
                break
                
        self.assertTrue(expired, "Poison failed to expire")
        
        child.sendline("quit")
        child.close()
