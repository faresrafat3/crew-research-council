# Role-Split TDD Protocol (Complete Specification)

## Executive Summary
Engineer and tester are separate agents, so classic solo TDD becomes a role-split protocol with explicit handoffs: the tester authors failing (RED) tests from REQ-IDs before implementation exists, witnesses them fail, and only then does the engineer implement against frozen tests (GREEN). The protocol runs as a 10-state async state machine with per-state timeouts, correlation IDs, a 3-round fix cap, and terminal verdicts (PROMOTE/HOLD/ROLLBACK) logged to an auditable ledger. Every handoff carries evidence: RED log, GREEN log, coverage JSON, mutation report. The design exists because single-agent self-verification is unreliable — generators rate their own code favorably, while independent verification cuts error rates by orders of magnitude. Flaky tests are tiered and quarantined rather than blocking, and tester bugs are caught by independent reruns and mutation gates rather than by trust.

## Key Findings
- The unit of value in TDD is the witnessed failing test, not ceremony: RED proves the test detects the missing behavior before implementation exists [Beck, 2003; Fowler, 2020].
- Role split is a verification architecture, not bureaucracy: self-preference bias makes a model rate its own code highly [Wataoka et al., 2024], and independent verifier filtering cut functional error from 65% to 2% in controlled generation [arXiv:2506.11021].
- RED must be witnessed by tool output (`pytest -v` showing the specific failure), not claimed; a false RED is detected by running the test against an empty implementation (it must fail there too) [DEEP DIVE §4].
- Engineer edits to tests after RED are an oracle violation: the tests are the contract and are frozen at handoff [Eleks, 2025].
- Async handoffs need explicit timeouts and correlation IDs: 15 min (tester RED), 30 min (engineer GREEN), 10 min/file (critic), with one auto-remind before escalation [DEEP DIVE §3; Priygop, 2026].
- Fix loops are capped at 3 rounds; beyond that the task escalates to a human with the full evidence trail — unbounded loops are the "death of a thousand round trips" antipattern [Tatham, 2024].
- Flaky tests never silently block GREEN: same-commit flips and no-change failures are quarantined advisory-only with a 14-day fix-or-delete SLA [Bell et al., 2018; Micco, 2016].
- LLM test output still requires this protocol: Meta's TestGen-LLM shipped 75% of recommendations as correctly building and 57% as coverage-increasing, but only after acceptance filtering against explicit criteria [arXiv:2402.09171] — the protocol below is that acceptance filter.

## Detailed Analysis

### The procedure (S1–S8)

| Step | Owner | Input | Action | Output | Gate |
|---|---|---|---|---|---|
| S1 SPEC | firstmate | task | derive REQ-IDs with acceptance criteria | REQ list | no REQ-IDs → AWAIT_SPEC (30 min timeout) |
| S2 RED | tester | REQ-IDs only | author unit + PBT + integration tests per REQ; run `pytest -v` | RED log with witnessed failures | test passes on empty impl → false-RED check |
| S3 HANDOFF | tester | RED log | post RED + test files with task_id/state/correlation_id | handoff message | tests frozen from here |
| S4 GREEN | engineer | RED tests | implement until RED tests pass; never touch tests | GREEN + self-check | any test edit → HOLD |
| S5 SUITE | tester | GREEN | full `pytest -q` + coverage JSON + mutation + assertion lints | gate report | coverage <80% or mutation <70% → HOLD |
| S6 CRITIC | critic (FULL only) | gate report | independent rerun without tester rationale | agree/split verdict | split → human |
| S7 VERDICT | tester | all evidence | PROMOTE/HOLD/ROLLBACK template with REQ map | ledger entry | HOLD blocks merge |
| S8 LEDGER | tester | verdict | log rounds, FP/ESC counters; KB entry on escapes | audit trail | escape without KB entry = process bug |

