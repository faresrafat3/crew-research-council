# Test Quality Metrics

## Executive Summary

16 metrics separate signal from false confidence: coverage, mutation, req coverage, property depth, flake, FP, escape, drill pass, duration, RED-witness, tautology, mock ratio, readability, quarantine age, KB lag.

Coverage without mutation is vanity; mutation without RED-witness is theater; all three without flake control is noise. The industry baseline is sobering: Google reports 1.5% flaky with 16% of suites showing some flakiness [VT 2022], 4.56% of daily failures are flakes with a 2-16% budget for reruns [Bell 2018], and DeFlaker achieves 95.5% recall with 1.5% false alarms [Bell 2018].

For Crew v2, the gate is: line >=80%, mutation >=70%, REQ >=90% FULL, flake <1% blocking, FP <2%, escape <1/20, RED 100%, duration <10 min. Anything less is advisory; anything more without calibration is false confidence.

## Key Findings

1. **Google flaky baseline:** 1.5% of tests flaky at any moment, 16% of suites exhibit some flakiness over time [VT 2022] — flakiness is systemic, not exceptional.
2. **TAP scale:** 73K commits / 1.6M executions measured, 4.56% of test failures attributed to flakes [Bell et al., 2018] — at scale, even small flake rates dominate failure triage.
3. **Flakiness economics:** 16% flakiness observed with 84% pass-to-fail flakes; teams budget 2-16% of CI for reruns [Bell et al., 2018] — reruns mask the problem while taxing velocity.
4. **DeFlaker validation:** 1,874 confirmed flakes detected with 95.5% recall and 1.5% false alarms by checking coverage of changed code [Bell et al., 2018] — no-change-no-blame is the core heuristic.
5. **Flake response playbook:** mock / quarantine / fix / remove / document / monitor — six canonical responses; quarantine is triage, not treatment.
6. **Auto-quarantine is advisory:** automatic quarantine without human review hides real regressions; keep it advisory with a 14-day SLA [FlakyTest 2026].
7. **PR gate budget:** PR gate <10 min, flake <1% blocking — beyond 10 min engineers bypass the gate [KnowMBA 2025].
8. **14-day SLA, 5-15 E2E:** quarantined tests must fix-or-delete within 14 days; cap E2E at 5-15 critical journeys, push the rest down the pyramid [KnowMBA 2025].
9. **FP erosion:** false positives erode trust faster than false negatives erode quality — one bad block teaches engineers to ignore the tester [ArizenAI 2025].
10. **High coverage + low mutation = false confidence:** 100% line coverage with 4% mutation score proves execution without assertion [ArXiv 2025] — coverage measures reach, mutation measures kill.

## Detailed Analysis

### 1. Flake detection: history flips + DeFlaker no-change-coverage

History-based detection flags tests that flip pass/fail on identical code across reruns (20-run history). DeFlaker adds the decisive filter: if a failing test did not execute any changed lines, it cannot be a true regression — mark flaky, not failed [Bell et al., 2018]. This yields 95.5% recall with 1.5% false alarms on 1,874 real flakes. Crew v2 ledger stores per-test 20-run histories to compute flip rate; DeFlaker logic applies at the tester gate (fail without coverage delta → quarantine candidate, not block).

### 2. Brittleness: refactor probes

Brittle tests break on behavior-preserving refactors (renames, extraction, reordering). Detection: run refactor probes — rename private, reorder independent statements, reformat — and flag tests that fail. A test that fails when nothing behavioral changed is coupled to implementation, not specification. Track brittle-break rate per suite; high rates predict future maintenance tax.

### 3. Oracle quality: AST lint for privates

Tests that assert on private methods, internal state, or implementation details rot first. AST lint flags: access to `_private`, `__mangled`, reflection into internals, snapshot of volatile output (timestamps, IDs, ordering without sort). Rule: test the contract (public API + REQ), not the machinery. Oracle violations are counted per task; gate is 0.

### 4. Vacuous pass: mutation survivors + assert lint + self-read tautology

