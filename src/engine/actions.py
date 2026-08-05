
from engine.action_registry import ActionContext
from engine.content_loader import RoomDef, ItemDef
import json
import random
import os
import tempfile

def move_action(ctx: ActionContext, args: list):
    if not args:
        ctx.game.say("Move where?")
        return
        
    direction = args[0].lower()
    shorthands = {"north": "n", "south": "s", "east": "e", "west": "w"}
    direction = shorthands.get(direction, direction)
    
    if direction not in ["n", "s", "e", "w"]:
        ctx.game.say(f"Use: move north/south/east/west")
        return
        
    room = ctx.game.get_cur_room()
    
    if direction not in room.exits:
        ctx.game.say("You can't go that way.")
        return
        
    next_room_id = room.exits[direction]
    
    # Gate check FIRST, before fleeing! (Bug 9)
    if room.id == "gate" and direction == "e" and not ctx.game.state.gate_unlocked:
        ctx.game.say("The gate is locked. A keyhole awaits a fitting key.")
        return
        
    if ctx.game.state.active_encounter:
        if random.random() < 0.5:
            ctx.game.say("You manage to flee!")
            ctx.game.state.active_encounter = None
        else:
            ctx.game.say("You failed to flee!")
            ctx.consume_turn = True
            return
            
    # Success
    ctx.consume_turn = True
    ctx.game.state.cur_room = next_room_id
    
    # If fled and moved, we shouldn't trigger encounter immediately, handled by safe_zone or tick check
    # But tick will happen AFTER this action anyway. Let's set a flag to prevent immediate spawn.
    ctx.game.state.flags['just_fled'] = True
    
    map_action(ctx, [])
    ctx.game.look()

def flee_action(ctx: ActionContext, args: list):
    if not ctx.game.state.active_encounter:
        ctx.game.say("You are not in combat.")
        return
        
    if random.random() < 0.5:
        ctx.game.say("You manage to flee!")
        ctx.game.state.active_encounter = None
    else:
        ctx.game.say("You failed to flee!")
        ctx.consume_turn = True

def look_action(ctx: ActionContext, args: list):
    if not args:
        ctx.game.look()
        return
        
    target = " ".join(args).lower()
    if target.startswith("at "):
        target = target[3:]
        
    # Check items in room and inventory
    room_items = ctx.game.state.room_items.get(ctx.game.state.cur_room, [])
    inv_items = ctx.game.state.inventory
    
    matches = []
    for i_id in room_items + inv_items:
        it = ctx.game.loader.get_item(i_id)
        if it and target in it.name.lower():
            if it not in matches:
                matches.append(it)
                
    if not matches:
        ctx.game.say(f"You don't see any '{target}' here.")
    elif len(matches) > 1:
        ctx.game.say("Which one? " + ", ".join(m.name for m in matches))
    else:
        ctx.game.say(matches[0].desc)

def take_action(ctx: ActionContext, args: list):
    if not args:
        ctx.game.say("Take what?")
        return
    wanted = " ".join(args).lower()
    
    room_item_ids = ctx.game.state.room_items.get(ctx.game.state.cur_room, [])
    if not room_item_ids and ctx.game.state.cur_room not in ctx.game.state.visited_rooms:
        pass 

    matches = []
    for i, it_id in enumerate(room_item_ids):
        it_def = ctx.game.loader.get_item(it_id)
        if it_def and wanted in it_def.name.lower() or wanted == it_id.lower():
            matches.append((i, it_id, it_def))
            
    if not matches:
        ctx.game.say("No such item here.")
    elif len(matches) > 1:
        # Check exact match
        exact = [m for m in matches if m[2].name.lower() == wanted]
        if len(exact) == 1:
            matches = exact
        else:
            ctx.game.say("Which one? " + ", ".join(set(m[2].name for m in matches)))
            return
            
    if len(matches) == 1:
        target_idx, target_id, target_def = matches[0]
        room_item_ids.pop(target_idx)
        ctx.game.state.inventory.append(target_id)
        ctx.game.say(f"You take the {target_def.name}.")
        ctx.consume_turn = True

