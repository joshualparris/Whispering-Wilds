import unittest
from tui import GameApp

class TestTUI(unittest.IsolatedAsyncioTestCase):
    async def test_tui_render_and_input(self):
        app = GameApp("src/content")
        async with app.run_test() as pilot:
            # 1. Start without errors
            self.assertTrue(app.is_running)
            
            # 2. Panels render
            self.assertIsNotNone(app.query_one("#narrative-log"))
            self.assertIsNotNone(app.query_one("#map-display"))
            self.assertIsNotNone(app.query_one("#stats-display"))
            self.assertIsNotNone(app.query_one("#inventory-display"))
            self.assertIsNotNone(app.query_one("#cmd-input"))
            
            # 3. Submit look updates narrative
            await pilot.click("#cmd-input")
            await pilot.press("l", "o", "o", "k", "enter")
            log = app.query_one("#narrative-log")
            
            # 4. Unknown command
            await pilot.click("#cmd-input")
            await pilot.press("x", "x", "z", "z", "enter")
            
            # 5. Movement buttons send command
            await pilot.click("#btn-n")
            snap = app.engine.get_snapshot()
            self.assertEqual(snap["room_name"], "Northern Grove")
            
            # 6. Stats/Inv update on state changes
            await pilot.click("#cmd-input")
            await pilot.press("t", "a", "k", "e", "space", "m", "i", "n", "t", "enter")
            inv_widget = app.query_one("#inventory-display")
            self.assertIn("Wild Mint", str(inv_widget.render()))
            
            # 7. Quit closes app
            await pilot.click("#cmd-input")
            await pilot.press("q", "u", "i", "t", "enter")
            
            self.assertFalse(app.is_running)
