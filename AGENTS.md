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

# gate (one definition: .githooks/pre-commit and CI both run this script)
bash tools/gate.sh            # docs style + witness tests + board freshness
python3 tools/check_docs.py   # docs style only
python3 -m unittest discover -s tests/unit   # witness tests only
python3 tools/gen_leaderboard.py --check     # CURRENT / STALE / SKIP
```

## Map

- `BLACKBOARD.md`, the board; the only place a decision becomes real
- `VOICES-LIVE-16.md`, voice registry (register/rhythm/lexicon/forms per bot)
- `crew/` `experiments/` · `ARENA.md` · `bets-ledger.md` · `ENTITY.md`
- `tools/check_docs.py`, the docs gate; `tools/gen_leaderboard.py`, the generated
  board numbers and their freshness check; `tools/gate.sh`, the one definition
  of "verified"; `tests/unit/`, witness tests that each input is read once;
  `.githooks/pre-commit` and CI both call `tools/gate.sh`

## Rules

- decisions are written to the board, never left in chat
- a bot speaks in its own register (VOICES is binding)
- artifacts English, chat with the Owner in Arabic; push everything straight to
  `main` (origin: faresrafat3/crew-research-council), no long-lived side branches
