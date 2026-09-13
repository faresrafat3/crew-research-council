# Test Quality Metrics (Complete Specification)

## Executive Summary
Sixteen metrics measure the crew's test quality across four families: defect effectiveness (coverage, mutation, REQ-coverage), suite health (flake rate, quarantine age, gate time, PBT depth), process compliance (RED-witness, rounds-to-green, verdict latency), and calibration (false positives, escapes, appeal success, block rate). Each metric has a definition, measurement source, target, and warning threshold — a metric without an action threshold is decoration and is excluded. Targets are phased from the measured zero-state baseline (Crew v2 currently has no test files) through 60/80/85% coverage and 50/70/80% mutation across implementation phases, using baseline-first target setting rather than industry numbers dropped onto a Level 1 process. Leading indicators — mutation survivors, coverage/mutation gap, RED-miss rate, quarantine age — predict future escapes before lagging dashboards show them.

## Key Findings
- Measurement precedes optimization: TMMi places quantitatively-managed testing at Level 4, above the crew's current Level 1 [TMMi Foundation, 2018].
- No single metric survives gaming: 100% line coverage with a 4% mutation score proves tests that execute without asserting [arXiv:2506.02954]; the coverage/mutation gap (>20 points) is itself a leading indicator of false confidence.
- Baseline-first targets: measure 20 ungated tasks, set targets near P50+1σ, tighten quarterly by ≤5 absolute [DEEP DIVE §2; KnowMBA, 2025].
- Industry anchors: Google runs ~150M tests/day with 1.5% reported flakiness (16% show some) [Micco, 2016; SQRBOK, 2025]; DeFlaker detects flakes at 95.5% recall / 1.5% false alarms [Bell et al., 2018].
- Mutation floors: practitioner guidance puts useful scores at 60-80%; unbiased LLM/human oracle baselines are ~43-45%, so targets must assume req-derived oracles plus per-REQ slices [CircleCI, 2026; Molinelli et al., ASE 2025].
- Leading indicators outperform lagging ones: mutation survivors, flake-trend slope, RED-miss rate, and quarantine age predict escapes and CI-trust erosion before dashboards do [DEEP DIVE §4].
- Both calibration directions need a metric: false positives (too strict) and escapes (too lenient) — a tester optimized on one silently fails the other.
- Visualization is layered: PR-level CTRF reports, artifact uploads, a 30-task trend dashboard, and ledger queries for audit [CTRF, 2026].

## Detailed Analysis

### The 16-metric catalog

| # | Metric | Formula / Source | Target | Warning |
|---|---|---|---|---|
| 1 | Line coverage | coverage JSON, project-wide | 80% (path: 60→80→85) | <70% |
| 2 | Branch coverage | `--cov-branch` | 70% | <65% |
| 3 | Mutation score | mutmut, per-REQ slice | 50→70→80% | <60% |
| 4 | REQ-coverage | REQ-IDs with ≥1 req-derived test | 90% (P1) | <70% |
| 5 | RED-witness rate | ledger | 100% | any miss |
| 6 | Flake rate (blocking) | 20-run flip history | <1% | >2% |
| 7 | Quarantine age | days in flaky lane | ≤14 days | >14 days |
| 8 | Gate time | commit → verdict | <10 min | >15 min |
| 9 | Verdict latency | GREEN → verdict | <5 min | >15 min |
| 10 | Rounds to green | fix loops per task | ≤3 (P50 ≤1) | >3 |
| 11 | False-positive rate | overturned blocks / blocks | <2% | >5% |
| 12 | Escape rate | post-PROMOTE bugs per 20 FULL | <1 | ≥2 |
| 13 | Appeal success | overturned appeals / appeals | 1-5% | >5% or <1% |
| 14 | Block rate | (HOLD+ROLLBACK) / verdicts | 5-50% | >50% or <5% |
| 15 | PBT depth | @given properties per function | ≥2 | <2 on new modules |
| 16 | KB lag | escapes without KB entry within 7d | 0 | >0 |

### Leading vs lagging
Leading (predict): mutation survivors >10% plus coverage/mutation gap >20 points predicts escape rate >1/10 within ~10 tasks → tighten mutation gate. Positive flake-trend slope with quarantine age >7 days predicts CI-trust erosion → enforce the 14-day fix-or-delete SLA. RED-miss >5% predicts engineer SOUL noncompliance → re-audit the iron law. Lagging (report): escape rate, false-positive rate, drill pass rate.

### Visualization
Four layers: (1) PR-level CTRF summary on every run; (2) artifacts — junit.xml, coverage JSON, mutation JSON; (3) a 30-task rolling trend dashboard for coverage, mutation, flake, escape, and gate time; (4) ledger queries for per-agent FP/escape and per-test 20-run histories. Tools: dorny/test-reporter, Allure, Grafana or a GitHub Pages static dashboard.

### Threshold harmonization
Per-commit changed-lines ≥90% and project-wide ≥80% are different denominators enforced at different points — DEEP DIVE Cycle 3 below reconciles this document's project-wide gates with the maturity model's per-commit floor and gives the copy-paste CI flags.

## Practical Recommendations
| Recommendation | Implementation | Tools | Threshold |
|---|---|---|---|
| Start with 5 metrics | coverage, mutation, flake, RED-witness, escape | ledger | week 1 |
| Baseline before gating | 20 ungated tasks measured | CI | targets at P50+1σ |
| Phase targets | 60/80/85 coverage; 50/70/80 mutation | quarterly | +5 absolute/quarter max |
| Watch the gap | alert when coverage − mutation >20 | dashboard | >20 → tighten |
| Pair every metric with an action | warning threshold → named response | policy | 100% of metrics actioned |
| Audit sample | human reviews 5% of PROMOTEs | random sample | 5% per quarter |

## Metrics and Targets
Phased targets from the zero-state baseline (measurement source: ledger + CI artifacts):

| Metric | Baseline (today) | Phase 2 | Phase 3 | Phase 4 |
|---|---|---|---|---|
| Line coverage | 0% | 60% | 80% | 85% |
| Mutation score | 0% | 50% | 70% | 80% |
| Flake rate (blocking) | unknown | <5% | <2% | <1% |
| REQ-coverage | 0% | 70% | 90% | 95% |
| RED-witness | 0% | 80% | 100% | 100% |
| Escape rate | unknown | <1/10 | <1/20 | <1/30 |

## References
1. [TMMi Foundation, 2018] TMMi Model (Level 4 = quantitative management). [verified: 2026-09-13]
2. [Micco, 2016] "Flaky Tests at Google" (1.5% / 16%). [verified: 2026-09-13]
3. [Bell et al., 2018] "DeFlaker," ICSE 2018 (95.5% recall, 1.5% false alarms). [verified: 2026-09-13]
4. [Molinelli et al., 2025] ASE 2025, pp. 278-290 (43% / 45% oracle mutation baselines). [verified: 2026-09-13]
5. [arXiv:2506.02954] MutGen (100% coverage / 4% mutation failure mode). [verified: 2026-09-13]
6. [CircleCI, 2026] Mutation testing floors 60-80%. [verified: 2026-09-13]
7. [CTRF, 2026] Common Test Report Format for GitHub Actions. [verified: 2026-09-13]
8. [Google Testing Blog, 2020] "Code Coverage Best Practices." [verified: 2026-09-13]
9. [KnowMBA, 2025] Test automation strategy (budgets, SLAs). [verified: 2026-09-13]

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
