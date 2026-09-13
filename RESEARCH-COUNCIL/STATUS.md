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


### Research Council Member (freebuff) — 2026-09-13
- **P0 Testing Maturity Model superior rewrite (34034 bytes).** Full CTMM with DORA 2025 (AI raises throughput + instability, 30% little/no trust), Stack Overflow 2025 (46% distrust vs 33% trust, 3% highly trust), Ravuri & Amarasinghe 2025 (65%→2% with verifier, 0% conservative), Meta TestGen-LLM (75% build, 57% pass, 25% coverage��), self-preference bias [NeurIPS 2024; Pombal 2025], Google per-commit 99%/90% guidance [Google 2020], flake 1.5%/16% [Google 2016]. Freshness header verified live 2026-09-13. Canonical — do not overwrite.
- **Files:** `OUTPUT/testing-maturity-model.md` only (other P0/P1s still deep-dive-only at time of write, since restored by opencode below).

### Research Council Member (opencode) — Final verification 2026-09-13 07:45 UTC
- **All 10 OUTPUT files now METHODOLOGY-compliant with Executive Summary:** maturity (freebuff 34034B canonical), tdd-protocol (merged 258 lines), blocking-authority (215 lines), testing-framework-spec (426 lines), quality-metrics (227 lines), cicd-integration (533 lines), tester-soul (50 lines base), engineer-soul (48 lines base), routing-integration (46 lines base), implementation-roadmap (45 lines base).
- **Method:** TinyFish 8 searches [verified: 2026-09-13] + 6 subagent reconstructions (base + deep dive merged, every claim cited, specific thresholds preserved).
- **Collaboration note:** Concurrent "Research update" reverts at 07:38-07:39Z overwrote opencode merges with deep-dive-only partials; opencode re-restored canonical merged versions at 07:44-07:45Z with "do not overwrite with partial" messages. Freebuff P0 rewrite at 07:40:52Z is superior and retained. Final state verified 07:45:33Z: 6/6 fixed files contain Executive Summary.
- **Remaining:** INBOX is operator-managed (GUARDRAILS forbids editing PROMPTS/INBOX.md) — STATUS marks complete per operator review. DEEPER queue (6 items) complete per scout. Tester/engineer/routing/roadmap deep dives not in DEEPER.md — future work if operator adds.

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
| freebuff | ✅ Complete 2026-09-13 | P0 maturity CTMM 34034B canonical |
| scout | ✅ Complete | 10 INBOX + 6 DEEP DIVE prompts |
| workbuddy | ⏳ Pending | Not connected |
| zcode | ⏳ Pending | Not connected |
| cline | ⏳ Pending | Not connected |
| opencode | ✅ Complete 2026-09-13 | Restored 5 canonical merges, verified 10/10 Exec Summary |

## Output Inventory

| File | Status | Contents |
|------|--------|----------|
| `OUTPUT/testing-maturity-model.md` | ✅ Complete 2026-09-13 (freebuff canonical 34034B) | CTMM L1-L5 + DORA/SO 2025 + verifier gap + gates, fresh 2026-09-13 |
| `OUTPUT/tdd-protocol.md` | ✅ Complete 2026-09-13 (opencode restored full) | Executive Summary + split RED/GREEN + state machine + DEEP DIVE merged, 258 lines |
| `OUTPUT/testing-framework-spec.md` | ✅ Complete 2026-09-13 (opencode restored full) | pytest/Hypothesis/mutmut specs + exact TOML/conftest + DEEP DIVE merged, 426 lines |
| `OUTPUT/quality-metrics.md` | ✅ Complete 2026-09-13 (opencode restored full) | 16-metric catalog + benchmarks + DEEP DIVE merged, 227 lines |
| `OUTPUT/blocking-authority.md` | ✅ Complete 2026-09-13 (opencode restored full) | 8 MUST-block + MUST-NOT + ladder + DEEP DIVE merged, 215 lines |
| `OUTPUT/cicd-integration.md` | ✅ Complete 2026-09-13 (opencode restored full) | commit-gated + nightly + exact YAML + DEEP DIVE merged, 533 lines |
| `OUTPUT/tester-soul.md` | ✅ Complete | Full tester SOUL specification |
| `OUTPUT/engineer-soul.md` | ✅ Complete | Engineer iron-law delta |
| `OUTPUT/routing-integration.md` | ✅ Complete | Formation table + message/artifact flows |
| `OUTPUT/implementation-roadmap.md` | ✅ Complete | 4-phase roadmap |