def drop_action(ctx: ActionContext, args: list):
    if not args:
        ctx.game.say("Drop what?")
        return
    wanted = " ".join(args).lower()
    
    matches = []
    for i, it_id in enumerate(ctx.game.state.inventory):
        it_def = ctx.game.loader.get_item(it_id)
        if it_def and wanted in it_def.name.lower() or wanted == it_id.lower():
            matches.append((i, it_id, it_def))
            
    if not matches:
        ctx.game.say("You don't have that.")
    elif len(matches) > 1:
        exact = [m for m in matches if m[2].name.lower() == wanted]
        if len(exact) == 1:
            matches = exact
        else:
            ctx.game.say("Which one? " + ", ".join(set(m[2].name for m in matches)))
            return
            
    if len(matches) == 1:
        target_idx, target_id, target_def = matches[0]
        # Unequip if equipped
        for slot, eq_id in ctx.game.state.equipment.items():
            if eq_id == target_id:
                ctx.game.state.equipment[slot] = None
        ctx.game.state.inventory.pop(target_idx)
        ctx.game.state.room_items.setdefault(ctx.game.state.cur_room, []).append(target_id)
        ctx.game.say(f"You drop the {target_def.name}.")
        ctx.consume_turn = True

def inv_action(ctx: ActionContext, args: list):
    if not ctx.game.state.inventory and not any(ctx.game.state.materials.values()):
        ctx.game.say("Inventory: (empty)")
    else:
        # Tally duplicates
        counts = {}
        for i_id in ctx.game.state.inventory:
            name = ctx.game.loader.get_item(i_id).name
            counts[name] = counts.get(name, 0) + 1
        
        item_names = []
        for name, count in counts.items():
            if count > 1:
                item_names.append(f"{name} x{count}")
            else:
                item_names.append(name)
                
        if item_names:
            ctx.game.say("Inventory: " + ", ".join(item_names))
        else:
            ctx.game.say("Inventory: (no items)")
            
        mats = [f"{k} x{v}" for k,v in ctx.game.state.materials.items() if v > 0]
        if mats:
            ctx.game.say("Materials: " + ", ".join(mats))

    def _slot(s):
        it_id = ctx.game.state.equipment.get(s)
        return ctx.game.loader.get_item(it_id).name if it_id else "(empty)"
    ctx.game.say(f"Equipped: weapon={_slot('weapon')}, armor={_slot('armor')}, trinket={_slot('trinket')}")

def stats_action(ctx: ActionContext, args: list):
    st = ctx.game.state
    ctx.game.say(f"HP: {st.hp}/{st.max_hp} | Gold: {st.gold} | XP: {st.xp}")
    ctx.game.say(f"ATK: {st.get_atk(ctx.game.loader)} | DEF: {st.get_def(ctx.game.loader)}")
    if st.status:
        sts = [f"{k}({v})" for k,v in st.status.items()]
        ctx.game.say("Status: " + ", ".join(sts))
    else:
        ctx.game.say("Status: Healthy")

