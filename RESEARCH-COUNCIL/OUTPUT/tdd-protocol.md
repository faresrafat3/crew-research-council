# Role-Split TDD Protocol for Multi-Agent Systems

## Executive Summary

Classical RED-GREEN-REFACTOR is split across two agents: a tester writes the failing test and an engineer writes minimal implementation code, with a critic verifying the outcome [verified: 2026-09-13]. Fully in-loop agentic TDD shows no quality gain and no mutation-score difference versus non-TDD baselines [Bockeler, 2026], so the protocol's value comes from oracle separation plus witnessed RED logs rather than from the loop ceremony itself. The operational pattern follows the VS Code Red-Green-Refactor handoff agents model, where each phase emits a structured message the next phase consumes [Microsoft, 2026].

## Key Findings

1. **Three role-split topologies exist (Tester→Engineer, Tester→Engineer→Critic, multi-model consensus):** the minimal split separates oracle (tester) from implementation (engineer); the FULL topology adds an independent critic rerun; the hardened topology adds two independent tester models with human tie-break [IJECS, 2026; Microsoft, 2026].
2. **Opus-judged evaluation shows no quality advantage for fully in-loop agentic TDD:** blind judge comparisons of TDD vs non-TDD agent output find no consistent quality gain, indicating the loop alone does not improve correctness [Bockeler, 2026].
3. **No mutation-score difference between TDD and non-TDD agent runs:** mutation testing on agent-produced suites shows parity between tests-first and tests-after output, so mutation strength must be enforced explicitly (≥70% gate) rather than assumed from TDD [Bockeler, 2026; ArXiv, 2025].
4. **VS Code handoff pattern — Green writes minimal implementation, never tests:** the Green agent is forbidden from editing tests and must produce the minimal code that turns the witnessed RED green, with test edits treated as oracle violations [Microsoft, 2026].
5. **Iron law — no production code without a witnessed failing test:** every implementation step requires a prior RED log (`pytest -v` showing the failure reason); unwitnessed code is rejected at the gate [Hermes TDD Skill, 2026].
6. **Tracer bullets — one test to one implementation slice:** each RED covers exactly one REQ-ID behavior slice, keeping RED→GREEN cycles small, diagnosable, and revertible [Hermes TDD Skill, 2026].
7. **TDAD benchmark for tests-after vs tests-first evaluation:** the TDAD benchmark (2026) provides a controlled comparison harness for test-driven vs test-after agent development, grounding claims about TDD efficacy in measured pass/mutation data [ArXiv, 2026].
8. **Tests-after vs tests-first parity under agentic conditions:** controlled comparisons show tests written after implementation achieve comparable coverage and mutation scores to tests-first when the oracle is derived from requirements, confirming that oracle independence matters more than ordering [Bockeler, 2026; ArXiv, 2026].
9. **4-iteration convergence cap:** empirical agent-fix loops converge within 4 iterations when they converge at all [ArXiv, 2025]; the protocol therefore caps fixes at 3 rounds / 90 minutes before human escalation to avoid thrash.
10. **QA escalation ladder with timeouts:** every stuck state (missing RED 15 min, missing GREEN 30 min, critic timeout 10 min/file and 30 min/task, human no-response 24 h) escalates deterministically up the ladder to human decision, with conservative auto-ROLLBACK as default [Priygop, 2026].

## Detailed Analysis

### A. Oracle Separation (Why the Split Works)

The defect in single-agent TDD is oracle collapse: the same model that writes the implementation also writes the test, so the test encodes the implementation's bugs (tautologies, code-derived constants) [Eleks, 2025]. Splitting roles restores oracle independence: the tester derives assertions exclusively from REQ-IDs and the specification, never from reading the implementation source. Enforcement mechanisms include AST lint for `assert f(x) == f(x)` tautology patterns, lint against code-derived assertion constants, and mandatory `pytest -v` RED logs showing the actual failure reason before any GREEN is accepted [Eleks, 2025; Hermes TDD Skill, 2026].

