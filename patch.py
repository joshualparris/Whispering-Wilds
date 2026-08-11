import os

# 1. Fix dialogue.py
with open("src/engine/dialogue.py", "r") as f:
    dlg = f.read()

# Fix Caretaker 'Goodbye' duplicate:
dlg = dlg.replace('opts.append(("I will heal the grove. (Accept Quest)", "ct_accept"))\n            opts.append(("Goodbye.", "bye"))', 'opts.append(("I will heal the grove. (Accept Quest)", "ct_accept"))')
dlg = dlg.replace('opts.append(("Here are the herbs. (Turn in Quest)", "ct_turnin"))\n            opts.append(("Goodbye.", "bye"))', 'opts.append(("Here are the herbs. (Turn in Quest)", "ct_turnin"))')

# Improve NPC dialogue
dlg = dlg.replace('if target == "Ranger": ctx.game.say(\'Ranger: "I keep the wilds from entirely consuming the paths."\')', 'if target == "Ranger": ctx.game.say(\'Ranger: "The Wilds encroach on the paths. It takes constant vigilance, and sharp steel, to keep the dark at bay."\')')
dlg = dlg.replace('elif target == "Trader": ctx.game.say(\'Trader: "I deal in what the forest provides, and what it leaves behind."\')', 'elif target == "Trader": ctx.game.say(\'Trader: "I trade in the forgotten and the salvaged. The forest provides, for those brave enough to take."\')')
dlg = dlg.replace('elif target == "Hermit": ctx.game.say(\'Hermit: "The spores sing to me... they whisper secrets."\')', 'elif target == "Hermit": ctx.game.say(\'Hermit: "The spores sing, you know. High and sweet. They tell secrets of the loam and the forgotten dead."\')')

dlg = dlg.replace('ctx.game.say(f\'{target}: "Look around, you will find what I need."\')', 'ctx.game.say(f\'{target}: "The forest hides what it values most. Tread carefully, and look where shadows gather."\')')

with open("src/engine/dialogue.py", "w") as f:
    f.write(dlg)

# 2. Fix actions.py (Bandage and Quests)
with open("src/engine/actions.py", "r") as f:
    acts = f.read()

# Fix bandage
old_bandage = """                ctx.game.state.status.pop("bleed", None)
                ctx.game.say("You use a bandage. HP restored. Bleeding stopped.")
                ctx.consume_turn = True"""
new_bandage = """                had_bleed = "bleed" in ctx.game.state.status
                ctx.game.state.status.pop("bleed", None)
                msg = "You use a bandage. HP restored."
                if had_bleed: msg += " Bleeding stopped."
                ctx.game.say(msg)
                ctx.consume_turn = True"""
acts = acts.replace(old_bandage, new_bandage)

# Fix quests output
old_quests = """def quests_action(ctx: ActionContext, args: list):
    if not ctx.game.state.quests:
        ctx.game.say("You have no active quests.")
        return
    ctx.game.say("Quests:")
    for q_id, state in ctx.game.state.quests.items():
        q = ctx.game.loader.quests.get(q_id)
        if q:
            ctx.game.say(f"{q.title} - {state}")"""
new_quests = """def quests_action(ctx: ActionContext, args: list):
    if not ctx.game.state.quests:
        ctx.game.say("You have no active quests.")
        return
    ctx.game.say("Quests:")
    for q_id, state in ctx.game.state.quests.items():
        q = ctx.game.loader.quests.get(q_id)
        if q:
            pretty_state = state.replace("_", " ").title()
            ctx.game.say(f"{q.title} - {pretty_state}")"""
acts = acts.replace(old_quests, new_quests)

with open("src/engine/actions.py", "w") as f:
    f.write(acts)
