# FINDINGS — mission ROUTER-V2, Round 03 (2026-09-22)

> Companion records: `PRE-REGISTRATION-R03.md` (sha256
> `1abb28538bb57f4f694b04851c61fbfd61558f7784a770f04fa4f5e1d384f706`, frozen
> before implementation and before any measurement), `logs/round-03-trial.txt`
> (verbatim arm output), `logs/r03-analysis.md` (GENERATED ruling + tables),
> `logs/round-03-postcut.txt` (post-ruling verification),
> `logs/round-03-adversarial.txt` (self-review),
> `logs/precut-sha256.txt` (the revision the trial measured),
> `ADR-ROUTER-V2-R03.md`, `DECISIONS-LOG.md`, `PRINCIPLES.md`.
>
> **Honesty header:** rule-based stack only; the model leg (torch + weights)
> never ran. Cost is a simulated tool-call proxy (per-run budget declared at
> 2000 calls; the highest arm spent 307). Grading is rule-based compliance
> against the fixture, not human judgment. n=46 expanded / 20 frozen.

## Mission

Close the two gaps R02 left open: the ADR-10 `routing_match` semantics defect
and the H5 class-table trial that R02 refuted with an arm that never ran the
ladder.

## What was built (Iron Law: RED → GREEN → measure)

- **RED witnessed first:** `14 failed, 4 passed` at 2026-09-22T07:07:08Z
  (`logs/RED-witness-r03.txt`), before any R03 production code.
- **GREEN:** `111 passed` (90 legacy + 21 new) — `logs/GREEN-witness-r03.txt`.
- **ADR-10 semantics:** `run_formation` now reports `planned` (the proposal) and
  `final` (derived from the stages that actually ran: meta→FULL, else
  researcher→PIPELINE, else verifier→DUO, else SOLO), plus `mismatch_reason`.
  `eval` records `proposed`/`used=final` per task, prints a
  `ROUTING-MISMATCH` line per mismatch, and counts mismatches per class in
  `RunLedger.mismatches()`/`summary()`.
- **A real ablation:** `routed-thresholds` used to run no ladder at all
  (hops=0, cost 70 on the frozen fixture — plain SOLO plus one risk-verifier).
  It now runs the same ladder and the same risk gate as `routed`, differing
  only in the first proposal's source (frozen threshold scorer).
- **Fairness fix:** every arm now spends through the same harness `Budget`
  (R02 let the ladder arms bypass it). Declared budget for R03: 2000 calls.
- **New reporting:** `hops` and `verifier_flips` in SUMMARY, and
  `--summary-json` so every table in this round is generated, not typed.
- **Expanded fixture:** `tasks/expanded-missions.json`, 46 tasks = the frozen
  20 verbatim + 26 new instances across the same 17 classes (12 PASS / 15 HOLD
  / 19 FLEX), sha256 `26b3b832…`. Validated before the freeze: the champion
  arm solves it 46/46 with grave=0.

## Results (seed 7 / authored order; verbatim in `logs/round-03-trial.txt`)

Frozen 20 (continuity, H10–H12):

| arm | passed | grave | resolved | cost | routing_match | hops |
|---|---|---|---|---|---|---|
| solo --hold-on-vague | 20/20 | 0 | 4 | 68 | 11/20 | 0 |
| routed (class table) | 20/20 | 0 | 9 | 127 | 19/20 | 15 |
| routed-thresholds (real ablation) | 20/20 | 0 | 9 | 122 | 11/20 | 25 |

Expanded 46 (primary endpoint, H13):

| arm | passed | grave | resolved | cost | resolved/100 calls | routing_match | hops | verifier_flips |
|---|---|---|---|---|---|---|---|---|
| solo --hold-on-vague | 46/46 | 0 | 12 | 159 | 7.55 | 23/46 | 0 | 0 |
| routed (class table) | 46/46 | 0 | 23 | 307 | 7.49 | 44/46 | 33 | 0 |
| routed-thresholds (real ablation) | 46/46 | 0 | 23 | 292 | 7.88 | 25/46 | 55 | 0 |