def use_action(ctx: ActionContext, args: list):
    if not args:
        ctx.game.say("Use what?")
        return
    wanted = " ".join(args).lower()
    
    if wanted == "bandage":
        if ctx.game.state.bandages > 0:
            if ctx.game.state.hp < ctx.game.state.max_hp or "bleed" in ctx.game.state.status:
                ctx.game.state.hp = min(ctx.game.state.hp + 3, ctx.game.state.max_hp)
                ctx.game.state.bandages -= 1
                had_bleed = "bleed" in ctx.game.state.status
                ctx.game.state.status.pop("bleed", None)
                msg = "You use a bandage. HP restored."
                if had_bleed: msg += " Bleeding stopped."
                ctx.game.say(msg)
                ctx.consume_turn = True
            else:
                ctx.game.say("You are already at max HP.")
            return
        else:
            ctx.game.say("You have no bandages.")
            return

    matches = []
    for i, it_id in enumerate(ctx.game.state.inventory):
        it_def = ctx.game.loader.get_item(it_id)
        if it_def and wanted in it_def.name.lower() or wanted == it_id.lower():
            matches.append((i, it_id, it_def))
            
    if not matches:
        ctx.game.say("You don't have that.")
        return
        
    target_idx, target_id, target_def = matches[0]
    
    if not target_def.usable:
        ctx.game.say(f"You can't use {target_def.name} like that.")
        return
        
    # Logic for specific items
    if target_id == "rust_key" and ctx.game.state.cur_room == "gate":
        ctx.game.state.gate_unlocked = True
        ctx.game.say("The rusty key turns with a harsh scrape. The gate is unlocked.")
        ctx.consume_turn = True
    elif target_id == "apple":
        ctx.game.state.inventory.pop(target_idx)
        ctx.game.state.hp = min(ctx.game.state.hp + 2, ctx.game.state.max_hp)
        ctx.game.say("You eat the apple. Sweet and crisp.")
        ctx.consume_turn = True
    elif target_id == "cooked_fish":
        ctx.game.state.inventory.pop(target_idx)
        ctx.game.state.hp = min(ctx.game.state.hp + 3, ctx.game.state.max_hp)
        ctx.game.say("You eat the cooked fish. It's hearty.")
        ctx.consume_turn = True
    elif target_id == "glowcap_tonic":
        ctx.game.state.inventory.pop(target_idx)
        ctx.game.state.status.pop("poison", None)
        ctx.game.say("You drink the tonic. Poison neutralized.")
        ctx.consume_turn = True
    else:
        ctx.game.say(f"You use the {target_def.name}. Nothing happens.")
        
def bandage_action(ctx: ActionContext, args: list):
    use_action(ctx, ["bandage"])

def equip_action(ctx: ActionContext, args: list):
    if not args:
        ctx.game.say("Equip what?")
        return
    wanted = " ".join(args).lower()
    
    matches = []
    for i, it_id in enumerate(ctx.game.state.inventory):
        it_def = ctx.game.loader.get_item(it_id)
        if it_def and wanted in it_def.name.lower() or wanted == it_id.lower():
            matches.append((i, it_id, it_def))
            
    if not matches:
        ctx.game.say("You don't have that.")
        return
        
    target_idx, target_id, target_def = matches[0]
    
    if not target_def.slot:
        ctx.game.say(f"{target_def.name} cannot be equipped.")
        return
        
    # unequip current if any
    cur = ctx.game.state.equipment.get(target_def.slot)
    if cur == target_id:
        ctx.game.say(f"You are already wearing {target_def.name}.")
        return
        
    ctx.game.state.equipment[target_def.slot] = target_id
    ctx.game.say(f"You equipped {target_def.name}.")
    ctx.consume_turn = True

def unequip_action(ctx: ActionContext, args: list):
    if not args:
        ctx.game.say("Unequip what?")
        return
    wanted = " ".join(args).lower()
    
    for slot, it_id in ctx.game.state.equipment.items():
        if it_id:
            it_def = ctx.game.loader.get_item(it_id)
            if wanted in it_def.name.lower() or wanted == it_id.lower():
                ctx.game.state.equipment[slot] = None
                ctx.game.say(f"You unequipped {it_def.name}.")
                ctx.consume_turn = True
                return
                
    ctx.game.say("You don't have that equipped.")

def hunt_action(ctx: ActionContext, args: list):
    room = ctx.game.get_cur_room()
    if room.id in ["sanctum", "gate", "wilds_camp", "wilds_hut", "wilds_post"]:
        ctx.game.say("There is no prey here.")
        return
        
    if ctx.game.state.active_encounter:
        ctx.game.say("You are already in combat!")
        return
        
    ctx.game.say("You search the area for prey...")
    # Get random creature from bestiary
    creatures = list(ctx.game.loader.bestiary.keys())
    if creatures:
        enemy_id = random.choice(creatures)
        ctx.game.start_encounter(enemy_id)
    else:
        ctx.game.say("But you find nothing.")
    ctx.consume_turn = True

