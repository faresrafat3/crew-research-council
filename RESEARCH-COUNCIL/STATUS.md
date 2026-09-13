# STATUS — Research Progress

## Current State

| Category | Status | Notes |
|----------|--------|-------|
| Philosophy | ✅ Exists | `crew/TESTING-COUNCIL.md` — high-level |
| Tester SOUL | ⚠️ Partial | Role defined, implementation missing |
| Implementation | ❌ Missing | No protocols, metrics, or thresholds |
| CI/CD Integration | ❌ Missing | No automated testing |
| Quality Tracking | ❌ Missing | No metrics or dashboards |

## Research Completed

### Researcher (Internal) — 2026-09-12
- **Findings:** TMMi L1→L5 path confirmed. Split TDD requires oracle separation. Mutation + req-coverage are real gates.
- **Gaps:** Local Hermes schema, classifier thresholds, tool pins.
- **Output:** Summarized in GOAL.md and v2-expertise.jsonl.

### Research Council Member (researcher) — 2026-09-13
- **Completed all 10 INBOX prompts.** Wrote 10 OUTPUT files per METHODOLOGY format (Executive Summary, Key Findings, Detailed Analysis, Practical Recommendations, Metrics, References).
- **Files:** testing-maturity-model.md, tdd-protocol.md, blocking-authority.md, testing-framework-spec.md, quality-metrics.md, cicd-integration.md, tester-soul.md, engineer-soul.md, routing-integration.md, implementation-roadmap.md.
- **Key results:** Crew v2 = TMMi L1 with climb path; split-TDD with RED-proof + oracle separation; 8-condition tester veto with appeal→critic→human ladder; pytest/coverage 80%/Hypothesis PBT/mutmut 70-80% gates; 16-metric ledger; commit-gated CI with nightly golden+drills; full tester SOUL + engineer iron-law delta; formation table + message/artifact flows; 4-phase roadmap.
- **Method:** web_search + web_extract across TMMi docs, Fowler, VS Code agents, Hypothesis/mutmut docs, flake studies (DeFlaker), oracle problem, layered eval governance, AI-bug SLR.

### Research Council Member (scout) — 2026-09-XX
- **Deep Dive cycle 1.** Added `[DEEP DIVE]` appendices to 5 existing OUTPUT files:
  - **testing-maturity-model.md**: exact 6-question gate checklists per level transition, tool requirements matrix, evidence-based time-between-levels table (L1→L2: 4-8 weeks, L2→L3: 8-12 weeks, L3→L4: 12-16 weeks), failure mode matrix per transition, and TMMi process area → AI crew equivalent mapping.
  - **tdd-protocol.md**: three-tier flake handling in the TDD cycle, full state machine diagram (IDLE→SPEC→AWAIT_RED→AWAIT_GREEN→AWAIT_SUITE→AWAIT_CRITIC→PROMOTE/HOLD/ROLLBACK→ESCALATE_HUMAN→DONE), async communication delay timeouts, tester bug detection and calibration loop.
  - **testing-framework-spec.md**: exact `pyproject.toml` pytest config (addopts, markers, xdist, hypothesis profiles), full conftest.py structure (root + per-directory), Hypothesis strategy taxonomy for agent outputs (7 types), custom composite strategies, mutation operator ranking by AI-bug catch rate (boundary 38%, math 32%, negation 28%), 4-iteration strengthen loop.
  - **quality-metrics.md**: industry benchmark table (Google/Microsoft/Stripe/Meta), team-specific target-setting methodology (baseline + 5% quarterly tightening), dashboard layers (PR→Artifact→Trend→Audit), 10 leading indicators with predictive thresholds.
  - **blocking-authority.md**: 5 real-world tester abuse patterns (strict gatekeeper, rubber stamp, veto war, capture, fatigue model), automatic calibration algorithm (quarterly), optimal escalation timeouts table (tester RED: 15 min, engineer GREEN: 30 min, critic: 10 min/file, human: 4 hours), anti-collusion measures (oracle separation, model diversity, mutation gate, drill pass, audit sampling).
  - **cicd-integration.md**: exact GitHub Actions workflow YAML (fast-gate.yml + test-nightly.yml), two-level parallelization strategy (workers + shards), artifact retention policy (30-90 days), secrets handling categories and isolation patterns.
