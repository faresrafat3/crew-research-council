# FINDINGS — mission ROUTER-V2, Round 04 (2026-09-22)

> Companion records: `PRE-REGISTRATION-R04.md` (sha256
> `ad9451cefd805d9567f5852eefb98d7d1683b11cffef94b524009fa740599717`, frozen
> before implementation and measurement), `logs/round-04-trial.txt` (verbatim
> arms), `logs/r04-analysis.md` (GENERATED ruling + tax/coverage tables),
> `logs/round-04-adversarial.txt` (self-review), `logs/RED-witness-r04.txt`,
> `logs/GREEN-witness-r04.txt`, `ADR-ROUTER-V2-R04.md`, `DECISIONS-LOG.md`,
> `PRINCIPLES.md`.
>
> **Honesty header:** stdlib-only, offline, rule-based executor; the model leg
> never ran. Cost is simulated tool calls. Grading is rule-based compliance
> against the fixture. n=46 expanded / 20 frozen.

## The question the Owner asked

Run the `--no-verifier` ablation on the 46-task fixture, measure the
verification stage's price **exactly**, and decide whether it stays or is
trimmed.

## The answer

**It stays — priced at exactly 14 calls of 292 (4.8%) on the expanded fixture
and 4 of 122 (3.3%) on the frozen one — and it buys nothing measurable on this
instrument.** Trimming or cutting it is *not* licensed by this round's
evidence, and the reason is structural, not a matter of taste: the blind
reviewer that grades every run **is** the rule set the verifier re-runs, so
`verifier_flips = 0` in every mode is instrument blindness, not proof of
worthlessness. Removing a safety mechanism on an instrument that cannot price
its benefit would be a value claim we cannot support (new P15).

## The exact price

Frozen before measurement the trigger's census (structural, from the router's
rules): 7 of 46 tasks selected (5 by planned formation, 2 by the risk gate,
no overlap) → 2 calls per pass → 14 predicted. Measured, with the per-task
identity `cost(pre) − cost(off) == verifier_calls` holding on **all 46 tasks**:

| mode | verifier_calls | verifier_tasks | cost | cost above `off` | share of arm cost |
|---|---|---|---|---|---|
| `pre` (status quo, shipped) | 14 | 7 | 292 | +14 | 4.79% |
| `final` (retarget candidate) | 10 | 5 | 288 | +10 | 3.47% |
| `off` (the ablation) | 0 | 0 | 278 | 0 | — |

Frozen 20 (seed 7): `pre` +4 (tasks T7, T15) of 122 = 3.28%; `off` 118.

The price is concentrated in four classes (2 calls each): needs-verification
(T7, T21, T22), multi-source-synthesis (T23), correction-handling (T40),
source-conflict (T15, T45). Per-class tables: `logs/r04-analysis.md`.

**Scope of "exact" (threat 4 of the self-review):** the figure prices the
*passes*. A verifier that rejects a delivery can also trigger a repair hop, and
that hop's cost would be part of the mechanism's true price — but
`verifier_flips = 0` in every mode, so no hop was caused by verification here
and the total price is exactly the pass count. On a fixture where a rejection
occurs, the price would include the repair hop.

## Quality: no measurable effect in either direction

| arm | passed | grave | resolved | verifier_flips |
|---|---|---|---|---|
| `routed --verify pre` | 46/46 | 0 | 23 | 0 |
| `routed --verify final` | 46/46 | 0 | 23 | 0 |
| `routed --verify off` | 46/46 | 0 | 23 | 0 |
| `solo --hold-on-vague` (champion) | 46/46 | 0 | 12 | 0 |

Identical in every mode on both fixtures. So the honest summary is
two-sided: **the stage buys nothing measurable, and removing it costs nothing
measurable** — the instrument cannot distinguish them (P15).

## Coverage: the finding that replaced my hypothesis

The round's registered X2/X3 were about a *timing hole*: because the gate is
one-way (DELIVER→HOLD) and `pre` runs it before the ladder, a delivery produced
by the escalation hop is never verified. Measured precisely, with a
selection/guard decomposition added after the fact and labeled as such:

| mode | guarded deliveries | hole (selected, unguarded) | unselected (trigger never chose) | unverified total |
|---|---|---|---|---|
| `pre` | 4 | **1** (T23) | 18 | 19 |
| `final` | 5 | **0** | 18 | 18 |
| `off` | 0 | — | 23 | 23 |

- **X1 CONFIRMED** — the tax identity holds per task; the price is exact.
- **X2 QUALIFIED** — a hole exists, but it is *exactly one task* (T23,
  multi-source-synthesis) on the expanded fixture and **zero** on the frozen
  one. The pre-registered metric (`unverified_deliveries(pre) > 0`) was
  satisfied largely by deliveries the trigger never selected, which is not a
  hole. That metric conflated two different facts; the round's headline
  number, 19, would have been misread without the decomposition.
- **X3 REFUTED as stated** — the registered clause was
  `unverified_deliveries(final) == 0`; measurement returns **18**, all of them
  unselected. The trigger, not the timing, bounds coverage.
- **X4 CONFIRMED** — quality is invariant across modes (the R03 H16 zero was
  not wrong).
