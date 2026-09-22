# PRE-REGISTRATION — ROUTER-V2, Round 03 (2026-09-22)

> **Frozen before implementation and before any measurement.** sha256 of this
> file is recorded in `logs/prereg-r03-sha256.txt` and appended to the council
> board. No hypothesis, bar, arm, or decision rule below may be edited after
> this freeze; deviations go in `DECISIONS-LOG.md` as dated rows with a reason.
>
> **Honesty header (unchanged from R02):** stdlib-only, offline, deterministic
> rule-based executor. The model leg (torch + weights) never ran and nothing
> here is a claim about LLM behavior. "Cost" is a simulated tool-call count,
> not tokens or wall-clock. Grading is rule-based compliance against the
> fixture, not human judgment.

## Mission

Close the two open gaps R02 handed to R03 (`FINDINGS.md` §Limitations):

1. **ADR-10 — routing_match semantics.** R02 compared a static mode label
   (`used=ROUTED`) against the router's proposal, so the metric measured
   nothing about routing. R03 must define it as *proposal vs the formation the
   task actually finished in*, re-measure, and re-report.
2. **H5 — class-table trial.** R02 REFUTED the class table, but its
   counter-arm (`routed-thresholds`) ran **no ladder at all** (hops=0, cost 70
   = plain SOLO + one risk-verifier). That arm could not falsify anything
   about the class table. R03 re-runs the trial with a *real* ablation on a
   fixture of ≥40 tasks and either keeps or cuts the class table.

## Frozen inputs

| Input | sha256 | Note |
|---|---|---|
| `tasks/real-missions.json` (20 tasks) | `28406677825eeeb5489e7ea6fc60ee7a992e55ea0629f8348436052cfba59a87` | byte-identical to the R02 pin; T1–T20 appear verbatim as the first 20 entries of the expanded fixture |
| `tasks/expanded-missions.json` (46 tasks) | `26b3b832a2233693875b5b12e1093b4d55d0c019421f63bfbbebab3c417898c0` | 17 classes, 12 PASS / 15 HOLD / 19 FLEX; authored locally, no external data |
| RED witness `logs/RED-witness-r03.txt` | — | `14 failed, 4 passed` at 2026-09-22T07:07:08Z, before any R03 production code |

The expanded fixture was validated **before** the trial: the champion arm
(`solo --hold-on-vague`) solves it 46/46 with grave=0 (`logs/` measurement is
run after freeze; the pre-freeze sanity value is recorded in DECISIONS-LOG as
fixture-authoring evidence, not as a result).

## Definitions (ADR-10, frozen here)

- `planned` = the formation the router proposed for this task, before dispatch.
- `final` = the formation the task *finished in*, derived structurally from the
  stages that actually ran: `meta`→FULL, else `researcher`→PIPELINE, else
  `verifier`→DUO, else SOLO. A ladder grounding hop counts as a `researcher`
  stage; the derivation reads stages, never intentions.
- `routing_match` = count of tasks where `planned == final`.
- `mismatch_reason` = `escalated:research-hop` when the ladder's hop changed the
  formation; `risk-verifier` when the risk gate added verification.
- For non-routed arms (`solo`, `duo`, `team`) `final` is the arm's own
  formation, so their `routing_match` is unchanged in meaning from R01/R02.

## Hypotheses (registered before measurement)

