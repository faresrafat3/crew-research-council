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

## [DEEP DIVE Cycle 3]: Threshold Harmonization — Per-Commit vs Project-Wide, 80% vs 90%, Mutation Floors

**Conflict:** `testing-maturity-model.md` (freebuff) mandates per-commit changed-lines coverage ≥90% floor / 99% aspirational [Google Testing Blog 2020], while 9 sibling council outputs gate at project-wide line ≥80%, branch ≥70/75%, mutation ≥70/80%. Engineer reading both cannot satisfy both if interpreted as the same gate on the same denominator.

**Verdict:** Both are correct. They measure different denominators at different enforcement points. This note locks a 2-tier rule, extends (does not repeat) the `quality-metrics.md` catalog (129 lines: industry benchmark table line 80% / branch 70/75% / mutation 70/80%, phased targets 60→80→85%, leading-indicator gap >20%), and gives copy-paste CI flags.

### 1. Resolution rule (2-tier: changed-lines ≥90% MUST + project-wide ≥80% MUST)

**Tier A — Per-commit changed-lines gate (new-code debt stop): MUST ≥90%, aspirational 99%.**

- Source: Google Testing Blog, "Code Coverage Best Practices" (Arguelles / Ivanković / Bender, 2020-08-07): "While project wide goals above 90% are most likely not worth it, per-commit coverage goals of 99% are reasonable, and 90% is a good lower [bound]" — search-result snippet, verified via TinyFish search Cycle 3; full-page fetch JS-blocked but snippet consistent across 2 independent queries (per-commit vs project-wide) and corroborated by Qt/Testlio summaries of Google bands 60% acceptable / 75% commendable / 90% exemplary.
- Denominator: lines added or modified in the PR diff only (not whole repo).
- Enforcement: BLOCK per commit / per PR. No PROMOTE if changed-lines <90%.

**Tier B — Project-wide floor (legacy-theater stop): MUST line ≥80%, branch ≥70% (PIPELINE) / ≥75% (FULL stripe target), mutation ≥70% PIPELINE / ≥80% FULL.**

- Source: `quality-metrics.md` benchmark table (Google 80% line / 70% branch; Microsoft 75–85% / 65–75%; Stripe 80% / 75%; Meta 70–90% / 60–80%) + `testing-framework-spec.md` / `cicd-integration.md` CI flags. 80% project-wide is "reasonable; 100% is vanity producing low-value tests" [PrecisionAI, 2026, via quality-metrics base].
- Denominator: whole `src/` tree.
- Enforcement: BLOCK PR merge on project-wide regression (no drop >1% per PR) + nightly trend gate.

**Why both must coexist (not either/or):**

| Gate alone | Failure it misses | Example |
|---|---|---|
| Only project-wide 80% | New debt hides in average. A 200k-line repo at 82% can merge a 500-line PR at 30% and stay at ~81.9% — green gate, rotting head. | Legacy theater: metric stays green while every new file is untested. |
| Only changed-lines 90% | Legacy rot hides behind new-code purity. Every PR is 95% on its diff, but 60% of `src/` has zero tests and 4% mutation (execution without assertion [ArXiv, 2025, via quality-metrics]). | New-code purity over a hollow base: coverage/mutation gap >20% predicts escapes within 10 tasks (quality-metrics §4 leading-indicator model). |
| Both together | Changed-lines stops inflow; project-wide + ratchet drains the stock. | Google's exact pairing: cap project-wide ambition at ~80–90%, demand ~90–99% on the commit. |

**Copy-paste enforcement (both flags in the same PR job):**

```yaml
# .github/workflows/test-gate.yml — PR blocking job (<10 min)
- name: Project-wide floor (Tier B)
  run: |
    pytest -q \
      --cov=src --cov-branch \
      --cov-report=json:artifacts/cov.json \
      --cov-report=term-missing \
      --cov-fail-under=80
    # branch gate read from cov.json by coverage-annotate step;
    # BLOCK if branch <70% (PIPELINE) — FULL stripe demands ≥75% (see §4 table)

- name: Changed-lines floor (Tier A, Google 2020)
  run: |
    diff-cover artifacts/cov.xml \
      --compare-branch=origin/main \
      --fail-under=90
    # aspirational 99%: warn at <99%, BLOCK at <90%
    # empty-diff (docs-only PR): diff-cover exits 0 with "no lines" — pass by design
```

```ini
# pyproject.toml — single source of truth
[tool.coverage.run]
branch = true
source = ["src"]
[tool.diff_cover]
compare_branch = "main"
fail_under = 90
```

- `pytest-cov --cov-fail-under=80` enforces Tier B line floor; `--cov-branch` enables Tier B branch measurement (70/75%).
- `diff-cover --compare-branch=main --fail-under=90` enforces Tier A changed-lines floor on the same `cov.xml`.
- PR annotation: post `term-missing` uncovered changed lines + `cov.json` delta (no drop >1% per PR per `cicd-integration.md`).
- Dispute path: tester HOLD cites which tier failed (changed-lines % vs project-wide %) — never a bare "coverage low."

### 2. Mutation floor justification (70% PR targeted / 80% FULL nightly; 100% is waste)

**Rule: mutation ≥70% on PR-targeted (touched lines, <10 min) MUST; ≥80% on nightly FULL (whole `src/`) MUST. 100% is explicitly NOT a gate.**

Evidence (TinyFish Cycle 3 searches + fetches):

- **70–80% is the realistic strong band.** Drizz (2026-06-16, fetched): "70-80% for business logic. 80%+ for payment, security, and authentication code. 100% is neither necessary nor achievable." Benchmarks inside same source: 60–70% typical/moderate, 70–80% strong, 80%+ excellent/critical-only. CircleCI "What is mutation testing?" (fetched, 2026): demo Stryker config uses `break: 70` threshold; "A floor of 60–80% on high-risk modules is realistic. Chasing 100% is usually wasted effort, since the last few percent are typically equivalent [mutants]." QASkills/Stryker guide (search): ">80% excellent, 60–80% good." InsiderEngineering (2026-03-27, search): "At 75–85% (strong): most surviving mutants are now in cosmetic code."
- **100% is wasted on equivalents + trivia.** Task floor states 5–15% equivalent-mutant rate; fetched evidence bounds it: Jia & Harman (IEEE TSE, 2011, via Drizz 2026): ~23% of generated mutants are equivalent unfiltered ("practical ceiling ~77%"); modern tooling (Stryker/CircleCI: "detects and skips obviously equivalent mutations") pushes the *residual* equivalent + cosmetic-trivial tail to ~5–15% on covered-lines-scoped runs — hence 80% FULL is the rational ceiling and 100% chases unkillables. Stryker docs "Equivalent mutants" (search hit): 100% line coverage can coexist with surviving equivalents by construction. CircleCI pattern (fetched): "Don't chase 100%."
- **70% PR is achievable in <10 min only in targeted mode.** `cicd-integration.md` (verified via gh api): targeted `mutmut` on PR-touched lines only, threshold 70, exit 2; full `src/` run threshold 80 with 60-min timeout on nightly. `implementation-roadmap.md` Phase 3 + `routing-integration.md` size tiers: unit + targeted mutation = Small (block every commit, <10 min); full mutation = Large (nightly async only) per Google Small/Medium/Large discipline [Stewart, 2010; SQRBOK, 2025]. MutGen [ArXiv, 2025, via quality-metrics]: 100% line / 4% mutation gap proves execution≠assertion; ~4 iterations to converge — targeted loop converges inside PR budget, full-suite does not.

