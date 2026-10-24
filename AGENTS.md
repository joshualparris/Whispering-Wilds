# AI coding agent instructions — original Whispering Wilds (Python)

This is **`joshualparris/Whispering-Wilds`**: a Python CLI adventure. It is **NOT** `Parris-Tech-Services/whispering-wilds`, which owns the 20+100 ElevenLabs browser-audio backlog.

**Read first:** [TASK_TRIAGE.md](TASK_TRIAGE.md) → [WORK_CHECKPOINT.md](WORK_CHECKPOINT.md) → [issue #1](https://github.com/joshualparris/Whispering-Wilds/issues/1) → [audit](audit/BEAUTIFUL_CODE_STANDARD_AUDIT.md). First eligible task: **WW-I1.1**, unless already claimed or verified since last review.

Before changing code, check open [PR #4](https://github.com/joshualparris/Whispering-Wilds/pull/4), which targets `feature/status-effects`, not `main`, and renames the legacy `code.py` to avoid shadowing a Python standard library module. Do not collide with this branch's restructuring or merge a PR into the wrong target.

Work one existing numbered criterion at a time. Claim it in `WORK_CHECKPOINT.md` with branch/time/agent; reproduce the behaviour, implement only the required change, add regression tests, run `python -m unittest discover -s tests`, check real CLI experience, document evidence and then mark complete. If blocked, log the obstacle and continue with the next independent eligible task. Don't make up scope for the under-specified issue #2. Preserve all existing IDs; use the triage sequence, not the raw numeric order of arbitrary docs.

Keep a durable checkpoint at task start, milestones, before switching and during extended work. Commits, merges and deployments must be actually verified before claiming them. Never conflate this repo's status with the web game's Parris VoiceBank audio status.
