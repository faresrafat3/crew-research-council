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

## [DEEP DIVE Cycle 4]: COORD-03 Validation Trial + Cost/Latency Budget

> Extends `implementation-roadmap.md` Phase 2 exit (`>=80% tests pre-done over 20 tasks, gate <10 min`). Does NOT repeat sequencing rationale, TMMi no-skip rule, or Phase 1/3/4 defenses (see roadmap tail deep dive). This file designs the single concrete next experiment that proves L1→L2 climb.

### 1. COORD-03 trial design (20 tasks: 5 SOLO, 5 DUO, 5 PIPELINE, 5 FULL)

**Why n=20 stratified 5×4.** Roadmap Phase 2 exit is defined over exactly 20 tasks [Roadmap, 2026]. Small-n is normal in SE experiments — SE datasets are "often criticized for using sample sizes that are too small," and cross-over/repeated-measures designs are the standard power fix [Kitchenham et al. in Springer, 2024]. COORD-03 copies that fix: every failure mode from COORD-01/02/T09-T12 recurs in at least 2 formations (within-trial replication), so n=20 yields 4 failure-mode families × 5 observations each, analyzable with rank-based effect sizes (probability of superiority / Cliff's d) that outperform StdMD on small non-normal samples [Springer, 2024]. External calibration: agent code pass rates are low (ChatGPT 13% accepted on 124 coding tasks [Elhambakhsh, 2025]; GPT-4o 8.6% individual tasks [DevOps, 2025]), so success is measured as gate-compliance climb, not raw pass rate.

**Failure modes replicated (1:1 with CONTEXT.md):** (a) zero-test shipments — COORD-01 three task types zero test files despite explicit "write tests," COORD-02 4 modules/135 lines zero tests, operator wrote 11 manually; (b) critic timeouts on complex tasks + wrong-directory search; (c) razor breaks constraints (changes wording when told not to); (d) missing regression — T09-T12 fixes shipped without pinning original failure cases, bugs recurred [Council Context / CONTEXT.md, 2026].

**Task list (seeded probes marked ★):**

| ID | Formation | Concrete task | Seeded failure mode |
|----|-----------|---------------|---------------------|
| C03-01 | SOLO (engineer) | FizzBuzz variant + CLI `--limit` flag, 1 module | (a) zero-test: REQ demands 6 unit tests pre-done |
| C03-02 | SOLO | Markdown link checker (read-only → write report) | (a) + completer non-blocking probe |
| C03-03 | SOLO | Currency-format helper (ported COORD-02 slice) | (a): must ship `test_format.py` or FAIL |
| C03-04 | SOLO | Grammar-fix function with "do not change wording except flagged spans" | (c) razor wording-break probe ★ |
| C03-05 | SOLO | Regression-fix: re-break T09 case, fix must pin failing test first | (d) missing-regression probe ★ |
| C03-06 | DUO (eng→critic) | Bug-finder: 3 seeded bugs in 80-line parser, critic verifies | (a)+(b) critic path-awareness (touched-files only) |
| C03-07 | DUO | Logic puzzle solver (COORD-01 IC1 replay) with tests required | (a) explicit-requirement ignore replay |
| C03-08 | DUO | Small refactor: extract function, keep behavior | (c) razor-style over-trim probe |
| C03-09 | DUO | T10 recurrence: previously fixed rule, must add regression test | (d) ★ |
| C03-10 | DUO | Arg-parser with timeout-prone large diff (200-line fixture) | (b) critic 10min/file budget probe ★ |
| C03-11 | PIPELINE | URL validator: researcher spec → architect design → engineer → critic | (a) full RED→GREEN witness chain |
| C03-12 | PIPELINE | Multi-module converter slice (2 of COORD-02's 4 modules) | (a) 100%-skip-rate replay, RED required |
| C03-13 | PIPELINE | Complex task (300-line diff) with critic time-box enforced | (b) timeout <5% probe ★ |
| C03-14 | PIPELINE | Doc-reword task with immutable REQ spans ("do not change wording") | (c) 0-violation probe ★ |
| C03-15 | PIPELINE | T11 recurrence fix with regression pin | (d) ★ |
| C03-16 | FULL | Full CLI converter (COORD-02 full replay, 4 modules) | (a) operator-11-tests now crew-authored |
| C03-17 | FULL | Large feature + E2E (async lane only), critic + tester + completer | (b) blocking <10min + async ≤60min probe |
| C03-18 | FULL | Redundancy-removal + wording freeze (razor under REQ lock) | (c) razor REQ-violation = HOLD probe ★ |
| C03-19 | FULL | T12 recurrence + escape-KB entry write | (d) escape-0 probe ★ |
| C03-20 | FULL | Mixed: refactor + new feature + regression suite green | (a)+(d) L1→L2 graduation demo |

**Success criteria (Phase 2 exit, all must hold):** RED-witness 100% on PIPELINE/FULL (10/10 merged carry REQ+RED log, CI-rerun nonzero-exit verified); ≥80% PIPELINE/FULL with tests pre-done before DONE claim (≥8/10); 0 razor REQ violations (any immutable-span edit = HOLD); critic timeout <5% (≤1/20 tasks hit PARTIAL_VERDICT path); escape 0 (no post-merge bug recurrence on seeded T09-T12 cases).

**Scoring rubric (per task, 0–5; PROMOTE needs 5/5 on PIPELINE/FULL, ≥4/5 on SOLO/DUO):**

| Pt | Dimension | Check (evidence artifact) |
|----|-----------|---------------------------|
| 1 | REQ present | `REQ-*.md` with frozen spans marked; razor diff touches none |
| 1 | RED witnessed | CI log shows failing test run, nonzero exit, independent rerun |
| 1 | GREEN + suite | GREEN log + `pytest -m "not slow"` green + JUnit XML attached |
| 1 | Verdict chain | critic verdict (PROMOTE/HOLD + evidence) + completer block on missing verdict |
| 1 | Regression pin | every fix links seeded-case test; T-probes assert original failure covered |

Trial-level report: RED-witness % (audit), pre-done % (ledger), razor violations (count), critic timeouts (count + PARTIAL rate), escapes (count). Analyze with rank-based comparison vs COORD-01/02 baseline (100% skip → target ≤20% skip); do not use parametric StdMD on n=5/formations [Springer, 2024].

### 2. Cost/latency budget per formation

**Ceilings (blocking gate; everything slower goes async):** SOLO <2 min, DUO <5 min, PIPELINE <10 min blocking, FULL <10 min blocking + async nightly ≤60 min. Suite-level under-10-minutes is the industry linter default (entire suite should run in under 10 minutes; model tests under 1.5 s each [thoughtbot Test Budget, 2026; search result]), and 12 min is the community "fine if team agrees" ceiling [Ministry of Testing, 2023]. Google Small-test discipline (no network/DB/threads/sleeps, seconds-scale; Medium/Large to PR/nightly) is the tiering precedent [Stewart, 2010].

| Formation | Blocking budget | pytest | coverage +1m | targeted mutation +3m | PBT +2m | E2E |
|-----------|----------------|--------|--------------|----------------------|---------|-----|
| SOLO | <2 min | `pytest -m "not slow"` ≤60 s | +≤60 s (`--cov`, `parallel=true`) | none blocking | none | none |
| DUO | <5 min | fast set ≤2 min | +1 min | touched-lines only ≤2 min (advisory) | 1 property ≤1 min | none blocking |
| PIPELINE | <10 min | fast set ≤4 min | +1 min | touched-lines ≤3 min | ≤2 min (seeded from KB) | capped, PR-lane only |
| FULL | <10 min blocking + async ≤60 min | fast set ≤4 min blocking | +1 min blocking | full-suite nightly only | full PBT nightly | ≤10 E2E nightly only |

**Breakdown notes:** coverage adds ~1 min (per-worker merge is automatic under xdist; set `parallel=true, branch=true` so branch data merges [QASkills pytest-xdist guide, 2026]); targeted mutation capped at +3 min on PR (touched-lines only, full suite nightly — MutGen/SQRBOK precedent in roadmap); PBT +2 min max blocking (Hypothesis seeded from escape KB, rest nightly); E2E never blocking (cap 10 per FULL, push down to unit/integration [Vocke, 2018]).

**Required split + parallelism (copy-paste):**

```ini
# pyproject.toml
[tool.pytest.ini_options]
markers = ["slow: medium/large/e2e/mutation/pbt-nightly"]
addopts = "-n auto --dist loadscope -m 'not slow'"
```

```bash
# blocking gate (all formations)
pytest -m "not slow" -n auto --dist loadscope --cov=src --cov-report=xml --junitxml=report.xml --maxfail=1
# async nightly (FULL only, ≤60 min)
pytest -m "slow" -n auto --dist loadscope --cov=src --cov-report=xml
```

**`pytest-xdist -n auto` requirement:** `-n auto` (one worker per physical core; controller + `gw0…gwN` subprocesses) is the default for local + CI and cuts wall-clock 4–8× on isolated suites [QASkills, 2026]. Require `--dist loadscope` (same class/module on one worker, shares scoped fixtures), `worker_id`-namespaced DBs/ports, and file-locked once-per-run fixtures; small suites (<50 tests) may run `-n 0` serial where worker startup exceeds savings [QASkills, 2026]. Pin `-n 4` explicitly when containerized runners misreport cores via `os.cpu_count()` [QASkills, 2026]. Coverage under xdist needs no extra flags beyond `parallel=true` (pytest-cov merges per-worker data automatically; do not hand-roll `coverage combine` after) [QASkills, 2026].

### 3. Go/no-go gates for Phase 2→3

| # | Gate (over 20 COORD-03 tasks) | GO threshold | Measure | NO-GO remediation (= hold Phase 2 +1 week) |
|---|-------------------------------|--------------|---------|----------------------------------------------|
| G1 | RED-witness | ≥80% overall, 100% PIPELINE/FULL | CI-rerun audit of RED logs | Re-run engineer iron-law drill on failed formations; add RED-log linter to completer; re-trial 5 tasks |
| G2 | Gate latency p95 | <10 min blocking | CI wall-clock p95 over 20 runs | Split slowest file (`pytest-split` / matrix shard), move top-3 slow tests to `slow` mark, re-measure |
| G3 | Flake rate | <5% (target <2%) | rerun-fail / total runs | Auto-quarantine >2% to advisory lane, 14-day fix/delete SLA [Micco, 2016; Tenki, 2026]; flaky test quarantined same-day |
| G4 | False-positive (HOLD overturned on appeal) | <5% | appeals upheld / total HOLDs | Loosen strictest lint 5%, audit 5% PROMOTE sample, recalibrate tester threshold once |
| G5 | Escape / razor | 0 escapes, 0 razor REQ violations | post-merge recurrence + REQ-span diff | Tighten: expand mutation operators on escaped lines, freeze razor spans in REQ schema, re-run C03-04/14/18 |

**Decision rule:** all five GO → promote to Phase 3 (add Hypothesis + mutmut + oracle lints + ledger). Any NO-GO → hold at Phase 2 exactly one more week, execute that row's remediation, then re-run minimum 5-task re-trial on the failed formation(s) before re-vote. Two consecutive NO-GOs on the same gate → escalate to operator review (threshold or task-design fault, not execution fault).

**References Cycle 4:**
- [Council Context / CONTEXT.md, 2026] COORD-01 (3 types, zero test files, explicit requirement ignored), COORD-02 (4 modules/135 lines, zero tests, 11 operator tests), T09-T12 (no regression pin, recurrence), critic timeout + path bugs, razor wording breaks, completer non-blocking.
- [Roadmap, 2026] Phase 2 exit: ≥80% tests pre-done over 20 tasks, gate <10 min; Phase 1 exit 100% REQ+RED over 10 tasks.
- [Springer / Kitchenham et al., 2024] Recommendations for analysing small sample size SE experiments — small-n prevalence, cross-over power fix, Cliff's d / probability-of-superiority over StdMD.
- [Elhambakhsh, 2025] ChatGPT 13% accepted on 124 coding tasks.
- [DevOps, 2025] GPT-4o 8.6% individual / 38.7% management tasks.
- [thoughtbot Test Budget, 2026] Suite-level <10 min, model tests <1.5 s (via search).
- [Ministry of Testing, 2023] 12-min community ceiling (via search).
- [QASkills pytest-xdist guide, 2026] `-n auto`, `--dist loadscope/loadfile/loadgroup/worksteal`, `worker_id` namespacing, coverage `parallel=true` merge, `-n 0` under 50 tests, pin `-n 4` on misreporting runners.
- [Stewart, 2010] Google Test Sizes (Small/Medium/Large).
- [Micco, 2016] Flaky Tests at Google (1.5% flake rate).
- [Tenki, 2026] 14-day quarantine SLA.
- [Vocke, 2018] Test pyramid / push-down.
