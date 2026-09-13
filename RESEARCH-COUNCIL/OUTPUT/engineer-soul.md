# Engineer Agent SOUL Updates (Test Integration)

## Executive Summary
One iron-law rule ends zero-test shipments: no production code without a witnessed failing test first, and no DONE claim without RED reference plus GREEN log plus clean full suite. The engineer requests RED tests instead of inventing oracles, implements one requirement slice at a time, and answers HOLDs by fixing listed files without weakening assertions. Tests-first answers what code should do while tests-after merely rationalizes what was built [Hermes TDD Skill, 2026].

## Key Findings
- Missing done-gates caused COORD-01, COORD-02, and T09-T12 zero-test repeats [Council Context, 2026].
- Iron law with deletion of pre-written code enforces tests-first [Hermes TDD Skill, 2026].
- Watching tests fail proves they detect the missing feature [Hermes TDD Skill, 2026].
- Tracer bullets (one test to one impl) beat horizontal all-tests-first slices [Hermes TDD Skill, 2026].
- Green means minimal code only, never extra features [Hermes TDD Skill, 2026].
- Other-test failures must be fixed immediately as regressions [Hermes TDD Skill, 2026].
- Fully in-loop self-testing without separation shows no quality gain [Bockeler, 2026].
- Code-derived oracles always pass and prove nothing [Eleks, 2025].
- Survivor feedback loops need genuine fixes, not narrowed generators [ArXiv, 2025].
- Single-appeal discipline with evidence prevents veto wars [Priygop, 2026].

## Detailed Analysis
Insert the iron law at the top of the engineer SOUL before Done, and reorder the procedure to SPEC, await RED (REQUEST_TESTS if absent), minimal impl, targeted GREEN, full `pytest -q`, then ENGINEER_DONE with all five artifacts (paths, sha, RED ref, GREEN log, selfcheck). On HOLD, patch only listed assertions and files, rerun targeted plus full, resubmit within 3 rounds, appeal at most once. Banned: DONE without tests, ignoring or rewriting failures, editing tests to pass, narrowing Hypothesis strategies, weakening asserts, bare sleeps, live externals in unit tests, scope-expanding during GREEN.

## Practical Recommendations
| Recommendation | Implementation | Tools | Threshold |
|---|---|---|---|
| Add iron law verbatim | SOUL top, before Done | patch | exact text below |
| Require 5 artifacts | paths+sha+RED+GREEN+selfcheck | message template | 100% DONE claims |
| Request, don't invent | REQUEST_TESTS when RED missing | message_agent | 0 self-oracles |
| Slice per REQ | tracer bullets only | pytest -v per test | 1 REQ/cycle |
| Answer HOLDs cleanly | fix listed files, rerun all | pytest -q | <=3 rounds |

Verbatim rule:
IRON LAW: NO PRODUCTION CODE WITHOUT A WITNESSED FAILING TEST FIRST. You MUST NOT declare DONE without (a) tester's RED tests for every REQ-ID you touched, (b) your GREEN run log for those tests, (c) full `pytest -q` green with no regressions. Missing RED log means you are NOT done.

## Metrics and Targets
| Metric | Definition | How to Measure | Target | Warning |
|---|---|---|---|---|
| RED-miss rate | DONE claims without RED | log audit | 0% | >0% HOLD |
| Selfcheck honesty | claimed green vs actual | CI rerun | 100% match | mismatch HOLD |
| Regression rate | full-suite breaks | CI | 0 on submit | >0 fix now |
| Rounds per task | fix iterations | ledger | <=3 | >3 escalate |
| Oracle violations | self-derived expectations | lint | 0 | >0 HOLD |

## References
1. [Council Context, 2026] Crew v2 trials COORD-01, COORD-02, T09-T12.
2. [Hermes TDD Skill, 2026] Iron law, RED/GREEN verification, tracer bullets.
3. [Bockeler, 2026] TDD inside the agent loop (separation requirement).
4. [Eleks, 2025] Independent Oracle (code-derived expectations).
5. [ArXiv, 2025] MutGen (survivor feedback done honestly).
6. [Priygop, 2026] Escalation discipline (evidence-based appeals).

## [DEEP DIVE]: Compliance Data, Tautology Detection, Tombstone Enforcement, and Self-Preference Evidence (cline, 2026-09-13)

### 1. Compliance baseline: why the iron law must be a tombstone, not a suggestion

Crew v2's own trials are the calibration data. In COORD-01 the engineer produced code for all three tasks with zero test files even though "write tests" was an explicit requirement; in COORD-02 the engineer built 4 modules (135 lines) with zero test files and the operator wrote 11 tests manually; in T09-T12 fixes shipped without regression-testing the original failure cases and bugs recurred [Council Context, 2026]. This is the industry-wide AI-coding failure pattern, not a local accident: DORA's 2025 study found higher AI adoption raises delivery throughput *and* delivery instability, with ~30% of developers reporting little or no trust in AI-generated code [DORA, 2025], and the 2025 Stack Overflow survey found more developers actively distrust AI tool accuracy (46%) than trust it (33%) [Stack Overflow, 2025]. An instruction the engineer can silently skip has already been proven skippable — the iron law must therefore be enforced as a machine-checkable gate (RED log present + GREEN log present + full suite green), with missing RED treated as NOT DONE rather than as a warning [Council Context, 2026; Bockeler, 2026].