**Copy-paste enforcement:**

```ini
# pyproject.toml / setup.cfg — mutmut (Python)
[tool.mutmut]
paths_to_mutate = ["src/"]
mutate_only_covered_lines = true   # REQUIRED: untested lines are a coverage failure, not a mutation failure
runner = "pytest -q -x -n auto"
time_limit_minutes = 8             # PR-targeted hard box; nightly FULL overrides to 60
```

```yaml
- name: PR targeted mutation (Tier B-i, <10 min)
  run: |
    mutmut run --paths-to-mutate=src --mutate-only-covered-lines=true --time-limit=8
    mutation-check --threshold=70 --report=artifacts/mutation-report.json || exit 2
    # exit 2 = gate failure (Mutagen 2026 convention per cicd-integration.md); attaches before/after report to PR

- name: Nightly FULL mutation (Tier B-ii, async, 60 min)
  if: github.event_name == 'schedule'
  run: |
    mutmut run --paths-to-mutate=src --time-limit=60
    mutation-check --threshold=80 --report=artifacts/full-mutation-report.json
    # survivors triaged: killable → gap tickets; equivalent/cosmetic → allowlist with justification, never counted toward 100%
```

- Scoping rule (CircleCI pattern, fetched): gate line coverage at 80% on every PR; run mutation on curated subset (touched lines) per PR + full suite on schedule. No full-suite mutation in the blocking path — it breaks the <10 min budget and forces engineers to bypass the gate.
- Calibration from base: coverage/mutation gap >20% → tighten mutation gate (quality-metrics §4); survivors >10% → predict escape >1/10 within 10 tasks.

### 3. Migration path (red today → green without lowering the bar)

Context: COORD-01/02 baseline is 0% (no test files). `quality-metrics.md` §2 already mandates: baseline first (20 tasks), P50+1σ, +5%/quarter, never below baseline. This section operationalizes it for the 2-tier system.

**If project-wide <80% today (expected): gate the inflow immediately, ratchet the stock quarterly.**

1. **Day 0 — Turn on Tier A (changed-lines ≥90%) immediately, leave Tier B in warn mode.** Every new PR must be ≥90% on its diff from today. Project-wide number is recorded but does NOT block yet — it is displayed as trend + "distance to 80%."
2. **Ratchet Tier B +5 absolute points per quarter to 80%, never lower.** Example from 45%: Q1 gate 50% (warn below, block regressions), Q2 55%, … until 80%, then lock at 80% as MUST. `blocking-authority.md` clamp helper bounds this: `coverage_threshold = clamp(coverage_threshold, 70, 95)`, `mutation_threshold = clamp(mutation_threshold, 60, 90)` — ratchet moves are ±5 (appeal success >5% → loosen 5; escape ≥1/10 → tighten 5; FP >5% → loosen + lint).
3. **Mutation ratchets in parallel:** PR-targeted 55% → 70% over the same quarters (starting point per quality-metrics Phase 2: 50%); nightly FULL 50% → 80% (Phase 2→4: 50→70→80). Do not demand 70% PR-targeted on a codebase at 0% baseline in week 1 — set 55% first (base rule: "never set targets below baseline" means never set the *first* gate above reachable P50+1σ; thereafter never *lower* an achieved gate).
4. **Never lower a published gate to make a PR green.** If a PR cannot hit 90% changed-lines for a legitimate reason (generated code, pure rename, deletion-only diff), exempt the lines with `pragma: no cover` + reviewer sign-off and record the exemption in the ledger — the threshold number itself does not move.

**Ledger tracking query (extends quality-metrics §3 Layer 4 + CTRF artifact schema):**

```sql
-- Quarterly ratchet tracker: are we +5/quarter toward 80/70?
-- Tables: tasks(id, merged_at, formation), coverage(task_id, line_pct, branch_pct, changed_lines_pct),
--         mutation(task_id, scope TEXT('targeted'|'full'), score_pct, survivors, equivalents)
SELECT
  strftime('%Y-Q%q', merged_at) AS quarter,
  COUNT(*) AS prs,
  ROUND(AVG(changed_lines_pct), 1) AS avg_changed_lines_pct,
  ROUND(MIN(changed_lines_pct), 1) AS min_changed_lines_pct,
  ROUND(AVG(line_pct), 1) AS avg_project_line_pct,
  ROUND(AVG(CASE WHEN scope='targeted' THEN score_pct END), 1) AS avg_mut_targeted,
  ROUND(AVG(CASE WHEN scope='full' THEN score_pct END), 1) AS avg_mut_full,
  SUM(CASE WHEN changed_lines_pct < 90 THEN 1 ELSE 0 END) AS tierA_breaches,
  SUM(CASE WHEN line_pct < 80 THEN 1 ELSE 0 END) AS tierB_below_floor
FROM tasks
LEFT JOIN coverage USING (task_id)
LEFT JOIN mutation USING (task_id)
WHERE merged_at >= date('now', '-4 quarters')
GROUP BY quarter ORDER BY quarter;
-- Ratchet decision: if tierA_breaches = 0 AND avg_project_line_pct >= current_gate + 3 → raise gate +5 next quarter.
-- If appeal success >5% (ledger verdicts overturned/total) → hold or loosen 5 per blocking-authority clamp.
```

Dashboard: plot `avg_project_line_pct` + `avg_changed_lines_pct` + both mutation series as 30-task rolling window (quality-metrics §3 trend chart: line 80%, mutation 70%, flake <1%, escape <1/20, gate <10 min, RED 100%).

### 4. Consistency table (all 10 OUTPUT files — which threshold each enforces, after-fix value)

After-fix principle: no file owns a private threshold. Tier A (changed ≥90%) and Tier B (line ≥80% / branch ≥70 PIPELINE, ≥75 FULL-stripe / mutation ≥70 targeted PR, ≥80 FULL nightly) are quoted verbatim; files only add *scope notes*.

