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
        
        # save / load shouldn't tick
        child.sendline("save")
        child.expect("Game saved.")
        child.expect("> ")
        
        child.sendline("load")
        child.expect("Game loaded.")
        child.expect("> ")
        
        # wait out the poison
        # duration is 3. We ticked once on the turn we got poisoned, once on second attack. So 1 turn left.
        # let's flee
        child.sendline("flee")
        # might fail or succeed, but either way it consumes a turn
        # wait, if we got poisoned during 'hunt' (before our first attack), then attack 1 ticked it, attack 2 ticked it.
        # it might expire!
        # let's check for expiration
        child.expect("The poison runs its course.")
        
        child.sendline("quit")
        child.close()
