# Whispering Wilds

A robust, data-driven text adventure game. Originally a simple prototype, the engine has been completely rewritten to support clean data pipelines, determinism, and robust state management.

---

## Quick start

To play the game, set the `PYTHONPATH` to `src` and run `main.py`:

```bash
PYTHONPATH=src python3 src/main.py
```

In game, try:

```text
help
look
take rust_key
move e
use rust_key
move e
map
```

---

## Architecture & Features

The game features a data-driven engine.

* **Content Pipeline:** Rooms, items, quests, and bestiary are defined in JSON inside `src/content/`.
* **State Management:** All player data is tracked explicitly in `GameState` (`src/engine/state.py`), ensuring clean persistence and zero data-loss on restart.
* **Deterministic E2E Testing:** The engine uses a fully deterministic `CLIHarness` with 100% test coverage for quests, economy, and combat mechanics.

### Core Systems
- **Combat:** Genuine random encounters based on the bestiary. `attack` to deal damage, `flee` to escape. Status effects (bleed, poison, chill) impact player health over time.
- **Quests:** Interact with NPCs (`talk caretaker`, `say 1`) to accept and turn in quests.
- **Gathering & Crafting:** `forage`, `mine`, `fish`, `harvest`, and `craft` items to survive the wilderness.
- **Save/Load:** Native JSON saving system. Use `save` to store your session to a file, and `load` to resume.

---

## Core commands

```text
help | look | map | stats | inv
move n/s/e/w  (or: go n/s/e/w)
take <item>   | drop <item>   | use <item>
equip <item>  | unequip <item>
talk <npc>    | say <n>

attack | rest | bandage | flee

forage | mine | fish | harvest | craft <thing>
buy <item> | sell <item>

note <text> | journal | erase <n> | hardmode on/off
save | load

bestiary | lore <creature>
quests

ascend (Watchtower completion)
quit
```

---

## Development & Testing

**Requirements:**
- Python 3.9+
- `pexpect` (for the E2E test suite)

**Running Tests:**

We provide a robust E2E test suite covering gameplay flows.

```bash
PYTHONPATH=src python3 -m unittest discover -s tests/e2e
```
