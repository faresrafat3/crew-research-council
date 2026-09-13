# TESTING MATURITY MODEL — Crew v2 (AI Agent Testing)

> **Research Council Output** | Prompt: P0 — Testing Maturity Model | Agent: freebuff | Date: 2026-09-13
> **Freshness:** All external claims verified live 2026-09-13 via web search against the sources listed in References. Internal claims cite repo documents (CONTEXT.md, STATUS.md).

---

## Executive Summary

Crew v2 currently sits at **Level 1 (Initial)** of the proposed Crew Testing Maturity Model (CTMM): across three recorded trial series (COORD-01, COORD-02, T09–T12), the engineer produced zero test files even when testing was an explicit task requirement [CONTEXT.md]. This is the documented industry failure pattern of the AI-coding era: DORA's 2025 study found higher AI adoption raises both delivery throughput *and* delivery instability, with 30% of developers reporting little or no trust in AI-generated code [DORA, 2025]; the 2025 Stack Overflow survey found more developers actively distrust AI tool accuracy (46%) than trust it (33%) [Stack Overflow, 2025]. The model below adapts the TMMi five-level staged architecture [TMMi Foundation] to agent-native realities — non-deterministic test authors, generated artifacts that must themselves be verified, and self-preference bias when the same system grades its own work [Pombal et al., 2025; NeurIPS, 2024] — while preserving TMMi's two hard rules: maturity is staged, and an organization's level equals **the lowest rating of its supporting process areas**, not its most advanced capability. The model defines five levels, each with measurable exit criteria, verification gates, and metric targets, so the operator can locate Crew v2 on a weekly basis and know exactly which single capability unlocks the next level. The practical path: L1→L3 is achievable in weeks because it requires only artifact discipline (tests exist, compile, pass, and a second agent gates them); L3→L5 requires measurement infrastructure (mutation scoring, escape-rate tracking, drift detection) and governance policy.

---

## Key Findings

1. **Classical TMMi is the right skeleton but the wrong muscle.** TMMi defines 5 levels and 16 process areas and requires *all* goals at a level to be satisfied before progressing [TMMi Foundation; Augment Code, 2026]. But TMMi assumes human-authored tests against a stable application — both assumptions are false in Crew v2, where agents generate both code and tests non-deterministically [Augment Code, 2026].
2. **The central design principle is the verification gap:** the distance between how confident AI output looks and how correct it is. Without verification, LLM code-gen error rates run ~65%; an execution-based verifier cuts returned-answer error to 2% [Ravuri & Amarasinghe, 2025].
3. **Generated tests are themselves unreliable artifacts.** Meta's TestGen-LLM: 75% of generated test cases built correctly, 57% passed reliably, only 25% increased coverage [Alshahwan et al., 2024]. An empirical study of invalid LLM-generated unit tests found 30.68% fail on unresolved-symbol errors and 17.25% on parameter mismatches — they break *before they run* [empirical study cited in Augment Code, 2026].
4. **A maturity model for agents must gate on artifacts, not process.** The agent-native QA maturity model gates each stage on a concrete verification control (compilation gate → live validation → outcome metrics → governance policy) rather than documented process [Augment Code, 2026].
5. **Self-verification is structurally biased.** LLM evaluators recognize and favor their own outputs [NeurIPS, 2024], and self-preference persists even with fully objective, programmatically verifiable rubrics [Pombal et al., 2025]. This is direct evidence for Crew v2's role-split (engineer ≠ tester ≠ critic) rather than a single self-checking agent.
6. **Independent multi-agent verification works.** Functional clustering (sample many candidates, execute on self-generated tests, cluster by I/O behavior) reduces error from ~65% to 2% and to 0% at a conservative threshold [Ravuri & Amarasinghe, 2025]. Meta's filter-based assurance architecture accepted 73% of LLM test improvements into production [Alshahwan et al., 2024].
7. **Trust data confirms the crew cannot rely on the engineer's self-report.** 30% of developers report little/no trust in AI-generated code [DORA, 2025]; 46% actively distrust AI tool accuracy vs 33% who trust it, only 3% highly trust [Stack Overflow, 2025]. A crew member with no blocking authority (current state) is therefore ungoverned automation.
8. **Coverage thresholds must follow Google's per-commit pattern, not project-wide vanity goals.** Google's guidance: per-commit coverage goals of ~99% are reasonable, 90% is a good lower bound; project-wide goals above 90% are mostly not worth it [Google Testing Blog, 2020].
9. **Multi-agent scaling has measured plateaus and error-amplification risks.** Independent agents amplify errors ~17.2× through unchecked propagation; centralized coordination contains this to ~4.4× [coordination benchmark cited in Augment Code, 2026]. Homogeneous agent systems plateau around 4 agents, heterogeneous around 8 [agent-scaling study cited in Augment Code, 2026]. Crew v2's 8-agent roster is at the heterogeneous plateau — adding agents is not a maturity strategy.
10. **Flakiness is a first-class maturity metric.** At Google, 1.5% of test runs are flaky and ~16% of tests are affected by flakiness [Google Testing Blog, 2016]; a maturity model that doesn't measure flake rate will confuse signal with noise at every level.

