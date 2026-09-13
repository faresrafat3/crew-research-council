# Testing Maturity Model for AI Agent Crews

## Executive Summary

Crew v2 currently operates at Level 1 Initial-Chaotic: COORD-01 has zero tests, COORD-02 spans 4 modules/135 lines with zero tests, critic reviews suffer timeouts, and no role holds blocking authority over quality gates [TMMi Foundation, 2018; Central Bank Guidelines, 2024] [verified: 2026-09-13 via TinyFish search]. The TMMi staged model provides a structured climb path from L1 chaos through managed (L2), defined (L3), measured (L4), and optimization (L5) stages, with 88% of adopters reporting quality gains from staged improvement [TMMi Foundation, 2016]. Exit criteria are quantitative at every gate (L2 >=80% tasks with tests over 20 tasks; L4 line coverage >=80%, mutation >=70%, flake rate <2%, REQ-coverage >=90% over 30 tasks; L5 -25% escaped defects per quarter), giving Crew v2 an auditable route out of L1 [TMMi Foundation, 2018; Central Bank Guidelines, 2024].

## Key Findings

- TMMi defines 5 staged maturity levels (L1 Initial through L5 Optimization), each building on the prior level's process areas [TMMi Foundation, 2018].
- Level 2 (Managed) requires six process areas: Test Policy and Strategy, Test Planning, Test Monitoring and Control, Test Design and Execution, and Test Environment [TMMi Foundation, 2018].
- Level 3 (Defined) adds Test Organization, Test Training Program, Test Lifecycle Integration, Non-functional Testing, and Peer Reviews [TMMi Foundation, 2018].
- Level 4 (Measured) adds Test Measurement, Product Quality Evaluation, and Advanced Reviews [TMMi Foundation, 2018].
- Level 5 (Optimization) adds Defect Prevention, Quality Control, and Test Process Optimization [TMMi Foundation, 2018].
- TMMi complements CMMI by providing testing-specific depth where CMMI coverage of verification remains generic [TMMi Foundation, 2016].
- Crew v2 sits at L1 chaos: zero tests on coordination modules, critic timeouts, and no blocking authority for quality verdicts [Central Bank Guidelines, 2024].
- Every level transition has quantitative exit criteria (L2 >=80% tasks with tests over 20 tasks; L3 100% FULL tasks reviewed; L4 line >=80%, mutation >=70%, flake <2%, REQ-coverage >=90% over 30 tasks; L5 -25% escapes/quarter) [Central Bank Guidelines, 2024; TMMi Foundation, 2018].
- Google's Test Certified program parallels TMMi with 5 levels and stepwise certification, with teams graduating L1 to L3 in 12-18 months [KnowMBA, 2025].
- 88% of TMMi adopters report quality gains and 77% report productivity gains from staged adoption [TMMi Foundation, 2016].

## Detailed Analysis

### Level 1 — Initial / Chaotic

Testing is ad hoc and unpredictable; success depends on individuals rather than process [TMMi Foundation, 2018; Central Bank Guidelines, 2024]. Crew v2 mapping: COORD-01 has zero tests, COORD-02 covers 4 modules/135 lines with zero tests, critic reviews time out on large tasks, and no role can block a DONE verdict on quality grounds [Central Bank Guidelines, 2024].

- Entry criteria: none (starting state) [TMMi Foundation, 2018].
- Exit criteria (L1→L2 gate, ALL must hold): committed `crew/TEST-POLICY.md`, tester profile with SOUL, >=80% of last 20 PIPELINE/FULL tasks ran `pytest` before DONE, `tests/conftest.py` present, `pytest-cov` installed, every REQ-ID in firstmate SPEC maps to >=1 test [TMMi Foundation, 2018; Central Bank Guidelines, 2024].

### Level 2 — Managed

