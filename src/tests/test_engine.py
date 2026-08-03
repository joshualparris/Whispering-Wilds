import unittest
import json
from engine.game import GameEngine

class TestEngine(unittest.TestCase):
    def setUp(self):
        self.game = GameEngine("src/content")
        self.assertTrue(len(self.game.loader.rooms) > 0)

    def test_movement_shorthand_encounter(self):
        self.game.process_input("n")
        self.assertTrue(self.game.state.cur_room != "sanctum" or "You can't go that way." in self.game.output_buffer)
        self.game.state.cur_room = "sanctum"
        self.game.process_input("move north")
        
    def test_failed_movement_does_not_flee(self):
        self.game.state.cur_room = "gate"
        self.game.start_encounter("stone_gnaw")
        self.game.process_input("s")
        self.assertIn("You can't go that way.", self.game.output_buffer)
        self.assertIsNotNone(self.game.state.active_encounter)

    def test_duplicate_items(self):
        self.game.state.inventory.append("apple")
        self.game.state.inventory.append("apple")
        self.assertEqual(self.game.state.inventory.count("apple"), 2)
        self.game.process_input("use apple")
        self.assertEqual(self.game.state.inventory.count("apple"), 1)

    def test_cooked_fish_not_owned(self):
        self.game.process_input("use cooked_fish")
        self.assertIn("You don't have that.", self.game.output_buffer)

    def test_hunting_in_safe_room(self):
        self.game.state.cur_room = "sanctum"
        self.game.process_input("hunt")
        self.assertIn("There is no prey here.", self.game.output_buffer)

    def test_bestiary_undiscovered(self):
        self.assertFalse(self.game.state.bestiary.get("whisper_wolf", False))

    def test_save_load(self):
        self.game.state.inventory = ["apple", "rust_dagger"]
        self.game.state.quests["test_quest"] = "started"
        d = self.game.state.to_dict()
        from engine.state import GameState
        new_state = GameState.from_dict(d)
        self.assertEqual(new_state.inventory, ["apple", "rust_dagger"])
        self.assertEqual(new_state.quests["test_quest"], "started")

    def test_npc_dialogue_location(self):
        self.game.state.cur_room = "sanctum"
        self.game.process_input("talk caretaker")
        self.assertIn("--- Talking to Caretaker ---", self.game.output_buffer)
        
        self.game.state.cur_room = "gate"
        self.game.process_input("talk caretaker")
        self.assertTrue(any("there is no one here to talk to" in line.lower() for line in self.game.output_buffer))

    def test_malformed_save(self):
        from engine.state import GameState
        with self.assertRaises(ValueError):
            GameState.from_dict({"save_version": 999})

    def test_equipment_cycle(self):
        self.game.state.inventory.append("rust_dagger")
        self.assertEqual(self.game.state.get_atk(self.game.loader), 0)
        self.game.process_input("equip rust_dagger")
        self.assertEqual(self.game.state.equipment["weapon"], "rust_dagger")
        self.assertEqual(self.game.state.get_atk(self.game.loader), 1)
        
        self.game.process_input("unequip rust_dagger")
        self.assertIsNone(self.game.state.equipment["weapon"])
        self.assertEqual(self.game.state.get_atk(self.game.loader), 0)
        self.assertIn("rust_dagger", self.game.state.inventory)
        
    def test_combat_resolution(self):
        import unittest.mock
        self.game.start_encounter("stone_gnaw")
        self.game.state.active_encounter["hp"] = 1
        with unittest.mock.patch('random.random', return_value=0.0):
            self.game.process_input("attack")
        
        self.assertIn("The Stone Gnaw dissipates.", self.game.output_buffer)
        self.assertIsNone(self.game.state.active_encounter)
        self.assertEqual(self.game.state.xp, 1)

    def test_combat_death(self):
        import unittest.mock
        self.game.start_encounter("stone_gnaw")
        self.game.state.hp = 1
        self.game.state.active_encounter["hp"] = 100
        with unittest.mock.patch('random.random', return_value=0.1):
            with unittest.mock.patch('random.randint', return_value=2):
                self.game.process_input("attack")
        
        self.assertIn("You collapse and awaken at the Sanctum.", self.game.output_buffer)
        self.assertEqual(self.game.state.cur_room, "sanctum")
        self.assertEqual(self.game.state.hp, self.game.state.max_hp)

    def test_save_load_action(self):
        self.game.state.inventory.append("apple")
        self.game.state.hp = 5
        self.game.state.quests["heal_grove"] = "completed"
        self.game.process_input("save")
        self.game.state.inventory.clear()
        self.game.state.hp = 10
        self.game.state.quests.clear()
        
        self.game.process_input("load")
        self.assertIn("apple", self.game.state.inventory)
        self.assertEqual(self.game.state.hp, 5)
        self.assertEqual(self.game.state.quests.get("heal_grove"), "completed")

if __name__ == '__main__':
    unittest.main()
