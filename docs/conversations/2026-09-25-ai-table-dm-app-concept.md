# AI Table DM App Concept — Conversation Record and Product Brief

Date captured: 2026-09-25
Repository: `joshualparris/Whispering-Wilds`
Reason this repo was chosen: it is already a text-based adventure project, so the AI Table DM / no-human-DM tabletop concept is more relevant here than in a general notes repo.

---

## Original concept from Josh

A group of friends or family are sitting around a table. Everyone wants to play DnD 5e, but no one wants to DM.

The proposed app works on Android, iPhone, and web browsers on Windows or Mac.

The host opens the app and says something like:

> Hey, we want to play DnD. Be our dungeon master.

The app replies with a Jackbox-style session flow:

> Okay, everyone open your phone and go to this link. Type in this generated code for this exact game session.

The session leader/host then chooses:

- character levels from 1 to 20
- campaign setting, story, or homebrew
- session zero content after consulting with the group
- tone and boundaries
- rules strictness

Players then choose race/species, character, class, or press **Choose for me** and the app generates a rules-valid character.

Once everyone is loaded, the group says **Begin**.

Then the AI voice Dungeon Master starts narrating the intro.

The app/website needs:

- settings
- onboarding
- item tracking
- campaign tracking
- character creation
- voice-to-text
- text-to-voice
- strict 5e mechanics
- ability to say no
- modern DM tools
- everything needed for a working AI DM table experience

Josh asked for a complete brief of what it would take to make the project viable, including everything that needs coding and doing.

---

## Core viability note

This project is viable, but only if the AI is **not** treated as the rules engine.

The correct architecture is:

> AI narrator + deterministic rules engine + structured game state + human host override.

The AI should narrate, roleplay, facilitate, remember, pace the session, and explain outcomes.

The code should calculate and enforce:

- dice rolls
- modifiers
- HP
- AC
- initiative
- action economy
- spell slots
- conditions
- inventory
- death saves
- rests
- legal character state

The core principle:

> Let the AI be creative where creativity is safe, and let code be strict where correctness matters.

---

# AI Table DM App — Complete Product and Technical Brief

## 1. Concept Summary

A group of friends or family sits around a table. Everyone wants to play a fifth-edition fantasy tabletop RPG, but no one wants to be the Dungeon Master.

The app becomes the DM.

The host opens the app and says something like:

> We want to play D&D. Be our Dungeon Master.

The app creates a session, gives the host a shareable link and a short room code, then tells everyone else to open the link on their phone, tablet, laptop, or desktop browser. Players join like a Jackbox-style game lobby. The host chooses the basic setup: character level, rules mode, campaign tone, setting type, session zero boundaries, and how strict the AI should be.

Each player creates or imports a character, or presses **Choose For Me** to generate a rules-valid character. Once everyone is ready, the host says **Begin**, and the AI DM starts narrating the adventure through voice and text.

The app tracks characters, inventory, initiative, combat, spell slots, conditions, NPCs, locations, choices, session memory, campaign continuity, rules, dice rolls, session zero agreements, and safety boundaries.

The core product promise:

> A voice-led, rules-aware, multiplayer AI Dungeon Master for groups who want to play now without preparing a DM.

---

## 2. Product Positioning

### What this is

A multiplayer AI tabletop RPG facilitator for in-person and online groups.

It combines:

- Jackbox-style session joining
- AI voice Dungeon Master
- browser-based multiplayer table state
- character builder
- dice roller
- rules engine
- encounter tracker
- campaign memory
- session zero and safety tools
- inventory and progression tracking
- adventure generation
- DM-style narration and NPC roleplay

### What this is not

It should not initially try to be:

- a full 3D virtual tabletop
- a replacement for D&D Beyond
- a replacement for Roll20 or Foundry VTT
- a rules-lawyer chatbot with no game state
- a generic AI story generator
- a product using copyrighted D&D settings, monsters, art, maps, or text without permission
- a fully autonomous DM with no host control

The first viable version should be a **table companion**, not a complete digital world simulator.

---

## 3. Legal and Licensing Requirements

This is one of the highest-risk parts of the project.

The app should initially use only fifth-edition-compatible content that is legally available under the relevant SRD and licence, or fully original content.

Avoid unauthorised use of protected D&D intellectual property such as:

- official campaign settings
- protected monsters outside the SRD
- D&D logos and trade dress
- official art
- official maps
- official adventure text
- proprietary class, subclass, species, background, or spell content not included in the SRD
- D&D Beyond account data unless there is a proper official integration or user-authorised import path

