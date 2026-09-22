# BOARD — mission ROUTER-V2 (opened 2026-09-22)

Operator-session mission under the Owner's goal (recorded as such, per the
CREW-EVIDENCE precedent). Sandbox:
`~/.hermes/crew/experiment/runs/2026-09-22-router-round-02/`. Papers live
beside this board (`PRE-REGISTRATION.md`, `FINDINGS.md`, `PRINCIPLES.md`,
`ADR-ROUTER-V2.md`, `REPRO-PACK.md`, `DECISIONS-LOG.md`); the verbatim
measurement log is `runs/…/logs/round-02-routed.txt`.

## GOAL (owner: @architect)

Turn the round-01 cosmetic router into a real decision system — escalation
ladder, risk-stratified verification, cognition layer, structural guards —
under a full scientific protocol (pre-registration → RED → GREEN →
measurement → findings), without touching any protected tree.

## CONSTRAINTS (max 7 active)

1. Sandbox-only code changes; protected trees untouched (`PROTECTED.md`).
2. Iron Law: RED before GREEN; no "done" without RED ref + GREEN log + clean
   suite (TEST-POLICY §3).
3. Pre-registration frozen (sha256 `7e14c9d2…`) before any new measurement.
4. Counts are generated at read time; every number cites a command (CONSTITUTION §1).
5. Shadow arms never self-promote; priors propose, never apply (D1/D2 laws).
6. The model leg is out of scope — say so, never fake it.
7. No commit while the Owner has not ruled on promotion (two-writer rule).

## EVIDENCE (owner: @scout — append-only, cite sources)

- E1 · RED witnessed: `43 failed, 1 passed` at `runs/…/logs/RED-witness.txt`
  (2026-09-22T06:08:46Z) — the 43 RED tests define mechanisms A1–A6, B1,
  D1–D3, E1–E3, H1–H5, G2 before they existed.
- E2 · GREEN witnessed: `90 passed` at `runs/…/logs/GREEN-witness.txt`
  (2026-09-22T06:20:41Z) — 46 legacy + 44 new, zero regressions.
- E3 · Round-01 defect confirmed on disk: `runs/2026-09-21-router-round-01/
  crew/eval.py` lines 46–52 — `routed` declared then crashed; second `used`
  literal overwrote the router proposal.
- E4 · Measured matrix (seed 7, `logs/round-02-routed.txt`): solo+hold 20/20
  grave=0 cost=68 resolved=4 · routed(no-hold) 19/20 grave=1 cost=127
  resolved=9 · routed+hold 20/20 grave=0 cost=127 resolved=9 ·
  routed-thresholds 20/20 grave=0 cost=70 resolved=4.
- E5 · Variance sweep (seeds 7/11/13/17/19): both arms identical SUMMARY per
  seed set — sd=0. Determinism double-run: byte-identical PASS.
- E6 · Guard + cognition probes: guard_flags=2 (T17 refused, T19 flagged);
  T10/T12/T14 DELIVER stand; H9 debate cost_ratio=2.00x graves 0→0; H8
  high-bucket success 1.000 (n=8); apply_priors → PermissionError (gate
  holds); H4 cards empty on clean ledger (correct).

## OPEN GAPS (owner: @scout)

- routing_match semantics: mode-label vs proposal compared this round; must
  be proposed==final-formation from R03 (ADR-10).
- Class table currently fails its own cost/value test (H5 REFUTED, cost 127
  vs 70): kill-or-keep trial needed on a ≥40-task fixture.
- Error budget (D3) implemented + tested but not live-fired on an injected
  grave.
- Belief ledger not yet in the routing loop (R04).

## DECISIONS (owner: @architect — each cites ≥2 EVIDENCE rows)

- D1 (E2, E4): the ladder + hold-rule is quality-equivalent to the champion
  and 2.25x on resolved — but NOT promoted: cost bar (≤88) failed.
- D2 (E4, E5): champion remains `solo --hold-on-vague` (cost 68, sd=0).
- D3 (E1, E2): mechanisms ship only as locus+test pairs; all 44 new tests
  pinned; no assertion weakened (one test contract aligned to the honest
  `used=ROUTED` label — logged in DECISIONS-LOG).
