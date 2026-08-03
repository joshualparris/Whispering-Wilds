from engine.action_registry import ActionContext

# Simplified conversation tree for Caretaker, Ranger, Trader, Hermit
# We can just hardcode the logic here for simplicity, but it must be robust.

def handle_talk(ctx: ActionContext, target: str, q_id: str):
    q = ctx.game.loader.quests[q_id]
    status = ctx.game.state.quests.get(q_id, "none")
    
    # We will set active dialogue state
    ctx.game.state.flags['dialogue_npc'] = target
    ctx.game.state.flags['dialogue_quest'] = q_id
    
    show_dialogue_menu(ctx, target, q_id, status)

def show_dialogue_menu(ctx: ActionContext, target: str, q_id: str, status: str):
    ctx.game.say(f"--- Talking to {target} ---")
    
    opts = []
    
    if target == "Caretaker":
        if status == "none":
            opts.append(("Who are you?", "ct_intro"))
            opts.append(("What is this place?", "ct_place"))
            opts.append(("Tell me about the Whispering Wilds.", "ct_wilds"))
            opts.append(("What threats lie beyond these walls?", "ct_threats"))
            opts.append(("What can you tell me about the grove?", "ct_grove_lore"))
            opts.append(("Is there any work I can do?", "ct_offer"))
        elif status == "offered":
            opts.append(("I will heal the grove. (Accept Quest)", "ct_accept"))
        elif status == "active":
            opts.append(("Remind me about the remedy.", "ct_remind"))
            opts.append(("Where can I find herbs?", "ct_herb_tips"))
            opts.append(("Tell me more about the grove's illness.", "ct_grove_sick"))
            
            # Check if ready for turnin
            has_items = True
            q = ctx.game.loader.quests[q_id]
            for k, v in q.need.items():
                if ctx.game.state.materials.get(k, 0) < v:
                    has_items = False
            
            if has_items:
                opts.append(("I have the herbs.", "ct_ready_turnin"))
        elif status == "ready_turnin":
            opts.append(("Here are the herbs. (Turn in Quest)", "ct_turnin"))
        elif status == "turned_in":
            opts.append(("How fares the grove now?", "ct_after"))
            opts.append(("Do you have any other tasks?", "ct_more_work"))
            opts.append(("Tell me a story.", "ct_story"))
            
    else:
        # Ranger, Trader, Hermit
        q = ctx.game.loader.quests[q_id]
        if status == "none":
            opts.append(("Who are you?", "npc_intro"))
            opts.append(("Any work?", "npc_offer"))
        elif status == "offered":
            opts.append((f"I will do it. (Accept {q.title})", "npc_accept"))
        elif status == "active":
            opts.append(("What did you need again?", "npc_remind"))
            opts.append(("Any tips?", "npc_tips"))
            
            has_items = True
            for k, v in q.need.items():
                if ctx.game.state.materials.get(k, 0) < v and ctx.game.state.inventory.count(k) < v:
                    has_items = False
                    
            if has_items:
                opts.append(("I have the items.", "npc_ready_turnin"))
        elif status == "ready_turnin":
            opts.append(("Here are the items. (Turn in Quest)", "npc_turnin"))
        elif status == "turned_in":
            opts.append(("How are things?", "npc_after"))
            
    opts.append(("Goodbye.", "bye"))
    
    # Save options to state so say can use them
    ctx.game.state.flags['dialogue_opts'] = [a for _, a in opts]
    
    for i, (text, _) in enumerate(opts):
        ctx.game.say(f"{i+1}. {text}")
    ctx.game.say("Type 'say <number>' to choose.")

def handle_say(ctx: ActionContext, args: list):
    if 'dialogue_npc' not in ctx.game.state.flags:
        ctx.game.say("No one is listening.")
        return
        
    if not args:
        ctx.game.say("Say what number?")
        return
        
    try:
        idx = int(args[0]) - 1
        opts = ctx.game.state.flags.get('dialogue_opts', [])
        if 0 <= idx < len(opts):
            action_id = opts[idx]
            execute_dialogue_action(ctx, action_id)
        else:
            ctx.game.say("Invalid choice.")
    except ValueError:
        ctx.game.say("Provide a number.")