---

## Part 1 — Sources and Design of the Model

### 1.1 What TMMi Provides

TMMi (Test Maturity Model integration) is a staged model: five levels, each containing process areas with specific goals; an organization must satisfy all goals at one level before advancing to the next [TMMi Foundation; TestFort, 2025]. Its level names and focus:

| TMMi Level | Name | Focus |
|---|---|---|
| 1 | Initial | Ad-hoc testing, no tracking, outcomes depend on individuals [TestFort, 2025] |
| 2 | Managed | Basic test policy, planning, monitoring; testing becomes visible to management [TestFort, 2025] |
| 3 | Defined | Organization-wide standards; lifecycle integration; traceability from requirements to tests [TestFort, 2025] |
| 4 | Measured | Quantitative management; statistical process control; data-driven decisions [TestFort, 2025] |
| 5 | Optimizing | Defect prevention; continuous improvement; "every risk has coverage" [TestFort, 2025] |

Adoption reality check from TMMi's worldwide survey: 42% of organizations reach Level 3, only 11% reach Level 5 [TMMi survey, cited in Augment Code, 2026]. Expect the same shape for crews: L3 is the workhorse level, L5 is rare and asymptotic.

### 1.2 Why TMMi Must Be Adapted for Agent Crews

Classical TMMi assumes [Augment Code, 2026]:

| Assumption | Classical TMMi | Crew v2 Reality |
|---|---|---|
| Test authorship | Human-written, version-controlled | Agent-generated, non-deterministic |
| Application stability | Planned releases | Engineer rewrites code continuously per task |
| Output reliability | Same test, same result | Variable test counts/coverage per run |
| Primary risk | Insufficient process discipline | Confident-but-wrong AI output |
| Top-level driver | Continuous process improvement | Verification controls at scale |

The empirical failure data behind the adaptation: 30.68% of invalid LLM-generated tests fail on unresolved symbols and 17.25% on parameter mismatches (broken before execution) [empirical study via Augment Code, 2026]; 35.2% of LLM-generated code is less robust than human code, ~90% of those cases from missing conditional checks [robustness study via Augment Code, 2026]; package-hallucination rates average 19.7% across coding models (5.2% commercial, 21.7% open-source) [USENIX Security analysis via Augment Code, 2026]. None of these failure modes are visible to a process-maturity model that only asks "is the process documented?"

### 1.3 Design Rule: Gate on the Lowest Verification Control

Two rules are inherited unchanged:

- **Staged progression:** all criteria at level N must be met before claiming N+1 [TMMi Foundation].
- **Lowest-gate scoring:** maturity = the lowest rating of supporting process areas [TMMi assessment principle, via Augment Code, 2026; TestFort, 2025]. Applied to crews: *a crew that runs multi-agent orchestration but has no test-existence gate is Level 1 with Level-4 decoration.* Teams systematically over-rate by their most sophisticated capability; this model rates by the weakest verification control [Augment Code, 2026].

---

## Part 2 — The Crew Testing Maturity Model (CTMM)

Five levels. Each level: definition, observable criteria (all must hold), verification gate, metrics with numeric targets, and exit criteria.

### Level 1 — INITIAL (Ad-hoc, no verification)

**Definition.** No systematic testing exists in the crew loop. Code quality depends entirely on the individual agent's habits; nothing blocks untested output.