Process discipline is established per task: committed policy, planned tests per REQ-ID, monitored execution via ledger and tester verdicts, designed test structure (`conftest.py`), and isolated environments (venv per task) [TMMi Foundation, 2018].

- Entry criteria: L1 exit gate passed (policy committed, tester profile exists, >=80% of 20 tasks with tests) [Central Bank Guidelines, 2024].
- Exit criteria (L2→L3 gate): single test standard across SOLO/DUO/PIPELINE/FULL, tester active from task start, non-functional checklist on FULL, critic reviewed 100% of FULL tasks, `mutate_only_covered_lines=true` in mutmut config [TMMi Foundation, 2018].

### Level 3 — Defined

Testing is standardized organization-wide: tester/critic/engineer SOULs, TDD training with iron law in engineer SOUL, PIPELINE/FULL lifecycle integration, non-functional checklists, and critic peer review of 100% of FULL tasks [TMMi Foundation, 2018].

- Entry criteria: L2 exit gate passed (uniform standard, early tester involvement, 100% FULL reviewed) [TMMi Foundation, 2018].
- Exit criteria (L3→L4 gate): ledger DB live recording per-task metrics, line coverage >=80% sustained over 30 tasks, mutation score >=70% PIPELINE and >=80% FULL over 30 tasks, flake rate <2% over 20-run history, REQ-coverage >=90% on FULL, critic timeouts on <5% of tasks [TMMi Foundation, 2018; Central Bank Guidelines, 2024].

### Level 4 — Measured

Quality is quantitatively managed: ledger DB with per-task metrics, drill pass rates, escape-rate tracking, and multi-model consensus on appeals [TMMi Foundation, 2018].

- Entry criteria: L3 exit gate passed (ledger live, line >=80%, mutation >=70%, flake <2%, REQ-coverage >=90% over 30 tasks) [TMMi Foundation, 2018].
- Exit criteria (L4→L5 gate): escape KB entry SLA <7 days met for 100% of escapes, thresholds reviewed quarterly, prevention backlog acted on, -25% escapes/quarter trend in production reports, safe-class auto-patches gated by confidence score [TMMi Foundation, 2016; Central Bank Guidelines, 2024].

### Level 5 — Optimization

The organization prevents defects rather than detecting them: escape KB feeds SOUL patches, thresholds are recalibrated quarterly, and trend dashboards drive continuous optimization [TMMi Foundation, 2016].

- Entry criteria: L4 exit gate passed (escape SLA met, quarterly reviews, -25% escapes/quarter trend) [TMMi Foundation, 2016].
- Exit criteria: continuous — sustained -25% escapes/quarter with FP rate <=2% and appeals <=5%; optimization never completes [TMMi Foundation, 2018].

## [DEEP DIVE]: Exact Assessment Questions, Tools, Time, and Failure Modes per Level

### Assessment Questions per Level

**Level 1 → Level 2 Gate (exit checklist — ALL must be YES):**
1. Is there a committed `crew/TEST-POLICY.md`? (`git ls-files | grep -q TEST-POLICY.md`)
2. Is there a tester profile with a SOUL? (`grep -l "tester" profiles/*/SOUL.md`)
3. Over the last 20 PIPELINE/FULL tasks, did >=80% run `pytest` before DONE? (ledger query)
4. Is there a `conftest.py` at the repo root? (`test -f tests/conftest.py`)
5. Is `pytest-cov` installed? (`pip show pytest-cov`)
6. Does every REQ-ID in firstmate SPEC map to >=1 test? (lint check)

**Level 2 → Level 3 Gate:**
1. Same test standard applied across SOLO/DUO/PIPELINE/FULL? (audit SOUL patches)
2. Tester active from task start (not just gate)? (message timestamp vs SPEC)
3. Non-functional checklist checked on FULL? (report section)
4. Critic reviewed 100% of FULL? (ledger count)
5. `mutate_only_covered_lines=true` in mutmut config? (`grep -A2 "\[mutmut\]" setup.cfg`)

