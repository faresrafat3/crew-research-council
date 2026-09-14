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

---

## [DEEP DIVE (freebuff, pass 2, 2026-09-14)]: Gate-Adoption Evidence — Tricorder Deployment Lessons and Shadow-Mode Rollout

The pass-1 deep dive defended the phase *sequencing*. This one defends the *rollout mechanics* — how to turn each gate on without triggering the failure modes the roadmap already lists (workarounds, flake storms, metric theater). The best-evidenced playbook for rolling out automated quality gates comes from Google's static-analysis program.

### R1. Tricorder's lessons, applied to the crew's gates

Google's Tricorder program (*Software Engineering at Google*, ch. 20; CACM 2018) is the largest documented deployment of automated checks into developer workflow, and its findings transfer directly:
- **Show results only where the developer is working:** "we focus analyses on files affected by a pending code change, and typically show analysis results only for edited files or lines" [Sadowski et al., 2018]. The crew's gates already do this (targeted mutation on touched lines; diff-coverage gate per testing-framework-spec pass 2) — keep it that way; project-wide blocking checks are the roadmap's "slow mutation" killer in new clothes.
- **New warnings only, not legacy debt:** "we generally focus on newly introduced warnings; existing issues in otherwise working code are typically only worth highlighting (and fixing) if they are particularly important" [Sadowski et al., 2018]. Roadmap translation: gates never retro-block — a new mutation threshold applies to PRs filed after the policy commit, never to open work.
- **False-positive discipline is the adoption gate:** tools are deployed only with low false-positive rates, with a live feedback loop where developers flag bad findings [Sadowski et al., 2018]. For the crew: a gate's FP rate (appeals overturned / blocks) must be below the ~5% line before it moves from advisory to blocking (calibration data already flows from blocking-authority.md §2).
- **Happiness is a tracked metric:** "For a static analysis project to succeed, developers must feel they benefit from and enjoy using it" [Sadowski et al., 2018, abstract]. Crew analog: track fix-latency and appeal-rate per gate; a gate engineers (agents) routinely route around is failing regardless of its catch statistics.

### R2. Shadow mode: every gate runs advisory before blocking

The roadmap's Phase 2→3 transition flips gates to blocking the moment they're installed. Insert a shadow window first — the progressive-delivery pattern production-deployment.md pass 1 applied to agent patches, applied here to the gates themselves:
1. Install gate in **comment mode** (posts findings to the task thread, never blocks) for a fixed window of 20 tasks.
2. Measure: would-have-blocked rate, estimated FP rate (operator adjudication of each would-have-block), fix-latency for commented findings.
3. Flip to blocking only if FP < 5% and would-have-blocked rate is in a sane band (not 0% — a gate that never fires is decorative, per blocking-authority.md Pattern 2; not >50% — Pattern 1, the overly strict gatekeeper).
4. Keep the advisory lane permanently after flip: findings that would block *new* work but exist in *legacy* code surface as comments only (R1's new-warnings rule).

Google's own results validate the endpoint: comment-first deployment built such trust that checks "educate developers and actually prevent antipatterns from entering the codebase," and the program reached effectively company-wide adoption [Sadowski et al., 2018].

### R3. Sequencing evidence recap: gates with the strongest causal backing go first

Within Phase 3, order matters when cutting scope. Rank by intervention evidence: (1) mutation findings presented as review comments — the Google interventional study showed exposure causally increased test strength [Petrović et al., 2021; tester-soul cycle 4 D7]; (2) the tautology/oracle lints — zero-FP by construction, pure AST checks; (3) diff-coverage — cheap and low-FP; (4) full mutation threshold — expensive, highest FP risk, last. This matches the roadmap's existing "targeted before full" instinct but gives it an evidence-based ordering and a shadow-mode wrapper.

### Roadmap risk-table extension (pass 2)

| Phase | Killer | Defense |
|---|---|---|
| 3 | Gate fatigue (agents route around noisy gates) | Shadow window + FP < 5% before blocking + per-gate appeal tracking [Sadowski et al., 2018] |
| 3 | Retro-blocking legacy debt freezes delivery | New-warnings-only rule; advisory lane for pre-existing issues |
| 4 | Gate decay after rollout | Quarterly adversarial drills on the gates (testing-maturity pass 2 §M3) |

### References (pass 2)
1. [Sadowski et al., 2018] "Lessons from Building Static Analysis Tools at Google," CACM 61(10) / *Software Engineering at Google* ch. 20. https://abseil.io/resources/swe-book/html/ch20.html [verified: 2026-09-14]
2. [Petrović et al., 2021] "Does mutation testing improve testing practices?" ICST 2021, arXiv:2103.07189. https://arxiv.org/abs/2103.07189 [verified: 2026-09-13, tester-soul cycle 4]
3. Cross-refs: production-deployment.md pass 1 (SLO-gated progressive rollout); blocking-authority.md Patterns 1–2; testing-framework-spec.md pass 2 (diff coverage).

## [DEEP DIVE (freebuff, pass 3, 2026-09-14)]: Evidence-Based Sequencing — Mining Repository History for Defect Hotspots Before Phasing the Rollout

Passes 1–2 specified *how* to phase and *how to deploy gates*. None specified *where to point the phases*. The bug-prediction literature offers a direct, validated input: history-based models — change frequency, code churn, complexity, and **change coupling** (files that change together) — are among the most consistently successful defect predictors, and **hotspots** (high change frequency × high defect density) concentrate defects far above baseline [Rahman et al., comparative study of bug-prediction techniques; D'Ambros et al., benchmark of defect prediction approaches — both snippet-verified].

**Protocol deltas for the roadmap.**
1. **Pre-phase mining step (new M0):** before ordering phases, mine the target repo: hotspot list, churn ranking, change-coupled clusters. Phases that first stabilize hotspots dominate any feature-order heuristic, because hotspot stabilization reduces the denominator of every later metric.
2. **Hotspots set the coverage-floor strictness** (framework-spec pass 2): the diff-coverage gate and ratchet apply at their strictest level on hotspot files, relaxed elsewhere. Uniform floors waste review attention on stable code (engineer-soul pass 3).
3. **Re-mine at every phase boundary.** Hotspots migrate as the crew refactors; a phase plan written once is stale by phase 2.
4. **Change-coupled clusters define the minimal RTS unit** (tester-soul pass 2): tests are selected per coupling cluster, not per file — selecting by file alone misses the coupled partner that breaks.
5. Roadmap milestones gain a **mining artifact requirement**: each phase's completion claim cites the fresh hotspot diff (what improved, what migrated) so the claim is checkable rather than narrative.

**Cross-links:** testing-framework-spec pass 2 (floors), tester-soul pass 2 (RTS clusters) and pass 3 (bandit arms weighted by escape cost — hotspots are the max-escape-cost arms), quality-metrics ledger (hotspot escape rate as a first-class row).

**Sources.**
1. [Rahman et al., 2013] "Bug Predicting via Code Mining" — comparative evaluation of history-based predictors [snippet-verified: 2026-09-14].
2. [D'Ambros et al., 2012] "Evaluating defect prediction approaches: a benchmark and an extensive comparison" *EMSE* [snippet-verified: 2026-09-14].
3. [Tufano et al., 2017/2019] JIT-defect prediction using deep learning on change-level features [literature, context].