**Observable criteria (any one confirms L1):**
- Engineer produces zero test files in completed tasks [CONTEXT.md: COORD-01 three task types, zero test files; COORD-02 4 modules/135 lines, zero tests]
- Explicit "write tests" task requirements are ignored [CONTEXT.md: COORD-01]
- No agent has authority to block code lacking tests [CONTEXT.md]
- Verification agent times out on complex tasks and searches wrong directories [CONTEXT.md: critic limitations]
- Defects recur across runs because original failure cases are never regression-tested [CONTEXT.md: T09–T12]

**Gate:** none. This is the problem — any agent-generated code flows to release ungated [Augment Code, 2026, Stage-1 boundary-mismatch pattern].

**Metrics:** none tracked (defining trait).

**Exit criteria (all required):**
1. Every engineer task produces at least one test file, enforced by task contract, not agent goodwill.
2. A completion declaration without test paths is structurally rejected (message format, not persuasion).
3. Test existence is recorded per task in a log a router can read.

**Crew v2 status: L1 confirmed** (evidence above).

---

### Level 2 — MANAGED (Engineer-owned verification, artifact gates)

**Definition.** The producing agent is required to self-verify with real artifacts: tests exist, compile, and run, every task. Corresponds to TMMi L2 (policy + planning + monitoring) mapped to the agent-native Stage-2 compilation gate [TMMi Foundation; Augment Code, 2026].

**Observable criteria:**
- Test policy exists in the engineer's task contract: minimum test set per task (one test file per module, happy path + error path + boundary per module entry point)
- Every task's deliverable includes: source files, test files, and a test-run transcript (command + exit code)
- Generated tests pass a **compilation and build gate before merge/review** — the non-negotiable Stage-2 control [Augment Code, 2026]. Rationale: 30.68%+17.25% of invalid generated tests die pre-execution (§1.2)
- Generated tests are filtered on **pass-reliability** before being counted (a test that fails or errors is not evidence) [TestGen-LLM filter pattern: only 57% of generated tests passed reliably, Alshahwan et al., 2024]
- Unverified dependencies are rejected (anti-package-hallucination: imports must resolve to real, pinned packages; USENIX-average hallucination rate 19.7% [§1.2])

**Gate (Stage-2 control set, per Augment Code, 2026):**

| Gate element | What it verifies | Failure boundary |
|---|---|---|
| Project config match | Tests target actual project structure | Tests exercise the wrong scaffold |
| Framework conventions | Output is executable under the chosen runner | Tests cannot run at all |
| Compilation validation | Builds before review | Invalid tests block execution paths |
| Pass-reliability filter | Tests pass consistently, not by luck | Unstable tests counted as coverage |
| Production review | A second party reviews accepted tests | Coverage trusted too early |

**Metrics (targets):**
- Test-existence rate: **100%** of engineer tasks (non-negotiable at L2)
- Per-commit line coverage of changed code: **≥ 90% floor** [Google Testing Blog, 2020]
- Test-run transcript present per task: **100%**
- Pre-execution validity (generated tests that compile/import): **≥ 90%** (Meta saw 75% build correctly on first production attempt [Alshahwan et al., 2024]; a filtered agent loop should beat the unfiltered first pass)

**Exit criteria (all required):**
1. 20 consecutive engineer tasks with 100% test-existence and ≥90% changed-code coverage.
2. The verifier role exists as a distinct agent (can be critic retargeted) that *runs* the gate rather than reading code.
3. Flake rate on the suite measured and < 5% of runs.

---

### Level 3 — DEFINED (Tester-gated, role-split, blocking authority)

**Definition.** Verification is a distinct agent role with defined procedure, standard test-design practice across all missions, and bounded blocking authority. Corresponds to TMMi L3 (organization-wide standards, lifecycle integration) and the agent-native Stage-3 live-validation mindset [TMMi Foundation; Augment Code, 2026].