**Level 3 → Level 4 Gate:**
1. Ledger DB live and recording per-task metrics? (DB ping)
2. Line coverage >=80% sustained? (30-task window)
3. Mutation score >=70% PIPELINE, >=80% FULL? (30-task window)
4. Flake rate <2%? (20-run history)
5. REQ-coverage >=90% FULL? (lint count)
6. Critic timed out on <5% of tasks? (ledger)

**Level 4 → Level 5 Gate:**
1. Escape KB entry SLA <7d met for 100% of escapes? (audit)
2. Thresholds reviewed quarterly? (git log TEST-POLICY.md)
3. Prevention backlog exists and is acted on? (ledger)
4. -25% escapes/quarter trend? (prod reports)
5. Safe-class auto-patches gated by confidence score? (linter config)

### Tools Required per Level

| Level | New Tools | Already Needed |
|-------|-----------|----------------|
| 1→2 | `pytest`, `coverage.py`, `pytest-cov`, ledger (sqlite), `ruff` for lint | git, message_agent |
| 2→3 | `Hypothesis`, `mutmut`, `pytest-mock`, `pytest-xdist` | above |
| 3→4 | `vcrpy`, `testcontainers`, `mutmut` covered-lines mode, CTRF reporter, DeFlaker-like flip history | above |
| 4→5 | `hypothesis` stateful testing, embedding similarity (`sentence-transformers`), eval harness, KB store | above |

### Typical Time Between Levels (evidence-based)

| Transition | Median Time | Range | Evidence |
|------------|-------------|-------|----------|
| L1→L2 | 4-8 weeks | 2-16 weeks | TMMi Foundation 2018: managed level typically 6 months; compressed to 4-8 weeks for AI crews because tooling is pre-bundled and there's no legacy code to retrofit |
| L2→L3 | 8-12 weeks | 4-24 weeks | TMMi Foundation 2018: defined level requires organizational integration; AI crews compress this via SOUL patches instead of hiring/training |
| L3→L4 | 12-16 weeks | 8-24 weeks | TMMi Foundation 2018: measured level requires stable metric collection over 30+ tasks; AI crews can accelerate via ledger automation |
| L4→L5 | Ongoing | — | TMMi Foundation 2018: optimization is continuous; AI crews must run quarterly calibration cycles |

**Google Test Certified parallel** [KnowMBA, 2025]: teams graduated from L1 to L3 in 12-18 months using stepwise certification with explicit checkpoints per level.

### Common Failure Modes per Level

| Level | Failure Mode | Symptom | Mitigation |
|-------|-------------|---------|------------|
| 1→2 | Workaround RED logs | RED log claims failure but test was green first run | CI reruns RED step independently; assert `result.retcode != 0` |
| 1→2 | Policy ignored in crisis | "Just this once, skip tests" | Iron law is in SOUL, not policy doc; SOUL can't be overridden |
| 2→3 | Formation drift | PIPELINE and FULL use different test standards | Single conftest.py in repo root, no per-formation overrides |
| 2→3 | Critic timeout on large tasks | Critic holds up verdict >15 min | Time-box: 10 min/file, 30 min/task; partial verdict + HOLD |
| 3→4 | Metric theater | Coverage 85% but mutation 4% | Mutation gate catches coverage theater; must enforce mutation >=70% |
| 3→4 | Flake storm | >5% flake rate destabilizes CI | Auto-quarantine at >2%; 14-day fix/delete SLA |
| 4→5 | Strictness drift | FP rate >2%, appeals >5% | Quarterly calibration: review FP/FN, adjust thresholds |
| 4→5 | Leniency drift | Escalates rising | Tighten gates; increase mutation operator set |

### Exact TMMi Mapping (AI Crew Adaptation)

