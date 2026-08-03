import pexpect
import os
import time
import re

class CLIHarness:
    def __init__(self, seed, transcript_path):
        os.makedirs(os.path.dirname(transcript_path), exist_ok=True)
        self.logfile = open(transcript_path, "w")
        self.child = pexpect.spawn(f"python3 src/main.py --seed {seed}", env={"PYTHONPATH": "src"}, encoding="utf-8")
        self.child.logfile = self.logfile
        self.command_count = 0
        self.expect("Welcome to the Whispering Wilds")
        self.expect("> ")
        
    def expect(self, pattern, timeout=2):
        self.child.expect(pattern, timeout=timeout)
        
    def command(self, cmd, expected=None):
        self.child.sendline(cmd)
        self.command_count += 1
        if expected:
            self.child.expect(expected)
        self.child.expect("> ")
        return self.child.before

    def close(self):
        self.child.sendline("quit")
        self.child.close()
        self.logfile.close()

    room_exits = {
        "Sanctum": {"n":"Northern Grove", "s":"Sunken Cellar", "w":"Ruined Courtyard", "e":"East Gate"},
        "East Gate": {"w":"Sanctum", "e":"Forest Path"},
        "Forest Path": {"w":"East Gate", "e":"Overgrown Verge"},
        "Overgrown Verge": {"w":"Forest Path", "e":"Whispering Wilds", "n":"Old Watchtower"},
        "Whispering Wilds": {"w":"Overgrown Verge", "n":"Moonlit Lake", "e":"Abandoned Mine", "s":"Ranger Camp"},
        "Ranger Camp": {"n":"Whispering Wilds", "e":"Trader's Post"},
        "Trader's Post": {"w":"Ranger Camp"},
        "Moonlit Lake": {"s":"Whispering Wilds"},
        "Abandoned Mine": {"w":"Whispering Wilds"},
        "Old Watchtower": {"s":"Overgrown Verge", "e":"Whispering Wilds", "w":"Hermit's Hut"},
        "Hermit's Hut": {"e":"Old Watchtower"},
        "Northern Grove": {"s":"Sanctum", "e":"Brook Crossing"},
        "Brook Crossing": {"w":"Northern Grove"},
        "Sunken Cellar": {"n":"Sanctum", "e":"Southern Thicket"},
        "Southern Thicket": {"w":"Sunken Cellar"},
        "Ruined Courtyard": {"e":"Sanctum"}
    }

    def get_current_room(self):
        o = self.command("look")
        for r in self.room_exits:
            if r in o: return r
        return None

    def clear_combat(self, last_out):
        o = last_out
        full = last_out
        for _ in range(50): # Bounded loop
            if not ("appears!" in o or "HP:" in o or "glares" in o or "strikes" in o or "failed to flee" in o):
                break
            o = self.command("attack")
            full += "\\n" + o
        return full

    def walk_to(self, target_room_name):
        for _ in range(20): # Bounded loop
            curr = self.get_current_room()
            if not curr:
                self.clear_combat(self.command("look"))
                continue
            if curr == target_room_name:
                break
            
            queue = [(curr, [])]
            visited = set()
            path = []
            for _bfs in range(100): # Bounded BFS
                if not queue: break
                node, p = queue.pop(0)
                if node == target_room_name:
                    path = p
                    break
                if node not in visited:
                    visited.add(node)
                    for direction, neighbor in self.room_exits.get(node, {}).items():
                        queue.append((neighbor, p + [direction]))
            if path:
                o = self.command(path[0])
                self.clear_combat(o)

    def do_action(self, room_name, action, success_text=None, count=1):
        gathered = 0
        full_out = ""
        for _ in range(30): # Bounded loop
            if gathered >= count: break
            self.walk_to(room_name)
            o = self.command(action)
            o = self.clear_combat(o)
            full_out += o
            if success_text:
                if success_text in o:
                    gathered += 1
            else:
                return o
        return full_out