**Observable criteria:**
- A tester agent exists with: activation conditions, operating procedure, blocking conditions, output format, and calibration rules (currently all missing per CONTEXT.md "The Gap")
- **Role-split is structural:** generator and evaluator are different agents. Evidence this matters: LLM evaluators favor their own generations [NeurIPS, 2024], and self-preference persists even with fully objective rubrics [Pombal et al., 2025]; single-model self-verification inherits the model's own failure modes [SonarSource, 2026]
- Standard test-design taxonomy applied per module: unit (happy/error/boundary), integration (module interfaces), and requirement-traceability (every acceptance criterion maps to ≥1 test) — the TMMi L3 traceability goal [TestFort, 2025]
- Test pyramid proportions enforced: majority unit, fewer integration, few E2E [Fowler, 2018; Google's unit-first pyramid, SWE Book Ch. 11/14]
- Regression discipline: every fixed bug adds a pinned failing-case test before the fix is declared done (direct counter to T09–T12 recurrence [CONTEXT.md])
- Tester outputs structured verdicts (PASS/BLOCK + reason + evidence), consumable by the router

**Gate:** tester verdict is a **required pipeline stage** for all write-class tasks. Blocking conditions are explicit and bounded (see the companion blocking-authority output; preview: missing test file, failing test, coverage below floor, requirement without test, regression without pinned case).

**Metrics (targets):**
- Requirement-to-test traceability: **100%** of acceptance criteria
- Defect containment efficiency (defects found pre-merge / total defects): **≥ 60–70%** (TMMi L2-L3 band [TestFort, 2025])
- Regression recurrence rate (fixed bugs reappearing): **0** per mission
- Test case reuse rate: **≥ 20–30%** (TMMi L2 band, rising through L3 to 40–60% [TestFort, 2025])
- Verdict latency: tester completes gate on standard task in **≤ 1 router tick** (timeout fix prerequisite — critic currently times out on complex tasks [CONTEXT.md]; the tester scope must be per-artifact, not per-mission)

**Exit criteria (all required):**
1. 4 consecutive weeks with zero releases lacking tester verdicts.
2. Blocking authority exercised and *upheld* at least once without operator override (calibration evidence).
3. Disagreement-resolution path exists and has been exercised (engineer objects → router arbitrates → outcome logged).
4. Metric baseline recorded for all L4 metrics.

---

### Level 4 — MEASURED (Quantitative management, outcome metrics, drift detection)

**Definition.** Verification quality is measured with outcome metrics (not activity counts), thresholds are calibrated from data, and agent verification behavior is monitored for drift over time. Corresponds to TMMi L4 and agent-native Stage-4 outcome metrics + drift detection [TMMi Foundation; Augment Code, 2026].

**Observable criteria:**
- **Outcome over activity:** defect escape rate (post-release bugs / total bugs) is the headline metric; test count and pass-rate vanity metrics are demoted — Stage-4 explicitly replaces test volume with released quality [Augment Code, 2026]
- **Mutation scoring on core modules:** mutation score (killed mutants / non-equivalent mutants) measured per module. Mutation score is a stronger adequacy measure than coverage because it tests whether tests detect injected defects [Jain et al., 2023; Codecov, 2022; ACM, 2024]
- **Flake management institutionalized:** flake rate tracked, flaky tests quarantined with owner and deadline (Google: 1.5% of runs flaky, 16% of tests affected — without quarantine, one flaky test invalidates every red/green signal [Google Testing Blog, 2016])
- **Statistical process control:** thresholds reviewed against observed distributions (e.g., escape-rate p85), not set once
- **Drift detection:** verification outcomes tracked over time so silent degradation of the tester/gate itself is caught — behavioral drift is the Stage-4 control [Augment Code, 2026, mapping to CSA Agentic NIST AI RMF AG-MG.2]
- Property-based testing on algorithmic modules with CI-tuned profiles (fast deterministic profile per commit, deeper profile nightly — max_examples=100 CI / 1000 nightly, deadline=None on slow profiles [Hypothesis docs; qaskills.sh, 2026])

**Metrics (targets, with warning lines):**

| Metric | Definition | Target | Warning |
|---|---|---|---|
| Defect escape rate | Post-release bugs / all bugs | ≤ 10% | > 15% |
| Mutation score (core modules) | Killed / non-equivalent mutants | ≥ 70% | < 60% |
| Defect containment efficiency | Found-in-phase / total defects | ≥ 75–85% [TestFort, 2025] | < 75% |
| Test case reuse rate | Reused / total test cases | ≥ 40–60% [TestFort, 2025] | Falling |
| Flake rate | Flaky runs / total runs | ≤ 1.5% [Google, 2016] | > 3% |
| Automation ROI vs coverage | (Savings − investment)/investment | ≥ 150–200% at ≥ 60–80% coverage [TestFort, 2025] | Negative |
| Gate false-block rate | Blocks overturned on appeal / blocks | ≤ 20% | > 30% (calibrator) |
| Verifier residual error | Bugs in verdict-passed artifacts | ≤ 5% (vs 65% unverified baseline [Ravuri & Amarasinghe, 2025]) | Rising |

**Exit criteria (all required):**
1. Eight weeks of continuous metric collection with no gaps.
2. At least one threshold recalibrated from data (proves the loop works).
3. Mutation scoring runs on ≥ 3 core modules with score ≥ 70%.
4. Drift alerting demonstrated: at least one real degradation caught by metric before human notice.

---

### Level 5 — OPTIMIZING (Defect prevention, self-improvement, governed autonomy)

**Definition.** Verification prevents defect classes proactively, the crew improves its own testing assets from failure data, and multi-agent verification runs under explicit governance policy. Corresponds to TMMi L5 and agent-native Stage-5 governed orchestration [TMMi Foundation; Augment Code, 2026].

**Observable criteria:**
- **Defect prevention loop:** recurring defect classes get standing property-based or fuzz tests *before* the next implementation task (TMMi L5 defect-prevention PA [TMMi Foundation])
- **"Every risk has coverage":** risk-based testing — each mission's risk register maps to test assets; risk coverage completeness tracked [TestFort, 2025]
- **Governed coordination policy:** explicit human-in-the-loop policy defining where agent judgment must escalate; delegation chains visible; autonomy calibrated to boundaries [Augment Code, 2026]. Rationale: independent agents amplify errors 17.2× unchecked vs 4.4× with centralized coordination [coordination benchmark via Augment Code, 2026]
- **Autonomy calibration as the maturity signal, not automation volume** — automation percentage is a false maturity proxy [Augment Code, 2026]
- **Cross-agent learning:** tester verdicts and escape data feed engineer contract updates (the improvement loop), with change control

**Metrics (targets):**

| Metric | Definition | Target | Warning |
|---|---|---|---|
| Risk coverage completeness | Covered risks / identified risks | ≥ 95% ("every risk has coverage" [TestFort, 2025]) | < 90% |
| Defect containment efficiency | Found-in-phase / total | ≥ 85–95% (L5 band [TestFort, 2025]) | < 85% |
| Test case reuse rate | Reused / total | ≥ 80% [TestFort, 2025] | Falling |
| Escape rate trend | Δ escape rate / quarter | ≤ 0 (monotonic decline) | Rising |
| Governed-agent compliance | Handoffs within policy / handoffs | 100% | < 98% |

**Exit criteria:** none — L5 is a maintenance regime, not a destination. TMMi survey data (42% of orgs at L3, 11% at L5 [TMMi survey via Augment Code, 2026]) predicts most crews stabilize at L3–L4; treat L5 claims with suspicion (§3, anti-pattern A5).

---

## Part 3 — Assessment Procedure (Crew Self-Assessment)

### 3.1 The Gate-Order Questionnaire (apply strictly in order)

Rate the crew by the **lowest unmet gate**, never the highest deployed capability [Augment Code, 2026; TMMi principle]. Answer from logs, not intentions.

| # | Question | If "No", maximum level |
|---|---|---|
| 1 | Do 100% of engineer tasks produce at least one test file, structurally enforced? | **L1** |
| 2 | Do all generated tests pass compile/build and pass-reliability gates before being counted? | **L1** |
| 3 | Does a distinct tester agent issue PASS/BLOCK verdicts on every write-class task, with blocking authority that has survived a live appeal? | **L2** |
| 4 | Is requirement-to-test traceability 100%, and is regression recurrence zero? | **L2** |
| 5 | Are escape rate, mutation score, and flake rate measured continuously with calibrated thresholds? | **L3** |
| 6 | Is behavioral drift of the verification layer itself detected and alerted? | **L3** |
| 7 | Is multi-agent coordination governed by explicit human-in-the-loop policy, with 100% handoff compliance? | **L4** |

**Scoring rule:** the crew's level is the highest N such that all questions up to and including the N-level questions are "Yes". One "No" at L2 questions caps the crew at L1 regardless of any L4 instrumentation that exists.

### 3.2 Worked Assessment — Crew v2, September 2026

| # | Question | Answer | Evidence |
|---|---|---|---|
| 1 | Test files structurally enforced? | **No** | COORD-01: zero test files despite explicit requirement [CONTEXT.md] |
| 2 | Compile/pass-reliability gates? | **No** | No gate exists; completer does not run tests [CONTEXT.md] |
| 3+ | — | n/a | Capped at Q2 |

**Verdict: CTMM Level 1.** Secondary confirmations: no blocking authority [CONTEXT.md]; critic times out on complex tasks [CONTEXT.md]; razor changes wording when told not to (ungoverned mutation of artifacts) [CONTEXT.md]; bugs recur un-regression-tested (T09–T12) [CONTEXT.md].

### 3.3 Immediate Priorities (unlocking L2)

1. **Structural, not persuasive, enforcement.** The root cause is documented: nothing in the engineer's instructions makes tests a completion condition, and no agent can block [CONTEXT.md]. The fix is a message contract: a "done" declaration without test paths + run transcript is malformed, and the router bounces it. Note Meta's filter-based architecture as the design pattern: filters (builds? passes reliably? adds coverage?) *before* human review [Alshahwan et al., 2024].
2. **Retarget the critic into the tester role for L2.** Do not build a new agent (guardrails prohibit roster changes; and agent-scaling research says heterogeneous systems plateau ~8 agents — Crew v2 is already there [agent-scaling study via Augment Code, 2026]). Fix the two documented critic defects while re-tasking: timeout on complex tasks, wrong-directory searches [CONTEXT.md] — scope the verifier to the task's artifact list, not the whole repo.
3. **Adopt Google's coverage posture now** (it costs nothing): per-commit ≥ 90% floor, 99% aspirational, no project-wide goal above 90% [Google Testing Blog, 2020].
4. **Instrument before optimizing:** log test-existence, coverage, and verdicts per task from day one of L2 — the L4 baseline.

---

## Part 4 — Anti-Patterns

| # | Anti-pattern | Why it fails | Source |
|---|---|---|---|
| A1 | Skipping levels ("we'll add mutation testing before tests exist") | Staged models break when foundations are missing; L4 metrics on an L1 process measure noise | [TMMi Foundation; TestFort, 2025] |
| A2 | Rating by highest capability | "We run multi-agent orchestration" while no compile gate exists = L1 with decoration; teams systematically over-rate | [Augment Code, 2026] |
| A3 | Vanity coverage | Project-wide >90% coverage goals are mostly not worth it; per-commit floors are what catch regressions | [Google Testing Blog, 2020] |
| A4 | Self-verification as maturity | Same-model self-checks carry documented self-preference bias, even with objective rubrics | [NeurIPS, 2024; Pombal et al., 2025] |
| A5 | Automation volume as maturity | Automation percentage is a false proxy; autonomy *calibration* is the signal | [Augment Code, 2026] |
| A6 | Unbounded agent addition | Error amplification 17.2× unchecked; heterogeneous plateaus ~8 agents; Crew v2 roster is at the plateau | [coordination & scaling studies via Augment Code, 2026] |
| A7 | Ignoring flakiness | 1.5% flaky runs can invalidate the suite's red/green signal entirely | [Google Testing Blog, 2016] |
| A8 | Trusting pass-counts of generated tests | Only 57% of Meta's generated tests passed reliably; unfiltered counts overstate quality | [Alshahwan et al., 2024] |

---

## Part 5 — Practical Recommendations

| Recommendation | Implementation | Tools | Threshold |
|---|---|---|---|
| Enforce test existence structurally | Engineer task contract: done-declaration requires test file paths + run transcript; router bounces malformed declarations | Message contract in crew protocol (no code change) | 100% of engineer tasks |
| Compile + pass-reliability gate | Two-stage filter: (1) tests import/collect, (2) pass on 2 consecutive runs | pytest `--collect-only`, repeat-run | 100% pre-execution validity; pass-reliability 2/2 |
| Per-commit coverage floor | Coverage measured on changed lines only, reported per task | coverage.py | ≥ 90% changed-line [Google, 2020] |
| Role-split verifier | Retarget critic → tester with per-artifact scope | Crew roster (no new agent) | Verdict on 100% of write tasks |
| Traceability | Every acceptance criterion → ≥ 1 test id, recorded in task record | Test ids in task log | 100% |
| Mutation scoring (L4 entry) | Score core modules only; expand by escape data | mutmut (Python) / Stryker (JS) / PIT (JVM) [mutmut docs; Stryker docs] | ≥ 70% core modules |
| Property-based profile (L4) | Fast CI profile + deep nightly profile | Hypothesis settings profiles [Hypothesis docs] | max_examples=100 CI / 1000 nightly |
| Flake quarantine (L4) | Auto-quarantine >3% flaky tests with owner+deadline; never block on quarantined tests | CI flake tracking | ≤ 1.5% run-level flake [Google, 2016] |
| Escape-rate headline (L4) | Post-release bugs / total bugs, weekly | Defect log | ≤ 10%, falling |
| Governance policy (L5) | Written human-in-the-loop policy: which verdicts agents may overturn vs must escalate | Policy doc + router rules | 100% handoff compliance |

---

## Part 6 — Metrics Catalog (cross-level summary)

| Metric | Level | Definition | Measure | Target | Warning |
|---|---|---|---|---|---|
| Test-existence rate | 2 | Engineer tasks with ≥1 test file / all engineer tasks | Task log | 100% | < 100% |
| Changed-line coverage | 2 | Lines covered in changed code / changed lines | coverage.py per task | ≥ 90% | < 90% |
| Pre-execution validity | 2 | Generated tests that collect / generated tests | pytest --collect-only | ≥ 90% | < 75% (Meta's unfiltered baseline) |
| Traceability | 3 | Acceptance criteria with ≥1 test / criteria | Task log | 100% | < 100% |
| Regression recurrence | 3 | Fixed bugs re-failing / fixed bugs | Regression suite | 0 | > 0 |
| Defect containment efficiency | 3–5 | Defects found pre-release / total [TestFort, 2025] | Defect log | ≥ 60%→85% by level | Falling |
| Test case reuse rate | 3–5 | Reused / total test cases [TestFort, 2025] | Test inventory | 20%→80% by level | Falling |
| Defect escape rate | 4 | Post-release / total bugs [Augment Code, 2026] | Defect log | ≤ 10% | > 15% |
| Mutation score | 4 | Killed / non-equivalent mutants [Jain et al., 2023] | mutmut/Stryker/PIT | ≥ 70% | < 60% |
| Flake rate | 4 | Flaky runs / total runs [Google, 2016] | CI stats | ≤ 1.5% | > 3% |
| Gate false-block rate | 4 | Overturned blocks / blocks | Appeal log | ≤ 20% | > 30% |
| Verifier residual error | 4 | Bugs in verdict-passed artifacts / verdict-passed artifacts | Sampling audit | ≤ 5% | Rising (vs 65% unverified [Ravuri & Amarasinghe, 2025]) |
| Risk coverage completeness | 5 | Covered risks / identified risks [TestFort, 2025] | Risk register | ≥ 95% | < 90% |
| Governed handoff compliance | 5 | In-policy handoffs / handoffs [Augment Code, 2026] | Router log | 100% | < 98% |

---

## References

1. [TMMi Foundation] TMMi Model — five levels, 16 process areas, staged assessment. https://www.tmmi.org/tmmi-model/
2. [TestFort, 2025] Baglai, O. & Kovalenko, I. "Testing Maturity Model: TMMi in Software Testing — 2025 Guide." Sep 3, 2025. Level definitions, observable signs, metrics-by-level table, TMMi user-survey impact data. https://testfort.com/blog/tmm-in-software-testing
3. [Augment Code, 2026] "QA Maturity Model for Agent-Native Teams: 5 Stages." Jun 30, 2026. Agent-native five-stage model; TMMi-vs-agent assumption table; verification-gap framing; TestGen-LLM filter architecture; invalid-test causes (30.68% symbols, 17.25% params); robustness (35.2%, 90% conditional checks); package-hallucination rates (19.7%/5.2%/21.7%, USENIX); multi-agent error amplification (17.2× vs 4.4×) and scaling plateaus (~4 homogeneous / ~8 heterogeneous); TMMi survey distribution (42% L3, 11% L5). https://www.augmentcode.com/guides/qa-maturity-model-agent-native-teams
4. [Ravuri & Amarasinghe, 2025] "Eliminating Hallucination-Induced Errors in LLM Code Generation with Functional Clustering." arXiv:2506.11021. MIT. Error ~65%→2% with execution-based verifier; 0% at conservative threshold. https://arxiv.org/abs/2506.11021
5. [Alshahwan et al., 2024] "Automated Unit Test Improvement using Large Language Models at Meta (TestGen-LLM)." arXiv:2402.09171; ACM FSE 2024. 75% built correctly, 57% passed reliably, 25% increased coverage; 73% of recommendations accepted for production. https://arxiv.org/abs/2402.09171
6. [DORA, 2025/2026] "Balancing AI tensions: Moving from AI adoption to effective SDLC use." Baolin & Harvey, Mar 10, 2026, reporting the 2025 DORA State of AI-assisted Software Development: 90% AI use at work; 30% little/no trust in AI code; higher AI adoption → higher throughput *and* instability; verification tax; small-batches countermeasure. https://dora.dev/insights/balancing-ai-tensions/
7. [Stack Overflow, 2025] 2025 Developer Survey — AI section: 46% distrust AI accuracy vs 33% trust; 3.1% highly trust. https://survey.stackoverflow.co/2025/ai
8. [Google Testing Blog, 2020] Arguelles, Ivanković, Bender. "Code Coverage Best Practices." Aug 7, 2020. Per-commit 99% reasonable, 90% lower bound; project-wide >90% mostly not worth it. https://testing.googleblog.com/2020/08/code-coverage-best-practices.html
9. [Google Testing Blog, 2016] "Flaky Tests at Google and How We Mitigate Them." May 27, 2016. 1.5% of test runs flaky; ~16% of tests affected; quarantine + automatic re-run strategies. https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html
10. [NeurIPS, 2024] "LLM Evaluators Recognize and Favor Their Own Generations." Self-preference bias evidence. https://neurips.cc/virtual/2024/poster/96672
11. [Pombal et al., 2025] "Self-Preference Bias in Rubric-Based Evaluation of Large Language Models." Self-preference persists with fully objective, programmatically verifiable criteria. https://openreview.net/forum?id=1837ctErks
12. [Jain et al., 2023] "The Difference Between Coverage and Mutation Score." Mutation score recommended over coverage for test adequacy. https://par.nsf.gov/servlets/purl/10555509
13. [ACM, 2024] "Mutation Testing as a Quality Assurance Technique" — mutation score more accurate than traditional coverage. https://dl.acm.org/doi/10.1145/3701625.3701629
14. [Fowler, 2023] "Test Driven Development." Red-Green-Refactor; test-list; interface-first benefit. https://martinfowler.com/bliki/TestDrivenDevelopment.html
15. [Fowler, 2018] "The Practical Test Pyramid." https://martinfowler.com/articles/practical-test-pyramid.html
16. [Hypothesis docs] Settings profiles for CI vs nightly depth (max_examples, deadline). https://hypothesis.readthedocs.io/en/latest/settings.html
17. [mutmut docs] Python mutation testing. https://mutmut.readthedocs.io/ | [Stryker docs] https://stryker-mutator.io/docs/
18. [SonarSource, 2026] "Agentic Automation" — agent self-checks inherit the model's own failure modes. https://www.sonarsource.com/resources/library/agentic-automation/
19. [Crew v2 internal] CONTEXT.md — trials COORD-01, COORD-02, T09–T12; agent limitations; "The Gap". STATUS.md — internal researcher findings (TMMi L1→L5 path, mutation + requirement-coverage gates confirmed). Both in faresrafat3/crew-research-council, RESEARCH-COUNCIL/.

---

*Cross-references: this model defines the ladder that `tdd-protocol.md` (L2–L3 procedure), `blocking-authority.md` (L3 gate design), `testing-framework-spec.md` (tool-level implementation), and `quality-metrics.md` (full metric catalog) build on. LEVEL ASSESSMENT SHOULD BE RE-RUN WEEKLY — the questionnaire in Part 3.1 is designed for log-based scoring in under 10 minutes.*
