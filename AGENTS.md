# crew-research-council — blackboard + veto pipeline

A hermes-native research council: the board is the **only** shared state.
Chat threads are Q&A only — no decision lives in chat.

## Contract

Global harness contract: `~/AGENTS.md` (permissions, single-source configs,
tools index). This file adds repo identity only — never contradicts it.

## Commands

No build step — this is a process/repository of record. The runtime is
hermes itself (project config in `.hermes/`):

```
hermes            # enter the council runtime from this directory
git status        # must be clean before claiming any decision landed
```

## Map

- `BLACKBOARD.md` — the board; the only place a decision becomes real
- `VOICES-LIVE-16.md` — voice registry (register/rhythm/lexicon/forms per bot)
- `crew/` `experiments/` · `ARENA.md` · `bets-ledger.md` · `ENTITY.md`

## Rules

- decisions are written to the board, never left in chat
- a bot speaks in its own register (VOICES is binding)
- artifacts English, chat with the Owner in Arabic; push everything
  (origin: faresrafat3/crew-research-council)