### B. Critic as Second Check

In FULL topology, the critic independently reruns the suite, replays the RED log against empty/broken implementations (false-RED/false-GREEN checks), and issues PROMOTE / HOLD / ROLLBACK verdicts. Critic–tester disagreement is itself a signal and escalates to human rather than auto-merging [IJECS, 2026]. The critic never writes production code and never edits tests; it only judges evidence.

### C. Multi-Model Consensus with HITL

For FULL tasks, two independent tester models generate oracles from the same REQ-IDs; disagreement escalates to human [IJECS, 2026]. This catches single-model blind spots (missed edge cases, weak assertions) at the cost of one extra inference pass. Human-in-the-loop is the terminal tie-breaker and the precedent-setter: every human decision becomes a knowledge-base entry for future runs.

### D. Time-Boxing

Critic review is time-boxed at 10 min/file and 30 min/task; on timeout the protocol emits a PARTIAL_VERDICT + HOLD rather than blocking the dispatch loop indefinitely [Priygop, 2026]. Tester RED is expected within 15 min of dispatch and engineer GREEN within 30 min of a witnessed RED; breaches trigger one auto-reminder then escalation. The fix loop is capped at 3 rounds / 90 min total before ESCALATE_HUMAN, consistent with the 4-iteration convergence observation [ArXiv, 2025].

### E. Deep Dive (Verbatim)

## [DEEP DIVE]: Flaky Tests in the TDD Cycle, State Machine, Async Delays, and Tester Bugs

### 1. Handling Flaky Tests in the TDD Cycle

**The flake problem in AI-agent TDD** [Bell et al., 2018; FlakyTest, 2026]:
- Flaky tests erode trust in the RED→GREEN gate. If a test flips between pass/fail on identical code, the engineer cannot know whether their fix worked.
- Google reports 1.5% of tests are flaky, but 16% exhibit some flakiness [VT, 2022].

**Three-tier flake handling in the TDD cycle** [KnowMBA, 2025; Bell et al., 2018]:

| Tier | Detection | Action | Gate Effect |
|------|-----------|--------|-------------|
| 1 Same-commit flip | 20-run history with identical commit hash | Flag as FLAKE, do not count toward GREEN | Does not block RED→GREEN |
| 2 No-change failure | DeFlaker: test fails but covers no changed lines | Auto-quarantine advisory-only | Never blocks GREEN |
| 3 Cross-run flip | Same test passes on commit A, fails on commit B (identical code) | Quarantine + 14-day fix/delete | Advisory in GREEN, blocks PROMOTE if blocking-suite |

**Implementation in the state machine:**
```
FLAKE_DETECTED:
  if same-commit flip and >2 flips in 20 runs:
    label FLAKE, move to quarantine
    do NOT count as regression
    schedule fix/delete within 14 days [KnowMBA, 2025]
  if DeFlaker no-change-coverage rule triggers:
    quarantine immediately, advisory only
  if test is in blocking suite and flaky:
    reroute to non-blocking lane (run advisory)
```

**Anti-flake patterns for AI-agent TDD:**
1. No bare sleeps — wrap time with `freezegun` or seeded clock stubs [Fowler, 2024]
2. Hermetic servers for integration — testcontainers/vcrpy, no live externals in gate [KnowMBA, 2025]
3. Deterministic seeds for PBT — `@settings(derandomize=True)` in CI, `seed=` on failure replay [Hypothesis Docs, 2026]
4. No hidden global state — fixtures scope="function" only for GREEN phase tests [Hermes TDD Skill, 2026]
5. Idempotent tests — each test creates its own data, never depends on prior test execution order

### 2. Full State Machine for the Role-Split TDD Protocol

**States and transitions:**