Per-class detail is generated in `logs/r03-analysis.md`. The table wins three
classes (external-source 28 vs 32, instruction-in-source 21 vs 24,
multi-source-synthesis 19 vs 26) and loses three (partial-grounding 44 vs 32,
truncation-severs-citation 42 vs 30, poisoned-source 22 vs 16); every other
class is identical in cost. Net: **+15 calls (+5.1%) for exactly the same 23
resolved deliveries.**

## The ruling (pre-registered rule, applied as written)

| clause | value | verdict |
|---|---|---|
| (a) routed.passed ≥ thresholds.passed | 46 vs 46 | HOLD |
| (b) routed.grave ≤ thresholds.grave | 0 vs 0 | HOLD |
| (c) routed.resolved > thresholds.resolved | 23 vs 23 | **FAIL** |
| (d) resolved/call strictly better | 0.07492 vs 0.07877 | **FAIL** |

**KILL.** The class table is deleted from the router (`crew/router.py`), with a
post-ruling verification (`logs/round-03-postcut.txt`, ALL-PASS) showing the
router exposes no table, that `routed` and `routed-thresholds` are now
behaviourally identical, and that the cut reproduces the ablation arm exactly
(122 calls frozen / 292 expanded, same 9 / 23 resolved). The pre-cut revision
that was measured is pinned by sha256 in `logs/precut-sha256.txt`.

## Hypothesis verdicts

| # | Verdict | Evidence |
|---|---|---|
| H10 | **CONFIRMED (scoped to the measured revision)** | Under ADR-10 the solo arm reported `routing_match=11/20` on the frozen fixture — the same value R02 published for that arm, so the fix changed routed-arm accounting only (trial log, frozen block). After the cut the live proposal source changed and the same arm reports 19/20; the claim is about the pre-cut revision (pinned), not about today's router |
| H11 | **CONFIRMED (scoped to the measured revision)** | The class-table arm reproduced R02 exactly: 20/20, grave 0, cost 127, resolved 9 (trial log). The cut then removed that arm by decree, which is the point of the ruling |
| H12 | **CONFIRMED** | The rebuilt ablation runs the ladder (hops 25 frozen / 55 expanded) and resolves as much as the table (9 / 23) at lower cost (122 / 292) |
| H13 | **RULED KILL** | Clauses (c) and (d) FAIL; see table above. The registered directional prediction (KILL) landed |
| H14 | **CONFIRMED** | Per-arm SUMMARY identical across seeds 7/11/13/17/19 (sd=0.000 on passed, resolved, cost, routing_match) and double-run stdout byte-identical for both ladder arms |
| H15 | **CONFIRMED** | Cost premium 307 > 292 with a resolved delta of 0 (≤ 2 as registered) |
| H16 | **CONFIRMED (non-vacuity controlled)** | `verifier_flips=0` on both ladder arms: no task's grading outcome changed because the verifier stage ran. A control suite drives a real flip (`tests/test_verifier_reachability.py`), so the zero is a measured absence, not a dead path |

Emergent (not pre-registered, recorded because it is the sharper lesson):
with the ADR-10 semantics **fixed**, the deleted table *wins* the metric 44/46
vs 25/46 — i.e. the new metric measures execution fidelity (how often the
proposal was the shape the task finished in), not value. A metric that can be
won by a mechanism that buys nothing must be labeled diagnostic, not promoted
to a bar (new P11).

## Threats to validity

- **Construct:** `verifier_flips=0` shows the verifier changed no grading
  outcome on this fixture — because the blind reviewer *is* the rule set that
  grades the run. The verifier's value is therefore unmeasurable here, and no
  claim is made that verification is worthless in general; only that this
  fixture cannot price it. Confirmation is a limitation of the instrument.
- **Internal:** the table and the risk gate read the same task signals; the
  ablation isolates the first proposal, not the whole routing pipeline.
- **External:** the expanded fixture was authored by the same operator who
  wrote the router, reuses the R02 class taxonomy, and is synthetic. Zero
  generalization beyond these 17 classes.