A test that passes on broken code is worse than no test — it manufactures confidence. Three overlapping detectors:
- **Mutation survivors:** mutmut/cosmic-ray mutants that survive the suite indicate unasserted behavior. Survivor >10% predicts escapes [ArXiv, 2025].
- **Assert lint:** flag tests with zero asserts, asserts on constants (`assert True`, `assert 1 == 1`), or asserts that cannot fail given the setup.
- **Self-read tautology check** [Eleks 2025]: re-read each test and ask "what input would make this fail?" If none exists, it is a tautology. Tautologies gate at 0.

### 5. Over-mock: counts

Mock ratio = mocked dependencies / total dependencies per test. Above 15% the test verifies the mocking framework, not the system. Count `Mock()`, `patch()`, `stub()` per test file; flag suites where mocks outnumber real collaborators. Integration holes hide behind mocked boundaries — every mock is an untested contract.

### 6. Ledger: per-task runs, per-agent FP/FN, per-test 20-run histories

The ledger is the measurement substrate. Per-task: runs, coverage, mutation, duration, RED-witness. Per-agent: FP/FN rates (overturned blocks / missed escapes) for tester calibration. Per-test: 20-run pass/fail/flaky history for flip-rate and trend slope. Without this ledger, all 16 metrics are anecdotes; with it, targets tighten empirically quarter over quarter.

## Practical Guidance

| Situation | Metric to watch | Action |
|-----------|-----------------|--------|
| Coverage rising, escapes flat | Mutation score, coverage/mutation gap | If gap >20%, gate on mutation not coverage |
| CI red but code correct | Flake rate, FP rate | Quarantine flip-rate >2%, appeal bad blocks |
| Suite slow, engineers bypass | Gate duration, E2E count | Slim to <10 min, cap E2E 5-15 |
| Tests pass, prod breaks | Escape rate, RED-witness, tautologies | Enforce RED 100%, tautology lint 0 |
| Mocks everywhere, integration breaks | Mock ratio | Cap <15%, add contract/integration test |
| Quarantine growing | Quarantine age | 14-day fix-or-delete SLA, no extensions |
| Same bug twice | KB lag | 0 escapes without KB entry |

## Metrics Catalog

| # | Metric | Definition | Target | Gate |
|---|--------|------------|--------|------|
| 1 | Line coverage | % executable lines exercised | >=80% | Advisory → blocking at 80% |
| 2 | Branch coverage | % branches taken both ways | >=70% (75% Stripe) | Advisory |
| 3 | Mutation score | % mutants killed | >=70% (80% stretch) | Blocking at 70% |
| 4 | REQ coverage | % REQs with FULL test | >=90% FULL | Blocking |
| 5 | PBT depth | @given properties per function | >=2 | Advisory |
| 6 | Flake rate | Flip-rate over 20 runs | <1% blocking, quarantine at >2% | Blocking / quarantine |
| 7 | False-positive rate | Overturned blocks / total blocks | <2% | Calibrate tester |
| 8 | Escape rate | Prod bugs per 20 tasks | <1/20 | Tighten gates if exceeded |
| 9 | Drill pass rate | Broken-REQ builds caught | 100% | Blocking |
| 10 | Gate duration | PR gate wall-clock | <10 min | Slim/parallelize if exceeded |
| 11 | RED-witness rate | DONE tasks with failing-first proof | 100% | Blocking |
| 12 | Tautologies | Tests that cannot fail | 0 | Blocking |
| 13 | Mock ratio | Mocked / total deps | <15% | Advisory → refactor |
| 14 | Readability score | Lint + naming + structure pass | >=90% | Advisory |
| 15 | Quarantine age | Days sidelined | <14 days | Fix-or-delete SLA |
| 16 | KB lag | Escapes without KB entry | 0 | Blocking follow-up |

## References