- D4 (E6): guards stay; they cost nothing measurable on legitimate flows.
- D5 (E4, OPEN GAPS): class table goes on trial in R03 — show value on a
  bigger fixture or the razor cuts it (PRINCIPLES P7).

## BET MEMO (owner: @edge — plan stage only)

Registered pre-measurement in `~/crew-research-council/bets-ledger.md`
(2026-09-22 row): routed ≥ 20/20, grave=0, cost ≤ 88, routing ≥ 16/20,
hold-rule seed-stable, stack byte-deterministic. Outcome: quality/hold/
determinism legs landed; cost leg lost (127); routing leg lost (0/20 —
semantics flaw). Lesson queued for the ledger's outcome column.

## ARTIFACT + TEST RESULTS (owner: @ship — pointers, not prose)

- `runs/2026-09-22-router-round-02/crew/` — formations, escalation, handoffs,
  guards, cognition, expertise, router v2 + router_thresholds (frozen scorer),
  eval v2.
- `runs/…/tests/` — 90 tests green (46 legacy + 44 new).
- `runs/…/logs/round-02-routed.txt` — verbatim measurement log (arms, sweep,
  determinism, probes).
- `runs/…/logs/{RED,GREEN}-witness.txt`, `logs/fixture-sha256.txt`,
  `logs/prereg-sha256.txt` — witnesses and pins.
- `runs/…/expertise/ledger-round02.jsonl` — append-only tracker ledger.
- Papers: `missions/ROUTER-V2/*.md` (mirrored from the sandbox `missions/`).

## ADVERSARIAL SELF-REVIEW (2026-09-22, post-measurement — gate before close)

11 attacks on the CONFIRMED verdicts, logged verbatim in
`runs/…/logs/round-02-routed.txt`:

- 1 real mechanism break found and FIXED: `handoffs.hop()` could grow a
  packet when the caller passed more gaps than the receipt carried — the
  shrink law (B1) is now structural (intersect with carried knowledge;
  new information requires a new receipt). Tests still 90/90 after the fix.
- 3 probe mis-specifications (review code asserted the inverse of the
  contract on H2; one NameError) — probes corrected, mechanisms untouched;
  both corrections are on the record here, not silently dropped.
- Result: `REVIEW-SUMMARY attacks=11 broken=0 status=ALL-HELD`.

# ROUND 03 (2026-09-22) — ADR-10 semantics fixed; class table CUT (H13 KILL)

Sandbox: `~/.hermes/crew/experiment/runs/2026-09-22-router-round-03/`. Papers:
`PRE-REGISTRATION-R03.md` (sha256 `1abb2853…`, frozen before code and before
measurement), `FINDINGS-R03.md`, `ADR-ROUTER-V2-R03.md`, `REPRO-PACK-R03.md`,
and the superseding `PRINCIPLES.md` (adds P11–P14) and `DECISIONS-LOG.md`
(adds the 12 R03 rows).

## GOAL-R03 (owner: @architect)

Apply the ADR-10 `routing_match` semantics fix and run the class-table trial on
a ≥40-task fixture so H5 either completes or dies — under the same scientific
protocol, with the ruling's consequence pre-committed in writing.

## CONSTRAINTS-R03 (max 7 active)

1. Sandbox-only changes; protected trees untouched; R02's frozen records left
   byte-identical (this append was diff-verified).
2. Iron Law: RED (`14 failed, 4 passed`) before any R03 production code.
3. Pre-registration frozen (sha256 `1abb2853…`) before code and measurement.
4. Counts generated at read time (`tools/run_trial_r03.py` →
   `logs/r03-analysis.md`); no hand-typed number in any report.
5. The pre-committed consequence binds: KILL means the code is deleted.
6. The model leg stays out of scope; no LLM-behaviour claim.
7. The ≤88 promotion bar is not rewritten after the fact.

## EVIDENCE-R03 (owner: @scout — append-only, cite sources)

- E7 · RED witnessed `14 failed, 4 passed` (2026-09-22T07:07:08Z,
  `logs/RED-witness-r03.txt`); GREEN `111 passed` (`logs/GREEN-witness-r03.txt`)
  after the cut and the control suite.
