import unittest
import json
import os
import tempfile
from engine.content_loader import ContentLoader

class TestMapValidation(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        os.makedirs(os.path.join(self.temp_dir.name, "rooms"))
        self.loader = ContentLoader(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def _write_rooms(self, data):
        with open(os.path.join(self.temp_dir.name, "rooms.json"), "w") as f:
            json.dump(data, f)

    def test_valid_map_pos(self):
        self._write_rooms([
            {"id": "a", "name": "A", "desc": "", "exits": {}, "map_pos": [0, 0]},
            {"id": "b", "name": "B", "desc": "", "exits": {}, "map_pos": [1, 0]}
        ])
        self.loader._load_rooms()
        self.assertEqual(self.loader.rooms["a"].map_pos, [0, 0])

    def test_missing_map_pos(self):
        # E2E content doesn't crash without map_pos
        self._write_rooms([
            {"id": "a", "name": "A", "desc": "", "exits": {}}
        ])
        self.loader._load_rooms()
        self.assertEqual(self.loader.rooms["a"].map_pos, [])

    def test_duplicate_map_pos(self):
        self._write_rooms([
            {"id": "a", "name": "A", "desc": "", "exits": {}, "map_pos": [0, 0]},
            {"id": "b", "name": "B", "desc": "", "exits": {}, "map_pos": [0, 0]}
        ])
        with self.assertRaises(ValueError) as cm:
            self.loader._load_rooms()
        self.assertIn("duplicate map_pos", str(cm.exception))

    def test_invalid_map_pos(self):
        self._write_rooms([
            {"id": "a", "name": "A", "desc": "", "exits": {}, "map_pos": [0]}
        ])
        with self.assertRaises(ValueError) as cm:
            self.loader._load_rooms()
        self.assertIn("invalid map_pos", str(cm.exception))
