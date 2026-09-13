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