- E8 · Expanded fixture on disk: 46 tasks, 17 classes, 12 PASS/15 HOLD/19 FLEX,
  sha256 `26b3b832…`; the frozen 20 appear verbatim as its first 20 entries.
- E9 · Real ablation confirmed: `routed-thresholds` now runs the ladder
  (hops 25 frozen / 55 expanded) instead of the R02 arm's hops=0.
- E10 · Measured matrix (expanded): solo 46/46 cost 159 resolved 12 · table
  `routed` 46/46 cost 307 resolved 23 · ablation 46/46 cost 292 resolved 23;
  frozen 20: solo 68/4, table 127/9, ablation 122/9 (R02's table number
  reproduced exactly).
- E11 · H13 ruling generated: clauses (c) and (d) FAIL → **KILL**
  (`logs/r03-analysis.md`).
- E12 · Cut verified on the live revision: no `CLASS_TABLE`, the two ladder
  arms behave identically, post-cut numbers equal the ablation arm's
  (`logs/round-03-postcut.txt`, ALL-PASS).
- E13 · Self-review `attacks=11 broken=0 status=ALL-HELD`
  (`logs/round-03-adversarial.txt`); six of them are HELD-WITH-LIMITATION and
  are written into FINDINGS-R03 §Threats/§Limitations.
- E14 · Pre-cut revision pinned by sha256 (`logs/precut-sha256.txt`) and the
  trial log left untouched (sha printed by the post-cut check) so the ruling's
  evidence stays auditable (P14).

## OPEN GAPS-R03 (owner: @scout)

- Verifier value unpriced: `verifier_flips=0`; needs a `--no-verifier`
  ablation to measure the tax's price (R04).
- Ungroundable FLEX classes (partial-grounding, truncation-severs,
  poisoned-source) resolve nothing while costing 30–44 calls per class-cell:
  a feasibility early-stop is unbuilt and unmeasured.
- Belief-ledger routing still not in the loop; the tracker now sees
  `final` vs `planned`, so mismatch-derived priors are possible (R04 gate).
- The promotion bar itself: R04 must pre-register a resolved-per-cost bar
  before measuring.
- Error budget (D3) still not live-fired on an injected grave (carried from R02).

## DECISIONS-R03 (owner: @architect — each cites ≥2 EVIDENCE rows)

- D6 (E10, E11): the class table is CUT (clauses c/d failed) — the ruling was
  mechanical, not discretionary.
- D7 (E12, E14): the cut ships with a verification and a hash-pinned pre-cut
  revision; a ruling without its deletion is a memo (new P13/P14).
- D8 (E10, E11): `routing_match`, now meaningful, is labeled **diagnostic** —
  the cut table won it 44/46 vs 25/46 while resolving the same 23 tasks
  (new P11).
- D9 (E9, E10): ablation arms must exercise the mechanism under test; R02's
  H5 refutation is superseded, not merely re-confirmed (new P12).
- D10 (E1, E13): the champion stays `solo --hold-on-vague`; the ladder's
  +11 resolved at +133 calls is a real gain against a bar that cannot express
  it — carried to R04, not resolved by editing the bar now.

## BET MEMO-R03 (owner: @edge — plan stage only)

Registered pre-measurement in `~/crew-research-council/bets-ledger.md`
(2026-09-22 R03 row, ahead of the trial): ADR-10 continuity reproduces solo
11/20; the table arm reproduces R02 on the frozen fixture; the rebuilt ablation
runs the ladder; **H13 predicts KILL**; expanded arms seed-stable and
byte-deterministic. Outcome: all legs landed, including the registered KILL
prediction. Lesson: when a mechanism's value claim rests on an arm that never
ran it, the re-trial usually costs more than the mechanism can pay.

## ARTIFACT + TEST RESULTS-R03 (owner: @ship — pointers, not prose)

- `runs/2026-09-22-router-round-03/crew/` — `router.py` (post-cut: single
  threshold proposal), `formations.py` (planned/final/mismatch/verifier_flips),
  `eval.py` (symmetric budget, summary-json, mismatch lines),
  `harness/state.py` (mismatch ledger).
- `runs/…/tests/` — 111 green (90 legacy + 19 R03 + 2 control).
- `runs/…/tools/` — `run_trial_r03.py`, `verify_postcut_r03.py`,
  `adversarial_r03.py`.
