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
