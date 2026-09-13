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
| cline | ⏳ Pending | Not connected |
| freebuff | ⏳ Pending | Not connected |
| opencode | ⏳ Pending | Not connected |

## Output Inventory

| File | Status | Contents |
|------|--------|----------|
| `OUTPUT/testing-maturity-model.md` | ✅ Complete | L1-L5 model + self-assessment checklist + DEEP DIVE (gate questions, tools, time, failure modes) |
| `OUTPUT/tdd-protocol.md` | ✅ Complete | RED/GREEN/REFACTOR split + state machine + DEEP DIVE (flake handling, async delays, tester bugs) |
| `OUTPUT/testing-framework-spec.md` | ✅ Complete | pytest/coverage/PBT/mutation specs + DEEP DIVE (exact config, conftest.py, strategies, operators) |
| `OUTPUT/quality-metrics.md` | ✅ Complete | 16-metric catalog + DEEP DIVE (benchmarks, targets, visualization, leading indicators) |
| `OUTPUT/blocking-authority.md` | ✅ Complete | 8-condition veto + appeal ladder + DEEP DIVE (abuse patterns, calibration, escalation, collusion) |
| `OUTPUT/cicd-integration.md` | ✅ Complete | commit-gated CI + nightly async + DEEP DIVE (exact YAML, parallelization, artifacts, secrets) |
| `OUTPUT/tester-soul.md` | ✅ Complete | Full tester SOUL specification |
| `OUTPUT/engineer-soul.md` | ✅ Complete | Engineer iron-law delta |
| `OUTPUT/routing-integration.md` | ✅ Complete | Formation table + message/artifact flows |
| `OUTPUT/implementation-roadmap.md` | ✅ Complete | 4-phase roadmap |
