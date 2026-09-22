# FINDINGS — mission ROUTER-V2, Round 02 (2026-09-22)

> Companion records: `PRE-REGISTRATION.md` (sha256
> `7e14c9d28120aa2703ac25e6af8d1929f49357bf41e326cb71b70a779524f0ba`, frozen
> before measurement), `logs/round-02-routed.txt` (verbatim measurement log),
> `DECISIONS-LOG.md` (method decisions), ADRs (mechanism rationale).
> **Honesty header:** rule-based stack only; the model leg (torch + weights)
> never ran. Cost is a simulated tool-call proxy. n=20 fixture tasks.

## Abstract

The round-01 router proposed formations that nothing executed: `routed` mode
crashed (KeyError) and `eval.py` overwrote the router's proposal with a static
CLI label. Round 02 implemented the declared ladder-and-cognition architecture
behind a 43-test RED wall, then measured. The routed ladder matches the
champion on compliance (20/20, grave=0, seed-stable across 5 seeds) while
resolving 2.25x more tasks (9 vs 4 resolved) at 1.87x cost (127 vs 68) — and
the ablation shows the class table is currently cost without benefit (20/20 at
cost 70 without it). Calibration, debate-boundedness, guard legitimacy,
receipt shrinkage, determinism, and the priors gate all held. H1 is CONFIRMED
on compliance and resolved, with the cost and routing-match failures recorded
honestly and routed NOT promoted.

## Related work (internal, cited)

- `~/.hermes/crew/experiment/VERDICT.md:2` — round-01 measured matrix; the
  hold rule (A+rule 20/20 @ 68) is the champion this round challenges.
- `GOAL.md` log (DECISIVE-01/REPLICATION/PROBES/P4 entries) — single-beats-team
  result, variance confession (5/12 cells swung), HOLD canonization.
- `REVIEW-02.md` §"Ownership yes" and §3 — gate-shares-executor-knowledge
  failure; enforced independence (A3) answers it structurally.
- `COORD-01` (GOAL.md log tail) — fixed-pipeline root cause; the ladder (A1)
  is the direct counter.
- `runs/2026-09-21-router-round-01/crew/eval.py:46-52` — the defect this round
  fixed (declared routed, crashed; double `used` literal).

## Method (frozen in PRE-REGISTRATION §Arms)

Fixture: `tasks/real-missions.json`, sha256 `28406677…59a87`, 20 tasks,
17 classes, expected PASS 4 / HOLD 8 / FLEX 8. Sandbox:
`runs/2026-09-22-router-round-02/`. Baseline witness at copy: 46 passed.
New RED suites first (43 failed / 1 passed — `logs/RED-witness.txt`), then
implementation, then full GREEN (`logs/GREEN-witness.txt`, 90 passed).

Mechanisms implemented (each with tests): A1 ladder+receipts, A2 risk-stratified
verification, A3 disjoint check registries, A4 rework loop bound 2, A5
verification-floor + announced degradation, A6 feasibility pre-check, B1 typed
shrinking receipts, D1 shadow-no-promotion, D2 priors-propose/apply-locked,
D3 error budget, E1 injection guard, E2 poison refusal, E3 least privilege,
H1 confidence, H2 belief ledger (hierarchy+conflicts+staleness), H3 bounded
debate, H4 next-experiment cards, H5 priced reflection, G2 drift alarms.

## Results (verbatim SUMMARY lines; full log `logs/round-02-routed.txt`)

| arm | passed | grave | cost | resolved | routing_match | escalations |
|---|---|---|---|---|---|---|
| solo --hold-on-vague (champion, seed 7) | 20/20 | 0 | 68 | 4 | 11/20 | 0 |
| routed (no hold-rule, seed 7) | 19/20 | 1 | 127 | 9 | 0/20 | 14 |
| routed --hold-on-vague (seed 7) | 20/20 | 0 | 127 | 9 | 0/20 | 15 |
| routed-thresholds (ablation, seed 7) | 20/20 | 0 | 70 | 4 | 0/20 | 0 |

