# Implementation Roadmap

## Executive Summary
Four phases climb TMMi levels without stalling delivery: Foundation (3-5 days) commits policy and SOUL gates; Mandatory Tests (1-2 weeks) enforces RED/GREEN evidence and fast CI; Quality Gates (2-3 weeks) adds property, mutation, oracle, and ledger gates; Continuous Improvement (ongoing) converts escapes into knowledge and calibration. Each phase names exact files, deltas, metrics, and risks so an operator can execute directly, following the staged TMMi climb [TMMi Foundation, 2016] with Test Certified-style graduation [KnowMBA, 2025].

## Key Findings
- Staged levels each lay foundations for the next; skipping stages fails [TMMi Foundation, 2016].
- Policy plus planning plus environments come before measurement [TMMi Foundation, 2018].
- Shared standards plus lifecycle integration precede meaningful metrics [TMMi Foundation, 2018].
- Measurement of process and product quality precedes optimization [TMMi Foundation, 2018].
- Prevention and process optimization close the loop [TMMi Foundation, 2018].
- Graduated test certification moves teams to full TDD stepwise [KnowMBA, 2025].
- Mutation feedback needs about 4 iterations to converge [ArXiv, 2025].
- Flake quarantine with 14-day SLAs protects velocity during rollout [KnowMBA, 2025].
- PROMOTE/HOLD/ROLLBACK gates prove stable across dozens of releases [ArXiv, 2026].
- Consensus plus human review on disagreement prevents automation capture [IJECS, 2026].

## Detailed Analysis
Phase 1 creates `crew/TEST-POLICY.md`, patches tester SOUL to full spec, adds engineer iron law, patches firstmate activation, scaffolds test dirs, installs pytest plus coverage. Phase 2 enforces message templates, fixes critic timeouts and paths, makes completer reject missing verdicts, and blocks merges on pytest plus coverage artifacts. Phase 3 adds Hypothesis, mutmut with covered-lines and stack limits, oracle/tautology/mock lints, ledger DB, verdict gates, nightly large plus golden eval plus break drills. Phase 4 runs prevention reviews, quarterly FP/FN calibration, safe-class auto-patches with human review, and trend dashboards. Risks per phase: workaround RED logs (audit them), critic timeouts (time-box now), flake storms (quarantine lane), E2E bloat (caps), slow mutation (targeted plus parallel), PBT difficulty (seed from KB), strictness drift (calibrate).

## Practical Recommendations
| Phase | Duration | Files and Deltas | Success Criteria | Risks |
|---|---|---|---|---|
| 1 Foundation | 3-5d | TEST-POLICY.md; tester/engineer/firstmate SOUL patches; test dirs; pytest+coverage | 100% new PIPE/FULL have REQ+RED (10 tasks) | workarounds; timeouts |
| 2 Mandatory | 1-2wk | message templates; critic fix; completer gate; CI pytest+coverage+JUnit | >=80% tests pre-done (20 tasks); <10 min | flakes; E2E bloat |
| 3 Gates | 2-3wk | Hypothesis+mutmut; lints; ledger; verdicts; nightly+golden+drills | mut 70/80%, req-cov 90%, flake<2%, drill 100% | speed; PBT learning |
| 4 Improve | ongoing | KB SLA; calibration; safe auto-fix; dashboards | -25% escapes/qtr; MTTR<14d; KB lag 0 | strict/lenient drift |

## Metrics and Targets
| Metric | Definition | How to Measure | Target | Warning |
|---|---|---|---|---|
| RED-witness | merged with RED | audit | 100% P2+ | <100% |
| Gate pass | PROMOTE share | ledger | rising | falling |
| Coverage/mutation | gates | CI | 80%/70-80% | below HOLD |
| Drill pass | REQ breaks caught | drill | 100% | <100% |
| Escape delta | per quarter | reports | -25% | rising |
| Phase slip | days overdue | plan | 0 | >3d replan |

## References
1. [TMMi Foundation, 2016] Staged model and benefits.
2. [TMMi Foundation, 2018] Level process areas.
3. [KnowMBA, 2025] Test Certified graduation, quarantine, budgets.
4. [ArXiv, 2025] MutGen iteration convergence.
5. [ArXiv, 2026] Self-testing gates at scale.
6. [IJECS, 2026] Consensus, HITL, safe auto-fix.
