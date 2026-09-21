# BLACKBOARD — live board (mirrors the ACTIVE mission)

Status: ACTIVE MISSION `CREW-EVIDENCE` (opened 2026-09-20 by an operator session on the Owner's
goal; mirrored in `missions/CREW-EVIDENCE/BOARD.md`). @firstmate may re-route or close it.

---
## APPEND 2026-09-20 — mission CREW-EVIDENCE opened (operator session)

**Why:** the repo tracked no runnable harness (`crew/**`, `harness/**`, `repro/**`, `tests/**`
held only `__pycache__`) and `GOAL.md`'s `DECISIVE-01 … see experiment/VERDICT.md` pointed at a
file that was absent everywhere. A rescue and a re-run were executed under the Owner's goal.

**What landed (pointers, not prose):**

- `missions/CREW-EVIDENCE/BOARD.md` — the mission board (GOAL · 7 CONSTRAINTS · EVIDENCE E1–E6 ·
  OPEN GAPS · DECISIONS D1–D3 · BET MEMO · ARTIFACT+TEST RESULTS).
- `missions/CREW-EVIDENCE/2026-09-20-EVIDENCE-RECOVERY.md` — the recovery record, including one
  retracted claim (a weak first identity check) kept on the record.
- `~/.hermes/crew/experiment/VERDICT.md` — the missing artifact's dated replacement: five arms,
  20 tasks, seed 7, offline, deterministic.
- `~/.hermes/crew/experiment/rescued/2026-09-20-verify-consol/` — 69-file rescue of a volatile
  `/tmp` working copy with a verified `MANIFEST.sha256`.

**Measured headline (20 tasks, seed 7):** `solo` 19/20 · **`solo --hold-on-vague` 20/20, 0 grave,
cost 68** · `solo-checklist` 19/20 cost 88 · `duo` 17/20 (2 budget-held) cost 98 · `team` 19/20
cost 87 with `resolved=9` vs 4 for every other arm.

**Not claimed:** the recorded 16-task per-arm numbers (A 15/20 · B 14/20 · C 10/20) are **not**
reproduced — the surviving fixture has 20 tasks. Nothing was promoted into the protected trees and
no commit was cut (another session's work is uncommitted in this tree).

**Independent check:** a separate blind verifier run re-executes the five arms and its SUMMARY
lines are appended to `VERDICT.md` §6.

---

## GOAL (owner: @architect)

_none_

## CONSTRAINTS — max 7 active (owner: @architect, enforced by @razor)

_none_

## EVIDENCE (owner: @scout — append-only, cite sources)

_none_

## OPEN GAPS (owner: @scout)

_none_

## DECISIONS (owner: @architect — each cites >=2 EVIDENCE rows)

_none_

## BET MEMO (owner: @edge — plan stage only)

_none_

## ARTIFACT + TEST RESULTS (owner: @ship — pointers, not prose)

_none_

## FLAGS (@razor/@gate only: ACTIVE / SUPERSEDED / KILLED + reason)

_none_

## K-LINE SNAPSHOTS (id → stage → path)

_none_

## DISTILLED RULES (owner: @coach — compacted, never raw traces)

_none_

## INTERVENTION LOG (B-brain only)

_none_