### Why the roles cannot merge
A single agent that generates code and judges it suffers self-preference bias [Wataoka et al., 2024]. Independent verification is what actually removes errors: verifier-gated generation reduced functional error from 65% to 2% by clustering and filtering outputs [arXiv:2506.11021]. The tester's RED-first authoring also defends against the dominant oracle failure — LLM-generated (and even human) oracles tend to encode actual behavior rather than expected behavior, averaging only ~43-45% mutation scores on unbiased datasets [Molinelli et al., ASE 2025]. Tests authored from REQ-IDs before the implementation is read are the countermeasure.

### Failure paths
False RED (fails on empty impl correctly → valid; passes → TESTER_BUG flag), false GREEN (test passes on broken impl → mutation gate catches weak assertions), oracle violation (assertion value derived from implementation → HOLD + rewrite from REQ), flake tiers (same-commit flip / no-change coverage / cross-run flip → quarantine, never silent block), and every state timeout → ESCALATE_HUMAN with evidence. The full state machine, timeout table, and tester-bug calibration loop are specified in DEEP DIVE §1–§4 below.

## Practical Recommendations
| Recommendation | Implementation | Tools | Threshold |
|---|---|---|---|
| Freeze tests at handoff | tester owns test files after S2 | git + ledger | 0 engineer test edits |
| Witness every RED | require `pytest -v` failure output in ledger | pytest | 100% RED-witness |
| Correlate async messages | task_id + state + timestamp + correlation_id | message_agent | 100% of messages |
| Cap fix rounds | 3 rounds then ESCALATE_HUMAN | state machine | ≤3 rounds |
| Time-box every state | per-state timeout with one auto-remind | dispatch loop | 15/30/10 min |
| Quarantine, don't block, flakes | tiered detection (DEEP DIVE §1) | 20-run history | <1% blocking flake |

## Metrics and Targets
| Metric | Definition | How to Measure | Target | Warning |
|---|---|---|---|---|
| RED-witness rate | merged tasks with witnessed RED | ledger | 100% | any miss → HOLD |
| Rounds to green | fix iterations per task | ledger | ≤3 (P50 ≤1) | >3 escalate |
| Handoff latency | ENGINEER_DONE → RED log | timestamps | <15 min | >30 min |
| Gate time | GREEN → verdict | timer | <10 min | >15 min |
| False-RED rate | REDs failing empty-impl check | CI rerun | <2% | >2% retrain tester |
| Escape rate | post-PROMOTE bugs per 20 FULL tasks | reports | <1 | ≥2 tighten |

## References
1. [Beck, 2003] Test-Driven Development: By Example, Addison-Wesley. [verified: 2026-09-13]
2. [Fowler, 2020] "TestDrivenDevelopment," martinfowler.com/bliki/TestDrivenDevelopment.html. [verified: 2026-09-13]
3. [arXiv:2506.11021] Verifier-gated generation via functional clustering: functional error 65% → 2%. [verified: 2026-09-13]
4. [arXiv:2402.09171] "TestGen-LLM" (Meta): 75% correctly build, 57% increase coverage; accepted only after explicit criteria filtering. [verified: 2026-09-13]
5. [Wataoka et al., 2024] "Self-Preference Bias in LLM Evaluators," arXiv:2410.21819. [verified: 2026-09-13]
6. [Bell et al., 2018] "DeFlaker: Detecting Flaky Tests," ICSE 2018 (95.5% recall, 1.5% false alarms). [verified: 2026-09-13]
7. [Micco, 2016] "Flaky Tests at Google," testing.googleblog.com (1.5% reported / 16% some flakiness). [verified: 2026-09-13]
8. [Molinelli et al., 2025] "Do LLMs Generate Useful Test Oracles?" ASE 2025, pp. 278-290 (LLM 43% vs human 45% mutation score). [verified: 2026-09-13]
9. [Eleks, 2025] "Stop Trusting AI Test Results" (oracle separation). [verified: 2026-09-13]
10. [Tatham, 2024] "Code Review Antipatterns" (Death of a Thousand Round Trips). [verified: 2026-09-13]

---

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
