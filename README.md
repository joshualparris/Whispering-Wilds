# Whispering-Wilds
Text based adventure
# Whispering Wilds — tiny, extensible text adventure

A single-file Python game you can read, run, and mod in one sitting. Seven “parts” stack on top of each other via a lightweight extension chain.

---

## Quick start

```bash
python3 game.py
```

In game, try:

```
help
look
take key
move e
use rust_key
move e
map
```

---

## What’s in the box

**Part 1 – Core**

* Rooms, items, NPCs, movement
* Inventory, **gear slots** (weapon/armor/trinket), `equip`, `unequip`
* ASCII **map**
* Gate/key mini-lock
* `stats`, `inv`, `talk`

**Part 2 – Wilds & basics**

* Wilds area stub
* `attack`, `rest`, XP, **bandages**

**Part 3 – Forage/Craft/Shop**

* `forage` → fiber/herb
* `craft bandage`
* `buy`, `sell`, gold, simple prices
* (Materials bag lives under `_p3["mats"]`)

**Part 4 – Quality of life**

* `note`, `journal`, `erase`
* `options hardmode on/off`
* **Base64 save/load** (`save`, `load <code>`)

**Part 5 – Encounters & statuses**

* Random encounters in the Wilds
* Bestiary (`bestiary`, `lore <name>`)
* **Status effects** with decay on time-costing actions:

  * **bleed** (−1/turn) → cured by **bandage**
  * **poison** (−1/turn) → cured by **glowcap tonic**
  * **chill** (−2/turn, **Reed Cloak** reduces to −1)

**Part 6 – Dialogue & a quest**

* Caretaker dialogue tree (`talk caretaker`, `say <n>`)
* Quest flow: `accept heal_grove` → collect herbs → `turnin heal_grove`
* `quests` shows progress (with material counters)

**Part 7 – Frontier expansion**

* New places: **Moonlit Lake**, **Abandoned Mine**, **Ranger Camp**, **Hermit’s Hut**, **Trader’s Post**, **Old Watchtower**
* Activities: `fish` (lake), `mine` (mine), `harvest` (glowcaps), `cook` (camp), `camp` (rest)
* NPC snippets: `talk trader|ranger|hermit`
* More creatures & drops
* Extra quests:

  * **Angler’s Aid** (`accept angler_aid`, deliver 2 fish)
  * **Mine Matters** (`accept mine_matters`, deliver 2 ore)
  * **Hermit’s Glow** (`accept hermit_glow`, deliver 3 glowcaps)
  * **Tower Echoes** (`accept tower_riddle`, deliver 1 coal at **Old Watchtower** → `turnin tower_riddle`)

---

## Core commands (player)

```
help | look | map | stats | inv
move n/s/e/w  (or: go n/s/e/w)
take <item>   | drop <item>   | use <item>
equip <item>  | unequip <slot|item>
talk <name>   | say <n>

# Part 2+
attack | rest | bandage

# Part 3+
forage | craft <thing> | buy <item> | sell <item>

# Part 4
note <text> | journal | erase <n> | options hardmode on/off
save | load <code>

# Part 5+
bestiary | lore <creature>

# Part 7+
fish | mine | harvest | cook | camp
accept <quest_key> | turnin <quest_key>
give <item/mat> <npc>
```

**Item tips**

* **Rust Dagger** (+ATK), **Reed Cloak** (+DEF, reduces chill), **Grove Charm** (+ATK/+DEF).
* **glow_tonic** cures poison (see “Crafting” note below).

---

## Crafting & cures

* `craft bandage` (cost: 1 fiber) → adds to Part 2 bandage pool.
* **Glowcap tonic**: brew from glowcaps (see Note below), then `use glow_tonic` to cure poison.
* `cook` at the Ranger Camp turns 1 fish into **Cooked Fish** (`use` heals +4 HP).

**Note on tonic**
If you can’t brew it yet, make sure your `Game.use` handles it and that crafting is wired:

```python
# Game.use(...)
elif target.id in ("glow_tonic", "tonic"):
    p5 = getattr(self, "_p5", None)
    if p5 and "status" in p5:
        p5["status"]["poison"] = 0
    self.say("You drink the glowcap tonic. (Poison cured)")
    self.player.remove_item(target.id)
```

And in Part 3 `craft`, ensure there’s a branch like:

```python
elif what in ("tonic", "glow_tonic"):
    if game._p3["mats"].get("glowcap", 0) >= 1:
        game._p3["mats"]["glowcap"] -= 1
        game.player.add_item(Item("glow_tonic", "Glowcap Tonic", "Cures poison.", usable=True))
        game.say("You brew a glowcap tonic.")
    else:
        game.say("You need 1 glowcap to brew a tonic.")
```

---

## Status ticks (when they apply)

* After **moves**, during **attacks**, and some actions, `_p5_tick_status` runs.
* Death = auto-respawn at **Sanctum** with full HP; encounter cleared.

---

## Map

`map` prints an ASCII grid:

* `@` you
* `·` visited
* `?` known/unvisited

Room coordinates are in `Game._init_positions()`; new rooms can be given `(x,y)` there.

---

## Save/Load

* `save` prints a base64 **SAVE CODE**.
* `load <code>` restores position, HP, inv, and Part 2–4 state.

---

## Files & structure

Everything lives in **one file**, ordered by parts. Each part captures the previous `ext_handle_command` and delegates, forming a chain:

```python
PREV_EXT = globals().get("ext_handle_command", None)

def my_ext_handle_command(cmd, args, game):
    # handle new commands...
    if PREV_EXT and PREV_EXT is not my_ext_handle_command:
        return PREV_EXT(cmd, args, game)
    return False

ext_handle_command = my_ext_handle_command
```

This means you can bolt on new systems without touching earlier parts.

---

## Adding content (short guide)

* **Room**: create `Room(id, name, desc)`, `world.add_room(room)`, and `link()` exits.
* **Item**: `Item(id, name, desc, usable=?, slot=?, atk=?, df=?)`; place into `room.items`.
* **NPC**: add `room.npcs.append("Name")`; respond in `talk`/dialogue handlers.
* **Command**: extend in your part’s `ext_handle_command`.
* **Encounter**: add to Part 5 bestiary (`hp` range, `lore`, optional `tags` like `evasive`, `armored`, `bleed`, `poison`, `chill`).

---

## Quests (keys & where to finish)

* `heal_grove` — Caretaker (Sanctum), needs **2 herb** → `turnin heal_grove` (with Caretaker).
* `angler_aid` — Trader (Trader’s Post), needs **2 fish** → `turnin angler_aid` (or `give fish trader`).
* `mine_matters` — Ranger (Ranger Camp), needs **2 ore** → `give ore ranger`.
* `hermit_glow` — Hermit (Hermit’s Hut), needs **3 glowcap** → `give glowcap hermit`.
* `tower_riddle` — **Old Watchtower**, needs **1 coal** → `turnin tower_riddle` at the tower.

Use `quests` anytime for progress.

---

## Known gotchas / troubleshooting

* **Gate**: unlocking is tracked by `game.gate_unlocked`. `use rust_key` at **East Gate** sets it; then `move e`.
* **Tonic crafting**: if `craft tonic` doesn’t work, add the craft branch shown above (some versions only had bandages).
* **Duplicates in bestiary**: `setdefault` avoids collisions; harmless if you see repeated entries in code.
* **Bandages vs items**: bandages are stored in `_p2["bandages"]`, not inventory.

---

## Requirements

* Python **3.9+**
* No external deps

---

## Tiny smoke test (optional)

```text
look
take key
move e
use rust_key
move e
forage
craft bandage
move e
hunt
attack
bandage
bestiary
quests
talk caretaker
say 5
accept heal_grove
forage
forage
quests
```

---