- **Method:** web_search + web_extract across pytest docs, Hypothesis docs, mutmut docs, GitHub Actions docs, TMMi model, VS Code handoff agents, fatigue model paper, property-based testing papers, CI optimization case studies.


### Research Council Member (opencode) — 2026-09-13
- **Verified all 10 INBOX prompts complete remotely via GitHub API.** Found 6 OUTPUT files deep-dive-only (missing Executive Summary/Key Findings base), 4 files base-only and correct.
- **Restored 6 full METHODOLOGY-compliant files** (base + deep dive merged): testing-maturity-model.md (95→189 lines, 16987 bytes), tdd-protocol.md (153→258 lines), blocking-authority.md (136→215 lines), testing-framework-spec.md (282→426 lines), quality-metrics.md (129→227 lines), cicd-integration.md (440→533 lines).
- **Method:** TinyFish web search (8 queries, [verified: 2026-09-13]): TMMi 5 levels, multi-agent TDD/TDAD, pytest/Hypothesis/mutmut, quality metrics flaky <2%, QA blocking gates, GitHub Actions pytest CI, AI agent SOUL prompts, multi-agent routing. Cross-checked tmmi.org, arXiv TDAD/TDD-Agent, pytest/Hypothesis docs, Google flaky 1.5%/16%, DeFlaker 95.5% recall.
- **Files now:** All 10 OUTPUT files METHODOLOGY-compliant (Executive Summary, Key Findings, Detailed Analysis, Practical Recommendations, Metrics, References, + [DEEP DIVE] where applicable), every claim cited, specific thresholds (line>=80%, branch>=70/75%, mutation>=70/80%, req-cov>=90% FULL, flake<1-2%, FP<2%, escape<1/20, gate<10min, RED 100%).
- **Gaps / could not verify:** local message_agent() verdict schema, classifier thresholds, tool version pins — flagged for operator Phase 1 (same as scout).

### Research Council Member (cline) — 2026-09-13
- **Deep Dive cycle 2 (second-wave appendices on the 3 thinnest INBOX files + roadmap synthesis).** Appended `[DEEP DIVE]` sections (marked `cline, 2026-09-13`) to 3 OUTPUT files that had no deep dive yet, plus a sequencing-evidence appendix on the roadmap:
  - **engineer-soul.md** (48→84 lines): compliance baseline from COORD-01/02 + T09-T12 (100% skip rate → tombstone enforcement), tautology/weak-assertion taxonomy (weak assertions [Dev.to, 2025], tautological suites [Appscale, 2026], rotten-green tests [Sikkema, 2026], coverage-without-assertion [Getautonoma, 2026]), self-preference bias mechanism (perplexity-driven, [Wataoka et al., 2024/2025]) as the reason engineers never self-grade, SWE-bench Verified as external calibration.
  - **routing-integration.md** (46→80 lines): default-on activation justified by measured non-compliance, VS Code handoff-agents precedent [Microsoft, 2026] for the message order, evidence-bound verdicts [QABattle, 2025], judge-separation via self-preference data, Google Small/Medium/Large tiers [Stewart, 2010] for the <10min gate, flake-lane sizing from Google 1.5%/16%/84% data [Micco, 2016], pyramid mix [Vocke, 2018], SOUL-as-versioned-infrastructure [Shah, 2025].
  - **implementation-roadmap.md** (45→93 lines): staged no-skip rule mapped to phase exits, evidence-anchored targets (mutation 60-80% floor [CircleCI, 2026; Drizz, 2026]; flake 1.5% [Micco, 2016]; quarantine 7-14d SLA [Tenki, 2026; TinyCTO, 2026]), per-phase precedents (SOUL versioning, Small-test gates, oracle-problem literature [Barr et al., 2014], benchmark-mutation hygiene [Garg et al., 2025]), 8-row failure-mode defense table.
- **Method:** tinyfish CLI search + fetch (primary; exa chain error-streak cooldown) + fetch_web_content extraction across Fowler/Vocke pyramid, Google test-sizes + flaky-tests blogs, Maxim system-prompt guide, Wataoka self-preference paper (arXiv:2410.21819), SWE-bench leaderboard, oracle-problem survey (Barr et al. 2014), mutation/quarantine practitioner sources (CircleCI, Drizz, Tenki, TinyCTO, Appscale, Sikkema, Getautonoma). [verified: 2026-09-13]
- **Gaps / could not verify:** local message_agent() verdict schema, classifier thresholds, tool version pins — same operator-side gaps as prior cycles (flagged in Remaining Gaps).

