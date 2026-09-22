# PRE-REGISTRATION — ROUTER-V2, Round 04 (2026-09-22)

> **Frozen before implementation and before any measurement.** sha256 of this
> file goes to `logs/prereg-r04-sha256.txt` and the council board. No
> hypothesis, arm, or decision rule below may be edited afterwards; deviations
> become dated rows in `DECISIONS-LOG.md` with a reason.
>
> **Honesty header (unchanged):** stdlib-only, offline, deterministic rule-based
> executor. The model leg never ran; nothing here is a claim about LLM
> behaviour. "Cost" is a simulated tool-call count. Grading is rule-based
> compliance against the fixture.

## Mission (from the Owner's order)

Run the `--no-verifier` ablation on the 46-task fixture, measure the
verification stage's cost **exactly**, and decide whether it stays or is
trimmed. R03's H16 left one number on the table (`verifier_flips=0`) and one
open gap: the verifier's tax was never priced.

## Frozen inputs

| input | sha256 / value |
|---|---|
| frozen fixture (20) | `28406677825eeeb5489e7ea6fc60ee7a992e55ea0629f8348436052cfba59a87` |
| expanded fixture (46) | `26b3b832a2233693875b5b12e1093b4d55d0c019421f63bfbbebab3c417898c0` |
| inherited revision | round-03 sandbox (post-cut router, single threshold proposal); baseline witness `111 passed` at copy time |
| RED witness | `logs/RED-witness-r04.txt` — `11 failed` at 2026-09-22T07:27:19Z |
| carrier note | R04's `logs/` still holds R03's frozen `round-03-trial.txt` copy for the continuity tests; the canonical one lives in the round-03 sandbox |

## Structural census (read off the router's rules, before any R04 measurement)

The verification stage is invoked when the planned formation is
DUO/FULL/PIPELINE **or** when `risk_score >= 0.5`, and it runs **before** the
escalation ladder. Counted over the expanded fixture:

- planned formations: SOLO 41 · DUO 3 · PIPELINE 2
- formation-triggered verification: 5 tasks (T7, T21, T22, T23, T40)
- risk-gate-triggered verification: 2 tasks (T15, T45)
- overlap: none → **7 tasks verified**, stage cost 2 calls each → predicted tax
  **14 calls** on 46 tasks (frozen 20: 2 tasks, 4 calls)

This census is structural (derived from the router and the fixture, no arm was
run). It is the reason the round asks a *targeting* question as well as a
pricing one.

## Hypotheses (registered before measurement)