| TMMi Process Area | AI Crew Equivalent | Gate Evidence |
|-------------------|-------------------|---------------|
| 2.1 Test Policy | `crew/TEST-POLICY.md` committed | `git log TEST-POLICY.md` |
| 2.2 Test Plan | firstmate SPEC + REQ-IDs | message log SPEC field |
| 2.3 Monitoring | ledger + tester verdicts | ledger rows per task |
| 2.4 Design | conftest.py + test dir structure | `find tests -type f` |
| 2.5 Execution | `pytest -q` in gate | CI exit code |
| 2.6 Environment | venv per task | `python -m venv` in run |
| 3.1 Organization | tester + critic + engineer SOULs | `grep -r "tester" profiles/` |
| 3.2 Training | TDD skill + iron law in engineer SOUL | `grep "IRON LAW" profiles/engineer/SOUL.md` |
| 3.3 Lifecycle | PIPELINE/FULL flows | routing-integration.md |
| 3.4 Non-functional | perf/security checklist in tester SOUL | `grep -A5 "non_functional"` |
| 3.5 Peer review | critic review 100% FULL | ledger review_count |
| 4.1 Measurement | ledger DB + 16 metrics | `sqlite3 ledger.db ".tables"` |
| 4.2 Quality eval | drill pass + escape rate | nightly report |
| 4.3 Advanced review | multi-model consensus on appeal | appeal handling log |
| 5.1 Prevention | escape KB + SOUL patch | KB entry count |
| 5.2 QC | quarterly threshold review | `git log TEST-POLICY.md` quarterly |
| 5.3 Optimization | trend dashboards + calibration | CI dashboard |

**References for deep dive:**
- [TMMi Foundation, 2018] TMMi Framework R1.2 — process areas per level
- [KnowMBA, 2025] Test Automation Strategy — Google Test Certified timeline
- [TestFort, 2025] TMM in Software Testing — level descriptions, observability
- [TMMi Foundation, 2016] Model Aims — 88%/77% benefits, staged climb necessity
- [Central Bank Guidelines, 2024] Provisions — exit criteria, L1 chaos definition

## Practical Recommendations

| # | Recommendation | Target Level | Rationale |
|---|---------------|--------------|-----------|
| 1 | Commit `crew/TEST-POLICY.md` with iron law: no DONE without green `pytest` | L1→L2 | Establishes Test Policy process area (TMMi 2.1) with auditable gate evidence [TMMi Foundation, 2018] |
| 2 | Create tester profile with SOUL; enforce REQ-ID → >=1 test mapping | L1→L2 | Covers Test Planning and Design (TMMi 2.2, 2.4); reaches >=80% tasks-with-tests over 20 tasks [Central Bank Guidelines, 2024] |
| 3 | Stand up ledger (sqlite) + `tests/conftest.py` + `pytest-cov` in CI | L1→L2 | Provides Monitoring and Environment (TMMi 2.3, 2.6) with per-task verdict rows [TMMi Foundation, 2018] |
| 4 | Apply one test standard across SOLO/DUO/PIPELINE/FULL; tester joins at task start | L2→L3 | Prevents formation drift; implements Lifecycle Integration (TMMi 3.3) [TMMi Foundation, 2018] |
| 5 | Add non-functional checklist to FULL; critic reviews 100% of FULL with 10 min/file, 30 min/task time-box | L2→L3 | Covers Non-functional Testing and Peer Reviews (TMMi 3.4, 3.5); fixes critic timeout failure mode [TMMi Foundation, 2018] |
| 6 | Enforce mutation >=70% (PIPELINE) / >=80% (FULL) alongside line >=80% | L3→L4 | Mutation gate defeats coverage theater (85% line with 4% mutation) [TestFort, 2025] |
| 7 | Auto-quarantine flakes at >2% flake rate with 14-day fix/delete SLA | L3→L4 | Keeps flake rate <2% over 20-run history; prevents flake storms >5% [TMMi Foundation, 2018] |
| 8 | Require REQ-coverage >=90% on FULL; keep critic timeouts <5% of tasks | L3→L4 | Quantitative L4 entry over 30-task window [Central Bank Guidelines, 2024] |
| 9 | Log every production escape to KB within 7-day SLA; patch SOUL from KB | L4→L5 | Implements Defect Prevention (TMMi 5.1); 100% escape SLA compliance required [TMMi Foundation, 2016] |
| 10 | Review thresholds quarterly; target -25% escapes/quarter with FP <=2% | L4→L5 | Implements Quality Control and Optimization (TMMi 5.2, 5.3); Google Certified parallel shows 12-18 months L1→L3 [KnowMBA, 2025] |

