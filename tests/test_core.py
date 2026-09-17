import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "code.py"
SPEC = importlib.util.spec_from_file_location("whispering_wilds_game", MODULE_PATH)
GAME = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(GAME)


def test_item_inventory_and_equipment_stats():
    player = GAME.Player()
    dagger = GAME.Item(
        "rust_dagger",
        "Rust Dagger",
        "Pitted blade but still sharp.",
        slot="weapon",
        atk=2,
    )

    player.add_item(dagger)
    assert player.inv["rust_dagger"] is dagger

    player.equipment["weapon"] = dagger
    assert player.get_atk() == 2
    assert player.get_def() == 0

    assert player.remove_item("rust_dagger") is dagger
    assert "rust_dagger" not in player.inv


def test_world_room_link_round_trip():
    world = GAME.World()
    sanctum = GAME.Room("sanctum", "Sanctum", "A quiet stone atrium.")
    gate = GAME.Room("gate", "East Gate", "An iron gate bars the way east.")

    sanctum.link("e", "gate")
    gate.link("w", "sanctum")
    world.add_room(sanctum)
    world.add_room(gate)

    assert world.get("sanctum").neighbors["e"] == "gate"
    assert world.get("gate").neighbors["w"] == "sanctum"


def test_game_builds_with_expected_starting_room():
    game = GAME.Game()

    assert game.cur_room == "sanctum"
    assert game.world.start_room == "sanctum"
    assert "gate" in game.world.rooms
    assert "rust_key" in {item.id for item in game.world.get("sanctum").items}
