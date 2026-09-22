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

---
## APPEND 2026-09-22 — mission ROUTER-V2 opened and CLOSED-GREEN (operator session)

**Why:** round-01's router was cosmetic — `eval.py` declared `routed` then
crashed (KeyError) and overwrote the router proposal with a static CLI label.
v2-ARCHITECTURE Phases 1–3 were still paper. The Owner approved a full
scientific round: pre-registration → RED → GREEN → measurement → findings.

**What landed (pointers, not prose):**

- `missions/ROUTER-V2/BOARD.md` — mission board (GOAL · 7 CONSTRAINTS ·
  EVIDENCE E1–E6 · OPEN GAPS · DECISIONS D1–D5 · BET MEMO · ARTIFACT+TESTS).
- `missions/ROUTER-V2/{PRE-REGISTRATION,FINDINGS,PRINCIPLES,ADR-ROUTER-V2,
  REPRO-PACK,DECISIONS-LOG}.md` — the papers: 9 falsifiable hypotheses with
  verdicts, 10 niche principles with evidence+code anchors and repeal
  conditions, 10 ADRs with reversal clauses.
- Sandbox `~/.hermes/crew/experiment/runs/2026-09-22-router-round-02/` —
  ladder+receipts (A1), risk-stratified verification with disjoint check
  registries (A2/A3), bounded rework (A4), budget governor with floor and
  announced degradation (A5), feasibility three-outcome (A6), typed shrinking
  receipts (B1), shadow-no-promotion and gate-locked priors (D1/D2), error
  budget (D3), injection/poison guards (E1/E2), confidence/beliefs/debate/
  reflection/next-experiment cards (H1–H5), drift alarms (G2).
- Tests: RED witnessed `43 failed, 1 passed` → GREEN `90 passed`
  (46 legacy + 44 new). Determinism: byte-identical double-run PASS.

**Measured headline (20 tasks, seed 7, fixture sha256 28406677…):**
`solo --hold-on-vague` 20/20 cost 68 resolved 4 (champion, sd=0 across 5
seeds) · `routed --hold-on-vague` 20/20 grave=0 cost 127 **resolved 9**
(2.25x champion) · routed WITHOUT hold-rule 19/20 grave=1 · ablation
`routed-thresholds` 20/20 cost 70 — the class table currently adds 57 calls
for no measurable gain (H5 REFUTED, on trial for R03).

**Not claimed:** no promotion (cost bar failed); no LLM-leg inference (model
leg out of scope); no generalization beyond the 17 fixture classes;
routing_match=0/20 is a semantics flaw recorded as an open gap (ADR-10).

**Verdicts:** H1 confirmed on compliance/resolved (cost+routing bars failed
honestly) · H2, H3, H4, H6, H7, H8, H9 CONFIRMED · H5 REFUTED (published, no
cosmetics). Champion unchanged: `solo --hold-on-vague`.

---
## APPEND 2026-09-22 (round 03) — ADR-10 semantics fixed; class table CUT (operator session)

**Why:** R02 handed two gaps forward in writing. (1) ADR-10: `routing_match`
compared a static mode label against the router's proposal, so the registered
>=16/20 bar measured nothing. (2) H5: the class table was refuted by an
ablation arm that ran **no ladder at all** (hops=0, cost 70) — a counter-arm
that could not falsify anything. R03 fixed the semantics and re-ran the trial
on a 46-task fixture with a faithful ablation.

**What landed (pointers, not prose):**

- Sandbox `~/.hermes/crew/experiment/runs/2026-09-22-router-round-03/` —
  `planned`/`final`/`mismatch_reason`/`verifier_flips` per task; per-task
  `proposed` vs `used=final` accounting with a generated mismatch histogram;
  one harness budget for every arm; `--summary-json` so all tables are
  generated; `routed-thresholds` rebuilt as a real ablation.
