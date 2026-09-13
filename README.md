# Crew Workflow — blackboard + veto pipeline

The board is the ONLY shared state. Chat threads are Q&A only; no decision lives in chat.

## The board

- Live board: `BLACKBOARD.md` (mirrors the ACTIVE mission). Per-mission boards: `missions/<id>/BOARD.md`.
- Owner: @firstmate — sole conflict-resolver. All writes are typed messages to the board: APPEND, FLAG, SNAPSHOT, RESTORE. Never bot-to-bot except Q&A.
- Write rights: @scout → EVIDENCE + OPEN GAPS. @architect → DECISIONS + CONSTRAINTS. @ship → ARTIFACT + TEST RESULTS. @razor/@gate → flags only (ACTIVE / SUPERSEDED / KILLED + reason), never delete. @edge → BET MEMO at plan stage only. @coach → harvests offline, compacts nightly.
- Max 7 active CONSTRAINTS (@razor enforces; overflow goes to OPEN GAPS).

## The pipeline (strict order per mission)

edge bets → scout evidence → architect plan → razor cut → ship build → razor cut → gate verdict → coach compound.
States: CLAIM → OBJECTION → VETO/SHAPE → VERDICT.

## Veto rights

- @razor holds hard VETO at both cut gates: must cite the deletion rule AND propose the smaller surviving subset. No subset, no veto.
- @gate holds binary SHIP/HOLD: must cite one @razor check, cannot edit — only judge.
- @firstmate routes, never rewrites content.

## B-brain (governors out of the work)

@firstmate + @coach watch A-traffic read-only on a slower tick. Stuck pattern (e.g. 3 rejections in a row, circling without new evidence) → freeze the thread, force a timeboxed swap (1 question + 1 assumption-swap). B restricts PROCESS, never dictates answers. Every intervention is logged on the board.

## K-lines (memory as restore points)

SNAPSHOT the board at every stage gate (`missions/<id>/snapshots/<stage>-<n>.md`). Disagreement about the past → RESTORE by snapshot id instead of re-arguing. @coach compacts snapshots into DISTILLED RULES nightly.

## Throughput (TOC — see THROUGHPUT.md)

Drum: @razor (standby: @gate), re-voted weekly from queue data. B1/B2/B3 buffers in `buffers/`; rope owned by @firstmate (release only on free slots; full = upstream stops and helps). T = gated+compounded value/week; I = everything stuck; OE = tokens + owner-min. Only drum-minutes count.