- **Statistical:** n=46; per-class cells are n=1–4 and are descriptive only.
  Wilson 95% CI on 46/46 is [0.923, 1.000], so the pass-rate comparison is
  saturated and carries no signal; the ruling rests on resolved and cost,
  which are counts, not estimates.
- **Bar construction:** the ≤88-call promotion bar was registered in R02 when
  `resolved` was not the primary endpoint. R03's data show the ladder buys +11
  resolved deliveries (+92%) for +133 calls on the expanded fixture — a trade
  the old bar cannot express. The bar is NOT changed post hoc; R04 must
  pre-register a resolved-per-cost bar with that reason on the record.
- **Ruling policy (surfaced by adversarial attack 3):** the keep rule's
  tie-break (equal resolved → KILL) is a *policy* frozen in advance, not a
  measurement. A mechanism that ties on value while winning calibration was
  cut by policy. This is declared rather than hidden; reversing it requires a
  pre-registered rule change, not a reinterpretation.

## Limitations (honest ceiling)

- The cut leaves one proposal mechanism, and its measured weakness is visible:
  `routed-thresholds` mismatches 21/46 (it under-proposes on every fetch class
  and pays the hop). The router that wins 44/46 no longer exists. That is the
  razor's price, and it is recorded rather than hidden.
- **Seed sweep scope (adversarial attack 9):** the five-seed sweep permutes
  task ORDER only, and this stack has no order-dependent state, so sd=0 is
  nearly tautological here. H14's real content is byte-stability; a stochastic
  leg (model, R05) will need a different protocol, and no seed-sensitivity
  claim is made for anything but order.
- The verifier tax is real but unpriced: R04 needs a `--no-verifier` ablation
  to measure what the verification floor costs and what it catches.
- FLEX classes that cannot be resolved at all (partial-grounding,
  truncation-severs-citation, poisoned-source) are pure cost for every arm;
  the ladder spends 30–44 calls per class-cell and resolves none of them.
  A feasibility-driven early stop for provably-ungroundable requirements is
  the obvious next mechanism — unbuilt, unmeasured, not claimed.
- `routed` is not promoted: the frozen-fixture cost bar (≤88) fails at 122.
  The champion remains `solo --hold-on-vague` (68).

## Adversarial self-review (2026-09-22, gate before close)

11 attacks on the confirmed verdicts, the ruling and the post-cut state, all
logged verbatim in `logs/round-03-adversarial.txt`:

- 5 HELD (executable where possible): stale-continuity scope, alias
  reproducibility, verifier-flip reachability (control suite), `final`
  accounting on receipts-only hops, and "keep the table only where it wins"
  (that is a new mechanism, deferred to ADR-12's reversal condition).
- 6 HELD-WITH-LIMITATION, each now written into §Threats/§Limitations above:
  authorship bias, the tie-break policy, the solvability-validation step, the
  tautological seed sweep, the synthetic cost currency, and the budget-cap
  choice (attack 4 confirmed the governor fails loudly: 18 budget-held rows at
  the historical cap of 100, none silent).
- Result: `REVIEW-SUMMARY attacks=11 broken=0 status=ALL-HELD`.

## Future work (pre-registered direction, R04+)

1. **Resolved-per-cost bar** (registered now, before R04 measures): the ladder's
   +11 resolved at +133 calls must be judged against a declared price per
   resolved delivery, not an absolute call cap.
2. **Verifier ablation** (`--no-verifier`): price the verification floor on the
   expanded fixture; if it catches nothing and costs ≥15%, cut or narrow it.
3. **Feasibility early-stop**: detect provably-ungroundable requirement sets
   before the ladder spends the hop, and measure the saving on the three
   FLEX classes that resolve nothing.
4. **Belief-ledger routing (R04 gate)**: the tracker now sees `final` vs
   `planned` per task (ADR-10), so priors can be derived from *mismatch*
   evidence rather than grades alone.
5. **Model leg (R05)**: only behind the Owner's gate; contracts unchanged.