def attack_action(ctx: ActionContext, args: list):
    if not ctx.game.state.active_encounter:
        ctx.game.say("There is nothing to attack here.")
        return
        
    foe = ctx.game.state.active_encounter
    atk = max(1, ctx.game.state.get_atk(ctx.game.loader))
    dmg = random.randint(1, atk)
    
    foe["hp"] -= dmg
    ctx.game.say(f"You strike the {foe['name']} for {dmg} damage!")
    
    if foe["hp"] <= 0:
        ctx.game.say(f"The {foe['name']} dissipates.")
        ctx.game.state.active_encounter = None
        # Rewards
        xp_gain = 1
        gold_gain = 1
        ctx.game.state.xp += xp_gain
        ctx.game.state.gold += gold_gain
        ctx.game.say(f"Victory! (+{xp_gain} XP, +{gold_gain} gold)")
        
    ctx.consume_turn = True

def rest_action(ctx: ActionContext, args: list):
    if ctx.game.state.active_encounter:
        ctx.game.say("You cannot rest in combat!")
        return
    room = ctx.game.get_cur_room()
    if room.id not in ["sanctum", "wilds_camp", "wilds_hut", "wilds_post"]:
        ctx.game.say("It is not safe to rest here.")
        return
        
    if ctx.game.state.hp < ctx.game.state.max_hp:
        ctx.game.state.hp = min(ctx.game.state.hp + 2, ctx.game.state.max_hp)
        ctx.game.say("You rest and recover some health.")
    else:
        ctx.game.say("You are already fully rested.")
    ctx.consume_turn = True

def save_action(ctx: ActionContext, args: list):
    if ctx.game.state.active_encounter:
        ctx.game.say("You cannot save during combat!")
        return
    import tempfile, shutil
    temp_fd, temp_path = tempfile.mkstemp(dir=os.path.dirname(os.path.abspath(__file__)))
    try:
        with os.fdopen(temp_fd, 'w') as f:
            json.dump(ctx.game.state.to_dict(), f)
        save_path = os.path.join(os.getcwd(), "save.json")
        shutil.move(temp_path, save_path)
        ctx.game.say("Game saved.")
    except Exception as e:
        ctx.game.say(f"Failed to save: {e}")

def load_action(ctx: ActionContext, args: list):
    save_path = os.path.join(os.getcwd(), "save.json")
    if not os.path.exists(save_path):
        ctx.game.say("No save file found.")
        return
        
    try:
        with open(save_path, 'r') as f:
            data = json.load(f)
            
        from engine.state import GameState
        temp_state = GameState.from_dict(data)
        
        # Validate critical state parts
        if temp_state.cur_room not in ctx.game.loader.rooms:
            raise ValueError("Save contains unknown room.")
            
        ctx.game.state = temp_state
        ctx.game.say("Game loaded.")
        ctx.game.look()
    except Exception as e:
        ctx.game.say(f"Failed to load: {e}")

# Gathering
def fish_action(ctx: ActionContext, args: list):
    room = ctx.game.get_cur_room()
    if room.id != "wilds_lake":
        ctx.game.say("You need a lake to fish.")
        return
        
    if random.random() < 0.1:
        ctx.game.state.inventory.append("lost_ring")
        ctx.game.say("You fish up a Lost Ring!")
    elif random.random() < 0.6:
        ctx.game.state.materials['fish'] = ctx.game.state.materials.get('fish', 0) + 1
        ctx.game.say("You catch a fish.")
    else:
        ctx.game.say("The fish aren't biting.")
    ctx.consume_turn = True

def mine_action(ctx: ActionContext, args: list):
    room = ctx.game.get_cur_room()
    if room.id != "wilds_mine":
        ctx.game.say("You need a rock face to mine.")
        return
        
    if random.random() < 0.2:
        ctx.game.state.materials['coal'] = ctx.game.state.materials.get('coal', 0) + 1
        ctx.game.say("You mine a chunk of coal.")
    elif random.random() < 0.6:
        ctx.game.state.materials['ore'] = ctx.game.state.materials.get('ore', 0) + 1
        ctx.game.say("You mine some ore.")
    else:
        ctx.game.say("You find nothing useful.")
    ctx.consume_turn = True