- Papers beside this board: `missions/ROUTER-V2/{PRE-REGISTRATION-R03,
  FINDINGS-R03,ADR-ROUTER-V2-R03,REPRO-PACK-R03}.md`, plus the superseding
  `PRINCIPLES.md` (adds P11–P14) and `DECISIONS-LOG.md` (adds 12 R03 rows) and
  `BOARD-R03.md` (the R03 board section; R02's `BOARD.md` left frozen).
- Verbatim logs: `logs/round-03-trial.txt`, `logs/r03-analysis.md` (generated
  ruling + tables), `logs/round-03-postcut.txt` (ALL-PASS),
  `logs/round-03-adversarial.txt`, `logs/{RED,GREEN}-witness-r03.txt`,
  `logs/precut-sha256.txt`, `logs/fixture-sha256.txt`.

**Measured headline (expanded fixture, 46 tasks, sha256 26b3b832…):**
`solo --hold-on-vague` 46/46 cost 159 resolved 12 · class-table `routed`
46/46 cost 307 **resolved 23** · faithful ablation 46/46 cost 292
**resolved 23**. Frozen 20 (continuity): solo 20/20 cost 68 resolved 4 ·
table arm 20/20 cost 127 resolved 9 (R02 reproduced exactly) · ablation 20/20
cost 122 resolved 9.

**Ruling (pre-registered, applied as written):** clause (c) `resolved 23 > 23`
FAIL and clause (d) `resolved/call 0.07492 > 0.07877` FAIL → **KILL**. The
class table is deleted from `crew/router.py`; the frozen threshold scorer is
the single proposal source; the ladder stays and is what converts HOLDs into
grounded deliveries (12 → 23 resolved). Post-cut verification ALL-PASS; the cut
reproduces the ablation arm exactly (122 frozen / 292 expanded).

**Verdicts:** H10, H11 CONFIRMED (scoped to the measured, hash-pinned pre-cut
revision) · H12, H14, H15, H16 CONFIRMED · H13 ruled KILL (registered
prediction landed) · adversarial self-review `attacks=11 broken=0 ALL-HELD`.

**Not claimed:** no promotion (frozen-fixture cost bar ≤88 fails at 122; the
champion stays `solo --hold-on-vague`); the verifier's detection value remains
unpriced on this fixture (H16 measures a tax, not a benefit); no
generalization beyond the 17 synthetic classes; the ≤88 bar is explicitly NOT
rewritten after the fact — R04 must pre-register a resolved-per-cost bar.

---
## APPEND 2026-09-22 (round 04) — verification stage priced exactly; it STAYS (operator session)

**Why:** R03 closed with one number left on the table — the verification
stage's tax was never priced, and `verifier_flips=0` could not say whether the
stage earned its keep. The Owner ordered the `--no-verifier` ablation on the
46-task fixture, an exact price, and a stay-or-trim decision.

**What landed (pointers, not prose):**

- Sandbox `~/.hermes/crew/experiment/runs/2026-09-22-router-round-04/` — one
  explicit mode flag `--verify pre|final|off` with `--no-verifier` as an alias
  for `off` (single code path, alias identity asserted); the trigger lives in
  exactly one function (`verification_selected`); per-task coverage is now
  reported as `verify_selected` / `verified` / hole / unselected, never as one
  conflated number; the champion arm's missing verifier is a generated column,
  not a footnote.
- Papers beside this board: `missions/ROUTER-V2/{PRE-REGISTRATION-R04,
  FINDINGS-R04,ADR-ROUTER-V2-R04,REPRO-PACK-R04}.md`, plus the superseding
  `PRINCIPLES.md` (adds P15–P18) and `DECISIONS-LOG.md` (adds 13 R04 rows).
- Verbatim logs: `logs/round-04-trial.txt` (sha256 64ac515d…),
  `logs/r04-analysis.md` (generated ruling + tables, sha256 6ec17759…),
  `logs/r04-no-verifier-ablation.txt` (independent reproduction through the
  literal `--no-verifier` alias, sha256 b6d07e83…),
  `logs/round-04-adversarial.txt`, `logs/{RED,GREEN}-witness-r04.txt`,
  `logs/prereg-r04-sha256.txt`, `logs/prewrite/` (pre-append board copies).

**Measured headline (verification modes, 46 tasks):** `routed --verify pre`
46/46 cost 292 tax **+14** · `--verify final` 46/46 cost 288 tax +10 ·
`--no-verifier` 46/46 cost 278 tax 0 · champion `solo` 46/46 cost 159
resolved 12 with **no verifier at all**. Frozen 20: pre 122 · final 120 ·
off 118 · solo 68. The per-task identity `cost(pre) − cost(off) ==
verifier_calls` holds on all 46 tasks (14 calls over 7 selected tasks = 4.79%
of the shipped arm; 0.304 calls/task).

**Ruling (pre-registered, applied as written):** `tax_pre = 14 ≠ 0` (not CUT)
· `U_pre = 19 ≠ 0` · `U_final = 18 ≠ 0` → clause 3 fails → **KEEP `pre`**. The
stage **stays**; the ablation is not licensed to delete it (a registered
no-CUT clause: the grader *is* the rule set the verifier re-runs, so zero
flips is instrument blindness, not worthlessness — new P15). `verify=final`
weakly dominates the shipped mode on every measured axis (cheaper, hole 1 → 0,
guarded 5 > 4, quality identical) and is **deliberately not adopted**: its
registered clause failed, and adopting it on the data that revealed the
clause's mis-specification is the failure the protocol blocks (new P18). It is
carried to R05 as a deferred trim with a `hole_deliveries`-based clause.

**Verdicts:** X1 CONFIRMED (exact, attributable tax) · X4 CONFIRMED (quality
invariant across modes) · X2 QUALIFIED (the hole is exactly one task, T23 —
the aggregate 19 mixed one hole with 18 never-selected deliveries; new P16) ·
X3 REFUTED as stated · X5 (the registered prediction of a REPLACE) FAILED, and
recorded as a miss for @edge · adversarial self-review `attacks=10 broken=0
ALL-HELD` (4 held, 6 held-with-limitation, all listed in FINDINGS-R04 §Threats).

**Not claimed:** nothing promoted (the ≤88-call bar still fails; champion
stays `solo --hold-on-vague`); the verifier's *detection value* is still
unpriced — this round prices the stage's cost and its coverage, not its
benefit; the T23 post-hop hole is a recorded defect whose one-line fix was
measured (+1 call on 46 tasks) and deliberately deferred, not fixed, so R05's
comparison stays interpretable (P17); the trigger question (5 of 7 invocations
come from estimated complexity, 18 deliveries never selected) is explicitly
out of scope and owed to R05; no generalization beyond the 17 synthetic
classes.

**Correction on the record:** the R03 append above names `BOARD-R03.md` as a
file that landed. No such file exists — R03's board section went into
`missions/ROUTER-V2/BOARD.md` directly, and its papers were mirrored as
`*-R03.md`. The frozen line is left exactly as written; this note is the
correction rather than an edit (same practice as the 2026-09-20 retracted
claim).