| # | File (RESEARCH-COUNCIL/OUTPUT/) | Pre-fix threshold language (verified via gh api grep) | After-fix value (normative) |
|---|---|---|---|
| 1 | `testing-maturity-model.md` (freebuff) | Per-commit changed ≥90% floor, ~99% aspirational [Google 2020]; core-module mutation table ≥70% / <60% red | **Tier A owner.** Keep 90%/99% wording, add: "changed-lines denominator; Tier B project-wide 80% lives in quality-metrics/cicd." Mutation row → "≥70% targeted PR, ≥80% nightly FULL" |
| 2 | `quality-metrics.md` (catalog base, 129 lines) | Line 80%, branch 70/75%, mutation 70/80%; phased 60→80→85% line / 50→70→80% mutation; gap >20% | **Tier B owner.** Add Tier A row: changed-lines ≥90% [Google 2020] + ratchet rule (§3). No number changes. |
| 3 | `testing-framework-spec.md` | `--cov-fail-under=80`, `--cov-branch` | Append Tier A: `diff-cover --compare-branch=main --fail-under=90` + mutmut `mutate_only_covered_lines=true`. Line 80 unchanged. |
| 4 | `tdd-protocol.md` | HOLD if coverage <80% / mutation <70% | Clarify: coverage <80% = Tier B project-wide; add HOLD if changed-lines <90% (Tier A). Mutation <70% = targeted-PR scope. |
| 5 | `cicd-integration.md` | `--cov-fail-under=80`; targeted mutation 70/exit-2; full 80/60-min; branch ≥80% row; no-drop >1% | Add `diff-cover --fail-under=90` step to PR job. Branch row → "≥70% gate, ≥75% FULL-stripe target" (reconciles 70/75 split: 70 blocks, 75 is the FULL aspiration). |
| 6 | `blocking-authority.md` | Clamp coverage 70–95, mutation 60–90; ±5 calibration; 100%/4% theater example | Add Tier A breach to 8 blocking conditions: "changed-lines <90% = HOLD (cite tier)." Clamps unchanged — they already admit 90. |
| 7 | `engineer-soul.md` | Mutation gate 70% PR / 80% nightly; 90%/30% vs 70%/75% comparison [Getautonoma] | Add: "coverage gate is two numbers: 90% changed-lines + 80% project-wide; either fails = DONE rejected." |
| 8 | `tester-soul.md` | Suite + coverage + mutation + lints; 8 blocking conditions | Same edit: blocking condition "coverage below floor" split into Tier A (90% changed) / Tier B (80% line, 70/75% branch). |
| 9 | `routing-integration.md` | PIPELINE 70% mutation BLOCK; FULL 80% mutation + 90% req-coverage BLOCKs; E2E ≤10 | Add per-commit 90% changed-lines to PIPELINE + FULL rows (RED-before-GREEN unchanged). REQ-coverage 90% is orthogonal (requirements, not lines) — keep. |
| 10 | `implementation-roadmap.md` | CI 80%/70–80%; Phase 3 exit mut 70/80%, req-cov 90%, flake <2%, drill 100% | Phase 2 exit: add "Tier A 90% changed-lines enforced from day 0"; Phase 3 exit: "Tier B 80% line ratchet complete OR +5/quarter on track." |

Notes: `README.md` (11th file in OUTPUT/) carries no threshold — excluded. Branch 70/75 split resolved as gate/aspiration (70 BLOCK everywhere, 75 FULL-stripe target per Stripe benchmark in quality-metrics table). Mutation 70/80 split resolved as scope (70 targeted-PR / 80 FULL-nightly per cicd-integration). REQ-coverage 90% (routing/roadmap) is not line coverage — no conflict.

**References Cycle 3:**
- [Google Testing Blog, 2020-08-07] Arguelles / Ivanković / Bender — "Code Coverage Best Practices": project-wide >90% mostly not worth it; per-commit ~99% reasonable, 90% good lower bound. Verified via TinyFish search snippets Cycle 3 (queries 1+2); direct fetch JS-blocked, snippet consistent across both queries. [verified: 2026-09-13, TinyFish search]
- [Qt / Testlio / LaunchDarkly summaries] Google bands 60% acceptable / 75% commendable / 90% exemplary; 80–90% healthy range. TinyFish search query 1, results 2/4/5. [verified: 2026-09-13, TinyFish search]
- [Drizz, 2026-06-16] "Mutation Testing Explained" (Mohanty) — fetched full text Cycle 3: 60–70% typical, 70–80% strong business logic, 80%+ critical-only; Jia & Harman (IEEE TSE, 2011) ~23% equivalent mutants unfiltered; 100% neither necessary nor achievable. [verified: 2026-09-13, TinyFish fetch]
- [CircleCI, 2026] "What is mutation testing?" — fetched full text Cycle 3: Stryker `break: 70` demo threshold; floor 60–80% high-risk modules realistic; don't chase 100% (equivalent tail); gate coverage 80% per-PR + mutation on curated subset on schedule. [verified: 2026-09-13, TinyFish fetch]
- [InsiderEngineering, 2026-03-27] "Why 100% Mutation Score Is Neither Necessary Nor Achievable" — 75–85% strong, survivors cosmetic past that. TinyFish search. [verified: 2026-09-13, TinyFish search]
- [QASkills / Stryker Mutator docs] >80% excellent, 60–80% good; equivalent-mutant definition (100% line coverage with surviving equivalents). TinyFish search. [verified: 2026-09-13, TinyFish search]
- [Council base, gh api] `quality-metrics.md` (129 lines, head-60 + tail fetched): benchmark table, phased targets, leading-indicator gap model, CTRF schema — extended, not repeated. [verified: 2026-09-13, gh api]
- [Council base, gh api] `testing-maturity-model.md` / `testing-framework-spec.md` / `tdd-protocol.md` / `cicd-integration.md` / `blocking-authority.md` / `engineer-soul.md` / `tester-soul.md` / `routing-integration.md` / `implementation-roadmap.md` threshold greps — pre-fix language quoted in §4 table. [verified: 2026-09-13, gh api]
- [Mutagen, 2026; CTRF, 2026; SQRBOK, 2025; Stewart, 2010] via cicd/routing base: exit-2 targeted gate, JUnit/JSON artifacts, Small/Medium/Large tiers, <10 min budget. Carried, not re-verified this cycle. [unverified — cutoff: 2026-09-13]

## [DEEP DIVE Cycle 4]: KB Learning Loop — Escape-to-Precedent in 7 Days, Quarterly Calibration Agenda

