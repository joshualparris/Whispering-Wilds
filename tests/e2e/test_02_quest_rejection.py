import unittest
from tests.e2e.cli_harness import CLIHarness

class TestQuestRejection(unittest.TestCase):
    def test_quest_rejection(self):
        h = CLIHarness(42, "tests/e2e/transcripts/test_quest_rejection.log")
        
        h.walk_to("Sanctum")
        h.command("talk caretaker")
        h.command("say 6")
        h.command("say 1")
        h.command("say 2")
        
        h.command("talk caretaker")
        o = h.command("say 1") # remind
        self.assertIn("2 herb", o)
        h.command("say 4") # bye
        
        h.walk_to("Northern Grove")
        o = h.command("talk caretaker")
        o = h.clear_combat(o)
        self.assertIn("there is no one here", o.lower())
        
        h.close()
