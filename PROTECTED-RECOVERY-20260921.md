# PROTECTED-RECOVERY — 2026-09-21 (the original declaration recovered and adopted)

**What this file is:** the dated record beside `PROTECTED.md`, per that file's own rule — a
supersession is filed as a new document, never a rewrite. It records how the original
declaration (created 2026-09-20) was lost, recovered, and adopted back over the interim
reconstruction.

## What happened

- The original was untracked (`git status` → `?? PROTECTED.md`). A cross-project condensation
  pass ran `git stash push -u` in this repo to protect uncommitted work before editing; the
  `-u` also swept the untracked `PROTECTED.md` and `missions/**` out of the worktree. That
  stash — not a hostile writer — is the "concurrent writer" named in the interim
  reconstruction note; the pass self-reported it in `~/local/compliance/2026-09-21-context-slim-incident.md`.
- Every byte survived inside the stash's untracked parent (`stash@{0}^3`): `PROTECTED.md`,
  `missions/CREW-EVIDENCE/BOARD.md`, `missions/CREW-EVIDENCE/2026-09-20-EVIDENCE-RECOVERY.md`.
  A pre-edit backup independently held the same original bytes.

## The bytes

| | |
|---|---|
| original — **adopted** | 41 lines / 2375 B · sha256 `a12092df17090b6660206caf31e72d61b7e7d3e28663eb85bd5925cc743d1bf3` |
| interim reconstruction — **superseded**, kept in git history | blob `f17a238d8c842c7e8454f3de3f5504b47e99c3e845c8e2dc803699f2dd4075a0` · commit `9304650` |
| evidence copy | `~/local/compliance/evidence/crew-research-council-PROTECTED.original-20260921.md` |
| original's safe-write-path referents | **16/16 present** on disk (checked 2026-09-21) |

## Restored and now tracked with it

- `missions/CREW-EVIDENCE/BOARD.md` + `missions/CREW-EVIDENCE/2026-09-20-EVIDENCE-RECOVERY.md`
  — back on disk and committed, so the one-copy failure mode (their own warning in the
  reconstruction row) cannot repeat.
- `BLACKBOARD.md` — the 2026-09-20 mission append recovered from the same stash; HEAD (`b7cd26e`,
  2026-09-13) held the pre-mission empty board, so this stash was the only carrier of the live
  board state.

## Decision (agent, revocable — R8 applies)

Adopt the original bytes as the operative declaration; the reconstruction's substance stays
reachable via git history and the incident record. The condensation pass's edits (README,
PROJECT, TEST-POLICY, TESTING-COUNCIL, VOICES, v2-ARCHITECTURE) are committed in the same
moment — all inside the safe write-path this declaration names, and compression is explicitly
not a veto reason (this file's own law).