> Phase 4 (Continuous Improvement) in `implementation-roadmap.md` / `quality-metrics.md` is aspirational prose: "learn from escapes, calibrate quarterly." This file makes it executable: a typed KB schema, a 7-day SLA-bound workflow with a state machine and human escalation, a 90-minute calibration meeting with inputs/outputs/versioning, and anti-gaming guards that keep the loop honest. It assumes Cycle 3 normative tiers (Tier A changed-lines ≥90%, Tier B line ≥80% / branch ≥70 gate + ≥75 FULL-stripe target / mutation ≥70 targeted-PR + ≥80 FULL-nightly) — not repeated here, only referenced as breach classes.

---

### 1. KB entry schema (one file per escape, typed + greppable)

**Storage (concrete):**
- Path: `RESEARCH-COUNCIL/KB/escapes/ESC-<YYYY>-<NNN>.md` (e.g. `ESC-2026-041.md`).
- Index: `RESEARCH-COUNCIL/KB/README.md` — append one row per escape (table below). CI check fails if entry file exists but index row missing, or vice versa.
- Ledger link: `RESEARCH-COUNCIL/OUTPUT/quality-ledger.md` (or CTRF-adjacent ledger) gets one line per closed escape: `ESC-ID | date-closed | KB path | fix SHA | policy version`.
- Front-matter is the schema. Body is the narrative. Both are required — front-matter for machines, body for humans (Google SRE: metadata fields enable trend analysis; Atlassian: extensive issue fields before the meeting).

**Field table (all required unless marked Optional):**

| Field | Type / Allowed values | Validation | Why |
|---|---|---|---|
| `escape_id` | `ESC-YYYY-NNN`, monotonically increasing per year | `grep -r` uniqueness; CI rejects duplicate | Stable join key across KB, ledger, Jira/gh issue |
| `date_filed` | `YYYY-MM-DD` (Day 0) | ISO date, ≤ today | SLA clock starts here |
| `date_closed` | `YYYY-MM-DD` or `null` while open | ≥ `date_filed` when set | SLA 7d measured `closed - filed ≤ 7` |
| `req_ids` | list of `REQ-XXX` | ≥1 entry; must exist in routing REQ registry | Connects escape to requirement coverage (routing 90% REQ-coverage BLOCK is orthogonal to line coverage) |
| `root_cause_class` | enum: `missing-test` / `weak-assert` / `oracle-violation` / `flake-escape` / `razor-break` / `misroute` | exactly 1 primary + Optional `secondary` | The only closed vocabulary in the KB — enables quarterly trend counts |
| `severity` | `S1` (user-visible / data-loss / rollback) / `S2` (degraded, mitigated <1h) / `S3` (latent, found by audit/drill) | maps to Atlassian rule: S1+S2 always get KB entry; S3 sampled | Prevents KB flooding while guaranteeing S1/S2 precedent |
| `tier_breached` | `Tier-A-90-changed` / `Tier-B-80-line` / `Tier-B-70-branch` / `Tier-B-70/80-mutation` / `REQ-90` / `none-passed-but-escaped` | ≥1 | Tells calibration which gate failed (or that all gates passed = oracle/razor gap) |
| `detection_point` | enum: `production` / `post-merge-CI` / `nightly-FULL` / `manual-QA` / `audit-sample` / `drill` / `customer-report` | exactly 1 | Measures shift-left: quarterly goal is detection-point moving left |
| `fix_diff_ref` | commit SHA or PR URL + one-line scope | must resolve (`git cat-file -e` or `gh pr view`) | The code fix — separate from the policy fix |
| `regression_test_ref` | file:line of new/strengthened test + drill result | test must fail pre-fix, pass post-fix (RED-before-GREEN proof) | Prevents "fix without test" closures |
| `soul_patch_ref` | path + version delta, e.g. `tester-soul.md §8 cond-3 v1.4→v1.5` or `null` with justification | if `null`, `no_policy_change_reason` required | Every escape must answer: does a SOUL/policy file change? "No" needs a reason, not silence |
| `owner` | github handle / agent profile | single accountable human or agent-ID, not a team | Atlassian postmortem-owner rule: one driver to approval |
| `approver` | handle, ≠ owner | must approve merge | No self-approved precedents |
| `sla_due` | `date_filed + 7d` | auto-computed, immutable | Breach clock |
| `status` | `OPEN` / `TRIAGED` / `FIXED` / `POLICY-PROPOSED` / `KB-MERGED` / `CLOSED` / `BREACHED` | transitions only per §2 state machine | Greppable pipeline health |
| `ledger_ref` | line pointer after close | filled at Day 7 | Closes the loop to metrics |

**Root-cause class definitions (use verbatim in triage — no free text):**

- `missing-test`: no test covered the path. Fix = add test. SOUL patch usually a razor/check addition.
- `weak-assert`: test existed but asserted too little (e.g. `status_code == 200` without body check). Fix = strengthen assert + drill proof.
- `oracle-violation`: test + assert existed but oracle (expected value / contract / snapshot) was wrong or stale. Fix = correct oracle + pinning rule.
- `flake-escape`: real bug masked by flaky suite (retry hid red, or quarantine hid signal). Fix = de-flake + quarantine-rule patch.
- `razor-break`: a REQ razor / routing rule misfired (wrong tier, wrong agent, skipped FULL). Fix = routing-integration patch.
- `misroute`: human/agent routing error (assigned to wrong owner, wrong severity, skipped approver). Fix = ownership/escalation patch.

**File template (`KB/escapes/_TEMPLATE.md` — copy, never edit in place):**

```markdown
---
escape_id: ESC-YYYY-NNN
date_filed: YYYY-MM-DD
date_closed: null
req_ids: [REQ-XXX, REQ-YYY]
root_cause_class: missing-test # | weak-assert | oracle-violation | flake-escape | razor-break | misroute
secondary_class: null
severity: S2
tier_breached: Tier-A-90-changed
detection_point: production
fix_diff_ref: null # fill Day 3: <SHA or PR URL>
regression_test_ref: null # fill Day 3: <path:line + RED/GREEN SHAs>
soul_patch_ref: null # fill Day 5: <file § + vX.Y->vX.Z> or null + reason
owner: @handle
approver: @handle
sla_due: YYYY-MM-DD  # = filed + 7d
status: OPEN
ledger_ref: null
---

# ESC-YYYY-NNN — <one-line summary>

## 1. Incident summary (Atlassian field set, condensed)
- Impact: <who saw what, how long, how many>
- Leadup: <change that introduced latent bug>
- Fault: <what didn't work as expected>
- Detection: <how found + how time-to-detect could halve>
- Response/Recovery: <who responded, mitigation, restore time>

## 2. Timeline (UTC, chronological)
- HH:MM — event

## 3. Five Whys (≥3 levels, end at systemic cause, not a name)
1. Why …? Because …
2. Why …? Because …
3. Why …? Because … → root_cause_class

## 4. Root cause (1 paragraph, proximate vs root distinguished)

## 5. Fix + regression proof
- Diff: <ref>
- Test: <ref> — RED pre-fix SHA: ___, GREEN post-fix SHA: ___
- Drill: <new test run through mutation/drill harness, kills ≥1 mutant or asserts strengthened value>

## 6. SOUL / policy patch (or explicit no-change reason)
- Patch ref + rationale, or `no_policy_change_reason: …`

## 7. Corrective actions (Atlassian wording: actionable + specific + bounded)
- [ ] Priority Action (root-cause fix): <verb …> — owner — due
- [ ] Improvement Action (detect/mitigate next time): <verb …> — owner — due

## 8. Lessons + prevention-backlog link
- Went well / could improve / got lucky (3 bullets)
- Backlog item: <link> (filed Day 5 even if scheduled later)

## 9. Backlog check + recurrence
- Backlog would-have-prevented? <yes/no + why not done>
- Same root cause before? <ESC-IDs or "first occurrence">
```