- `runs/…/logs/` — `round-03-trial.txt`, `r03-analysis.md`,
  `round-03-postcut.txt`, `round-03-adversarial.txt`,
  `{RED,GREEN}-witness-r03.txt`, `precut-sha256.txt`, `fixture-sha256.txt`,
  `prereg-r03-sha256.txt`, `artifacts-sha256.txt`.
- Generated surface: `crew-research-council/leaderboard.md` (regenerated by
  `tools/gen_leaderboard.py`, which now reads both round logs).

# ROUND 04 (2026-09-22) — the verification stage priced exactly; it STAYS

Sandbox: `~/.hermes/crew/experiment/runs/2026-09-22-router-round-04/`. Papers:
`PRE-REGISTRATION-R04.md` (sha256 `ad9451ce…`, frozen before code and before
measurement), `FINDINGS-R04.md`, `ADR-ROUTER-V2-R04.md`, `REPRO-PACK-R04.md`,
and the superseding `PRINCIPLES.md` (adds P15–P18) and `DECISIONS-LOG.md`
(adds the 13 R04 rows).

## GOAL-R04 (owner: @architect)

Run the `--no-verifier` ablation on the 46-task fixture, measure the
verification stage's price **exactly**, and decide whether it stays or is
trimmed — without deleting a safety mechanism on an instrument that cannot
price its benefit.

## CONSTRAINTS-R04 (max 7 active)

1. Sandbox-only changes; protected trees untouched; R02/R03 frozen records left
   byte-identical (both appends diff-verified against pre-write copies).
2. Iron Law: RED (`11 failed`) before any R04 production code.
3. Pre-registration frozen (sha256 `ad9451ce…`) before code and measurement;
   the decision rule is mechanical and three-way.
4. Counts generated at read time (`tools/run_trial_r04.py` →
   `logs/r04-analysis.md`; `tools/ablation_no_verifier_r04.py` →
   `logs/r04-no-verifier-ablation.txt`); no hand-typed number in any report.
5. `off` may never be chosen by the ruling (registered no-CUT clause).
6. The model leg stays out of scope; no LLM-behaviour claim.
7. No promotion, and the ≤88 bar is not rewritten after the fact.

## EVIDENCE-R04 (owner: @scout — append-only, cite sources)

- E15 · RED witnessed `11 failed` (2026-09-22T07:27:19Z,
  `logs/RED-witness-r04.txt`); GREEN `126 passed`
  (`logs/GREEN-witness-r04.txt`) — 111 inherited + 13 R04 + 2 control.
- E16 · Structural census frozen before measurement: 7 of 46 tasks are selected
  for verification (5 by planned formation, 2 by the risk gate, no overlap) →
  predicted tax 2 × 7 = 14 calls; frozen 20 → 2 tasks, 4 calls.
- E17 · Measured modes (expanded 46): `pre` cost 292 tax **+14** · `final`
  288 tax +10 · `off` 278 tax 0; frozen 20: 122 / 120 / 118; champion
  `solo --hold-on-vague` 46/46 cost 159 with `verifier_calls=0` (it runs no
  verification mechanism at all).
- E18 · Exactness: the per-task identity `cost(pre) − cost(off) ==
  verifier_calls` holds on all 46 tasks (14 = 7 × 2); the tax is 4.79% of the
  shipped arm and 0.304 calls/task. Reproduced independently through the
  literal `--no-verifier` alias (`logs/r04-no-verifier-ablation.txt`, sha256
  `b6d07e83…`): aggregate identical, outcomes identical.
- E19 · Coverage, decomposed (selection vs guarding): `pre` guards 4 deliveries
  with **1 hole** (T23, selected then replaced by an escalation hop) and 18
  never-selected deliveries; `final` guards 5 with 0 holes; `off` has 5 holes.
  Quality is identical in all three modes — 46/46 passed, grave 0, resolved 23,
  `verifier_flips=0` (frozen 20 too: 20/20, 0, 9).
- E20 · Ruling generated (`logs/r04-analysis.md`): `tax_pre ≠ 0` and
  `U_pre = 19 ≠ 0` and `U_final = 18 ≠ 0` → **KEEP `pre`** (the registered
  fallback: the retarget failed its clause).
