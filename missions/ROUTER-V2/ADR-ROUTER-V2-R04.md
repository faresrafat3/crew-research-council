# ADR-ROUTER-V2 — Round 04 (2026-09-22)

Round 04 continues the numbering (ADR-1…ADR-13). It prices the verification
stage, gives it explicit modes, and refuses to change the shipped mode because
the registered clause said so.

## ADR-14: the verification gate gets explicit modes, and `pre` stays shipped

- **Context:** R03's H16 recorded `verifier_flips=0` and left the stage's price
  unpriced. The Owner ordered the `--no-verifier` ablation and a stay-or-trim
  decision.
- **Decision:** `crew/formations.py::run_formation(..., verify=...)` and
  `crew/eval.py --verify pre|final|off` (with `--no-verifier` as an alias for
  `off`). `pre` remains the shipped default. `final` (guard the artifact that is
  actually returned; skip HOLDs a one-way gate cannot act on; re-verify after a
  repair hop) is implemented, measured, and **not adopted**.
- **Evidence:** tax `pre` = +14 calls of 292 (4.79%) on the expanded fixture,
  +4 of 122 (3.28%) on the frozen one, with the per-task identity
  `cost(pre) − cost(off) == verifier_calls` holding on all 46 tasks; zero flips
  and identical passed/grave/resolved in every mode (`logs/r04-analysis.md`).
- **Rejected:** cutting the stage (the grader *is* the rule set the verifier
  re-runs, so the instrument cannot price detection — P15); adopting `final`
  although it dominates on every measured axis (its registered clause,
  `unverified_deliveries(final) == 0`, failed at 18, and bending a frozen rule
  to the dominant arm is the failure mode the protocol exists to block).
- **Reversal:** R05 pre-registers the corrected clause
  (`hole_deliveries(final) == 0` and strictly better than `pre`, quality
  unchanged, tax not rising) on a fixture not used to define the metric. If it
  holds, `final` becomes the default and this ADR is superseded.

## ADR-15: one trigger, and coverage metrics must separate selection from guarding

- **Context:** R04's X2/X3 were specified against `unverified_deliveries`, a
  metric that mixes two different facts: deliveries the trigger never selected
  (18 of 19 on the expanded fixture) and deliveries the trigger selected but
  the timing left unguarded (1 — T23). The registered clause
  `unverified_deliveries(final) == 0` therefore could never have held, and the
  hypothesis was refuted for reasons unrelated to its mechanism.
- **Decision:** the trigger lives in exactly one function
  (`verification_selected(formation, risk)`); `run_formation` reports
  `verify_selected`, `verified`, `unverified_delivery`, and the split
  `hole_delivery` / `unselected_delivery`; `eval` sums them into
  `hole_deliveries` and `unselected_deliveries` alongside the original
  `unverified_deliveries` (kept for continuity with the R04 pre-registration).
- **Evidence:** all 46 tasks report selection consistent with the helper (0
  disagreements, adversarial attack 8); `sum(unverified) == hole + unselected`
  is asserted by the suite; the decomposition reproduces the exact known sets
  (`hole = {T23}` on the expanded fixture, `{}` on the frozen one).
- **Rejected:** leaving the ambiguous metric and fixing it in prose (it would
  re-mislead the next round); replacing `unverified_deliveries` outright
  (it is the R04 pre-registered metric and must stay reproducible).
- **Reversal:** if a future coverage question is fully captured by one number,
  collapse the split — with the reason on the record.

## ADR-16: no back-door adoption — a defect does not override a frozen rule

- **Context:** the retarget closes a real correctness defect (a *selected*
  delivery, T23, escapes the guard because the ladder replaced the artifact
  after the pass). The minimal defect fix inside `pre` semantics — also verify a
  delivery produced by a hop — is one extra pass (+1 call on the expanded
  fixture, +0 on the frozen one) and would leave the shipped mode's timing
  intact.
- **Decision:** **do not ship it this round.** The hole is recorded as a defect
  with its measured fix candidate and price (`FINDINGS-R04.md` §Coverage,
  §Future work 1), and R05 owns the trial that decides between `pre`,
  `pre + post-hop guard`, and `final`.
- **Why:** the pre-registration governs *changes to the mechanism under test*;
  shipping a partial retarget after seeing the data is adoption by the back
  door, and it would make R05's comparison uninterpretable. The defect's
  practical impact here is nil (zero rejections were observed), so deferring one
  round costs nothing measurable while keeping the test honest.
- **Rejected:** shipping the one-line fix now (uninterpretable next round);
  silently leaving the defect unmentioned (the opposite failure).
- **Reversal:** if a rejection is ever observed on a delivered artifact that
  reached delivery through a hop, the fix ships immediately as a correctness
  patch, outside the trial protocol, with that event cited.