Product naming should avoid implying official Wizards of the Coast endorsement.

Unsafe examples:

- D&D AI Dungeon Master
- D&D Beyond AI DM
- Official 5e AI DM

Safer examples:

- TableLore
- QuestHost
- FableTable
- FifthForge
- PartyQuest AI
- Narrator’s Table
- The Living DM

Marketing should use wording like:

> A fifth-edition-compatible fantasy tabletop RPG assistant.

Not:

> An official Dungeons & Dragons DM replacement.

Before public launch, get legal review for:

- product name
- marketing claims
- SRD attribution
- paid subscription model
- character builder content
- AI-generated content using SRD terms
- user-generated homebrew content
- content moderation and safety
- storage of player voice recordings/transcripts
- copyright ownership of generated adventures

---

## 4. Core User Experience

### Host flow

1. Host opens mobile app or browser app.
2. Host chooses **Start New Game**.
3. App asks whether this is:
   - one-shot
   - ongoing campaign
   - continue saved campaign
   - tutorial game
   - kids/family game
   - strict rules game
   - light cinematic game
4. App creates a game session.
5. Host receives:
   - session link
   - short room code
   - QR code
6. Host shares link/code with players.
7. Players join on their own devices.
8. Host configures session:
   - rules version
   - level range
   - party size
   - tone
   - difficulty
   - safety boundaries
   - session length
   - combat frequency
   - roleplay/combat/exploration balance
   - setting style
   - homebrew allowed or not
9. Host reviews lobby.
10. Host presses or says **Begin**.

### Player flow

1. Player opens link.
2. Player enters room code if needed.
3. Player chooses display name.
4. Player creates a character, imports a saved app character, or chooses **Generate For Me**.
5. Player confirms:
   - name
   - species/race
   - class
   - background
   - level
   - ability scores
   - equipment
   - spells
   - personality hooks
6. Player joins table lobby.
7. During play, player can:
   - speak actions aloud
   - type actions
   - roll dice physically and enter result, or roll digitally
   - view character sheet
   - track hit points
   - track spell slots
   - view inventory
   - see current scene summary
   - see party notes
   - whisper private notes to AI DM if enabled

### AI DM flow

The AI DM should:

1. Greet the table.
2. Confirm group expectations.
3. Summarise session zero boundaries.
4. Introduce the setting.
5. Ask players to introduce characters.
6. Present the opening scene.
7. Ask, “What do you do?”
8. Interpret player actions.
9. Request rolls when needed.
10. Apply rules through the rules engine.
11. Narrate outcomes.
12. Track world state.
13. Ask clarifying questions when player intent is unclear.
14. Say no when an action is impossible, unsafe, against boundaries, or rules-invalid.
15. Offer alternatives when appropriate.

---

## 5. Essential Design Principle: The AI Can Say No

A good DM does not simply allow anything. The app must be able to say no kindly, firmly, and consistently.

The AI DM should refuse or redirect when:

- a player tries to break agreed safety boundaries
- a player tries to control another player’s character without permission
- a player attempts impossible actions
- a player asks for rules benefits they do not have
- a player tries to gain items, spells, or levels without justification
- a player repeatedly derails the group
- an action would violate the agreed tone of the game
- a player asks for harmful, hateful, sexual, or abusive content
- a player tries to bypass dice rolls where uncertainty matters

Example:

> No, you can’t simply declare that the dragon dies. You can attempt to attack it, frighten it, bargain with it, distract it, or flee. Which approach are you taking?

This is essential for making the app feel like a DM rather than a wish-fulfilment chatbot.

---

## 6. Rules Philosophy

### Three rules modes

#### Strict Mode

- Uses deterministic rules engine wherever possible
- Requires action economy in combat
- Tracks spell slots, ammunition, HP, death saves, concentration, conditions, rests, inventory, encumbrance if enabled
- AI cannot invent mechanical benefits outside the rules
- Homebrew disabled unless explicitly added

#### Guided Mode

- Uses core rules but allows light cinematic rulings
- AI can suggest advantage/disadvantage based on scene context
- Host can approve exceptions
- Better for casual family play

#### Story Mode

- Rules-light
- Fewer rolls
- AI focuses on story and character moments
- Good for children, first-time players, or one-shots

Default should be **Guided Mode**.

