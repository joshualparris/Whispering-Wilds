from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Static, Input, Button, RichLog

from engine.game import GameEngine

class GameApp(App):
    CSS = """
    Screen {
        layout: vertical;
    }
    #narrative-container {
        height: 1fr;
        border: solid green;
    }
    #middle-container {
        height: 1fr;
        layout: horizontal;
    }
    #map-container {
        width: 1fr;
        border: solid cyan;
    }
    #stats-container {
        width: 1fr;
        layout: vertical;
    }
    #stats-top {
        height: 1fr;
        border: solid yellow;
    }
    #inventory-box {
        height: 1fr;
        border: solid magenta;
    }
    #input-container {
        height: auto;
        border: solid blue;
    }
    #buttons-container {
        height: auto;
        layout: horizontal;
        padding: 1;
    }
    Button {
        margin: 1;
    }
    """

    def __init__(self, content_dir: str = "src/content"):
        super().__init__()
        self.engine = GameEngine(content_dir)
        self.engine.output_callback = self.on_engine_output

    def on_engine_output(self, msg: str):
        log = self.query_one("#narrative-log", RichLog)
        log.write(msg)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(id="narrative-container"):
            yield RichLog(id="narrative-log", markup=True)
            
        with Horizontal(id="middle-container"):
            with Container(id="map-container"):
                yield Static("Map", id="map-display")
            with Vertical(id="stats-container"):
                with Container(id="stats-top"):
                    yield Static("Stats", id="stats-display")
                with Container(id="inventory-box"):
                    yield Static("Inventory", id="inventory-display")
                    
        with Container(id="input-container"):
            yield Input(placeholder="Enter command...", id="cmd-input")
            with Horizontal(id="buttons-container"):
                yield Button("North", id="btn-n")
                yield Button("South", id="btn-s")
                yield Button("East", id="btn-e")
                yield Button("West", id="btn-w")
                yield Button("Look", id="btn-look")
                yield Button("Attack", id="btn-attack")
                yield Button("Inventory", id="btn-inv")

    def on_mount(self):
        self.engine.say("Welcome to the Whispering Wilds.")
        self.engine.look()
        self.update_ui()
        self.query_one("#cmd-input", Input).focus()

    def update_ui(self):
        snap = self.engine.get_snapshot()
        
        # Update map
        map_widget = self.query_one("#map-display", Static)
        map_str = snap.get('map_string', '')
        map_widget.update(f"[b]Map[/b]\n\n{map_str}")
        
        # Update stats
        stats_widget = self.query_one("#stats-display", Static)
        stats_text = f"HP  {snap['hp']}/{snap['max_hp']}\n"
        stats_text += f"ATK {snap['atk']}    DEF {snap['def']}\n"
        stats_text += f"Gold {snap['gold']}   XP {snap['xp']}\n\n"
        
        if snap['status']:
            stats_text += f"Status: {', '.join(snap['status'])}\n"
            
        if snap['encounter']:
            foe = snap['encounter']
            stats_text += f"\n[red]Combat: {foe['name']} (HP: {foe['hp']}/{foe['max_hp']})[/red]"
            
        stats_widget.update(stats_text)
        
        # Update inventory
        inv_widget = self.query_one("#inventory-display", Static)
        inv_text = "[b]Inventory[/b]\n"
        if snap['inventory']:
            for item in snap['inventory']:
                inv_text += f"- {item}\n"
        else:
            inv_text += "(empty)\n"
            
        # Equipment
        eq = snap['equipment']
        inv_text += "\n[b]Equipped[/b]\n"
        
        def format_item(item):
            return item.name if hasattr(item, 'name') else str(item) if item else 'none'
            
        inv_text += f"Weapon: {format_item(eq.get('weapon'))}\n"
        inv_text += f"Armor:  {format_item(eq.get('armor'))}\n"
        inv_text += f"Trinket: {format_item(eq.get('trinket'))}\n"
        
        inv_widget.update(inv_text)

    async def on_input_submitted(self, event: Input.Submitted):
        cmd = event.value
        event.input.value = ""
        self.process_command(cmd)

    def on_button_pressed(self, event: Button.Pressed):
        cmd_map = {
            "btn-n": "n",
            "btn-s": "s",
            "btn-e": "e",
            "btn-w": "w",
            "btn-look": "look",
            "btn-attack": "attack",
            "btn-inv": "inv"
        }
        cmd = cmd_map.get(event.button.id)
        if cmd:
            self.process_command(cmd)

    def process_command(self, cmd: str):
        log = self.query_one("#narrative-log", RichLog)
        log.write(f"\n> [b]{cmd}[/b]")
        
        if cmd.strip().lower() in ("quit", "exit", "q"):
            self.exit()
            return
            
        self.engine.process_input(cmd)
        self.update_ui()

if __name__ == "__main__":
    app = GameApp()
    app.run()