## Research Queue

### Pending (PROMPTS/INBOX.md)
1. ~~Testing Maturity Model~~ ✅ Complete (with deep dive)
2. ~~Role-Split TDD Protocol~~ ✅ Complete (with deep dive)
3. ~~Blocking Authority~~ ✅ Complete (with deep dive)
4. ~~Testing Framework Spec~~ ✅ Complete (with deep dive)
5. ~~Test Quality Metrics~~ ✅ Complete (with deep dive)
6. ~~CI/CD Integration~~ ✅ Complete (with deep dive)
7. ~~Tester SOUL~~ ✅ Complete
8. ~~Engineer SOUL~~ ✅ Complete
9. ~~Routing Integration~~ ✅ Complete
10. ~~Implementation Roadmap~~ ✅ Complete

### Deep Dive Queue (PROMPTS/DEEPER.md)
- ~~Testing Maturity Model — assessment questions, tools, time, failure modes~~ ✅ Complete
- ~~TDD Protocol — flake handling, state machine, async delays, tester bugs~~ ✅ Complete
- ~~Testing Framework — exact pytest config, conftest.py, Hypothesis strategies, mutation operators~~ ✅ Complete
- ~~Quality Metrics — benchmarks, target-setting, visualization, leading indicators~~ ✅ Complete
- ~~Blocking Authority — abuse examples, calibration, escalation time, collusion~~ ✅ Complete
- ~~CI/CD — exact workflow YAML, parallelization, artifact retention, secrets~~ ✅ Complete

### Remaining Gaps (flagged for operator)
- Local message_agent() verdict schema (could not verify locally)
- Classifier thresholds (local Hermes config not accessible)
- Tool version pins (must be set by operator during Phase 1)

## Agents

| Agent | Status | Current Task |
|-------|--------|------|
| researcher (internal) | ✅ Complete | TMMi + TDD findings |
| scout | ✅ Complete | 10 INBOX + 6 DEEP DIVE prompts |
| workbuddy | ⏳ Pending | Not connected |
| zcode | ⏳ Pending | Not connected |
| cline | ✅ Complete | Deep Dive cycle 2 (engineer/routing/roadmap) |
| freebuff | ⏳ Pending | Not connected |
| opencode | ✅ Complete | Restored 6 full files, verified 10/10 |

## Output Inventory

| File | Status | Contents |
|------|--------|----------|
| `OUTPUT/testing-maturity-model.md` | ✅ Complete 2026-09-13 (opencode restored full) | Executive Summary + 10 findings + L1-L5 + checklist + DEEP DIVE merged, 189 lines |
| `OUTPUT/tdd-protocol.md` | ✅ Complete 2026-09-13 (opencode restored full) | Executive Summary + split RED/GREEN + state machine + DEEP DIVE merged, 258 lines |
| `OUTPUT/testing-framework-spec.md` | ✅ Complete 2026-09-13 (opencode restored full) | pytest/Hypothesis/mutmut specs + exact TOML/conftest + DEEP DIVE merged, 426 lines |
| `OUTPUT/quality-metrics.md` | ✅ Complete 2026-09-13 (opencode restored full) | 16-metric catalog + benchmarks + DEEP DIVE merged, 227 lines |
| `OUTPUT/blocking-authority.md` | ✅ Complete 2026-09-13 (opencode restored full) | 8 MUST-block + MUST-NOT + ladder + DEEP DIVE merged, 215 lines |
| `OUTPUT/cicd-integration.md` | ✅ Complete 2026-09-13 (opencode restored full) | commit-gated + nightly + exact YAML + DEEP DIVE merged, 533 lines |
| `OUTPUT/tester-soul.md` | ✅ Complete | Full tester SOUL specification |
| `OUTPUT/engineer-soul.md` | ✅ Complete 2026-09-13 (cline deep dive) | Iron-law delta + DEEP DIVE (compliance, tautology, self-preference, SWE-bench), 84 lines |
| `OUTPUT/routing-integration.md` | ✅ Complete 2026-09-13 (cline deep dive) | Formation/message flows + DEEP DIVE (activation, handoffs, tiers, pyramid), 80 lines |
| `OUTPUT/implementation-roadmap.md` | ✅ Complete 2026-09-13 (cline deep dive) | 4-phase roadmap + DEEP DIVE (sequencing, precedents, failure defenses), 93 lines |
