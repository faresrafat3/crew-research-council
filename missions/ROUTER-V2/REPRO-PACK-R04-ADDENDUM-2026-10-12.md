# REPRO-PACK-R04 — ADDENDUM (2026-10-12): precondition, revision pin, R05 duty

> Filed *beside* the frozen `REPRO-PACK-R04.md`, per `PROTECTED.md` L38–41
> ("add a new dated document beside it"). It **adds** rows and preconditions; it
> rewrites no number, claim or ruling of R02–R04, and it re-runs nothing.
> Approved by the Owner 2026-10-12 after the audit
> `REPRO-PACK-R04-AUDIT-2026-10-12.md` (evidence table R1–R19). Owner: Fares.
> Language: English (artifacts) / Arabic (chat).

## 1. Reproduction precondition

Every command in `REPRO-PACK-R04.md` runs inside the sandbox
`~/.hermes/crew/experiment/runs/2026-09-22-router-round-04/` (`REPRO-PACK-R04.md`
L20), which is **outside version control** (`.gitignore`: `.hermes/`). *A fresh
clone can audit the papers, not the run.* Absent from all 33 refs of `origin`:
`crew/formations.py` (the module ADR-14 amends), `crew/escalation.py`,
`cognition.py`, `expertise.py`, `handoffs.py`, `router_thresholds.py`,
`tests/**`, `tools/run_trial_r04.py`, `tools/ablation_no_verifier_r04.py`,
`tools/adversarial_r04.py`, `tasks/expanded-missions.json`, and every `logs/**`
file the pack cites.

## 2. Frozen inputs — one row added

| item | value |
|---|---|
| frozen fixture (20) | `tasks/real-missions.json` — sha256 `28406677…a87`, **retrievable from git**: `git cat-file -p origin/orx/r9-consolidation-ledger-backed-laws-written-into:tasks/real-missions.json \| sha256sum` (byte-identical on 15 of the 31 non-`main` refs; the other 16 carry six *divergent* fixture revisions — never substitute one for another) |
| **measured revision** | **UNPINNED for R04.** R04 records fixture, pre-registration (`ad9451ce…`, `PRE-REGISTRATION-R04.md` L3–5) and log hashes, but **no hash of the code that produced 292 / 288 / 278**. R03 pinned its measured revision (`BOARD.md` L206–207, `PRINCIPLES.md` P14 L147–159); R04 did not. Consequence: a future re-run cannot be shown to have used the revision behind the ruling — the pin cannot be back-filled, only restored from the sandbox |

## 3. Duty before R05 measures (P14)

R05 writes into its own sandbox and cites both files in `REPRO-PACK-R05.md`
**before** any measurement:

- `logs/artifacts-sha256.txt` — `crew/*.py`, `tests/**`, `tools/*.py`;
- `logs/fixture-sha256.txt` — every fixture it measures.

Rationale: R05's trial decides between `pre`, `pre + post-hop guard` and `final`
(`ADR-ROUTER-V2-R04.md` ADR-14 Reversal), so its numbers must not inherit R04's
unpinned revision.

## 4. Status of R04's numbers (unchanged, and stated plainly)

Reported and internally consistent (audit R13); pre-registration byte-verified
(audit R12); **not reproduced** — no artifact that produced them is reachable in
this repository. Historical logs are not proof of a fresh run. Nothing here
reconstructs, replaces or re-scores a historical result.

---
**Addendum filed 2026-10-12 · base commit `ecaa656` · companion audit
`REPRO-PACK-R04-AUDIT-2026-10-12.md`.**