```
IDLE
  → on task dispatch: SPEC
  → on missing REQ-IDs: AWAIT_SPEC

AWAIT_SPEC
  → firstmate emits REQ-IDs: SPEC_COMPLETE
  → firstmate timeout (30 min): ESCALATE_HUMAN (missing spec)

AWAIT_RED
  → tester posts RED log: RED_WITNESSED
  → tester posts RED but no actual failure (false-red): TESTER_BUG (see §4)
  → tester timeout (15 min): ESCALATE_HUMAN (tester stuck)
  → flake detected in RED test: RED_FLAKE (do not count, retry up to 3x)

AWAIT_GREEN
  → engineer posts GREEN + selfcheck: GREEN_SELF
  → engineer GREEN but full suite red: REGRESSION
  → engineer timeout (30 min): ESCALATE_HUMAN (engineer stuck)
  → engineer edits test to pass: TESTER_BUG (oracle violation, HOLD)

AWAIT_SUITE
  → `pytest -q` clean: SUITE_CLEAN
  → suite red on listed files: HOLD (rounds < 3)
  → suite red on other files: REGRESSION (immediate fix)
  → coverage < 80%: HOLD (add tests)
  → mutation < 70%: HOLD (strengthen assertions)

AWAIT_CRITIC (FULL only)
  → critic reruns + PROMOTE: CRITIC_PASS
  → critic reruns + HOLD: CRITIC_SPLIT
  → critic timeout (10 min/file, 30 min/task): PARTIAL_VERDICT + HOLD
  → critic-tester disagreement: ESCALATE_HUMAN

PROMOTE
  → merge allowed, ledger updated

HOLD
  → engineer patches, rerun, resubmit: → AWAIT_GREEN (if rounds < 3)
  → rounds >= 3: ESCALATE_HUMAN
  → engineer appeal (once): → AWAIT_CRITIC
  → appeal rejected: ESCALATE_HUMAN

ROLLBACK
  → revert impl + RED, restart: → AWAIT_RED
  → rollback with KB entry: log escape

ESCALATE_HUMAN
  → human decision: → PROMOTE or ROLLBACK or AWAIT_RED
  → decision becomes KB precedent

DONE
  → final state (from PROMOTE)
```

**State persistence:** each transition writes to ledger with timestamp, actor, and evidence. Full state machine is auditable for post-mortems.

### 3. Async Communication Delays

**Problem:** message_agent() is fire-and-forget. Tester or engineer may not respond immediately. Meanwhile the dispatch cycle continues.

**Solutions per delay type:**

| Delay Type | Timeout | Action |
|------------|---------|--------|
| Tester RED not received | 15 min from ENGINEER_DONE | Auto-remind tester once; then ESCALATE_HUMAN |
| Engineer GREEN not received | 30 min from RED_WITNESSED | Auto-remind engineer once; then HOLD |
| Critic review not received | 10 min/file, 30 min/task | Partial verdict + HOLD |
| Human escalation response | 24 hours | Auto-ROLLBACK (conservative default) |
| Flake rerun cycle | 5 min per rerun, max 3 reruns | If still flaky, quarantine |

**Async patterns:**
- All agent messages carry `task_id`, `state`, `timestamp`, `correlation_id` for reassembly.
- Dispatch loop is NOT blocked waiting for any single agent. It tracks per-task state and advances on events.
- If an agent crashes mid-task, the dispatch detects missing heartbeat after timeout and re-dispatches the step.

**VS Code handoff parallel** [Microsoft, 2026]: VS Code uses explicit handoff agents with message queues. Each phase emits a structured message that the next phase consumes. If a phase times out, the queue holds the message and retries once before escalating.

### 4. When the Tester Itself Has Bugs

**Problem:** The tester is an AI agent. It can write buggy tests, false REDs, or miss real regressions.

**Detection mechanisms:**