| # | Claim | Falsifier |
|---|---|---|
| X1 | The tax is exact and attributable: for every task, `cost(pre) - cost(off) == verifier_calls`, and `verifier_calls == 2` iff the stage ran, else 0; arm-level `verifier_calls == 2 × verifier_tasks` | any task where the identity fails |
| X2 | **The hole:** because the verifier runs before the ladder and the gate is one-way (DELIVER→HOLD), every delivery produced *by the escalation hop* is never verified. `unverified_deliveries(pre) > 0` on both fixtures | `unverified_deliveries(pre) == 0` (then the hole claim is false and X3's justification collapses to cost only) |
| X3 | The retarget (`verify=final`) guards the delivery actually returned: post-hop deliveries get verified, and verification is skipped where it provably cannot act (final verdict HOLD). `unverified_deliveries(final) == 0` and `verifier_calls(final) <= verifier_calls(pre)` | any unguarded delivery under `final`, or a higher tax than `pre` |
| X4 | No quality trade: passed, grave_errors and resolved are identical across `pre`, `final` and `off` on both fixtures | any difference (would falsify R03's H16 zero and must be reported as such) |
| X5 | Registered directional prediction: the ruling is **REPLACE `pre` with `final`** — tax falls (14 → predicted 10 calls on the expanded fixture) while the number of unguarded deliveries falls from >0 to 0 | the rule's fallback branch (KEEP `pre`) fires |

## Arms (fixed before measurement)

All arms `--hold-on-vague --max-tool-calls 2000`.

1. `routed --verify pre` — status quo (the configuration R02/R03 shipped).
2. `routed --verify off` (equivalently `--no-verifier`) — the Owner's ablation.
3. `routed --verify final` — the retarget candidate.
4. `solo --hold-on-vague` — declared: the champion arm runs **no verifier at
   all**, so the ablation is a no-op there and the tax measured in this round
   is the *ladder's* tax, not the system's. Reported, not hidden.
5. Both fixtures: the three modes × {routed} × {frozen 20 (seed 7), expanded 46
   (authored order)}; plus the champion arm for the standing comparison.
6. Variance sweep: seeds 7/11/13/17/19 for all three modes on the expanded
   fixture. Determinism: each mode run twice, stdout byte-identical.

## Analysis plan (declared)

- **Primary endpoint:** the ruling from the rule below, computed by
  `tools/run_trial_r04.py` from the three modes' SUMMARY blocks.
- **Tax accounting:** total `verifier_calls` per mode, per fixture, and per
  class; the delta against `off` is the *exact* price of the stage. All numbers
  generated into `logs/r04-analysis.md`.
- **Guard accounting:** `unverified_deliveries` per mode (the X2/X3 metric),
  and `verifier_flips` per mode.
- **Quality:** passed / grave / resolved / Wilson 95% CI per mode.
- **Per-task table:** the 7 trigger tasks and their `verified` flag under each
  mode, so the reader can see exactly which deliveries each mode guards.

## Decision rule (registered, mechanical, three-way)

Let `U_pre`, `U_fin` be `unverified_deliveries` under `pre` and `final`;
`tax_x = total_cost(x) − total_cost(off)`; `Q(x) = (passed, grave, resolved)`.

1. **CUT** iff `tax_pre == 0` (the stage is structurally dead). Not expected:
   the census says it fires on 7 tasks.
2. Else if `U_pre == 0` (X2 falsified): **KEEP `pre`** unless
   `Q(final) == Q(pre)` and `tax_final < tax_pre`, in which case adopt `final`
   as a pure cost saving.
3. Else (**X2 holds**): **REPLACE `pre` with `final`** iff
   `U_fin == 0` **and** `Q(final) == Q(pre)` **and** `tax_final <= tax_pre`.
   Otherwise **KEEP `pre`** and publish the failure of the retarget.

**No-CUT clause (registered explicitly):** `off` may never be chosen by this
rule. The instrument cannot price a benefit (the blind reviewer *is* the rule
set that grades the run, so `verifier_flips=0` is instrument blindness, not
proof of worthlessness). Deleting a safety mechanism on an instrument that
cannot price its benefit is forbidden; only *re-targeting it to measured
signals* is licensed. (Earned here, recorded as P15.)

## Out of scope (registered so it is not smuggled in later)

- **Trigger composition** (formation-implied vs wound signals). The census
  shows 5 of 7 invocations come from the estimated-complexity trigger, but
  choosing between trigger families needs its own pre-registered trial with a
  wound-signal definition; R05 may do it on new fixtures.
- **The champion's lack of verification.** `solo` verifies nothing. Whether the
  champion should carry a risk-gated check is a separate mechanism question and
  is not measured here.
- **Verifier detection value.** Unchanged: unpriced on this fixture.

## Promotion rule (unchanged from R02/R03)

Nothing is promoted this round: the ≤88-call bar on the frozen fixture still
fails (the ladder costs 122 calls there before any R04 change), and R04 does
not touch routing. The champion remains `solo --hold-on-vague`. The ladder's
gain is carried to the resolved-per-cost bar R04 registers for R05.

## Registered threats to validity

- The instrument-blindness argument (above) cuts both ways: it forbids CUT and
  it also means the retarget cannot be shown to *improve* safety — only to
  guard strictly more deliveries at no extra cost. That is the claim being
  tested: a superset of guarded deliveries, not a better verifier.
- `unverified_deliveries` is a structural count of "final verdict DELIVER and
  no verifier pass ran before the return"; it does not measure whether the
  verifier *would* have found something, which is unmeasurable here.
- The 46-task fixture is authored by the same operator as the router; zero
  generalization beyond its 17 synthetic classes.
- `verifier_calls == 2` is an implementation fact (blind regrade + brief
  crosscheck); if a future verifier grows, the identity in X1 must be restated.
