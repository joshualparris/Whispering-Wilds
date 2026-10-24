# Original Whispering-Wilds Python game — AI task triage

**Reviewed:** 2026-10-24. **Scope:** `joshualparris/Whispering-Wilds` on `main`. This is a **Python terminal adventure**, not `Parris-Tech-Services/whispering-wilds` (the active browser game with recorded speech). Do not mix the two queues.

> ## NEXT TASK — **WW-I1.1** in GitHub [issue #1](https://github.com/joshualparris/Whispering-Wilds/issues/1)
> **P1:** Ensure malformed and oversized base64/JSON save codes are rejected with a friendly `Bad code.` response and never crash. First reproduce this using `_p4_load` in `code.py` on current `main`, then write a failing regression test, implement size/schema guards and rerun the suite. Do not assume the old issue is still reproducible without testing.

**Before touching code:** There is an [open PR #4](https://github.com/joshualparris/Whispering-Wilds/pull/4), `fix/rename-legacy-code-py` targeting **`feature/status-effects` (not `main`)**, intended to prevent root `code.py` from shadowing the Python stdlib `code` module. Check that branch/PR and ongoing agent claims first. Avoid simultaneous renames/refactors; do not merge #4 into the wrong base branch merely to make tests green.

## Authoritative task sources and ordered next work

For this Python repo, use its [issues](https://github.com/joshualparris/Whispering-Wilds/issues), [Beautiful Code Standard audit](audit/BEAUTIFUL_CODE_STANDARD_AUDIT.md) and [podcasttodo.md](podcasttodo.md). The issue/checkbox identifiers already exist; the audit identifiers are fixed `WW-PY-A01`–`WW-PY-A05`. Do not use audio task IDs `014–020`, `040–048` here; those belong to the web game.

| Priority / order | Task ID / source | Exact next outcome and acceptance |
| --- | --- | --- |
| P1 1 | **WW-I1.1** — issue #1 | Reproduce then prevent crash on malformed/huge save code; friendly `Bad code.` and tests |
| P1 2 | **WW-I1.2** — issue #1 | Clamp extreme HP, gold, XP and resources; add deterministic boundary tests |
| P1 3 | **WW-I1.3** — issue #1 | Safely ignore unknown rooms/items or replace with known harmless placeholders; tests |
| P1 4 | **WW-I1.4** — issue #1 | Update README/Wiki statement on validated untrusted save codes; verify text |
| P1 5 | **WW-PY-A02** — audit | Expand behavioural regression tests around save/load and every actual bug fix, not arbitrary internals |
| P1 6 | **WW-I1.5** — issue #1 | Verify Old Watchtower offers Tower Echoes quest through the real in-game dialogue |
| P1 7 | **WW-I1.6** — issue #1 | Verify handing over 1 coal completes quest exactly once and consumes material |
| P1 8 | **WW-I1.7** — issue #1 | Verify +4 gold, +2 XP and journal updates; prevent duplicate rewards |
| P1 9 | **WW-I1.8** — issue #1 | Ensure help text explains tower quest hook; smoke-test user flow |
| P2 10 | **WW-PY-A05** — audit | Automated primary command→quest→save/load end-to-end smoke test |
| P2 11 | **WW-PY-A03** — audit | Surface broader lint and static analysis findings without masking them, define explicit warning vs gating policy |
| P2 12 | **WW-PY-A04** — audit | Add dependency/security audit to CI if dependencies/distribution warrant it |
| P2 13 | **GitHub issue #2** | `Create new quests` is **not implementation-ready**; first write a concrete quest spec, gameplay triggers, rewards and tests in that existing issue, then implement after acceptance is defined |
| P2 14 | **WW-PY-A01** — audit | Review current branch restructuring/PR #4; extract only coherent modules when proven safe, keeping backward-compatible gameplay |
| CONDITIONAL | **WW-PY-030** — podcasttodo | Only if this Python adventure gains a genuine browser UI: reuse shared podcast bank, do not add web code to current CLI |

**Task #2 remains a scope/acceptance blocker**, not an invitation to guess content. The open #4 rename PR must be resolved on its own correct base-branch path before any code move/refactor overlaps with it. Document blockers and continue on independent tasks.

## First execution recipe (WW-I1.1)

1. Read `AGENTS.md`, `WORK_CHECKPOINT.md`, this queue, [issue #1](https://github.com/joshualparris/Whispering-Wilds/issues/1), [PR #4](https://github.com/joshualparris/Whispering-Wilds/pull/4) and the audit. Fetch latest `main`. If a task has an active claim, take the next unclaimed/unblocked independent item.
2. Run baseline `python -m unittest discover -s tests`; inspect `tests/test_core.py` and `_p4_load`/`_p4_save` in `code.py`. `pytest` may be affected by `code.py` shadowing the standard library; distinguish a test-import/branch issue from a gameplay regression.
3. Add a safe *test-only* corpus of malformed, huge, unknown-key and out-of-range save codes; prove the failing case before changing production logic. Never execute untrusted saved content.
4. Harden parsing to enforce a sane size limit, schema/valid-room/item validation and helpful user-visible errors. Add focused tests; retest ordinary saves, quests and gameplay.
5. Verify the exact checked criteria from issue #1; commit code + tests + `WORK_CHECKPOINT.md` and document SHA and command results. Reconcile only the relevant issue checklist items as proof permits; do not close all of issue #1 until its Tower Echoes criteria are independently verified.

## Agent handoff and completion rule

- **Claim:** Add task ID, agent name, branch, UTC time and baseline SHA to `WORK_CHECKPOINT.md`. Check live PRs before claiming. Re-fetch checkpoint before conflicting edits.
- **Status:** `OPEN` → `IN_PROGRESS` → `VERIFIED_COMPLETE` only after reproducible test and actual behaviour. If unavailable, `BLOCKED` with reason, alternatives and next action, and move to the next independent entry.
- **Evidence:** exact commit SHA, commands/exit codes, test results, manual/automated command journey and any merge/deployment result. Don't claim test success from a PR description alone.
- **Continuity:** update durable checkpoint at task start, meaningful milestones, before switching and during long work; commit it with the implementation.
- **Authority:** The web audio tracker is not a task source for this repo. Do not renumber existing issue IDs, audit IDs or `WW-PY-030`.