1. [VT, 2022] Flaky Tests at Google: 1.5% flaky, 16% suites affected.
2. [Bell et al., 2018] DeFlaker: 73K commits, 1.6M executions, 4.56% failures from flakes, 95.5% recall, 1.5% false alarms on 1,874 flakes; 2-16% rerun budget.
3. [FlakyTest, 2026] Auto-quarantine must remain advisory with human review.
4. [KnowMBA, 2025] Test Automation Strategy: <10 min gate, <1% flake, 14-day SLA, 5-15 E2E journeys.
5. [ArizenAI, 2025] The End of Determinism: FP erosion destroys CI trust.
6. [ArXiv, 2025] MutGen: 100% coverage / 4% mutation gap proves false confidence; survivors predict escapes.
7. [Eleks, 2025] Self-read tautology check: every test must have a failing input.
8. [SQRBOK, 2025] Industry Quality Practices: Google 150M tests/day, pyramid distribution.

---

## [DEEP DIVE]: Industry Benchmarks, Team-Specific Targets, Visualization, and Leading Indicators

### 1. Industry Benchmarks for Each Metric

| Metric | Google [VT, 2022; Bell et al., 2018] | Microsoft [SQRBOK, 2025] | Stripe [KnowMBA, 2025] | Meta [ArXiv, 2025] | Crew v2 Target |
|--------|------|----------|--------|------|----------------|
| Line coverage | 80% (recommended) | 75-85% | 80% | 70-90% | 80% |
| Branch coverage | 70% | 65-75% | 75% | 60-80% | 70/75% |
| Mutation score | — | — | — | 60-80% | 70/80% |
| Flake rate | 1.5% reported, 16% some | <2% | <1% | <2% | <1% blocking |
| False-positive rate | — | — | — | — | <2% |
| Escape rate | — | <1/20 tasks | — | — | <1/20 |
| PBT depth | — | — | — | 2-5 props/func | >=2 |
| E2E count | — | 5-15 journeys | — | — | <=10 FULL |
| PR gate time | <10 min | <15 min | <10 min | — | <10 min |
| Test count/day | 150M | — | — | — | N/A (per-task) |

**Key benchmark sources:**
- Google: 150M tests/day, 1.5% flaky, 4.56% of failures from flakes [VT, 2022; Bell et al., 2018]
- 100% line coverage with 4% mutation score proves execution without assertion [ArXiv, 2025]
- 80% coverage is reasonable; 100% is vanity producing low-value tests [PrecisionAI, 2026]
- DeFlaker: 95.5% recall, 1.5% false alarms on 1,874 flakes [Bell et al., 2018]

### 2. Setting Team-Specific Targets

**Target-setting methodology** [KnowMBA, 2025; TMMi Foundation, 2018]:

1. **Baseline first**: Run 20 tasks with no gates. Measure actual coverage, mutation, flake, escape rates.
2. **Set targets at P50 + 1σ**: If baseline coverage is 65%, target 75% (not 90% immediately).
3. **Tighten every quarter**: Increase targets by 5% absolute each quarter until industry benchmark is reached.
4. **Never set targets below baseline**: If baseline mutation is 40%, don't set 70% immediately — set 55% first.

**Crew v2 specific targets (evidence-based):**

| Metric | Baseline (COORD-01/02) | Phase 2 Target | Phase 3 Target | Phase 4 Target |
|--------|------------------------|----------------|----------------|----------------|
| Line coverage | 0% | 60% | 80% | 85% |
| Mutation score | 0% | 50% | 70% | 80% |
| Flake rate | unknown | <5% | <2% | <1% |
| REQ-coverage | 0% | 70% | 90% | 95% |
| RED-witness | 0% | 80% | 100% | 100% |
| Escape rate | unknown | <1/10 | <1/20 | <1/30 |

**Target adjustment rules:**
- If appeal success > 5%: loosen threshold by 5% absolute.
- If escape rate >= 1/10: tighten threshold by 5% absolute.
- If FP rate > 5%: loosen and add lint rules.
- If gate time > 10 min: slim suite or parallelize.

### 3. Visualizing Test Quality Over Time

**Dashboard layers** [GitHub Community, 2025; CTRF, 2026]:

| Layer | Tool | What It Shows |
|-------|------|---------------|
| 1. PR-level | CTRF GitHub Action | Flaky summary, pass/fail per PR |
| 2. Artifact | `upload-artifact` + `dorny/test-reporter` | JUnit XML, coverage JSON, mutation report |
| 3. Trend | Custom dashboard (Grafana/HTML) | Coverage/mutation/flake trend over 30 tasks |
| 4. Audit | Ledger DB query | Per-agent FP/FN, per-test 20-run history |

**CTRF report structure** [CTRF, 2026]:
```json
{
  "results": {
    "tool": { "name": "pytest" },
    "summary": {
      "tests": 42, "passed": 40, "failed": 1, "flaky": 1,
      "start": 1706828654274, "stop": 1706828655782
    },
    "tests": [
      { "name": "test_currency_conversion", "status": "passed", "duration": 801 },
      { "name": "test_flaky_network", "status": "flaky", "duration": 1200 }
    ]
  }
}
```

**Trend chart metrics (30-task rolling window):**
- Line coverage (target: 80%)
- Mutation score (target: 70%)
- Flake rate (target: <1%)
- Escape rate (target: <1/20)
- Gate duration (target: <10 min)
- RED-witness rate (target: 100%)

**Visualization tools:**
- GitHub Pages: host static HTML dashboard from `gh-pages` branch
- Allure Report: `pytest --alluredir=allure-results`, upload as artifact
- Grafana: query ledger DB for real-time metrics
- Simple: `coverage html` generates `htmlcov/index.html` per run

### 4. Leading Indicators That Predict Test Effectiveness

**Leading indicators** (predict future quality, not just report past quality) [KnowMBA, 2025; ArXiv, 2025]:

| Leading Indicator | What It Predicts | How to Measure | Warning Threshold |
|-------------------|------------------|----------------|-------------------|
| **Mutation survivor count** | Future escape rate | mutmut survivors per task | >10% survivors |
| **Flake rate trend** | CI trust erosion | 20-run history slope | Positive slope |
| **RED-miss rate** | Engineer compliance | % DONE without RED | >5% |
| **Oracle violation rate** | Test quality decay | Lint count per task | >0 |
| **Appeal success rate** | Tester calibration | Overturned blocks / total | >5% |
| **Coverage/mutation gap** | False confidence | coverage% - mutation% | >20% gap |
| **PBT depth** | Edge case coverage | @given count per function | <2 |
| **Quarantine age** | Flake debt | Days sidelined | >14 days |
| **KB lag** | Prevention decay | Escapes without KB entry | >0 |
| **Rounds to green** | Engineer TDD skill | Fix iterations per HOLD | >3 |

**Predictive model:**
- If mutation survivors > 10% AND coverage/mutation gap > 20%: predict escape rate will exceed 1/10 within 10 tasks. Action: tighten mutation gate.
- If flake rate trend is positive AND quarantine age > 7 days: predict CI trust will erode. Action: enforce 14-day fix/delete SLA.
- If RED-miss rate > 5%: predict engineer SOUL is not being followed. Action: re-add iron law, audit SOUL.

**Lagging indicators** (report past quality, for comparison):
- Escape rate (confirmed bugs in production)
- False-positive rate (overturned blocks)
- Drill pass rate (broken REQs caught)

**References for deep dive:**
- [VT, 2022] Flaky Tests at Google: 1.5%/16% flakiness benchmarks
- [Bell et al., 2018] DeFlaker: 95.5% recall, 1.5% false alarms
- [SQRBOK, 2025] Industry Quality Practices: Google 150M tests/day, pyramid
- [KnowMBA, 2025] Test Automation Strategy: budgets, 14-day rule, targets
- [PrecisionAI, 2026] Frontend Testing: 80% vs vanity 100%
- [ArXiv, 2025] MutGen: 100%/4% gap, mutation survivors predict escapes
- [GitHub Community, 2025] Native Test Results Dashboard: workarounds
- [CTRF, 2026] Flaky Tests on Actions: JSON report format
- [TMMi Foundation, 2018] Level 4: measurement precedes optimization
- [ArizenAI, 2025] The End of Determinism: FP erosion prediction