| Bug Type | Detection | Response |
|----------|-----------|----------|
| False RED (test fails before any impl) | CI reruns RED step independently; if test fails on empty impl, it's a valid RED. If it passes on empty impl, it's a false-red. | HOLD + TESTER_BUG flag. Human reviews test. |
| False GREEN (test passes on broken impl) | Mutation testing: if mutant survives, test is weak. Critic rerun: if critic finds bug tester missed, TESTER_BUG. | Strengthen test, add to KB. |
| Tautology (asserts expected from same read as actual) | AST lint: detect `assert f(x) == f(x)` pattern [Eleks, 2025]. | HOLD + rewrite test. |
| Oracle violation (code-derived constant) | Lint: detect assertion value derived from impl source. | HOLD + rewrite test from REQ only. |
| Flaky test written by tester | 20-run history detects flips. | Quarantine + 14-day fix/delete. |
| Tester timeout | Heartbeat timeout (15 min). | ESCALATE_HUMAN. |

**Calibration loop for tester bugs:**
1. Every TESTER_BUG is logged to ledger with evidence.
2. Monthly review: count TESTER_BUG by type.
3. If false-RED rate > 2%, tighten tester SOUL: require `pytest -v` output showing actual failure reason.
4. If false-GREEN rate > 2%, add mutation step before GREEN acceptance.
5. If tautology rate > 0%, add AST lint to tester's pre-submit checklist.

**Multi-model consensus** [IJECS, 2026]: For FULL tasks, use two independent tester models. If they disagree, escalate to human. This catches single-model blind spots.

**References for deep dive:**
- [Bell et al., 2018] DeFlaker: same-commit flip detection, no-change-coverage rule
- [VT, 2022] Flaky Tests at Google: 1.5%/16% flakiness rates
- [KnowMBA, 2025] Test Automation Strategy: 14-day fix/delete SLA, hermetic servers
- [Fowler, 2024] Eradicating Non-Determinism: no bare sleeps, seeded clocks
- [Microsoft, 2026] VS Code handoff agents: message queue pattern
- [IJECS, 2026] Closing the Detect-Fix-Learn Loop: multi-model consensus
- [Eleks, 2025] Stop Trusting AI Test Results: tautology detection, oracle violation
- [Hermes TDD Skill, 2026] Iron law, tracer bullets, RED/GREEN verification
- [Hypothesis Docs, 2026] derandomize, seed, database profiles
- [Priygop, 2026] Escalation Frameworks: timeout-based escalation

## Practical Recommendations

| Step | Owner | Action | Evidence / Gate |
|------|-------|--------|-----------------|
| 0. Spec | Firstmate / Dispatcher | Emit REQ-IDs per behavior slice; no work without REQ-IDs [Hermes TDD Skill, 2026] | SPEC_COMPLETE; missing spec → AWAIT_SPEC, 30-min timeout → ESCALATE_HUMAN [Priygop, 2026] |
| 1. Tester RED | Tester | Write one failing test per REQ-ID slice from REQ text only; run `pytest -v` and post RED log with failure reason [Hermes TDD Skill, 2026] | RED_WITNESSED required; false-red → TESTER_BUG + HOLD [Eleks, 2025] |
| 2. Engineer GREEN | Engineer | Write minimal implementation to turn RED green; never edit tests; run self-check suite [Microsoft, 2026] | GREEN_SELF; test edit → oracle violation, HOLD [Eleks, 2025] |
| 3. Critic review | Critic | Independently rerun RED + suite + mutation spot-check within 10 min/file, 30 min/task; issue verdict [IJECS, 2026] | Timeout → PARTIAL_VERDICT + HOLD; disagreement → ESCALATE_HUMAN |
| 4. Verdict gate | Dispatcher | PROMOTE (merge allowed), HOLD (patch + resubmit), or ROLLBACK (revert impl + RED, restart) [Microsoft, 2026] | Ledger entry with timestamp, actor, evidence; audit trail required |
| 5. Fix cap | All | Max 3 rounds / 90 min per task, consistent with 4-iteration convergence [ArXiv, 2025]; single appeal allowed | Rounds ≥ 3 → ESCALATE_HUMAN; appeal rejected → ESCALATE_HUMAN |

