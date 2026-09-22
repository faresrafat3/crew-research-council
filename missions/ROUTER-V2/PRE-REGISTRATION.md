# PRE-REGISTRATION — mission ROUTER-V2, Round 02 (2026-09-22)

> **Status:** FROZEN. This file is pinned before any round-02 measurement runs.
> Any later change is a new dated file (supersession), never an edit.
> sha256 (pinned at freeze, see BOARD.md): recorded after this file is written
> and before the first measurement command runs.

## Fixture and environment (frozen inputs)

- Tasks: `tasks/real-missions.json` — 20 tasks, sha256
  `28406677825eeeb5489e7ea6fc60ee7a992e55ea0629f8348436052cfba59a87`.
- Sandbox: `~/.hermes/crew/experiment/runs/2026-09-22-router-round-02/`.
- Baseline witness at copy time: source suite `46 passed` (logs/RED-witness.txt
  records the new RED suites: 43 failed / 1 passed before implementation).
- Environment: stdlib only, offline, deterministic rule-based executor.
  **The model leg (torch + weights) is out of scope; nothing here is a claim
  about LLM behavior.**

## Hypotheses (registered before measurement)

| # | Hypothesis | Falsifier |
|---|---|---|
| H1 | `routed` (escalation ladder, class table + priors) achieves passed=20/20, grave=0 on seed 7, and resolved >= 4 | routed loses on passed, grave, or resolved vs `solo --hold-on-vague` (68 cost baseline) |
| H2 | Verification tax concentrates on high-risk classes (contested/correction/fetch), not on calm classes | verifier stages appear on >= 3 calm classes (simple-edit, unverifiable-claim, constraint-respect) |
| H3 | hold-rule behavior is seed-stable (same verdict pattern across 5 seeds) | any verdict difference for a fixed task across seeds in the same arm |
| H4 | Rule-based stack is fully deterministic: byte-identical stdout on repeated runs, sd=0 across seeds for fixed task sets | any byte difference between repeated runs |
| H5 | Class-table routing reaches routing accuracy >= 16/20 (80%) vs thresholds-only fallback | routed routing_match < 16/20 |
| H6 | Handoff receipts shrink or stay flat across hops | any escalation packet larger than the task dict it replaces |
| H7 | Guards (E1 injection scan, E2 poison refusal) block T19-carrying instructions and T17 poison without breaking T10/T12/T14 legitimate flows | any legitimate external-source flow flips to HOLD/broken by guards |
| H8 | Confidence calibration: high-confidence (>=0.8) DELIVERs realize >= 0.85 success on the fixture | high-bucket success_rate < 0.85 in reliability_curve() |
| H9 | Structured debate (max 2 rounds) adds grave-detection on contested classes at cost <= 2x that class's solo cost | debate-on-contested arm cost > 2x solo cost on T9/T11/T15 with zero grave-detect gain |

## Arms (fixed before measurement)

1. `solo --hold-on-vague --shuffle-seed 7` (champion reference, round-01: 20/20 cost 68)
2. `routed --shuffle-seed 7` (ladder, hold-rule off)
3. `routed --hold-on-vague --shuffle-seed 7` (ladder + hold-rule)
4. `routed-thresholds` (ablation: threshold fallback only, no class table) — shadow
5. `debate-on-contested` (H9: structured debate on T9/T11/T15) — shadow
6. Variance sweep: arms 1 and 3 across seeds 7, 11, 13, 17, 19.
7. Determinism: arm 3 run twice, stdout diff must be empty.

## Analysis plan (declared)

- Primary endpoint: passed count (blind reviewer grade) on seed 7, arm 3 vs arm 1.
- Secondary: grave_errors, resolved, total_cost, routing_match, wall_s.
- Paired task-level comparison arm-by-arm on the same 20 tasks (same seed);
  McNemar-style discordant-pair count reported where arms differ.
- Wilson 95% CI for pass rates (reported in FINDINGS).
- Variance: per-arm per-seed SUMMARY table; sd of cost and passed across seeds
  (expected 0 under H4).
- Calibration: reliability_curve() buckets from the tracker ledger (H8).
- Guard impact: per-task verdict deltas arm 3 vs round-01 baseline (H7).

## Promotion rule (pre-declared)

`routed` may be recorded as the new champion only if H1 holds AND the full
suite is green AND H7 shows no legitimate-flow regression. Otherwise the
champion stays `solo --hold-on-vague` and the loss is recorded verbatim.
Shadow arms (4, 5) are never promoted from within the run: proposals only
(D1/D2 advisory law).

## Honesty constraints

- Cost is a simulated tool-call proxy, not tokens or wall-clock LLM spend.
- The reviewer is rule-based; "grade" measures fixture compliance, not human
  quality.
- n=20; all CIs are wide; no claim of generalization beyond the 17 fixture
  classes.
