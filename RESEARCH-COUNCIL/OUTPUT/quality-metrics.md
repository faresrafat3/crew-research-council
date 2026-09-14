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

---

## [DEEP DIVE (freebuff, pass 2, 2026-09-14)]: Reading the Ledger Right — Small-Sample Statistics and Control Charts for Per-Task Metrics

The pass-1 dashboard plots rolling 30-task means against fixed targets. At crew scale (20–30 tasks per window), that presentation invites reacting to noise: a three-point "trend" can be pure common-cause variation, and the 16 metrics become triggers for premature calibration moves. Statistical process control (SPC) is the discipline built exactly for this — separating routine variation from signals that the process actually changed [Anhøj & Olesen, 2018].

### Q1. Rate metrics get p-charts, not point thresholds

Half the ledger is proportions with varying denominators (escape rate, FP rate, flake rate, RED-miss, appeal success). Proportions with variable subgroup size belong on a **p-chart** with per-point limits p̄ ± 3√(p̄(1−p̄)/nᵢ); the np-chart requires constant subgroup size and does not apply [Oregon State Extension EM 9110]. When denominators swing wildly across windows, stabilized (Z) attribute charts normalize the variation [iSixSigma, short-run SPC].

Concrete consequence for the flake target: the pass-1 benchmark table lists "flake rate <1% blocking." At n=20 runs, a 0-for-20 streak and a 1/20 rate are statistically indistinguishable (5% vs 0%, with overlapping binomial uncertainty) — the <1% claim is unverifiable at crew sample sizes. Restate it c=0-style: **"0 flaky flips in the trailing 20 runs"** is the verifiable form (same construction as blocking-authority pass-2 §B1).

### Q2. Run rules, not single-point alarms

With n=20–30 per window, a single point beyond 3σ is rare to the point of uselessness — the real drifts (strictness/leniency decay, flake creep) move slowly. The practical detectors are the Western Electric/Nelson run rules on the chart: 8 consecutive points on one side of the centerline; 2 of 3 beyond 2σ same side; 6 consecutive rising or falling; and the 3σ point rule [SPC for Excel, control-chart rules]. Wire the dashboard to fire on run rules, annotate the offending points, and route every firing to the quarterly calibration agenda instead of auto-adjusting thresholds — the calibration loop stays human-governed (blocking-authority §2 governance).

### Q3. Trend claims need a stated method

Two pass-1 items are implicitly regression claims on small n: the roadmap's "−25% escapes/quarter" and the leading indicator "flake rate trend positive → CI trust erosion" (§4). Both should carry a stated decision rule — e.g., sign test or Spearman slope on the rolling window, with "no significant change" as an explicit possible outcome. Without it, non-significant wiggles get narrated as improvement or decline, and quarterly calibration inherits the noise. One more small-n trap: consecutive tasks share modules and agents, so points are **correlated** — treating them as independent produces too many false alarms [PCD&F, SPC sampling notes]; widen limits or aggregate before running rules where correlation is known.

### Q4. Minimum baseline before any signal

SPC convention: establish the baseline (≥20 points) before rules fire; a chart with no stable baseline signals a process still out of control — which is itself the finding. For the crew this matches the roadmap's Phase 2 baseline run (20 tasks, no gates): the ledger's first 20 rows per metric are the baseline window, and pass-1's P50+1σ target-setting is the natural seed for p̄.

### Q5. Dashboard spec (concrete)

1. Plot **per-task points**, never monthly aggregates (aggregation hides the run-rule signals).
2. p-chart limits for the six rate metrics; individuals-style chart (XmR) for latency/gate-duration variables.
3. Run-rule signals annotated on-chart with the rule that fired.
4. Baseline lock: no rule evaluates until 20 points exist per metric.
5. Every firing lands in the calibration agenda with the chart excerpt attached — signal, not verdict.

### Numbers for calibration (pass 2)

| Quantity | Value | Source |
|---|---|---|
| Chart type for varying-n rates | p-chart, limits 3√(p̄(1−p̄)/nᵢ) | [Oregon State EM 9110] |
| Wild-denominator variant | stabilized/Z charts | [iSixSigma] |
| Flake target, verifiable form | 0 flips / trailing 20 runs | derivation (c=0 form) |
| Signal detection | run rules (8-same-side, 2-of-3@2σ, 6-trend, 3σ) | [SPC for Excel] |
| Baseline before rules fire | ≥20 points | SPC convention |
| Correlation caution | shared-module tasks → widen limits | [PCD&F] |

### References (pass 2)
1. [Anhøj & Olesen, 2018] "Sense and sensibility: on the diagnostic value of control chart rules," based on SPC primer. https://pmc.ncbi.nlm.nih.gov/articles/PMC6171235/ [verified: 2026-09-14]
2. [Oregon State Extension, 2023] "SPC Part 8: Attributes Control Charts" (EM 9110) — p vs np chart sample-size rules. https://extension.oregonstate.edu/catalog/em-9110-statistical-process-control-part-8-attributes-control-charts [verified: 2026-09-14, snippet]
3. [SPC for Excel] "Control Chart Rules and Interpretation" — the 8 Western Electric/Nelson rules. https://www.spcforexcel.com/knowledge/control-chart-basics/control-chart-rules-interpretation/ [verified: 2026-09-14, snippet]
4. [iSixSigma, 2024] "Short-Run SPC Techniques" — stabilized (Z) attribute charts for varying sample sizes. https://www.isixsigma.com/control-charts/short-run-statistical-process-control-techniques/ [verified: 2026-09-14, snippet]
5. [PCD&F, 2023] "SPC Charts: Sampling Frequency, Subgroups and Plans" — correlated data produce false alarms. https://pcdandf.com/pcdesign/index.php/editorial/menu-features/17031-statistical-process-control-charts-sampling-frequency-subgroups-and-plans [verified: 2026-09-14, snippet]
6. Cross-refs: quality-metrics pass 1 (benchmarks, leading indicators); implementation-roadmap pass 1 (baseline phase); blocking-authority pass 2 (c=0 sampling); testing-maturity pass 2 (calibration governance).