**Handoff formats:**

```
ENGINEER_DONE:
  task_id: <id>
  state: AWAIT_RED
  req_ids: [REQ-xxx]
  files_changed: [...]
  correlation_id: <uuid>
  timestamp: <iso8601>

TEST VERDICT:
  task_id: <id>
  state: AWAIT_CRITIC | CRITIC_PASS | CRITIC_SPLIT
  req_id: REQ-xxx
  red_log: <pytest -v excerpt with failure reason>
  suite: <pytest -q result>
  coverage: <pct> (gate ≥ 80%)
  mutation: <pct> (gate ≥ 70%)
  verdict: PROMOTE | HOLD | ROLLBACK
  correlation_id: <uuid>
  timestamp: <iso8601>

APPEAL (max once per task):
  task_id: <id>
  state: HOLD → AWAIT_CRITIC
  grounds: <why verdict is wrong + counter-evidence>
  correlation_id: <uuid>
  timestamp: <iso8601>
```

**State machine (summary):** IDLE → SPEC → AWAIT_RED → AWAIT_GREEN → AWAIT_SUITE → AWAIT_CRITIC (FULL only) → PROMOTE / HOLD / ROLLBACK → DONE; HOLD loops to AWAIT_GREEN while rounds < 3, else ESCALATE_HUMAN; ROLLBACK restarts at AWAIT_RED; see Deep Dive §2 for the full transition table with flake, timeout, and tester-bug edges [Priygop, 2026; Hermes TDD Skill, 2026].

## Metrics

| Metric | Target | Source / Rationale |
|--------|--------|--------------------|
| RED-witness rate | 100% of GREENs preceded by witnessed `pytest -v` RED log | Iron law [Hermes TDD Skill, 2026] |
| False-green rate | 0% surviving mutants on gated assertions (mutation gate ≥ 70%) | No mutation difference vs non-TDD without gate [Bockeler, 2026; ArXiv, 2025] |
| Regression rate | < 2% of PROMOTEs cause suite red on other files | Full-suite `pytest -q` gate; DeFlaker no-change rule excludes flakes [Bell et al., 2018] |
| Fix rounds | ≤ 3 rounds / 90 min per task | 4-iteration convergence [ArXiv, 2025] |
| Time-to-verdict | < 5 min median critic verdict (timeout 10 min/file, 30 min/task) | Time-box [Priygop, 2026; IJECS, 2026] |
| Appeal rate | < 5% of HOLDs appealed; appeal allowed once per task | Appeal path; rejected appeal → ESCALATE_HUMAN |

## References

1. Bockeler, 2026 — Fully in-loop agentic TDD shows no quality gain; no mutation-score difference vs non-TDD; Opus-judged parity.
2. Microsoft, 2026 — VS Code Red-Green-Refactor handoff agents pattern; Green writes minimal implementation, never tests; message-queue handoff.
3. Hermes TDD Skill, 2026 — Iron law (no prod code without failing test); tracer bullets (one test to one impl slice); RED/GREEN verification; function-scoped fixtures.
4. ArXiv, 2026 (TDAD) — TDAD benchmark for test-driven vs test-after agent development evaluation.
5. ArXiv, 2025 (MutGen) — Agent fix-loop convergence within 4 iterations; mutation-testing harness for agent suites (≥70% gate).
6. Eleks, 2025 — Stop Trusting AI Test Results: tautology (`assert f(x) == f(x)`) and code-derived oracle violation detection.
7. IJECS, 2026 — Closing the Detect-Fix-Learn Loop: multi-model consensus with HITL tie-break for tester/critic disagreement.
8. Priygop, 2026 — QA escalation ladder: timeout-based escalation (15-min RED, 30-min GREEN, 10-min/file critic, 24-h human default ROLLBACK).