**Index row (`KB/README.md`):**

```markdown
| ESC-ID | Filed | Class | Tier | Detection | Owner | Status | KB path |
|---|---|---|---|---|---|---|---|
| ESC-2026-041 | 2026-05-11 | weak-assert | Tier-B-80-line | nightly-FULL | @fares | CLOSED | KB/escapes/ESC-2026-041.md |
```

**Full example entry (file `KB/escapes/ESC-2026-041.md` — realistic, complete):**

```markdown
---
escape_id: ESC-2026-041
date_filed: 2026-05-11
date_closed: 2026-05-17
req_ids: [REQ-114, REQ-118]
root_cause_class: weak-assert
secondary_class: null
severity: S2
tier_breached: Tier-B-80-line
detection_point: nightly-FULL
fix_diff_ref: PR faresrafat3/crew-research-council#212 (SHA 9f3ac41)
regression_test_ref: tests/test_routing.py:187 test_full_stripe_requires_branch75 (RED 9f3ac40 / GREEN 9f3ac41)
soul_patch_ref: tester-soul.md §8 cond-4 v1.4->v1.5 (assert-strength rule)
owner: @fares
approver: @council-lead
sla_due: 2026-05-18
status: CLOSED
ledger_ref: quality-ledger.md:L314
---

# ESC-2026-041 — FULL-stripe branch gate passed with stubbed coverage uploader

## 1. Incident summary
- Impact: 14% of nightly FULL runs 05-09→05-11 reported branch 78% as 81% (uploader stub averaged file-level instead of line-level); 2 PRs merged below the ≥75 FULL-stripe target. No prod outage; quality-signal corruption.
- Leadup: coverage-uploader refactor 05-08 introduced `mean(files)` fast path behind `STUB_UPLOADER=1` left set in nightly env.
- Fault: branch-coverage aggregator returned inflated value; gate compared inflated value.
- Detection: nightly-FULL trend alert (branch +3pp overnight with zero code change) + audit-sample drill re-ran uploader with fixture.
- Response/Recovery: on-call reverted env flag 05-11 09:20 UTC; re-ran 3 nightlies; 2 merged PRs re-checked (1 still ≥75 true value, 1 reverted + re-tested).

## 2. Timeline (UTC)
- 05-08 16:00 — uploader refactor merged (PR #209), STUB flag added for local dev.
- 05-09 02:00 — nightly FULL #881 reports branch 81% (true 78%); flag leaked via env snapshot.
- 05-10 02:00 — nightly #882 same inflation; no alert (threshold was absolute, not delta).
- 05-11 07:55 — audit drill replays uploader fixture, expects 78.0, gets 81.2 → escape filed 08:10.
- 05-11 09:20 — flag cleared, rerun ordered.
- 05-13 15:00 — fix PR #212 merged (true line-level mean + env-flag guard).
- 05-15 11:00 — SOUL patch proposed (assert-strength rule).
- 05-17 10:00 — KB entry merged, ledger L314 linked.

## 3. Five Whys
1. Why did the gate pass? Because uploader reported 81% > 75%. 
2. Why did it report 81%? Because STUB path averaged per-file percentages (unweighted) instead of line-level aggregation. 
3. Why didn't the test catch it? Because the only uploader test asserted `result > 75` (boolean gate), never the numeric value against a fixture — classic weak-assert. 
4. Why was the flag set in nightly? Because nightly env snapshot inherited a dev export; no guard asserted flag absence in CI. → systemic: weak asserts at two levels (value + env).

## 4. Root cause
Proximate: stub averaging bug. Root: weak-assert — gate-shape test (`>75`) instead of value-shape test (`== 78.0 ±0.1` on fixture) plus missing env-guard assert. Tier-B-80-line family; Tier A unaffected (changed-lines still diff-cover, different path).

## 5. Fix + regression proof
- Diff: PR #212 — `uploader.py: mean(lines)/sum(lines)` replaces `mean(file_pct)`; adds `assert STUB_UPLOADER != "1" in CI` guard in `conftest.py:22`.
- Test: `tests/test_routing.py:187` now asserts `branch == pytest.approx(78.0, abs=0.1)` on `fixtures/uploader_mixed.json`; RED pre-fix (81.2), GREEN post-fix (78.0). Second test `test_stub_flag_blocked_in_ci` fails with flag set, passes without.
- Drill: new value-assert kills 3/3 uploader mutants (mean→median, weighted→unweighted, rounding); old boolean-assert killed 0/3. Drill log: `drills/ESC-2026-041.log`.

## 6. SOUL / policy patch
- `tester-soul.md §8 cond-4 v1.4->v1.5`: "Gate-shape asserts (`> threshold`) are insufficient for aggregators; require fixture-pinned value asserts (±tolerance) for any coverage/mutation math." Also `testing-framework-spec.md` conftest guard pattern added as recommended snippet.

## 7. Corrective actions
- [x] Priority Action: fix uploader aggregation + CI env guard — @fares — done 05-13.
- [x] Improvement Action: add nightly delta-alert (branch Δ >2pp with <50-line diff pages on-call) — @council-lead — done 05-16.
- [ ] Improvement Action (backlog PREV-089): audit all `> threshold` asserts in metrics path, convert to fixture-pinned — @fares — due 06-15.

## 8. Lessons + prevention-backlog link
- Went well: audit drill caught in 2 days what absolute gate missed; trend-alert idea came from postmortem meeting.
- Could improve: nightly env should never inherit dev exports; need env-allowlist.
- Got lucky: only 2 PRs merged in window; true values showed 1 was still green.
- Backlog: PREV-089 filed.

## 9. Backlog check + recurrence
- Backlog would-have-prevented? Partially — PREV-071 ("pin uploader fixture") existed since 04-02, deprioritized for roadmap Phase 2. Honest reason: uploader seen as infra, not gate-critical. Reclassified as gate-critical.
- Same root cause before? No prior weak-assert escape on uploader; similar pattern ESC-2026-033 (mutation math, S3) — shared prevention item merged into PREV-089.
```