- **X5 (registered directional prediction) FAILED** — I predicted the ruling
  would be REPLACE `pre` with `final`. The registered rule's fallback fired
  instead: KEEP `pre`. Recorded as a miss for @edge's track record.

## The ruling (registered rule, applied as written)

`tax_pre = 14 ≠ 0` (so not CUT) · `U_pre = 19 ≠ 0` (so not X2-falsified) ·
`U_final = 18 ≠ 0` → clause 3 fails → **KEEP `pre`**.

`--verify final` is not adopted. It weakly dominates `pre` on every measured
axis (tax 10 < 14; hole 1 → 0; guarded 5 > 4; quality identical), and adopting
it now would be a post-hoc edit of the rule that was frozen before the data —
the exact failure mode this protocol exists to block. It is deferred to R05
with a **corrected clause** and, critically, with the metric fixed in code so
the corrected clause can be stated precisely:

- R05 clause (to be pre-registered before measuring): REPLACE `pre` with
  `final` iff `hole_deliveries(final) == 0` **and**
  `hole_deliveries(final) < hole_deliveries(pre)` **and** quality is unchanged
  **and** the tax does not rise **and** the corrected metric is applied to a
  fixture not used to define it.

## Two things this round exposed that nobody asked about

1. **The champion verifies nothing.** `solo --hold-on-vague` runs no verification
   mechanism at all: 12 deliveries on the expanded fixture, 12 unverified. The
   ladder's 4.8% tax is therefore not comparable to the champion's zero — the
   champion is cheap partly because it never asks a second opinion. Any future
   claim that "the ladder costs more" must carry that asymmetry (it is now in
   the generated champion row: `logs/r04-analysis.md`).
2. **Coverage is a trigger question, not a timing question.** 18 of the 19
   unguarded deliveries in `pre` were never selected. Whether the trigger
   (planned formation or `risk >= 0.5`) is the right trigger is the larger
   decision; R03's census already showed 5 of 7 invocations came from the
   estimated-complexity side. R05 owns that trial; this round deliberately
   refuses to smuggle it in.

## Threats to validity

- **Instrument blindness (the central caveat).** `verifier_flips = 0` reflects
  that the grader and the verifier share a rule set. The verifier's detection
  value is unpriced, and this round pays for a floor it cannot evaluate. It also
  forbids the flattering reading: "zero flips" is not evidence the verifier is
  useless.
- **Metric mis-specification (self-inflicted).** X2/X3 were specified against a
  metric that mixed *unselected* with *hole* deliveries. The decomposition was
  introduced after the refutation, is marked exploratory, and is not used in
  the ruling; it exists so R05 can register the corrected clause against new
  fixtures instead of re-scoring this round's data.
- **n=1 hole.** "Exactly one task" is a count on a synthetic fixture, not a
  rate. The frozen fixture has zero. The structural claim (a selected delivery
  can escape the guard) is what generalizes; the count does not.
- **Cost currency.** Simulated tool calls; no token or wall-clock claim. The
  tax is a share of a synthetic budget.
- **Arm asymmetry, declared.** The 14-call tax is the *ladder's*; the champion
  has no verifier to price. `--verify` is a no-op on non-ladder arms.
- **Authoring.** Fixture and router share an author; 17 synthetic classes; zero
  generalization claimed.

## Limitations (honest ceiling)

- The trigger composition question (planned formation vs wound signals vs risk
  threshold) is **not** answered here and was declared out of scope before
  measuring. Its evidence base is R03's census plus this round's 18 unselected
  deliveries.
- `verify=final` ships as an unadopted measurement mode, exercised by the suite
  and kept because R05's registered trial runs it (same pattern as R03's
  `routed-thresholds`).
- The seed sweep still permutes task order only; sd=0 remains nearly
  tautological for this stack (carried from R03).
- The promotion question is untouched: nothing is promoted, the champion stays
  `solo --hold-on-vague`, and the resolved-per-cost bar for the ladder is still
  owed by R05 (registered in R03's future work).

## Adversarial self-review (2026-09-22, gate before close)

10 attacks, logged verbatim in `logs/round-04-adversarial.txt`:
`REVIEW-SUMMARY attacks=10 broken=0 status=ALL-HELD HELD=4
HELD-WITH-LIMITATION=6`. The six limited verdicts are exactly the threats above
(the ruling-vs-data tension, instrument blindness, the post-hoc metric, the
price's scope, the champion asymmetry, n=1, and the tautological sweep). Two
executable checks confirmed implementation invariants: `final` mode cannot
exceed the two-hop bound (max hops 2), and the reported selection can never
disagree with the trigger helper (0 disagreements on 46 tasks).

## Future work (registered before R05 measures)

1. **Verification timing trial with the corrected clause** (above), on a
   fixture not used to define the metric.
2. **Trigger composition trial**: is `planned formation or risk >= 0.5` the
   right selection rule, given 18 unselected deliveries? Candidates: wound
   signals only (correction / contested / tight truncation); risk threshold
   only; no trigger (verify every delivery — priced at 46 calls here).
3. **Champion verification**: price a risk-gated check on `solo`, the arm that
   currently delivers with no second opinion.
4. **Resolved-per-cost bar** for the ladder (owed since R03).
5. Model leg (R05 gate, unchanged).