| # | Hypothesis | Falsifier |
|---|---|---|
| H10 | Under ADR-10 semantics the `solo` arm's routing_match on the frozen fixture is exactly **11/20** — reproducing the value R02 reported for that arm, proving the fix changes only routed-arm accounting | any other value, or any `used` value outside {SOLO,DUO,PIPELINE,FULL} |
| H11 | Refactor fidelity: the class-table `routed` arm on the frozen fixture still yields passed=20, grave=0, cost=127, resolved=9 exactly as in R02 | any of the four numbers differs |
| H12 | The re-built `routed-thresholds` arm is a real ablation: it runs the same ladder (hops ≥ 1 on fetch classes) and reaches passed=20, grave=0, resolved ≥ 9 on the frozen fixture | hops = 0, or resolved < 9, or it consults `CLASS_TABLE` |
| H13 | **Primary — the H5 ruling on the expanded fixture (46 tasks).** KEEP the class table **iff all four** hold: (a) `routed.passed ≥ thresholds.passed`; (b) `routed.grave ≤ thresholds.grave`; (c) `routed.resolved > thresholds.resolved`; (d) `routed.resolved/routed.cost > thresholds.resolved/thresholds.cost`. **Otherwise KILL** (equal resolved is a KILL by the razor: an unused mechanism is deleted, PRINCIPLES P7) | the rule above inverted, i.e. any KEEP clause failing while the table is retained |
| H14 | Seed stability on the expanded fixture: for each arm the SUMMARY is identical across seeds 7/11/13/17/19 and a repeated run is byte-identical | any per-seed difference in passed/grave/cost/resolved, or any byte difference between repeated runs |
| H15 | Cost premium, not quality premium: on the expanded fixture `routed.cost > thresholds.cost` while `resolved` differs by ≤ 2 — the table pays a premium for a speculative research stage | cost premium ≤ 0 |
| H16 | Verifier tax: on the expanded fixture `verifier_flips == 0` for both ladder arms (no task's grading outcome changes because the verifier stage ran) — the verification tax is real, its detection value is unmeasurable on this fixture | any arm reports `verifier_flips ≥ 1` |

## Registered directional prediction (scored, not gated)

Proposed by the operator before the run, from R02 evidence and the ladder's
structure: **H13 resolves to KILL.** Reasoning: the ladder's grounding hop
already buys the resolved deliveries that the class table pays a *speculative*
research stage for, and R02 measured the table's premium at +57 calls for zero
resolved gain. This prediction does not affect the H13 rule; it is scored after.

## Arms (fixed before measurement)

All arms use `--hold-on-vague`. Expanded runs and frozen-20 runs both use
`--max-tool-calls 2000`: the harness budget is **per run**, not per task, and
the expanded fixture needs 159 calls for the champion alone; 2000 is a safety
net no arm approaches. (R02's default of 100 was never reached because the
ladder arms bypassed the governor — a fairness defect fixed in R03: every arm
now spends through the same `Budget`.)

1. `solo --hold-on-vague --max-tool-calls 2000` — champion reference, no shuffle on the expanded fixture (the fixture's authored order is the seed).
2. `routed --hold-on-vague` — class table + ladder.
3. `routed-thresholds --hold-on-vague` — frozen threshold scorer + **the same ladder** (the real ablation).
4. Seeds: arms 1–3 across `--shuffle-seed 7, 11, 13, 17, 19` on the expanded fixture; arm 1 with seed 7 on the frozen fixture for continuity.
5. Determinism: arms 2 and 3 run twice; stdout must be byte-identical.
6. Frozen-fixture continuity for all three arms (H10–H12).

## Analysis plan (declared)

- **Primary endpoint:** the H13 ruling (KEEP/KILL) computed from the expanded
  fixture's three SUMMARY lines at the authored order; reported with the four
  clause values side by side.
- **Secondary:** passed, grave_errors, resolved, total_cost, resolved-per-100-calls,
  routing_match, and the mismatch class histogram from `RunLedger.mismatches()`.
- **Per-class table:** for each of the 17 classes, the arm verdicts and costs on
  the expanded fixture (generated from the logs, never hand-written).
- **Paired comparison:** task-level arm-vs-arm verdict/cost deltas on the same
  46 tasks; discordant task count reported where arms differ.
- **Wilson 95% CI** for pass rates on n=46.
- **Variance:** per-arm per-seed SUMMARY table; sd of passed and cost across the
  5 seeds (expected 0 under H14).

## Decision consequences (pre-committed, both directions)

- **If H13 = KEEP:** the class table stays, `routed` is re-measured with the
  corrected semantics, and R04 works on routing the table from the belief
  ledger's priors. The ladder's premium is then justified by the resolved gain.
- **If H13 = KILL:** `CLASS_TABLE` is **removed from the router** in this round
  (the razor's deletion rule): `route()` keeps the threshold fallback, the
  ladder stays, and the frozen scorer becomes the single proposal source. The
  cut is recorded in ADR-11 and DECISIONS-LOG with the failing clause. No code
  is left behind "just in case"; the table's history stays in the papers.
- **Promotion rule (unchanged from R02):** `routed` or `routed-thresholds` may
  be recorded as champion only if it holds passed=20/20, grave=0 on the frozen
  fixture AND costs ≤ 88 calls there. Otherwise the champion stays
  `solo --hold-on-vague` (cost 68). Shadow arms still never self-promote.

## Registered threats to validity

- **Construct:** the verifier cannot add detection value on this fixture because
  the blind reviewer *is* the rule set that grades the run — H16 measures that
  limitation rather than assuming it away. Cost is simulated tool calls.
- **Internal:** the class table and the risk gate both read the same task
  signals, so H13's attribution is confounded between "table" and "verifier on a
  table-routed class". The ablation isolates the *first proposal* only.
- **External:** the expanded fixture is authored by the same operator who wrote
  the router; its 26 new instances reuse the R02 class taxonomy. Zero
  generalization beyond these 17 classes is claimed.
- **Statistical:** n=46; class-level cells have n=1–2, so per-class numbers are
  descriptive only, never tested.
- **Authoring:** the expanded fixture was validated for solvability by the
  champion arm before the freeze; that validation cannot falsify H13 and is
  declared here as fixture evidence.
