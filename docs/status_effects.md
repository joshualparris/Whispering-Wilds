# Status Effects System

The Whispering Wilds engine features a deterministic, data-driven status effect system. It is responsible for handling damage over time (e.g., bleed, poison), healing over time (e.g., regeneration), and stat modifiers (e.g., weakness) that apply to the player.

## Schema: `status_effects.json`

Status effects are defined in `src/content/status_effects.json`. 

### Supported Fields
* `id` (string): The unique identifier for the effect (e.g., `"bleed"`).
* `name` (string): Human-readable name.
* `type` (string): `"buff"` or `"debuff"`.
* `duration` (int): Number of turns the effect lasts.
* `damage_per_turn` (int, optional): Flat HP damage subtracted from the player each turn. Default `0`.
* `heal_per_turn` (int, optional): Flat HP restored to the player each turn, capped at `max_hp`. Default `0`.
* `stat_mod_atk` (int, optional): Modifier to the player's attack stat while active. Default `0`.
* `message_apply` (string, optional): Message shown when the effect is first applied.
* `message_tick` (string, optional): Message shown each turn when the effect deals damage or heals.
* `message_expire` (string, optional): Message shown when the effect expires naturally.
* `immunity_armor` (string, optional): The ID of an armor item (e.g., `"reed_cloak"`) that provides immunity to this effect.

## Duration and Tick Timing

**What constitutes a turn?**
A turn is consumed by any command that takes in-game time. This includes `move`, `take`, `drop`, `equip`, `unequip`, `hunt`, `attack`, `flee`, `rest`, and gathering/crafting commands (`fish`, `mine`, etc.).
Commands that do NOT consume a turn include `look`, `inv`, `stats`, `map`, `journal`, `save`, and `load`.

**Tick Execution:**
When a turn is consumed, the `GameEngine.tick()` method executes.
1. Status effects are processed FIRST. They deal damage/healing and decrement their duration by 1.
2. If the player reaches 0 HP from a status effect, they immediately collapse and respawn at the Sanctum. Combat is cancelled.
3. If the player survives, enemy combat actions are processed.

This guarantees that effects do not accidentally tick twice during combat, when displaying stats, while saving, or on rejected commands.

## Application and Refresh Rules

* **Application**: Status effects are applied via `GameEngine.apply_status(id)`. 
* **Immunity**: Before application, the engine checks if the player has the `immunity_armor` equipped. If so, the application is ignored.
* **Refresh**: If the player is already afflicted with a status effect and it is applied again, its duration is **refreshed** back to the maximum defined in the JSON. Stacking intensity is not supported.

## How Content Applies Effects

Currently, status effects are natively integrated into the combat encounter system. 
In `bestiary.json`, creatures can define a list of `tags`. If a tag matches a status effect ID (e.g., `"tags": ["poison"]`), that creature has a 30% chance to apply the effect to the player every time it lands a successful attack.

## Save Compatibility

The status effect state is fully persistent and backwards-compatible:
* Active effects and their remaining durations are stored in `save.json` as a dictionary: `"status": {"poison": 4}`.
* Loading an older save format (from before the data-driven update) gracefully parses missing or empty status fields as `{}`, safely defaulting the player to a "Healthy" state.