def forage_action(ctx: ActionContext, args: list):
    room = ctx.game.get_cur_room()
    if room.id in ["sanctum", "gate"]:
        ctx.game.say("You can't forage here.")
        return
        
    found = "herb" if random.random() < 0.5 else "fiber"
    if room.id == "thicket_se" and random.random() < 0.3:
        found = "glowcap"
        
    ctx.game.state.materials[found] = ctx.game.state.materials.get(found, 0) + 1
    ctx.game.say(f"You find 1 {found}.")
    ctx.consume_turn = True

def harvest_action(ctx: ActionContext, args: list):
    room = ctx.game.get_cur_room()
    if room.id not in ["wilds_hut", "wilds_mine", "cellar_s", "gate"]:
        ctx.game.say("You harvest nothing.")
        return
    chance = 0.3
    if room.id == "wilds_hut": chance = 0.75
    if random.random() < chance:
        ctx.game.state.materials['glowcap'] = ctx.game.state.materials.get('glowcap', 0) + 1
        ctx.game.say("You harvested a glowcap.")
    else:
        ctx.game.say("You harvest nothing.")
    ctx.consume_turn = True

def craft_action(ctx: ActionContext, args: list):
    if not args:
        ctx.game.say("Craft what?")
        return
    recipe = " ".join(args).lower()
    mats = ctx.game.state.materials
    
    if recipe == "bandage":
        if mats.get("fiber", 0) >= 1:
            mats["fiber"] -= 1
            ctx.game.state.bandages += 1
            ctx.game.say("You craft a bandage.")
            ctx.consume_turn = True
        else:
            ctx.game.say("You need 1 fiber.")
    elif recipe == "cooked_fish":
        if ctx.game.state.cur_room != "wilds_camp":
            ctx.game.say("You need a campfire (Ranger Camp) to cook this.")
            return
        if mats.get("fish", 0) >= 1:
            mats["fish"] -= 1
            ctx.game.state.inventory.append("cooked_fish")
            ctx.game.say("You craft a cooked_fish.")
            ctx.consume_turn = True
        else:
            ctx.game.say("You need 1 fish.")
    elif recipe in ["stove_pin", "stove pin"]:
        if mats.get("ore", 0) >= 1:
            mats["ore"] -= 1
            ctx.game.state.inventory.append("stove_pin")
            ctx.game.say("You craft a stove_pin.")
            ctx.consume_turn = True
        else:
            ctx.game.say("You need 1 ore.")
    elif recipe in ["tonic", "glowcap tonic"]:
        if mats.get("glowcap", 0) >= 1 and mats.get("herb", 0) >= 1:
            mats["glowcap"] -= 1
            mats["herb"] -= 1
            ctx.game.state.inventory.append("glowcap_tonic")
            ctx.game.say("You craft a glowcap_tonic.")
            ctx.consume_turn = True
        else:
            ctx.game.say("You need 1 glowcap and 1 herb.")
    else:
        ctx.game.say("Unknown recipe.")

def map_action(ctx: ActionContext, args: list):
    map_str = ctx.game.get_map_string()
    ctx.game.say(map_str)
    
    room = ctx.game.get_cur_room()
    ctx.game.say(f"You are at: {room.name if room else 'Unknown'}")
    ctx.game.say("Legend: @ you, · visited, ? known (unvisited), blank = off-map")

def journal_action(ctx: ActionContext, args: list):
    if not ctx.game.state.journal:
        ctx.game.say("Journal is empty.")
    else:
        ctx.game.say("Journal:")
        for idx, entry in enumerate(ctx.game.state.journal):
            ctx.game.say(f"{idx+1}. {entry}")

def note_action(ctx: ActionContext, args: list):
    if not args:
        ctx.game.say("Note what?")
        return
    entry = " ".join(args)
    ctx.game.state.journal.append(entry)
    ctx.game.say("Added to journal.")

