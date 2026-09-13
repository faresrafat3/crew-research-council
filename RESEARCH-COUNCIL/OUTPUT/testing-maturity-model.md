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