Strict Mode should exist, but the product must be very careful before claiming perfect strict 5e publicly. Strict mode is hard and full of edge cases.

### Rules engine must be separate from AI

The app needs dedicated rule modules for:

- character creation
- ability checks
- saving throws
- attack rolls
- damage rolls
- initiative
- movement
- conditions
- spellcasting
- concentration
- advantage/disadvantage
- resting
- hit dice
- death saves
- inventory
- equipment
- armour class
- proficiency bonus
- skill proficiencies
- spell save DC
- spell attack modifiers
- challenge rating and encounter difficulty

The AI should call tools/functions such as:

- `request_roll()`
- `resolve_attack()`
- `apply_damage()`
- `start_encounter()`
- `advance_initiative()`
- `cast_spell()`
- `consume_resource()`
- `add_inventory_item()`
- `update_location_state()`
- `summarise_session()`

The AI should not directly mutate game state without validation.

---

## 7. Product Modules

### 7.1 Session Lobby Module

Purpose: let everyone join a shared game quickly.

Features:

- host creates game session
- short session code
- shareable link
- QR code
- player join/leave tracking
- ready status
- host controls
- reconnect support
- device detection
- cross-platform browser support
- spectator mode optional
- private player view
- shared table view

Coding required:

- session creation API
- unique code generator
- lobby database records
- WebSocket or real-time channel
- join session route
- player identity/session token
- host permissions
- reconnect handling
- presence tracking
- ready-state logic

Suggested data model:

```ts
type GameSession = {
  id: string;
  code: string;
  hostUserId: string;
  status: 'lobby' | 'session_zero' | 'active' | 'paused' | 'completed';
  rulesMode: 'strict' | 'guided' | 'story';
  createdAt: string;
  updatedAt: string;
};

type SessionParticipant = {
  id: string;
  sessionId: string;
  userId?: string;
  displayName: string;
  role: 'host' | 'player' | 'spectator';
  characterId?: string;
  ready: boolean;
  connected: boolean;
};
```

### 7.2 Session Setup Module

Purpose: help the group configure the game before play begins.

Features:

- level selection 1–20
- one-shot or campaign
- campaign tone
- difficulty
- content boundaries
- player consent tools
- rules mode
- homebrew permissions
- voice settings
- dice settings
- adventure length
- combat frequency
- exploration frequency
- puzzle frequency
- romance allowed or not
- PvP allowed or not
- character death mode
- safety pause word

Suggested presets:

- family-friendly heroic fantasy
- classic dungeon crawl
- mystery investigation
- wilderness survival
- political intrigue
- high-combat tactical mode
- rules-light first-timers
- strict RAW table

### 7.3 Session Zero Module

Purpose: get everyone aligned before the AI starts the adventure.

Features:

- lines and veils
- PvP settings
- romance boundaries
- horror intensity
- gore intensity
- child safety boundaries
- player agency rules
- table etiquette
- turn-taking expectations
- device use expectations
- session length and break timing
- safety word or pause button
- tone agreement summary
- player comfort check

The AI must treat session zero boundaries as higher priority than story continuity.

### 7.4 Character Builder Module

Purpose: let players quickly create legal characters.

Features:

- choose species/race
- choose class
- choose background
- choose level
- ability score method
- proficiencies
- starting equipment
- spell choices
- personality traits
- character portrait optional
- auto-generate name
- auto-generate backstory
- Choose For Me random character
- export character summary
- save character for future games

MVP shortcut: start with pre-generated archetypes and a limited SRD character builder before attempting full level 1–20 creation.

### 7.5 Character Sheet Module

Purpose: give each player a simple, live, mobile-friendly sheet.

Features:

- HP tracker
- AC
- initiative
- ability scores
- saving throws
- skills
- attacks
- spells
- spell slots
- features
- inventory
- conditions
- notes
- rest buttons
- roll buttons
- concentration tracker
- death saves

In strict mode, players should not be able to secretly edit HP, spell slots, magic items, or gold without host approval or log visibility.

### 7.6 Dice Engine Module

Purpose: make dice rolling transparent, trusted, and fun.

Features:

- digital dice roller
- manual physical dice entry
- public rolls
- private rolls
- DM secret rolls
- advantage/disadvantage
- roll history
- roll reason attached to every roll
- modifier breakdown
- critical hit/fumble detection
- reroll mechanics where supported

Suggested data model:

```ts
type DiceRoll = {
  id: string;
  sessionId: string;
  characterId?: string;
  rollerType: 'player' | 'ai_dm' | 'system';
  formula: string;
  result: number;
  breakdown: DiceBreakdown;
  reason: string;
  visibility: 'public' | 'private' | 'dm_only';
  createdAt: string;
};
```

### 7.7 Rules Engine Module

Purpose: resolve mechanics correctly.

This is the backbone of the product.

Submodules needed:

#### Character rules

- ability modifiers
- proficiency bonus
- skill bonuses
- saving throws
- passive perception
- AC calculation
- HP calculation
- spell save DC
- spell attack bonus

#### Combat rules

- initiative
- turn order
- movement
- actions
- bonus actions
- reactions
- opportunity attacks
- dodge
- dash
- disengage
- help
- hide
- ready
- grapple/shove if supported
- cover
- attack rolls
- damage rolls
- resistance/vulnerability/immunity
- critical hits
- death saves

#### Spellcasting rules

- spell slots
- prepared/known spells
- components if enabled
- concentration
- range
- duration
- saving throws
- spell attacks
- area effects
- upcasting
- ritual casting if supported

#### Resting rules

- short rest
- long rest
- hit dice
- resource recovery
- exhaustion if implemented

#### Inventory rules

- equipment
- weapons
- armour
- ammunition
- gold
- carrying capacity if enabled
- magic items if implemented

This module should be developed like accounting software: boring, tested, explicit, and reliable.

### 7.8 AI DM Orchestration Module

Purpose: convert player intent and game state into a coherent session.

The AI DM needs several internal roles:

- narrator
- rules interpreter
- world keeper
- encounter director
- safety moderator
- table facilitator

Coding required:

- AI prompt templates
- system prompts per rules mode
- context assembly logic
- tool/function calling
- state validation
- memory retrieval
- scene summaries
- NPC voice/personality management
- error recovery
- hallucination guardrails
- refusal/redirect patterns
- host override handling

AI should receive structured state, not a giant unstructured chat history.

Example context packet:

```ts
type AiDmContext = {
  session: GameSession;
  currentScene: SceneState;
  party: CharacterSummary[];
  activeEncounter?: EncounterState;
  knownWorldFacts: WorldFact[];
  sessionZero: SafetyAndToneAgreement;
  recentEvents: TimelineEvent[];
  unresolvedHooks: Hook[];
  rulesMode: RulesMode;
};
```

### 7.9 Voice Input Module

Purpose: let players speak naturally at the table.

Features:

- push-to-talk per player
- host-controlled open mic mode optional
- speaker identification
- transcription
- action intent extraction
- confirmation for ambiguous actions
- noise handling
- family table support with background noise
- mute controls
- text fallback

Always support text input. Voice will fail sometimes.

### 7.10 Voice Output Module

Purpose: make the DM feel present.

Features:

- AI DM voice narration
- adjustable voice style
- speed control
- skip/interrupt narration
- text transcript shown alongside audio
- different NPC voices optional
- host mute button
- accessibility captions
- replay last narration

MVP approach: start with one good narrator voice and subtitles. Add NPC voices later.

### 7.11 Campaign Memory Module

Purpose: keep continuity across sessions.

Features:

- session summaries
- character arcs
- NPC memory
- world facts
- places visited
- promises made
- quests accepted
- unresolved mysteries
- faction relationships
- items gained/lost
- deaths and consequences
- player preferences

Important distinction:

- proposed fiction
- confirmed fiction
- mechanical state
- session summary
- canonical campaign facts

### 7.12 Adventure Generator Module

Purpose: create playable adventures from host/group preferences.

Features:

- one-shot generator
- campaign arc generator
- scene-by-scene outline
- NPC generator
- location generator
- encounter generator
- treasure generator
- mystery/clue tracker
- faction generator
- villain generator
- hooks per character

Suggested adventure schema:

```ts
type Adventure = {
  id: string;
  title: string;
  premise: string;
  tone: string;
  levelRange: [number, number];
  scenes: AdventureScene[];
  npcs: Npc[];
  locations: Location[];
  encounters: EncounterTemplate[];
  secrets: Secret[];
  treasure: TreasureEntry[];
  safetyNotes: string[];
};
```

### 7.13 Encounter Manager Module

Purpose: run combat and structured challenges.

Features:

- start encounter
- add PCs
- add monsters/NPCs
- roll initiative
- track turns
- track HP
- track conditions
- track concentration
- resolve attacks
- resolve saves
- resolve damage
- monster tactics
- end encounter
- award loot/XP/milestone progress

