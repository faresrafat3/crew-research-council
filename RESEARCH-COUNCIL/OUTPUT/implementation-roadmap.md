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

## [DEEP DIVE]: Sequencing Evidence, Phase-Level Precedents, and Failure-Mode Defenses (cline, 2026-09-13)

### 1. Why staged sequencing: TMMi's no-skip rule and the crew's phase gates

The 4-phase order (Foundation → Mandatory → Gates → Improve) implements TMMi's staged architecture: each level lays the foundation for the next, maturity equals the lowest-rated process area, and skipping stages fails [TMMi Foundation, 2016; TMMi Foundation, 2018]. Phase success criteria are written as the level-exit checklists from testing-maturity-model: Phase 1 exit (100% of new PIPE/FULL carry REQ+RED over 10 tasks) is the L1→L2 gate; Phase 2 exit (≥80% tests pre-DONE over 20 tasks, gate <10 min) is the L2→L3 gate; Phase 3 exit (mutation 70/80%, req-cov 90%, flake <2%, drill 100%) is the L3→L4 gate; Phase 4 (-25% escapes/quarter, MTTR <14d, KB lag 0) is the L4→L5 operating loop. Metric targets are evidence-anchored, not aspirational: line coverage 80% with branch 70/75% reflects the Google/Microsoft/Stripe/Meta benchmark band (70-90%) documented in quality-metrics; mutation 70/80% sits inside the realistic 60-80% floor for high-risk modules (100% is wasted effort against equivalent mutants) [CircleCI, 2026; Drizz, 2026]; flake <2% matches Google's measured 1.5% run-flake rate [Micco, 2016]; quarantine fix-or-delete within 14 days follows the industry SLA band (7-day aggressive in TinyCTO, 2026; 14-day reasonable in Tenki, 2026) [Tenki, 2026; TinyCTO, 2026].

### 2. Phase-level precedents from verified sources

- **Phase 1 (policy + SOUL gates, 3-5d):** treats system prompts as versioned infrastructure — prompts are the operational blueprint governing agent behavior, and minor variations change output distribution entirely, so the TEST-POLICY.md + SOUL patches ship as reviewed artifacts with the same rigor as code [Shah, 2025]. The iron law lands here because compliance data (COORD-01/02: 100% skip rate) proves instructions alone do not stick [Council Context, 2026].
- **Phase 2 (mandatory tests + fast CI, 1-2wk):** implements Google's Small-test discipline in the commit gate (no network/DB/threads/sleeps, seconds-scale) with Medium/Large pushed to PR/nightly tiers [Stewart, 2010]. SWE-bench Verified is the external calibration point for what agent-built code can achieve: a human-validated 500-instance benchmark of real GitHub issues in a fixed harness environment [SWE-bench Team, 2026] — internal gate-pass trends should be read against this frontier, not against 100%.
- **Phase 3 (quality gates, 2-3wk):** adds the oracle-separation gate (tester-authored expectations only), motivated by the oracle problem literature: determining correct output for a given input is the hard problem, with specified/derived/implicit oracle categories surveyed across 1978-2012 [Barr et al., 2014; Wikipedia contributors]. The mutation + tautology + oracle-violation lints exist because LLM suites are measured weak at fault detection [ArXiv, 2025; Dev.to, 2025], and self-preference bias data [Wataoka et al., 2024/2025] justifies keeping the critic on a different model family.
- **Phase 4 (continuous improvement, ongoing):** runs the calibration loop from blocking-authority (quarterly FP/escape review, ±5% threshold moves clamped to 70-95% coverage / 60-90% mutation) plus the prevention backlog fed by escape KB entries within the 7-day SLA. Evaluation hygiene follows the benchmark-mutation lesson: re-validate gates against perturbed tasks so the crew does not overfit its own suite [Garg et al., 2025].

### 3. Failure-mode defenses per phase (what kills rollouts, and the counter)

| Phase | Killer | Defense (already in plan) | Source |
|-------|--------|---------------------------|--------|
| 1 | Workaround RED logs (fake failing tests) | CI reruns RED step independently; assert nonzero exit | testing-maturity deep dive |
| 1 | Policy ignored in crisis ("just this once") | Iron law in SOUL text, not policy doc — SOUL cannot be overridden per-dispatch | compliance data |
| 2 | Flake storm (>5% destabilizes CI) | Auto-quarantine at >2%, 14-day fix/delete SLA, advisory-only lane | Micco, 2016; Tenki, 2026 |
| 2 | E2E bloat (slow, brittle, expensive) | Cap 10 per FULL, push down to unit/integration | Vocke, 2018; KnowMBA, 2025 |
| 3 | Metric theater (85% coverage, 4% mutation) | Mutation gate 70/80% catches coverage theater | Getautonoma, 2026 |
| 3 | Slow mutation (full-suite cost) | Targeted touched-lines on PR, full only nightly, parallelize | MutGen; SQRBOK, 2025 |
| 4 | Strictness drift (FP >5%, appeals climb) | Quarterly calibration, loosen 5%, audit sample 5% of PROMOTEs | IJECS, 2026 |
| 4 | Leniency drift (escapes climb) | Tighten 5%, expand mutation operators, drill pass must stay 100% | IJECS, 2026 |

### References for deep dive
- [TMMi Foundation, 2016] Staged model and benefits.
- [TMMi Foundation, 2018] Level process areas.
- [CircleCI, 2026] Mutation testing floor 60-80%; 100% wasted effort.
- [Drizz, 2026] Mutation score bands: 70-80% business logic, 80%+ payments/security.
- [Micco, 2016] Flaky Tests at Google (1.5%/16%/84%).
- [Stewart, 2010] Test Sizes (Small/Medium/Large).
- [Tenki, 2026] Flaky Test Quarantine in GitHub Actions (14-day SLA).
- [TinyCTO, 2026] Flaky Test Quarantine Patterns (7-day fix clock).
- [Shah, 2025] System prompts as operational blueprints.
- [Barr et al., 2014] The Oracle Problem in Software Testing: A Survey.
- [Wikipedia contributors] Test oracle (categories: specified/derived/implicit).
- [ArXiv, 2025] LLMs for Unit Test Generation (weak fault detection).
- [Dev.to, 2025] Autogenerated tests anti-pattern (weak assertions).
- [Wataoka et al., 2024/2025] Self-Preference Bias (arXiv:2410.21819).
- [SWE-bench Team, 2025/2026] Verified benchmark; mini-SWE-agent 65%.
- [Garg et al., 2025] Saving SWE-Bench: Benchmark Mutation.
- [Council Context, 2026] Trials and root causes.
- [KnowMBA, 2025] Test Certified graduation, quarantine, budgets.
- [IJECS, 2026] Consensus, HITL, safe auto-fix.
- [Vocke, 2018] Practical Test Pyramid.