def execute_dialogue_action(ctx: ActionContext, action_id: str):
    target = ctx.game.state.flags['dialogue_npc']
    q_id = ctx.game.state.flags['dialogue_quest']
    q = ctx.game.loader.quests[q_id]
    
    if action_id == "bye":
        ctx.game.say("You end the conversation.")
        ctx.game.state.flags.pop('dialogue_npc', None)
        ctx.game.state.flags.pop('dialogue_quest', None)
        ctx.game.state.flags.pop('dialogue_opts', None)
        return
        
    # Caretaker specific
    if action_id == "ct_intro":
        ctx.game.say('Caretaker: "I am but a watcher of thresholds, bound to the stones of the Sanctum. I sweep the dust of ages, keep the small fires lit, and wait for travelers like you to find their way."')
    elif action_id == "ct_place":
        ctx.game.say('Caretaker: "These halls are called the Sanctum. Built by hands that have long since returned to dust. It is a fragile island of stone amidst an ocean of root and thorn. The Wilds press close to our doors, ever hungry."')
    elif action_id == "ct_wilds":
        ctx.game.say('Caretaker: "A tangle of old paths, twisted trees, and newer fears. Time flows differently out there. Rivers remember the names of the drowned, but the trees... they forget. Tread carefully, for the forest watches."')
    elif action_id == "ct_threats":
        ctx.game.say('Caretaker: "Wolves thin as morning mist, bramble-things with long, cruel memory, and shades that drink warmth from your very breath. The deeper you go, the older the dark."')
    elif action_id == "ct_grove_lore":
        ctx.game.say('Caretaker: "The northern grove was once tended by druids, long gone. Now a creeping blight nibbles its roots. A simple draught of herbs might restore the soil, but the Wilds are reluctant to yield their bounty."')
    elif action_id == "ct_offer":
        ctx.game.say('Caretaker: "The northern grove is sick, its leaves silvering with an unnatural rot. Bring me 2 herbs for a remedy, and I shall reward you."')
        ctx.game.state.quests[q_id] = "offered"
        ctx.game.state.journal.append(f"Caretaker offered a task: {q.title}")
    elif action_id == "ct_accept":
        ctx.game.say('Caretaker: "Thank you. Time is a luxury we no longer possess."')
        ctx.game.state.quests[q_id] = "active"
        ctx.game.say(f"Quest accepted: {q.title}")
    elif action_id == "ct_remind":
        ctx.game.say('Caretaker: "Gather 2 herb. The grove north of here is fading."')
    elif action_id == "ct_herb_tips":
        ctx.game.say('Caretaker: "You’ll find herbs where shade and damp linger—abandoned cellars, ancient tower footings, and beneath mossy stones that haven\'t seen the sun in centuries."')
    elif action_id == "ct_grove_sick":
        ctx.game.say('Caretaker: "Leaves silver at the edges, sap gone thin and black. It is not true death—just a terrible forgetting of how to grow. The remedy will remind the roots of life."')
    elif action_id == "ct_ready_turnin":
        ctx.game.say('Caretaker: "You have them? Good. If you are certain you wish to part with them, give them here."')
        ctx.game.state.quests[q_id] = "ready_turnin"
    elif action_id == "ct_turnin":
        ctx.game.say('Caretaker: "The grove breathes easier. A heavy silence has lifted from the branches. You have my profound thanks, traveler."')
        complete_quest(ctx, q_id)
    elif action_id == "ct_after":
        ctx.game.say('Caretaker: "The grove breathes easier."')
    elif action_id == "ct_more_work":
        ctx.game.say('Caretaker: "Others wandering the Wilds will ask for aid. A stoic ranger needs ore; a weary trader seeks fish; a mad hermit whispers to glowcaps. Seek them out."')
    elif action_id == "ct_story":
        ctx.game.say('Caretaker: "Once, when the moon was swallowed by the sky, a lantern moth led me back to these halls. Its dust remembered my name far better than I did myself. Some lights never truly go out."')
    
    # Generic NPC actions
    elif action_id == "npc_intro":
        if target == "Ranger": ctx.game.say('Ranger: "The Wilds encroach on the paths. It takes constant vigilance, and sharp steel, to keep the dark at bay."')
        elif target == "Trader": ctx.game.say('Trader: "I trade in the forgotten and the salvaged. The forest provides, for those brave enough to take."')
        elif target == "Hermit": ctx.game.say('Hermit: "The spores sing, you know. High and sweet. They tell secrets of the loam and the forgotten dead."')
    elif action_id == "npc_offer":
        need_str = ", ".join(f"{v} {k}" for k, v in q.need.items())
        ctx.game.say(f'{target}: "I need {need_str}."')
        ctx.game.state.quests[q_id] = "offered"
    elif action_id == "npc_accept":
        ctx.game.say(f'{target}: "Good. Hurry back."')
        ctx.game.state.quests[q_id] = "active"
        ctx.game.say(f"Quest accepted: {q.title}")
    elif action_id == "npc_remind":
        need_str = ", ".join(f"{v} {k}" for k, v in q.need.items())
        ctx.game.say(f'{target}: "I still need {need_str}."')
    elif action_id == "npc_tips":
        ctx.game.say(f'{target}: "The forest hides what it values most. Tread carefully, and look where shadows gather."')
    elif action_id == "npc_ready_turnin":
        ctx.game.say(f'{target}: "Ah, you have it! Give it here."')
        ctx.game.state.quests[q_id] = "ready_turnin"
    elif action_id == "npc_turnin":
        ctx.game.say(f'{target}: "Excellent. Here is your reward."')
        complete_quest(ctx, q_id)
    elif action_id == "npc_after":
        ctx.game.say(f'{target}: "Thanks for the help."')
        
    show_dialogue_menu(ctx, target, q_id, ctx.game.state.quests.get(q_id, "none"))

def complete_quest(ctx, q_id):
    q = ctx.game.loader.quests[q_id]
    
    # Remove items/mats
    for k, v in q.need.items():
        if k in ctx.game.state.materials:
            ctx.game.state.materials[k] -= v
        else:
            for _ in range(v):
                if k in ctx.game.state.inventory:
                    ctx.game.state.inventory.remove(k)
                    
    gold = q.reward.get("gold", 0)
    xp = q.reward.get("xp", 0)
    ctx.game.state.gold += gold
    ctx.game.state.xp += xp
    ctx.game.say(f"(+{gold} gold, +{xp} XP)")
    
    ctx.game.state.quests[q_id] = "turned_in"
    ctx.game.state.journal.append(f"Quest completed: {q.title}")