MVP shortcut: theatre-of-the-mind combat and simple position tags rather than grid-based tactical combat.

Position tags:

- engaged
- near
- far
- hidden
- behind cover
- flying
- prone
- restrained

### 7.14 Map and Table View Module

Purpose: give the group a shared visual reference without trying to replace full VTTs immediately.

MVP features:

- shared scene image or abstract map
- party location marker
- NPC/monster tokens optional
- scene notes
- current objective
- initiative display
- party status

Later features:

- grid maps
- fog of war
- token movement
- range measurement
- line of sight
- asset library
- map drawing
- AI-generated scene images

Do not build a full VTT in the first version. Start with a shared table dashboard.

### 7.15 Inventory and Item Tracking Module

Purpose: prevent campaign drift and arguments.

Features:

- player inventory
- party inventory
- gold tracking
- consumables
- ammunition
- magic items
- attunement if implemented
- loot distribution
- item history
- trade/give item flow
- host approval for major changes

### 7.16 Notes and Recap Module

Purpose: keep the group oriented.

Features:

- session recap
- current quest list
- known NPCs
- known locations
- party goals
- character-specific notes
- host notes
- AI-generated summary after session
- Previously On narration

### 7.17 Host Control Module

Purpose: keep a human in final control.

Features:

- pause game
- resume game
- skip scene
- rewind scene
- correct AI
- override ruling
- adjust difficulty
- mute voice
- move spotlight to quiet player
- end session
- save campaign
- approve homebrew
- approve character changes
- approve loot

Even if no one wants to DM, one person should still be the session leader. That person does not need to prepare or narrate, but they should have control over the app.

### 7.18 Safety and Moderation Module

Purpose: make the app safe for mixed groups, families, schools, public games, and online sessions.

Features:

- session zero boundaries
- pause button
- rewind/redo
- skip content
- player discomfort check
- age/tone presets
- content moderation
- no sexual content involving minors
- no graphic child harm
- no hateful content
- PvP consent enforcement
- private report to host
- AI refusal patterns

### 7.19 Account and Identity Module

Purpose: let users save campaigns and characters.

Features:

- guest play
- account creation
- login
- saved characters
- saved campaigns
- subscription status if paid
- parental controls if needed
- privacy settings

Recommendation: allow guest play for first sessions. Do not force account creation before the group can try the app.

### 7.20 Billing Module

Potential pricing models:

- free tier with limits
- host subscription
- group subscription
- credit model for voice/AI usage

Recommendation: host subscription plus fair usage limits. Voice AI can become expensive.

---

## 8. Technical Architecture

### Recommended stack

Frontend:

- Next.js or Remix for web app
- React Native / Expo for mobile app if native app required
- PWA first approach for fastest cross-platform launch
- Tailwind or similar design system
- WebSockets for real-time state

Backend:

- Node.js / TypeScript backend
- PostgreSQL for relational game state
- Redis for session presence and real-time ephemeral state
- vector database or Postgres vector extension for campaign memory
- object storage for audio, images, exports
- serverless functions or container backend depending on voice streaming needs

Real-time layer options:

- WebSockets
- Supabase Realtime
- Liveblocks
- Socket.IO
- PartyKit
- Ably/Pusher

AI layer:

- provider-agnostic LLM gateway
- tool/function calling
- rules engine tools
- content safety classifier
- prompt versioning
- context budgeting
- memory retrieval
- output validation

Voice layer:

- speech-to-text provider
- text-to-speech provider
- audio streaming
- browser microphone handling
- captions/transcripts
- push-to-talk

Database:

- PostgreSQL
- tables for users, sessions, characters, campaigns, encounters, dice rolls, inventory, world facts, notes, events, billing, and safety settings

Hosting:

- Vercel can work for frontend and simple APIs
- persistent backend or real-time service likely needed for voice and WebSockets
- consider Fly.io, Render, Railway, AWS, GCP, or Azure for backend services

High-level system:

```txt
Players' phones/tablets/laptops
        |
        v
Web/PWA/Mobile Client
        |
        +--> Real-time lobby/session channel
        |
        +--> Backend API
                 |
                 +--> Game State DB
                 +--> Rules Engine
                 +--> Dice Engine
                 +--> AI Orchestrator
                 +--> Voice STT/TTS
                 +--> Campaign Memory
                 +--> Safety/Moderation
                 +--> Billing/Usage Metering
```