def erase_action(ctx: ActionContext, args: list):
    if not args:
        ctx.game.say("Erase what? (Provide index)")
        return
    try:
        idx = int(args[0]) - 1
        if 0 <= idx < len(ctx.game.state.journal):
            ctx.game.state.journal.pop(idx)
            ctx.game.say("Journal entry erased.")
        else:
            ctx.game.say("Invalid journal index.")
    except ValueError:
        ctx.game.say("Provide a number.")

def hardmode_action(ctx: ActionContext, args: list):
    if args:
        if args[0].lower() == "on":
            ctx.game.state.hardmode = True
        elif args[0].lower() == "off":
            ctx.game.state.hardmode = False
    else:
        ctx.game.state.hardmode = not ctx.game.state.hardmode
    state_str = "ON" if ctx.game.state.hardmode else "OFF"
    ctx.game.say(f"Hard mode is now {state_str}.")

def bestiary_action(ctx: ActionContext, args: list):
    discovered = [k for k, v in ctx.game.state.bestiary.items() if v]
    if not discovered:
        ctx.game.say("You have not discovered any creatures.")
    else:
        ctx.game.say("Bestiary:")
        for c_id in discovered:
            c = ctx.game.loader.bestiary.get(c_id)
            if c:
                ctx.game.say(f"- {c.name}")

def lore_action(ctx: ActionContext, args: list):
    if not args:
        ctx.game.say("Read lore for what?")
        return
    name = " ".join(args).lower()
    for c_id, c in ctx.game.loader.bestiary.items():
        if name in c.name.lower() or name == c_id:
            if ctx.game.state.bestiary.get(c_id):
                ctx.game.say(f"{c.name}: {c.lore}")
            else:
                ctx.game.say("You haven't discovered that creature yet.")
            return
    ctx.game.say("No such creature found.")

def ascend_action(ctx: ActionContext, args: list):
    room = ctx.game.get_cur_room()
    if room.id != "wilds_tower":
        ctx.game.say("You cannot ascend here.")
        return
        
    if ctx.game.state.active_encounter:
        ctx.game.say("You cannot ascend while fighting!")
        return

    if ctx.game.state.game_completed:
        ctx.game.say("You have already restored the Whispering Wilds. The ending gate is open.")
        return

    completed_quests = sum(1 for status in ctx.game.state.quests.values() if status == "turned_in")
    if completed_quests < 4:
        ctx.game.say("The stairs are blocked by a magical seal. You need to complete more quests to break it.")
        return

    ctx.game.say("GAME COMPLETED! You ascend the Watchtower, gazing out over a healed land.")
    ctx.game.state.game_completed = True

def help_action(ctx: ActionContext, args: list):
    cmds = ["move", "look", "take", "drop", "inv", "stats", "use", "bandage", "equip", "unequip", "hunt", "attack", "flee", "rest", "fish", "mine", "forage", "harvest", "craft", "map", "journal", "note", "erase", "options hardmode", "bestiary", "lore", "talk", "save", "load", "quit"]
    ctx.game.say("Available commands: " + ", ".join(cmds))

from engine.dialogue import handle_talk, handle_say

def talk_action(ctx, args: list):
    room = ctx.game.get_cur_room()
    if not room.npcs:
        ctx.game.say("There is no one here to talk to.")
        return
        
    if not args:
        if len(room.npcs) == 1:
            target = room.npcs[0]
        else:
            ctx.game.say(f"Who do you want to talk to? {', '.join(room.npcs)}")
            return
    else:
        target_in = " ".join(args).lower()
        matches = [npc for npc in room.npcs if target_in == npc.lower()]
        if not matches:
            ctx.game.say(f"There is no one named '{target_in}' here.")
            return
        target = matches[0]

    q_id = None
    if target == "Caretaker": q_id = "heal_grove"
    elif target == "Trader": q_id = "angler_aid"
    elif target == "Ranger": q_id = "mine_matters"
    elif target == "Hermit": q_id = "hermit_glow"
    
    if not q_id:
        ctx.game.say(f"{target} has nothing to say.")
        return
        
    handle_talk(ctx, target, q_id)

def quests_action(ctx: ActionContext, args: list):
    if not ctx.game.state.quests:
        ctx.game.say("No active quests.")
    else:
        for q_id, status in ctx.game.state.quests.items():
            q = ctx.game.loader.quests[q_id]
            ctx.game.say(f"{q.title} - {status}")