- E21 · Self-review `attacks=10 broken=0 status=ALL-HELD`
  (`logs/round-04-adversarial.txt`); six are HELD-WITH-LIMITATION and are
  written into FINDINGS-R04 §Threats/§Limitations.
- E22 · Determinism and variance: sd=0.000 across seeds 7/11/13/17/19 for all
  three modes, byte-identical double runs per mode.

## OPEN GAPS-R04 (owner: @scout)

- Trigger composition is now the biggest open question: 18 of the 19
  unguarded deliveries in `pre` were never selected (5 of 7 invocations come
  from estimated complexity). Needs its own pre-registered trial with a
  wound-signal definition (R05).
- `verify=final` is a measured, unadopted deferred trim: R05 must re-register
  the corrected clause (`hole_deliveries(final) == 0`, strictly fewer holes,
  quality unchanged, tax not rising) on a fixture not used to define it.
- The T23 post-hop hole is a recorded defect with a measured fix price (+1 call
  on 46 tasks, +0 on 20), deliberately unfixed so R05's comparison stays
  interpretable (P17).
- The champion verifies nothing: a risk-gated check for `solo` is unbuilt and
  unmeasured.
- Resolved-per-cost promotion bar still owed (carried from R03); error budget
  (D3) still not live-fired (carried from R02).

## DECISIONS-R04 (owner: @architect — each cites ≥2 EVIDENCE rows)

- D11 (E17, E18): the verification stage **stays** at its current scope. The
  price is exact, bounded and attributable; the ablation licenses no cut, and
  widening the trigger is an arithmetic +92 calls for the same unmeasured
  benefit (new P15).
- D12 (E19, E20): `verify=final` is NOT adopted despite dominating on every
  measured axis — it failed the clause frozen before the data, so it is a
  deferred trim with a corrected metric and clause (new P18).
- D13 (E15, E19): the coverage metric is decomposed (hole vs unselected) after
  X3 was refuted on the aggregate; the split is marked exploratory, is not used
  in the ruling, and the pre-registered aggregate is still reported (new P16).
- D14 (E16, E21): nothing is promoted; the champion stays
  `solo --hold-on-vague` and the resolved-per-cost bar is registered for R05
  rather than set by the round that wants to pass it.

## BET MEMO-R04 (owner: @edge — plan stage only)

Registered pre-measurement in `~/crew-research-council/bets-ledger.md`
(2026-09-22 R04 row, ahead of the trial): the tax is exactly 2 calls per
verified task (7 of 46 → 14 calls); the gate has a hole (`unverified_deliveries
(pre) > 0`); `verify=final` closes it at no extra cost; and — the directional
leg — the ruling would be **REPLACE `pre` with `final`**. Outcome: three legs
landed (exact tax, a hole exists, `final` is cheaper and closes it) and the
directional leg **MISSED** (KEEP `pre`), because the hole turned out to be one
task rather than the aggregate. Recorded as a miss on @edge's track record.

## ARTIFACT + TEST RESULTS-R04 (owner: @ship — pointers, not prose)

- `runs/2026-09-22-router-round-04/crew/formations.py` — verification modes
  (`pre`/`final`/`off`) with a single trigger helper and per-task
  selection/guard reporting.
- `runs/…/crew/eval.py` — `--verify pre|final|off`, `--no-verifier` alias
  (one code path), verification fields in every SUMMARY and ledger row.
- `runs/…/tests/` — 126 green (111 inherited + 13 R04 + 2 control).
- `runs/…/tools/` — `run_trial_r04.py`, `ablation_no_verifier_r04.py`,
  `adversarial_r04.py`.
- `runs/…/logs/` — `round-04-trial.txt` (sha256 `64ac515d…`), `r04-analysis.md`
  (sha256 `6ec17759…`), `r04-no-verifier-ablation.txt` (sha256 `b6d07e83…`),
  `round-04-adversarial.txt`, `{RED,GREEN}-witness-r04.txt`,
  `prereg-r04-sha256.txt`, `prewrite/` (pre-append board copies used for the
  frozen-region diffs).
- Generated surface: `crew-research-council/leaderboard.md` (regenerated by
  `tools/gen_leaderboard.py`, which now reads all three round logs).