Suggested monorepo:

```txt
ai-table-dm/
  apps/
    web/
    mobile/
  packages/
    rules-engine/
    game-state/
    ai-dm/
    content-srd/
    ui/
    config/
  services/
    api/
    realtime/
    worker/
  prisma/
  docs/
  tests/
```

---

## 9. Data Model Overview

Core entities:

- User
- GameSession
- Campaign
- SessionParticipant
- Character
- CharacterResource
- DiceRoll
- Encounter
- Combatant
- InventoryItem
- SpellState
- Scene
- TimelineEvent
- WorldFact
- NPC
- Location
- Quest
- SafetyAgreement
- AiMessage
- RulesEvent
- HostOverride
- BillingSubscription
- UsageRecord

Important principle:

The game should be event-sourced or at least event-logged. Every meaningful state change should have a reason, actor, timestamp, and previous/new value.

Example:

```ts
type GameEvent = {
  id: string;
  sessionId: string;
  campaignId?: string;
  type:
    | 'ROLL_REQUESTED'
    | 'ROLL_COMPLETED'
    | 'DAMAGE_APPLIED'
    | 'ITEM_ADDED'
    | 'SPELL_SLOT_USED'
    | 'SCENE_CHANGED'
    | 'NPC_CREATED'
    | 'HOST_OVERRIDE'
    | 'SAFETY_PAUSE';
  actorId: string;
  payload: unknown;
  createdAt: string;
};
```

---

## 10. AI Prompting and Tool Design

The AI DM should be built around structured tools, not freeform authority.

System prompt principles:

- You are the narrator and facilitator, not the source of rules truth.
- Use tools for mechanical outcomes.
- Never silently change character resources.
- Ask for clarification when player intent is unclear.
- Respect session zero boundaries.
- Do not control player characters.
- Keep narration concise during combat.
- Invite quieter players into scenes.
- Say no when needed.
- Escalate to host on uncertainty.

Tool examples:

```ts
requestRoll({
  characterId,
  rollType: 'ability_check',
  ability: 'dexterity',
  skill: 'stealth',
  dc: 15,
  reason: 'Sneaking past the sentries'
});
```

```ts
resolveAttack({
  attackerId,
  targetId,
  weaponId,
  advantageState: 'normal'
});
```

```ts
applyDamage({
  targetId,
  amount,
  damageType: 'fire',
  source: 'Burning hands spell'
});
```

```ts
createWorldFact({
  fact: 'The old mill is secretly used by the Red Ash smugglers.',
  visibility: 'dm_only',
  confidence: 'canonical'
});
```

AI output validation should catch:

- unsupported rules claims
- forbidden content
- contradiction of known canon
- unauthorised item or resource changes
- player agency violations
- overlong narration
- hallucinated official content

---

## 11. Minimum Viable Product

MVP goal:

> A group of 2–5 players can join a browser session, create or choose simple characters, and play a 60–90 minute AI-led fantasy one-shot with voice narration, text fallback, dice rolling, basic combat, and saved recap.

Must have:

- web app/PWA
- host creates session
- room code/link/QR
- players join from phone browser
- simple session setup
- basic session zero
- limited character builder or pre-gens
- AI DM text narration
- text-to-speech narration
- push-to-talk or text input
- dice roller
- basic rules engine
- basic encounter tracker
- HP tracking
- inventory notes
- session recap
- save campaign state
- host pause/override

Should not have in MVP:

- full level 1–20 character builder
- full spell system
- full grid VTT
- AI-generated art
- D&D Beyond import
- native mobile apps
- every subclass/species/spell
- advanced subscriptions
- multiplayer online audio chat
- complex homebrew marketplace

MVP rules scope:

- levels 1–3
- 4 core classes
- limited species/races
- limited backgrounds
- basic weapons and armour
- basic skill checks
- basic saving throws
- basic attack/damage
- basic spells if included
- short/long rest
- death saves
- small condition list

MVP adventure scope:

- village problem
- small dungeon
- missing person
- bandit camp
- haunted ruin
- monster in the woods

The first version should include a few hand-authored adventure frames. Pure AI-generated adventures are harder to keep coherent.

---

## 12. Development Phases

### Phase 0 — Discovery and Legal Foundation

Duration: 2–4 weeks.

Tasks:

- confirm licensing strategy
- choose SRD version/content base
- define product name
- define target user
- build clickable prototype
- write rules scope
- write safety policy
- estimate AI/voice costs
- validate with 3–5 tabletop groups

Deliverables:

- product brief
- legal assumptions document
- feature list
- MVP scope
- wireframes
- technical architecture
- risk register

### Phase 1 — Table Lobby Prototype

Duration: 4–8 weeks.

Tasks:

- build web app
- create host session flow
- create room code joining
- create lobby UI
- add player ready states
- add basic real-time sync
- add text chat/action input
- add simple AI narrator response

Success test:

A group can join a session from multiple phones and the host can start the game.

### Phase 2 — Character and Dice Prototype

Duration: 6–10 weeks.

Tasks:

- add pre-generated characters
- add simple character sheets
- add dice roller
- add ability checks
- add saving throws
- add attack rolls
- add HP tracking
- add roll history
- connect AI to dice requests

Success test:

The app can run an exploration scene and a simple fight without losing track of HP or rolls.

### Phase 3 — AI DM One-Shot Engine

Duration: 8–12 weeks.

Tasks:

- create adventure schema
- add scene tracking
- add NPCs
- add basic world facts
- add one-shot generator or curated templates
- add session recap
- add memory summarisation
- add safety boundaries
- add host override

Success test:

A group can complete a short adventure with beginning, middle, climax, and conclusion.

### Phase 4 — Voice Layer

Duration: 6–12 weeks.

Tasks:

- add text-to-speech narration
- add push-to-talk
- add speech-to-text
- add transcript correction
- add audio playback controls
- add caption display
- add interruption/skip

Success test:

The app can be played around a real table without constant typing.

### Phase 5 — Campaign Continuity

Duration: 8–16 weeks.

Tasks:

- add campaign saves
- add world memory
- add NPC memory
- add quest tracker
- add player notes
- add Previously On recap
- add canonical fact editor

Success test:

A group can return one week later and the app accurately remembers what mattered.

### Phase 6 — Native Apps and Scaling

Duration: 12–24 weeks.

Tasks:

- build React Native/Expo app or wrap PWA
- add push notifications
- add offline character access
- add better audio handling
- add billing
- add usage metering
- add analytics
- add production monitoring
- add support tools

---

## 13. Team Needed

Minimum early team:

- product lead / designer
- full-stack TypeScript developer
- rules engine developer
- AI engineer / prompt/tooling engineer
- UX/UI designer
- tabletop game designer
- QA tester familiar with 5e

Later team:

- mobile developer
- backend infrastructure engineer
- security/privacy engineer
- content designer
- voice/audio specialist
- legal/IP advisor
- community/support manager

A solo developer could build a prototype, but not a reliable commercial version quickly.

---

## 14. Major Risks

### Rules complexity risk

D&D-style rules have many edge cases. Full strict 5e is a huge job.

Mitigation:

- start with limited levels and content
- use deterministic rule modules
- write tests
- add host override
- avoid claiming perfect strictness too early

### AI hallucination risk

The AI may invent rules, items, lore, or outcomes.

Mitigation:

- tool-based state changes
- output validation
- rules engine
- canonical memory
- host correction
- limited context

### Licensing risk

Using protected content incorrectly could kill the project.

Mitigation:

- use SRD material only
- create original settings
- avoid official art/lore/names
- get legal review
- provide attribution

### Voice cost risk

Voice-to-text and text-to-speech can become expensive.

Mitigation:

- push-to-talk
- text fallback
- usage limits
- host subscription
- cache repeated narration where appropriate
- track cost per session

### Latency risk

Slow AI responses ruin table flow.

Mitigation:

- stream narration
- keep prompts compact
- use scene summaries
- pre-generate likely content
- use deterministic tools quickly
- use shorter narration in combat

### Multiplayer sync risk

Players need shared state to be reliable.

Mitigation:

- event log
- real-time server
- reconnect support
- optimistic UI carefully
- authoritative backend state

### Product scope risk

This idea can balloon forever.

Mitigation:

- MVP one-shot only
- no full VTT first
- no full level 1–20 builder first
- no official content imports first
- focus on the table experience

---

## 15. Everything That Needs Coding Checklist

Frontend:

- landing page
- host start screen
- session setup wizard
- room code join page
- QR code display
- lobby screen
- player ready state
- character selection screen
- character builder
- character sheet
- dice roller UI
- shared table dashboard
- AI narration panel
- voice input button
- transcript panel
- encounter tracker
- initiative display
- inventory screen
- notes/recap screen
- host control panel
- safety pause button
- settings page
- account page
- billing page later

