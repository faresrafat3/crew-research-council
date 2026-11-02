# crew-research-council, blackboard + veto pipeline

A hermes-native research council: the board is the **only** shared state.
Chat threads are Q&A only, no decision lives in chat.

## Contract

Global harness contract: `~/AGENTS.md` (permissions, single-source configs,
tools index). This file adds repo identity only, never contradicts it.

## Commands

No build step, this is a process/repository of record. The runtime is
hermes itself (project config in `.hermes/`):

```
hermes            # enter the council runtime from this directory
git status        # must be clean before claiming any decision landed

# gate (runs in .githooks/pre-commit; CI still runs only the docs gate)
python3 tools/check_docs.py   # OUTPUT headings sentence case; READMEs clean; refs resolve
python3 -m unittest discover -s tests/unit   # witness tests for both tools
python3 tools/probe_state_machines.py   # state-machines closed/open, exit 1 on drift

bash tools/gate.sh   # the same three, in the order the hook runs them
```

## Map

- `BLACKBOARD.md`, the board; the only place a decision becomes real
- `VOICES-LIVE-16.md`, voice registry (register/rhythm/lexicon/forms per bot)
- `crew/` `experiments/` · `ARENA.md` · `bets-ledger.md` · `ENTITY.md`
- `tools/check_docs.py`, the docs gate; `tools/gen_leaderboard.py`, the generated
  board numbers; `tools/probe_state_machines.py`, the read-only reproduction of
  `IMPLICIT-STATE-MACHINES.md`; `tests/unit/`, witness tests that each input is
  read once; `.githooks/pre-commit` runs the gate and the tests

## Rules

- decisions are written to the board, never left in chat
- a bot speaks in its own register (VOICES is binding)
- artifacts English, chat with the Owner in Arabic; push everything straight to
  `main` (origin: faresrafat3/crew-research-council), no long-lived side branches