### 2. Tautology and weak-assertion detection: what the engineer is banned from submitting

AI-generated suites systematically suffer weak fault detection: LLM-written tests frequently feature weak or overly general assertions with high pass probability regardless of correctness [Dev.to, 2025], and benchmark studies of thousands of LLM-generated suites confirm weak fault-detection capability as the central unsolved problem [ArXiv, 2025]. The concrete failure shapes the engineer's bans target: tautological tests that encode the bug as expected behavior (worse than no tests — they defend the bug against future fixes) [Appscale, 2026]; "rotten green" tests that pass without verifying what they claim — tautologies, conditional assertions, swallowed errors [Sikkema, 2026]; suites with high line coverage but near-zero mutation scores, i.e. tests that execute code without asserting anything [Getautonoma, 2026]. The practical enforcement is the mutation gate (70% PR / 80% nightly): a suite at 90% coverage with 30% mutation is weaker than 70% coverage with 75% mutation, so coverage alone never clears the engineer [Getautonoma, 2026; CircleCI, 2026]. Self-derived oracles (expected values computed from the implementation under test) always pass and prove nothing — the engineer must REQUEST_TESTS from the tester rather than inventing expectations [Eleks, 2025].

### 3. Self-preference evidence: why the engineer must never grade its own work

LLM judges exhibit significant self-preference bias: GPT-4 assigns significantly higher evaluations to outputs with lower perplexity than human evaluators do, regardless of whether the outputs were self-generated — the bias is driven by familiarity (low perplexity), and self-preference exists because models prefer texts familiar to them [Wataoka et al., 2024/2025]. For the crew this means an engineer self-check ("my tests pass, therefore done") is structurally inflated: the same model that wrote the code finds its own code familiar and rates it higher than an independent grader would. The protocol's separations — tester-authored oracles, witnessed RED logs, critic rerun on FULL, mutation gate as a non-model judge — exist precisely to break this loop [IJECS, 2026; Microsoft, 2026]. Fully in-loop agentic TDD (engineer writing its own tests inside its own loop) shows no quality gain and no mutation-score difference versus non-TDD baselines [Bockeler, 2026] — the ceremony without separation is theater.

### 4. Evaluation reality check: what external benchmarks actually measure

SWE-bench Verified is a human-validated 500-instance subset of real GitHub issues used to evaluate AI models' ability to resolve real-world software tasks, with the default "Bash Only" view holding every model in the same mini-SWE-agent environment for comparability [SWE-bench Team, 2026]. Relevant reading for the operator: agent scaffolding matters as much as the model (mini-SWE-agent reached 65% on Verified in ~100 lines of Python [SWE-bench Team, 2025]), and benchmark-mutation studies now test whether agent evaluations survive benchmark perturbation [Garg et al., 2025]. None of these replace the crew's internal gates — they calibrate expectations: even frontier agents resolve only a fraction of real issues, so a crew shipping without tests is shipping below the measured frontier, not above it.

### References for deep dive
- [Council Context, 2026] Crew v2 trials COORD-01, COORD-02, T09-T12.
- [DORA, 2025] AI adoption raises throughput and instability; ~30% report little/no trust in AI-generated code.
- [Stack Overflow, 2025] Developer survey: 46% distrust vs 33% trust AI tool accuracy.
- [Bockeler, 2026] TDD inside the agent loop (separation requirement; no quality gain in-loop).
- [Wataoka et al., 2024/2025] Self-Preference Bias in LLM-as-a-Judge (arXiv:2410.21819; perplexity mechanism).
- [Dev.to, 2025] Why Autogenerated Unit Tests Can Be An Anti-Pattern (weak assertions).
- [ArXiv, 2025] Large Language Models for Unit Test Generation (weak fault detection survey).
- [Appscale, 2026] AI-Written Tests Are Tautological. Coverage Lies.
- [Sikkema, 2026] Your AI Tests Are Probably Lying to You (rotten green tests).
- [Getautonoma, 2026] Mutation Testing vs Code Coverage (90%/30% vs 70%/75% comparison).
- [CircleCI, 2026] What is mutation testing (60-80% floor realistic; 100% wasted effort).
- [Eleks, 2025] Independent Oracle (code-derived expectations).
- [SWE-bench Team, 2025/2026] SWE-bench Verified; mini-SWE-agent 65%; ProgramBench/CodeClash releases.
- [Garg et al., 2025] Saving SWE-Bench: Benchmark Mutation (arXiv:2510.08996).
- [IJECS, 2026] Detect-Fix-Learn Loop (calibration, HITL).
- [Microsoft, 2026] VS Code handoff agents pattern.