def buy_action(ctx: ActionContext, args: list):
    room = ctx.game.get_cur_room()
    if "Trader" not in room.npcs:
        ctx.game.say("No one is selling here.")
        return
    if not args:
        ctx.game.say("Buy what? (e.g. 'buy apple' for 2g, 'buy bandage' for 3g)")
        return
        
    wanted = args[0].lower()
    if wanted == "apple":
        if ctx.game.state.gold >= 2:
            ctx.game.state.gold -= 2
            ctx.game.state.inventory.append("apple")
            ctx.game.say("You bought apple.")
            ctx.consume_turn = True
        else:
            ctx.game.say("Not enough gold.")
    elif wanted == "bandage":
        if ctx.game.state.gold >= 3:
            ctx.game.state.gold -= 3
            ctx.game.state.bandages += 1
            ctx.game.say("You bought bandage.")
            ctx.consume_turn = True
        else:
            ctx.game.say("Not enough gold.")
    else:
        ctx.game.say("The trader doesn't sell that.")

def sell_action(ctx: ActionContext, args: list):
    room = ctx.game.get_cur_room()
    if "Trader" not in room.npcs:
        ctx.game.say("No one is buying here.")
        return
    if not args:
        ctx.game.say("Sell what?")
        return
        
    wanted = " ".join(args).lower()
    prices = {"apple": 1, "mint": 1, "reed_cloak": 2, "grove_charm": 3, "torch": 1, "rust_dagger": 1, "lost_ring": 6}
    
    for i, it_id in enumerate(ctx.game.state.inventory):
        it_def = ctx.game.loader.get_item(it_id)
        if wanted in it_def.name.lower() or wanted == it_id:
            val = prices.get(it_id, 0)
            if val > 0:
                ctx.game.state.inventory.pop(i)
                ctx.game.state.gold += val
                ctx.game.say(f"Sold {it_id} for {val} gold.")
                ctx.consume_turn = True
                return
            else:
                ctx.game.say("The trader doesn't want that.")
                return
                
    ctx.game.say("You don't have that.")

def say_action(ctx, args: list):
    handle_say(ctx, args)

def register_all(registry):
    registry.register("move", move_action, aliases=["n", "s", "e", "w", "north", "south", "east", "west", "go", "walk", "run"])
    registry.register("look", look_action, aliases=["l", "x", "examine"])
    registry.register("take", take_action, aliases=["get", "grab", "pickup"])
    registry.register("drop", drop_action)
    registry.register("inv", inv_action, aliases=["inventory", "i"])
    registry.register("use", use_action, aliases=["eat", "drink", "consume"])
    registry.register("bandage", bandage_action)
    registry.register("equip", equip_action, aliases=["wield", "wear"])
    registry.register("unequip", unequip_action, aliases=["remove"])
    registry.register("hunt", hunt_action)
    registry.register("attack", attack_action, aliases=["hit", "strike", "kill"])
    registry.register("flee", flee_action)
    registry.register("rest", rest_action, aliases=["camp"])
    registry.register("fish", fish_action)
    registry.register("mine", mine_action)
    registry.register("forage", forage_action)
    registry.register("harvest", harvest_action)
    registry.register("craft", craft_action, aliases=["brew", "cook"])
    registry.register("map", map_action)
    registry.register("stats", stats_action, aliases=["status"])
    registry.register("journal", journal_action)
    registry.register("note", note_action)
    registry.register("erase", erase_action)
    registry.register("hardmode", hardmode_action)
    registry.register("bestiary", bestiary_action)
    registry.register("lore", lore_action)
    registry.register("save", save_action)
    registry.register("load", load_action)
    registry.register("talk", talk_action, aliases=["speak"])
    registry.register("say", say_action)
    registry.register("quests", quests_action, aliases=["quest"])
    registry.register("ascend", ascend_action, aliases=["climb"])
    registry.register("buy", buy_action)
    registry.register("sell", sell_action)
    registry.register("help", help_action)