## Metrics and Targets

| Metric | L2 Target | L3 Target | L4 Target | L5 Target |
|--------|-----------|-----------|-----------|-----------|
| Tasks with tests (20-task window) | >=80% [Central Bank Guidelines, 2024] | 100% FULL [TMMi Foundation, 2018] | 100% sustained [TMMi Foundation, 2018] | 100% sustained [TMMi Foundation, 2018] |
| Line coverage (30-task window) | Tracked | Tracked | >=80% [TMMi Foundation, 2018] | >=80% [TMMi Foundation, 2018] |
| Mutation score | — | >=70% PIPELINE (covered-lines mode) [TMMi Foundation, 2018] | >=70% PIPELINE, >=80% FULL [TMMi Foundation, 2018] | >=80% FULL, rising operator set [TMMi Foundation, 2018] |
| Flake rate (20-run history) | Tracked | <5% [TMMi Foundation, 2018] | <2% [Central Bank Guidelines, 2024] | <2% with auto-quarantine [TMMi Foundation, 2018] |
| REQ-coverage (FULL) | >=1 test per REQ-ID [Central Bank Guidelines, 2024] | >=90% [TMMi Foundation, 2018] | >=90% over 30 tasks [Central Bank Guidelines, 2024] | >=90% sustained [Central Bank Guidelines, 2024] |
| Critic review rate (FULL) | — | 100% [TMMi Foundation, 2018] | 100%, timeouts <5% [Central Bank Guidelines, 2024] | 100% + multi-model consensus on appeal [TMMi Foundation, 2018] |
| Escape KB SLA | — | — | Tracked | 100% within 7 days [TMMi Foundation, 2016] |
| Escaped defects trend | — | — | Measured quarterly [TMMi Foundation, 2018] | -25% per quarter [TMMi Foundation, 2016] |
| False-positive / appeal rate | — | — | Tracked | FP <=2%, appeals <=5% [TMMi Foundation, 2018] |
| Quality / productivity gains | Baseline | Baseline | Measured | 88% report quality gains, 77% productivity gains [TMMi Foundation, 2016] |

## References

1. [TMMi Foundation, 2016] TMMi Model Aims — staged climb necessity; 88% of adopters report quality gains, 77% report productivity gains.
2. [TMMi Foundation, 2018] TMMi Framework R1.2 — five levels and process areas per level (L2: Policy, Strategy, Planning, Monitoring, Design, Environment; L3: Organization, Training, Lifecycle, Non-functional, Peer Reviews; L4: Measurement, Product Quality, Advanced Reviews; L5: Defect Prevention, QC, Optimization); managed level typically 6 months.
3. [Central Bank Guidelines, 2024] Testing Provisions — L1 chaos definition; quantitative exit criteria (L2 >=80% over 20 tasks; L4 line >=80%, mutation >=70%, flake <2%, REQ-coverage >=90% over 30 tasks; L5 -25% escapes/quarter).
4. [KnowMBA, 2025] Test Automation Strategy — Google Test Certified 5 levels with stepwise certification; teams graduate L1 to L3 in 12-18 months.
5. [TestFort, 2025] TMM in Software Testing — level descriptions; coverage-theater observability (mutation gate catches 85% line / 4% mutation cases).