---

### 2. Escape-to-precedent workflow (7-day SLA, Day 0 → Day 7)

**Principle (Google SRE + Atlassian, adapted):** blameless, owner-driven, approved, action-tracked — but time-boxed to 7 days so precedent compounds instead of rotting. Day counts are calendar days from `date_filed`. Every transition is a file + issue state change, not a meeting vibe.

| Day | Milestone | Owner | Inputs | Outputs (artifacts) | Gate to proceed |
|---|---|---|---|---|---|
| **Day 0** | File escape | Finder (anyone/agent) | Failing signal, prod symptom, audit hit | `KB/escapes/ESC-*.md` created at `status: OPEN` + gh issue `ESC-*` opened + `date_filed`/`sla_due` set | File exists + index row added (CI `kb-index-check` passes) |
| **Day 1** | Triage + assign | Council-lead / on-call | Entry draft, REQ registry, severity rubric | `root_cause_class` (preliminary), `severity`, `owner` + `approver` assigned, `status: TRIAGED` | Owner ≠ approver; severity set; SLA clock acknowledged in issue comment |
| **Day 3** | Fix + regression test + drill | Owner | Codebase, failing test, drill harness | `fix_diff_ref` + `regression_test_ref` (RED/GREEN SHAs) + drill log; `status: FIXED` | New/strengthened test fails pre-fix and passes post-fix; drill kills ≥1 mutant OR documents strengthened value (weak-assert proof); reviewer confirms |
| **Day 5** | SOUL/policy patch proposal | Owner (author) + approver (reviewer) | Fix, Five Whys, SOUL files | `soul_patch_ref` OR `no_policy_change_reason`; prevention-backlog item filed; `status: POLICY-PROPOSED` | Approver confirms patch scope is narrow + bounded (Atlassian actionable/specific/bounded wording); backlog item linked |
| **Day 7** | KB entry merged + ledger linked | Approver | Completed entry, fix SHA, policy version | `date_closed`, `ledger_ref`, `status: CLOSED`; index row updated; KB PR merged | All required fields non-null; approver sign-off comment; ledger line appended; `closed - filed ≤ 7` |

**Day-by-day commands (copy-paste; `gh` + `git`):**

```bash
# Day 0 — file (finder)
cp RESEARCH-COUNCIL/KB/escapes/_TEMPLATE.md RESEARCH-COUNCIL/KB/escapes/ESC-2026-042.md
# edit front-matter: escape_id, date_filed=$(date +%F), req_ids, owner=TBD, status=OPEN, sla_due=+7d
gh issue create --title "[ESC-2026-042] <one-line>" --body "KB: KB/escapes/ESC-2026-042.md | severity:TBD | class:TBD" --label escape,OPEN
# append README index row with status OPEN

# Day 1 — triage (lead)
gh issue edit <N> --add-label TRIAGED --remove-label OPEN
# set root_cause_class/severity/owner/approver in front-matter; comment: "SLA due YYYY-MM-DD, owner @x, approver @y"

# Day 3 — fix (owner)
# prove RED then GREEN; attach SHAs + drill log path in §5; set status FIXED
gh pr create --title "[ESC-2026-042] fix + regression" --body "Closes #<N> (code part). RED <sha> GREEN <sha>. Drill: drills/ESC-2026-042.log"

# Day 5 — policy (owner proposes, approver reviews)
# file prevention item, set soul_patch_ref or no_policy_change_reason, status POLICY-PROPOSED

# Day 7 — close (approver merges)
echo "ESC-2026-042 | $(date +%F) | KB/escapes/ESC-2026-042.md | <fixSHA> | TEST-POLICY vX.Y" >> RESEARCH-COUNCIL/OUTPUT/quality-ledger.md
# set date_closed, ledger_ref (e.g. quality-ledger.md:L315), status CLOSED; merge KB PR; close issue
```

**State machine (allowed transitions only; anything else fails CI `kb-lint`):**

```
        Day0 file          Day1 triage         Day3 fix            Day5 policy          Day7 merge
OPEN ─────────────► TRIAGED ───────────► FIXED ───────────► POLICY-PROPOSED ──────────► KB-MERGED ──► CLOSED
 │                    │                    │                       │                        │
 │ Day1+24h           │ Day3+48h           │ Day5+48h              │ Day7+24h               │ approve
 │ no-owner           │ no-fix             │ no-policy             │ checks-fail            │ fails
 ▼                    ▼                    ▼                       ▼                        ▼
BREACHED ─────────────────────────────────────────────────────────────────────────────── (any state past sla_due without gate met)
 │ human-escalation (below) → re-plan with new due + reason, or accept BREACHED→CLOSED with waiver (approver + human sign only)
 └─► (after recovery) re-enters at the missed state, status BREACHED cleared only by human comment
```

