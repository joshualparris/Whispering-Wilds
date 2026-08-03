
import random
from engine.state import GameState
from engine.content_loader import ContentLoader
from engine.action_registry import ActionRegistry
from engine.actions import register_all

class GameEngine:
    def __init__(self, content_dir: str):
        self.loader = ContentLoader(content_dir)
        self.loader.load_all()
        self.state = GameState()
        self.registry = ActionRegistry()
        register_all(self.registry)
        
        self.output_buffer = []

    def get_cur_room(self):
        return self.loader.get_room(self.state.cur_room)

    def say(self, msg: str):
        self.output_buffer.append(msg)
        print(msg) # CLI output

    def look(self):
        r = self.get_cur_room()
        
        if r.id not in self.state.visited_rooms:
            self.state.visited_rooms.add(r.id)
            self.state.room_items[r.id] = list(r.items)
            
        self.say(f"{r.name}\n{r.desc}")
        
        room_items = self.state.room_items.get(r.id, [])
        if room_items:
            names = [self.loader.get_item(i).name for i in room_items if self.loader.get_item(i)]
            if names:
                self.say("Items here: " + ", ".join(names))
                
        if r.npcs:
            self.say("You see: " + ", ".join(r.npcs))
            
        exits = ", ".join(sorted(r.exits.keys()))
        self.say(f"Exits: {exits if exits else 'none'}")

    def start_encounter(self, enemy_id):
        enemy = self.loader.bestiary.get(enemy_id)
        if not enemy:
            return
            
        hp = random.randint(enemy.hp[0], enemy.hp[1])
        self.state.active_encounter = {"id": enemy_id, "name": enemy.name, "hp": hp, "max_hp": hp, "tags": enemy.tags}
        self.say(f"A wild {enemy.name} appears!")
        self.state.bestiary[enemy_id] = True

    def tick(self):
        # Handle status effects first
        if "bleed" in self.state.status:
            self.say("You bleed (-1 HP).")
            self.state.hp -= 1
        if "poison" in self.state.status:
            self.say("Poison courses through your veins (-1 HP).")
            self.state.hp -= 1
        if "chill" in self.state.status:
            # mitigated by reed cloak
            if self.state.equipment.get("armor") == "reed_cloak":
                pass
            else:
                self.say("You shiver from the chill (-1 HP).")
                self.state.hp -= 1
                
        if self.state.hp <= 0 and not self.state.game_completed:
            self.say("You collapse and awaken at the Sanctum.")
            self.state.hp = self.state.max_hp
            self.state.cur_room = "sanctum"
            self.state.active_encounter = None
            self.state.status = {}
            return

        if self.state.active_encounter:
            foe = self.state.active_encounter
            if random.random() < 0.5:
                df = self.state.get_def(self.loader)
                incoming = random.randint(1, 2)
                if self.state.hardmode: incoming += 1
                
                dmg = max(0, incoming - df)
                if dmg == 0:
                    self.say(f"The {foe['name']}'s blow glances off your gear.")
                else:
                    self.state.hp = max(0, self.state.hp - dmg)
                    self.say(f"The {foe['name']} strikes you (-{dmg} HP).")
                    
                    if "bleed" in foe["tags"] and random.random() < 0.3:
                        self.state.status["bleed"] = 1
                        self.say("You are bleeding!")
                    if "poison" in foe["tags"] and random.random() < 0.3:
                        self.state.status["poison"] = 1
                        self.say("You have been poisoned!")
                    if "chill" in foe["tags"] and random.random() < 0.3:
                        self.state.status["chill"] = 1
                        self.say("You have been chilled!")
                        
                if self.state.hp <= 0:
                    self.say("You collapse and awaken at the Sanctum.")
                    self.state.hp = self.state.max_hp
                    self.state.cur_room = "sanctum"
                    self.state.active_encounter = None
                    self.state.status = {}
            else:
                self.say(f"The {foe['name']} glares at you.")
            return
            
        # Spawn random encounter
        if self.state.flags.get('just_fled'):
            self.state.flags['just_fled'] = False
            return
            
        room = self.get_cur_room()
        safe_zones = ["sanctum", "wilds_camp", "wilds_hut", "wilds_post"]
        if "safe_zone" not in room.tags and room.id not in safe_zones:
            if random.random() < 0.15:
                creatures = list(self.loader.bestiary.keys())
                if creatures:
                    self.start_encounter(random.choice(creatures))

    def process_input(self, text: str) -> bool:
        if text.strip().lower() in ("quit", "exit", "q"):
            return False
            
        self.output_buffer.clear()
        
        parts = text.strip().split()
        if not parts:
            return True
            
        cmd = parts[0].lower()
        if cmd in ("n", "s", "e", "w", "north", "south", "east", "west"):
            text = f"move {cmd}"
            
        if cmd not in self.registry.handlers and cmd not in self.registry.aliases:
            self.say("Unknown command. Try 'help'.")
            return True
            
        self.registry.dispatch(self, text)
        return True
