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

---

## [DEEP DIVE (freebuff, pass 2, 2026-09-14)]: Does TDD Actually Work? — Human Evidence, LLM Evidence, and What Changes for Probabilistic Code

The pass-1 protocol inherits the human TDD tradition but never states the evidence base — or what must change when the system under test is probabilistic. Both gaps matter: the crew's iron law is expensive, and it deserves defense from data, not ceremony.

### T1. The human evidence: real, modest, and conditioned
- Nagappan, Maximilien, Bhat and Williams' case studies at Microsoft and IBM found pre-release defect density **40–90% lower** in the four TDD products relative to comparable non-TDD projects, at a cost of **15–35% more initial development time** [Nagappan et al., 2008]. A synthesis of the early empirical studies concludes TDD improves quality, especially in "test-infected" teams with mature test tooling [InfoQ, 2009].
- The effect is not automatic: a comparative case study of three projects measuring TDD's effect on program design reports mixed results across projects and phases [Siniaalto & Abrahamsson, arXiv:1711.05082]. Crew translation: expect a **transient productivity dip** when the iron law lands (roadmap Phases 1–2) — the 15–35% initial-time-increase figure is the planning number, and the roadmap's phase exit criteria should not assume instant velocity parity.

### T2. The LLM evidence: test-first prompting measurably helps LLM code generation
- **WebApp1K** (1,000 tasks, 20 application domains, 19 frontier models) evaluates TDD where test cases serve as both prompt and verification. Findings: instruction following and in-context learning are the critical capabilities for TDD success — surpassing general coding proficiency — and *instruction loss in long prompts* is a top bottleneck [Cui, 2025, arXiv:2505.09027]. This is direct evidence for the crew's SPEC discipline: REQ-IDs must be short, explicit, and adjacent to the tests, because long context degrades exactly the capability TDD-for-LLMs depends on.
- Microsoft Research's test-driven interactive code generation user study measured an average **+45.97% absolute pass@1 improvement** across datasets and LLMs within 5 feedback iterations [Microsoft Research, 2024].
- An ACM study of TDD with LLM-based code generation found tests plus remediation strategies collectively raise success rates by **~17%**, with many difficult problems remaining [ACM, 2024, DOI 10.1145/3691620.3695527].
- Note the ordering effect matters: pass-1's ban on engineer-authored oracles stands — these studies hand *tester-authored* tests to the generator, which is precisely the crew's RED→GREEN split (cross-ref engineer-soul.md pass-1: in-loop self-testing shows no gain).

### T3. What changes for probabilistic code: GREEN needs tolerance bands
The RED→GREEN cycle assumes a deterministic system under test. For LLM-in-the-loop components the GREEN event must be redefined, or the ledger fills with noise:
1. **RED stays deterministic** — tester-authored tests from REQ-IDs remain the spec; a witnessed RED is still a binary fact.
2. **GREEN becomes a rate** — for probabilistic paths, run n≥5 samples and require pass-rate ≥k (k set per REQ criticality; P0 = 1.0, P1 ≥ 0.8). Point-equality assertions are replaced by property invariants and schema checks (cross-ref cicd-integration.md golden-eval three layers).
3. **GREEN records provenance** — model version, temperature, and pass-rate must accompany the GREEN log, else a later regression cannot be distinguished from sampling noise (cross-ref quality-metrics.md pass-2 SPC deep dive for the control-chart treatment).
4. **Flake policy gains a new class** — a probabilistic-path failure that reproduces at the recorded model/temp/seed is a bug; one that does not is sampling variance, and belongs to the same quarantine lane as pass-1's flake tiers.

### Numbers for calibration (pass 2)

| Quantity | Value | Source |
|---|---|---|
| TDD defect-density reduction (MS/IBM, 4 products) | 40–90% | [Nagappan et al., 2008] |
| TDD initial dev-time cost | +15–35% | same |
| TDD effect on design (3-project case study) | mixed | [Siniaalto & Abrahamsson, 2017] |
| WebApp1K scale | 1,000 tasks / 20 domains / 19 models | [Cui, 2025] |
| WebApp1K critical capabilities | instruction following + ICL; instruction loss in long prompts | same |
| Test-driven interactive codegen pass@1 gain | +45.97% absolute | [Microsoft Research, 2024] |
| Tests + remediation success-rate gain (ACM) | ~17% | [ACM, 2024] |
| Probabilistic GREEN protocol | n≥5 samples, pass-rate ≥k, provenance logged | crew mapping |

### References (pass 2)
1. [Nagappan et al., 2008] "Realizing quality improvement through test driven development: results and experiences of four industrial teams," Empirical Software Engineering (Microsoft/IBM case studies). [verified: 2026-09-14, secondary summaries]
2. [InfoQ, 2009] "Empirical Studies Show Test Driven Development Improves Quality." https://www.infoq.com/news/2009/03/TDD-Improves-Quality/ [verified: 2026-09-14]
3. [Siniaalto & Abrahamsson, 2017] "A Comparative Case Study on the Impact of Test-Driven Development on Program Design," arXiv:1711.05082. https://arxiv.org/pdf/1711.05082 [verified: 2026-09-14]
4. [Cui, 2025] "Tests as Prompt: A Test-Driven-Development Benchmark for LLM Code Generation" (WebApp1K), arXiv:2505.09027. https://arxiv.org/abs/2505.09027 [verified: 2026-09-14]
5. [Microsoft Research, 2024] "LLM-Based Test-Driven Interactive Code Generation: User Study and Empirical Evaluation." https://www.microsoft.com/en-us/research/publication/llm-based-test-driven-interactive-code-generation-user-study-and-empirical-evaluation/ [verified: 2026-09-14]
6. [ACM, 2024] "Test-Driven Development and LLM-based Code Generation," DOI 10.1145/3691620.3695527. https://dl.acm.org/doi/10.1145/3691620.3695527 [verified: 2026-09-14, snippet only]