- `KB-MERGED` is the transient "PR approved, ledger pending" state; automation moves it to `CLOSED` when ledger line lands. Humans never set `CLOSED` directly without ledger ref.
- Reopen: `CLOSED → OPEN` allowed only with `reopened_because` comment + new `sla_due`; preserves history (append, don't rewrite).
- `null` is legal for `fix_diff_ref` / `soul_patch_ref` only in `OPEN`/`TRIAGED`. From `FIXED` onward they must be set or explicitly waived with reason.

**SLA breach escalation to human (no silent slips):**

| Breach | Detector (automated) | Escalation | Action |
|---|---|---|---|
| Day 1 +24h still `OPEN` (no owner) | nightly `kb-sla-check` (cron) comments on issue + tags lead | → council-lead paged; must assign within 24h or record `capacity-blocked` reason | If 2nd consecutive triage breach, quarterly calibration auto-adds "ownership capacity" agenda item |
| Day 3 +48h still `TRIAGED` (no fix) | same check | → owner + approver notified; owner posts blocker or partial diff within 24h | Approver may reassign; if blocked on external dep, file `waiver-request` (human approves new Day 3+3) |
| Day 5 +48h still `FIXED` (no policy proposal) | same check | → approver nudges; owner proposes patch or `no_policy_change_reason` within 24h | "No patch" without reason is rejected — forces the precedent question |
| Day 7 +24h not `CLOSED` | `sla_due` passed | → status auto-flips to `BREACHED`, human owner (Fares / council-lead) assigned, issue labeled `BREACHED` + `P1` | Human decides within 48h: (a) grant dated extension with reason (status returns to missed state, `sla_due` unchanged for metrics + `extension_granted` note), or (b) accept breach (stays `BREACHED→CLOSED` with waiver, counted in quarterly breach-rate metric). Bots/agents cannot waive their own breach — human sign required. |
| Reviewer overload (approver holds >5 open escapes) | workload cap check (§4) | → auto-suggest second approver; lead redistributes | Prevents "approved by exhaustion" |

Breach-rate itself is a quarterly calibration input (target: <10% BREACHED/quarter; >20% triggers process retro, not just more time).

---

### 3. Quarterly calibration agenda (90 minutes, same script every quarter)

**Cadence:** first week of Jan/Apr/Jul/Oct. Owner: council-lead. Required attendees: tester + engineer SOUL owners, routing owner, metrics owner. Optional: any escape owner from the quarter. No calibration without the input packet (below) posted 48h before — meeting cancelled/rescheduled if packet missing (forces data discipline over opinion).

**Timebox (90 min total, timer enforced):**

| Block | Min | Question | Inputs from packet | Output (decision or item) |
|---|---|---|---|---|
| 1. FP/FN review | 20 | Where did gates lie or miss? | FP list (blocked but shouldn't), FN list (escaped = this quarter's ESC-IDs), drill kill deltas | Per-gate keep/loose/tighten straw vote; FN classes feed prevention backlog |
| 2. Threshold vote | 20 | Do Tier A/B numbers move? | Current `TEST-POLICY.md` version + clamp math + breach/escape counts | Binding vote: adjust any threshold by ±5pp max per quarter, within clamps (coverage 70–95, mutation 60–90 per blocking-authority); or hold. Version bump (§ below). |
| 3. Flake / escape trends | 20 | Are we getting more stable or just luckier? | Flake-rate trend, quarantine list, detection-point histogram, root-cause-class histogram, MTTD/MTTR | Flake-budget decision (quarantine cap), detection-shift goal for next quarter, top-1 systemic fix funded |
| 4. Prevention backlog groom | 20 | What actually gets built? | PREV backlog (from §2 Day-5 items + prior quarters), cost/impact tags | Ranked top-3 funded + owners + dues; close stale items with reason; carry rest |
| 5. Policy version bump + close | 10 | What did we decide, in writing? | Decision log draft | `TEST-POLICY.md` version bumped, decision log merged, next quarter date set |

**Input packet checklist (posted as `CALIB-YYYY-QN-packet.md`, 48h before; meeting invalid without all 8):**

- [ ] 1. Threshold snapshot: current Tier A/B + REQ-90 values + `TEST-POLICY.md` version (quote, don't paraphrase).
- [ ] 2. Gate outcomes: # PRs evaluated, # HOLD/BLOCK per tier, FP appeals + overturn rate.
- [ ] 3. Escape list: all ESC-IDs closed + BREACHED this quarter with class/tier/detection-point table (from `KB/README.md`).
- [ ] 4. FP/FN exhibits: ≥3 FP appeal cases (diff + verdict + human ruling) + all FN escapes mapped to missed gate.
- [ ] 5. Flake report: flake-rate %, quarantined tests, retry-masked reds, top-5 flakiest files.
- [ ] 6. Drill/mutation deltas: targeted-PR mutation mean + FULL-nightly mean, drill-pass rate on new tests, equivalent-mutant notes.
- [ ] 7. Audit sample: 10% verdict re-review results (per §4) — agreement rate + disagreements.
- [ ] 8. Prevention backlog status: prior PREV items done / overdue / stale + new Day-5 items awaiting rank.

**Threshold-vote rules (binding, anti-drift):**

- Scope: Tier A changed-lines, Tier B line/branch/mutation, REQ-coverage, flake budget, drill-pass bar. One motion per threshold, seconded, majority of required attendees.
- Step limit: ±5pp per threshold per quarter (e.g. Tier B line 80→75 or 85 max). Prevents oscillation and big-bang loosening.
- Clamps (from blocking-authority, non-negotiable without MAJOR + human sign): coverage ∈ [70, 95], mutation ∈ [60, 90]. Any motion outside clamps is out of order.
- Ratchet guidance (from quality-metrics phased model): prefer upward ratchet when escape-rate <5% and FP-overturn <10%; prefer hold when mixed; loosen only with ≥2 quarters of FP-overturn >20% AND escape-rate flat — never loosen because a single team complains.
- Quorum: 3/4 required roles present; absent role delegates in writing or vote deferred.

**Decision log template (append to `TEST-POLICY.md` changelog + standalone `CALIB-YYYY-QN-decisions.md`):**

```markdown
# CALIB-2026-Q3 decisions (2026-07-08, chair @council-lead, quorum 4/4, packet CALIB-2026-Q3-packet.md)
| # | Motion | Evidence (packet §) | Vote (for/against/abstain) | Result | Policy delta |
|---|---|---|---|---|---|
| 1 | Hold Tier A 90% changed | ESC-041/042 weak-assert, FP-overturn 6% | 4/0/0 | PASS | none |
| 2 | Tier B branch FULL-target 75→80 | 0 escapes via branch, FP-overturn 4% | 3/1/0 | PASS | TEST-POLICY v2.3->v2.4 (MINOR) |
| 3 | Fund PREV-089 uploader-assert audit | 2 related escapes | 4/0/0 | PASS | backlog PREV-089 owner @fares due 08-15 |
| 4 | … | | | | |
Breach-rate Q2: 1/9 = 11% (ESC-2026-038, waiver signed @fares, reason: external dep).
Next calibration: 2026-10-07. Packet due 2026-10-05.
```

**Versioning `TEST-POLICY.md vX.Y` (semver-lite, enforced by CI tag check):**

- `vX.Y` header line 1 of `TEST-POLICY.md`: `# TEST-POLICY v2.4 (2026-07-08, CALIB-2026-Q3)`.
- MAJOR (`X+1`, e.g. v2→v3): any clamp change, Tier A floor change, or severity-definition change. Requires human (Fares) sign + 2-quarter evidence.
- MINOR (`Y+1`, e.g. v2.3→v2.4): threshold ±5pp move, new razor/check, detection-point redefinition, flake-budget change. Requires calibration vote (this meeting).
- PATCH (`v2.4.1`-style or date suffix allowed): wording, examples, template fixes. Owner + approver, no vote.
- Every bump appends a changelog row (version, date, CALIB-ID, motions, author). `git tag test-policy-vX.Y` on merge. KB entries reference the version they closed under (`soul_patch_ref` + ledger line include it) so precedent is traceable to the rule set that produced it.

---

### 4. Anti-gaming guards (the loop only works if cheating is more expensive than complying)

**The four standing guards (always on, not quarterly):**

1. **Mutation floor prevents coverage theater.** Tier B mutation ≥70 targeted / ≥80 FULL-nightly is a hard BLOCK independent of line coverage. Adding uncovered-line-free "comment tests" or `assert True` raises line % but kills 0 mutants → mutation gate still red. CI runs `mutmut --mutate-only-covered-lines` (targeted) so uncovered-line gaming can't even inflate the denominator.
2. **Drill-pass prevents weak asserts.** Every new/changed test from a fix (Day 3) must pass the drill: facilitator mutates the fixed code (operator swap, off-by-one, stub-average, flag-flip) and the test must flip RED. Boolean gate-asserts (`> 75`) fail drill by construction (ESC-2026-041 proof: 0/3 kills). No drill log = `FIXED` gate rejected.
3. **Audit sampling 10% verdicts/quarter.** Metrics owner re-reviews a random 10% of PASS/HOLD verdicts + all BREACHED waivers each quarter (packet item 7). Disagreement rate >15% triggers reviewer retro + counts against the reviewer's calibration standing, not the author's. Sample seed published in packet for reproducibility (`shuf --random-source=<(openssl enc ...)` or documented `random.seed(CALIB-ID)`).
4. **Reviewer workload cap 5 escalations/week.** No approver holds >5 open escape reviews or >5 FP appeals in any rolling 7 days. Breach auto-suggests a second approver and blocks self-merge. Prevents rubber-stamping under load and "reviewer shopping" (reassigning until someone waves it through — reassignments logged, >2 reassigns/escape flags in packet).

**3 gaming scenarios + detection (concrete, with the query that catches each):**

**Gaming 1 — Coverage theater (trivial asserts to hit Tier A 90% changed).**
- *Play:* author adds `def test_smoke(): assert import_module(...)` or `assert result is not None` over 200 new lines → diff-cover 92% green, mutation untouched.
- *Why it tempts:* Tier A is per-commit and visible; fastest way to unblock a PR.
- *Detection (layered):* (a) mutation gate stays red (0 kills on theater tests) → PR still BLOCKED; (b) quarterly `assert-density` scan flags files with >50 added lines and <1 value-assert per 20 lines (`grep -c "assert.*==\|approx\|raises\|match"` vs added lines); (c) drill on sampled new tests fails → author asked to strengthen in the PR, not after. *Precedent:* file as `weak-assert` escape if it ever merges (detection_point `audit-sample`), proving the guard fired late but fired.

**Gaming 2 — Flake laundering (retry/quarantine to hide real red).**
- *Play:* team marks a failing regression test `@pytest.mark.flaky(reruns=5)` or moves it to quarantine so the suite goes green; escape later blamed on "infra."
- *Why it tempts:* fixes the build without fixing the code; invisible in pass-rate dashboards.
- *Detection:* (a) flake-rate + quarantine-list are packet items — any test quarantined >14 days without a PREV item auto-pages owner; (b) retry-masked-red metric (`passed-after-retry / total-passed`) tracked per nightly — spike >5% triggers calibration block-3 deep dive; (c) root-cause class `flake-escape` exists precisely to name this, and Day-5 policy patch must tighten the quarantine rule (e.g. max 7-day quarantine + mandatory PREV). Repeat offenders lose quarantine-write permission (human decision, logged).

**Gaming 3 — Diff-splitting / razor-shopping (dodge Tier A or FULL).**
- *Play A (split):* author slices a 400-line change into 5 stacked 80-line PRs each hitting 90% changed trivially while the feature as a whole is under-tested. *Play B (shop):* author re-labels a feature PR as `docs`/`chore` to route to PIPELINE instead of FULL, dodging the ≥75 FULL-stripe + ≥80 mutation gates.
- *Why it tempts:* Tier A denominator is per-PR; routing is label-driven.
- *Detection:* (a) stacked-PR detector: >3 PRs by same author touching same module within 72h with shared REQ-IDs auto-flag for combined diff-cover (`diff-cover --compare-branch=main~N`) — combined <90% reopens HOLD; (b) label-vs-diff check: `docs/chore` PRs with >50 code-line diffs auto-rerouted to FULL + logged as `razor-break` candidate; (c) audit sample includes 10% of PIPELINE-routed PRs re-evaluated against FULL criteria — systematic under-routing shows up as a calibration motion to tighten razor rules, with the misrouter named by role (blameless wording, systemic fix).

---

**References Cycle 4:**
- [Google SRE Book, Ch. Postmortem Culture — Lunney/Lueder] Postmortem = impact + actions + root cause(s) + follow-ups; blameless tenet; review criteria (data collected? impact complete? root deep enough? action plan + priority? stakeholders shared?); repository + metadata fields for trend analysis; reward writing. Fetched full text. [verified: 2026-09-13, TinyFish fetch]
- [Atlassian Incident Management Handbook — Postmortems] S1/S2 mandatory postmortems; owner drives to approval, approvers prioritize backlog; Priority Action (root-cause) vs Improvement Action + SLO 4/8 wks; Five Whys; proximate-vs-root + category table (Bug/Change/Scale/Architecture/Dependency/Unknown); action wording actionable/specific/bounded with before→after examples. Fetched full text. [verified: 2026-09-13, TinyFish fetch]
- [TinyFish search "postmortem knowledge base schema lessons learned 2024"] Results corroborate Google/Atlassian as canonical templates; PMI/RMCLS lessons-learned framing (store in org process assets), PostHog/Rootly agenda+roles templates. [verified: 2026-09-13, TinyFish search]
- [TinyFish search "defect escape root cause corrective action template 2024"] 8D D5 confirm-capable-corrective-action rule; Lockheed RCA guidebook (systematic contributors-before-action); Joint Commission RCA framework template; 8Dflow worksheet structure. Informs Day-5 confirm-no-side-effects + Day-3 RED/GREEN proof. [verified: 2026-09-13, TinyFish search]
- [TinyFish search "software quality quarterly review calibration metrics 2024"] Returned HR performance-calibration noise (Lattice/Deel/PeopleGoal), no software-quality-threshold calibration standard found — confirms this file's quarterly script (FP/FN + ±5pp vote + flake/escape trends + PREV groom + version bump) is original synthesis, not a copy; vote/clamp mechanics instead grounded in council base below. [verified: 2026-09-13, TinyFish search]
- [Council base, gh api — quality-metrics.md tail-30] Tier A/B normative table (10 OUTPUT files, after-fix values: Tier A changed ≥90%; Tier B line 80% / branch 70-gate+75-target / mutation 70-targeted+80-nightly; clamps coverage 70–95 / mutation 60–90; ±5 calibration) — breach classes + vote limits in §§1–3 cite this, not re-argued. [verified: 2026-09-13, gh api]
- [Council base, prior cycles] blocking-authority ±5 calibration + theater example; cicd-integration targeted-70/exit-2 + FULL-80/60-min + no-drop >1%; routing-integration PIPELINE-70 / FULL-80 + REQ-90 BLOCKs; engineer/tester-soul blocking conditions — escalation caps + drill/mutation guards in §§2/4 extend these. [carried — cutoff: 2026-09-13]