Variance sweep (seeds 7/11/13/17/19): both arms byte-stable per seed set —
solo: 20/20, cost 68 on every seed; routed+hold: 20/20, cost 127 on every
seed. Determinism double-run: **byte-identical PASS**.

Probes (verbatim in log): H9 debate-on-contested cost_ratio=2.00x,
graves 0→0 — CONFIRMED at the registered boundary. H8 calibration
high-bucket success_rate=1.000 (n=8) — CONFIRMED. H4 next-experiment cards:
empty on a clean ledger (correct: no graves → no proposals). D2 apply-lock:
PermissionError raised — gate holds.

## Hypothesis verdicts

| # | Verdict | Evidence |
|---|---|---|
| H1 | **CONFIRMED on compliance/resolved; cost and routing bars FAILED** | 20/20 grave=0, resolved 9 vs 4 (log ARM3 vs ARM1); cost 127 > 88 bar; routing_match 0/20 |
| H2 | **CONFIRMED** | verifier stages appear only on risk>=0.5 or table classes; simple-edit/unverifiable-claim ran SOLO with no verifier (task lines, ARM3) |
| H3 | **CONFIRMED** | hold-rule verdict pattern identical across all 5 seeds (sweep block) |
| H4 | **CONFIRMED** | DETERMINISM byte-identical: PASS; sd=0 across seeds both arms |
| H5 | **REFUTED** | routed-thresholds ablation matches quality at near-solo cost (70); the class table adds cost (127) with zero routing_match gain |
| H6 | **CONFIRMED** | test_receipt_shrinks_across_hops GREEN; escalation packets smaller than task dict |
| H7 | **CONFIRMED** | guard_flags=2 (T17 poison refused, T19 injection flagged); T10/T12/T14 DELIVER stand (task lines) |
| H8 | **CONFIRMED** | high-bucket success 1.000 ≥ 0.85 (RELIAB lines) |
| H9 | **CONFIRMED at boundary** | cost_ratio 2.00x ≤ 2x with no grave regression |

## Threats to validity

- **Construct:** "cost" is simulated tool calls, not tokens/wall-clock; the
  reviewer is rule-based, so "grade" measures fixture compliance, not human
  quality. Confidence is a structural prior, not a learned probability.
- **Internal:** one executor implementation across arms — formation effects
  are isolated, but the router's table and the verifier's trigger share the
  risk_score signal, so H2's attribution is partly confounded with routing.
- **External:** locally-adapted 20-task fixture; zero generalization claimed
  beyond these 17 classes. Rule-based executor — nothing here predicts LLM
  behavior (R05 gate).
- **Statistical:** n=20; Wilson 95% CI on 20/20 is [86.2%, 100%]; the
  resolved delta (9 vs 4) sits inside a small fixture where FLEX tasks
  dominate resolved outcomes.

## Limitations (honest ceiling)

- routing_match=0/20 is an accounting artifact AND a real finding: `used`
  reports the ROUTED label while `proposed` reports the table's choice; the
  registered >=16/20 bar measured agreement between label and proposal, not
  routing quality. Round 03 must define routing_match as
  proposed==per-task-final-formation.
- The class table (H5 REFUTED) currently pays 57 calls for nothing measurable;
  under the razor it must either show value on a broader fixture or be cut.
- Debate showed no grave-detection gain on this fixture (graves were already
  0 with the hold rule); its 2x cost buys robustness only where graves exist.

## Future work (pre-registered direction, R03+)

1. routing_match semantics fix + re-measure (cheap, next round).
2. Class-table trial: kill or keep on a >=40-task fixture (H5 falsifier).
3. Error-budget (D3) live-fire: inject a grave-producing task and verify
   tighten:hold fires.
4. Belief-ledger loop: tracker writes measured beliefs; router reads them as
   advisory priors; measure routing improvement (R04 gate).
5. Model leg (R05): only behind the Owner's gate; contracts already stable.
