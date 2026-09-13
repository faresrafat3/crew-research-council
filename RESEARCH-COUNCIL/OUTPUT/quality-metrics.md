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