Backend:

- auth API
- guest identity API
- session creation API
- room code generation
- session join API
- player presence
- real-time state sync
- character API
- dice API
- rules engine API
- encounter API
- inventory API
- campaign API
- notes API
- AI DM API
- voice transcription API
- TTS API
- safety/moderation API
- billing API
- usage metering
- admin/support tools

Rules engine:

- dice formula parser
- ability modifier calculator
- proficiency calculator
- skill check resolver
- saving throw resolver
- attack resolver
- damage resolver
- initiative resolver
- AC calculator
- HP calculator
- death save resolver
- rest resolver
- spell slot tracker
- concentration tracker
- condition tracker
- inventory validator
- level progression later
- encounter balancing later

AI system:

- prompt templates
- tool definitions
- context assembler
- memory retriever
- scene summariser
- adventure generator
- NPC roleplay engine
- safety boundary enforcer
- output validator
- host override adapter
- prompt/version testing
- AI eval scripts

Voice:

- microphone capture
- push-to-talk
- speech-to-text streaming
- transcript storage
- TTS generation
- audio queue
- playback interruption
- captions
- voice settings

Database:

- user table
- session table
- participant table
- campaign table
- character table
- dice roll table
- encounter table
- combatant table
- inventory table
- spell/resource table
- scene table
- timeline event table
- world fact table
- NPC table
- location table
- quest table
- safety agreement table
- AI message table
- usage table
- billing table

QA and testing:

- unit tests for rules
- unit tests for dice
- integration tests for AI tool calls
- multiplayer sync tests
- reconnect tests
- voice latency tests
- safety tests
- character builder validation tests
- encounter flow tests
- campaign memory tests
- browser compatibility tests
- mobile responsiveness tests

---

## 16. Success Criteria

The product is working when:

- a non-technical host can start a game in under 3 minutes
- four players can join from phones without accounts
- players understand what to do next
- the AI DM can run a coherent opening scene
- the app knows when to ask for rolls
- the dice and modifiers are correct
- combat can run without losing track of turns or HP
- the AI remembers important NPCs and choices
- the host can pause, correct, and resume
- the AI respects boundaries
- a session recap is generated accurately
- the group says, “That actually felt like playing D&D”

---

## 17. Suggested First Prototype

The first prototype should not be a full commercial app. It should prove the central table experience.

Build this:

> A browser-based AI DM one-shot runner where the host creates a session, players join by code, choose from 6 pre-generated characters, and play a 45-minute fantasy adventure with text narration, digital dice, basic HP tracking, and a saved recap.

Prototype scope:

- browser only
- no native app
- no payment
- no full character builder
- no voice input yet
- TTS optional
- levels 1–3 only
- one original setting
- one curated adventure template
- simple combat
- host override

This prototype answers the most important question:

> Is the table experience actually fun?

---

## 18. Practical Build Order

Do not build in this order:

1. native mobile app
2. full character builder
3. AI-generated maps
4. voice acting for every NPC
5. level 1–20 rules
6. subscriptions
7. marketplace

Build in this order:

1. browser lobby
2. shared session state
3. pre-generated characters
4. dice engine
5. basic rules engine
6. AI narration loop
7. host override
8. basic encounter tracker
9. session recap
10. voice output
11. voice input
12. campaign memory
13. character builder
14. better content
15. native app
16. billing

---

## 19. Final Product Thesis

This project is viable if it is treated as a multiplayer rules-aware game platform, not just a chatbot.

The winning version is:

- fast to start
- easy for non-DMs
- rules-aware
- voice-friendly
- human-controllable
- legally clean
- original-content-first
- good at saying no
- good at remembering
- fun around a real table

The core build challenge is not making an AI talk like a DM. That is the easy part.

The real challenge is making the game state reliable enough that the table trusts it.

> Trust is the product.

---

## Follow-up from conversation

Josh later asked where the download link was because the ChatGPT canvas did not show one clearly on Android mobile.

PDF and DOCX exports were generated in the ChatGPT session, but this GitHub commit stores the durable Markdown version in the repo so it is accessible from anywhere GitHub is available.

Best next build step remains:

> Build the tiny vertical slice first: host creates session, players join by code, pick pre-gens, AI narrates, dice engine resolves one scene and one combat.
