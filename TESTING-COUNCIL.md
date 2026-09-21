# TESTING COUNCIL — Deep Design Document

## Philosophy

**Testing is not a phase — it is a way of thinking about correctness.**

Testing's purpose is not to prove code works but to **discover how it fails** before users do. A passing test found nothing; a failing test taught you something.

## Core Principles

### 1. Test Behavior, Not Implementation
What the function returns → test that · how it computes → don't · if refactors break tests, the tests are wrong.

### 2. Test at the Right Level
| Level | Tests | Speed | Cost | Use When |
|-------|-------|-------|------|----------|
| Unit | 70% | ms | low | Pure logic, functions, edge cases |
| Integration | 20% | sec | medium | Component interaction, DB, API calls |
| E2E | 10% | min | high | Critical user flows, revenue paths |

### 3. Independent Tests
No cross-test state · no execution-order dependence · each test sets up and tears down its own data.

### 4. Repeatable Tests
Same input → same output, every time · no flakiness from timing, randomness, or external state · flaky → fix or delete, never ignore.

### 5. Fast Feedback
Unit tests in milliseconds · full suite in minutes, not hours · CI 30+ min → tests are too high-level.

## The Testing Lifecycle

### For Every Feature

```
1. Define acceptance criteria (what "done" looks like)
2. Write tests BEFORE or ALONGSIDE code (TDD ideal, not mandatory)
3. Write code to pass tests
4. Run full suite — all green
5. Refactor if needed — re-run, all still green
6. Merge
```

### TDD Cycle (when used)

```
RED → write test that fails
GREEN → write minimum code to pass
REFACTOR → clean up while staying green
REPEAT
```

## Test Types & Responsibilities

### Unit Tests (@tester responsibility)
Pure functions (input → expected output) · edge cases (empty, null, zero, negative, max) · error paths (invalid input, missing data, boundary) · no mocking of core logic — only I/O.

### Integration Tests (@tester + @engineer)
Module interaction (does A call B right?) · DB (queries return correct data?) · external API (real responses handled?) · cache (TTL + invalidation?).

### E2E Tests (@tester + @executor)
Critical user journey (core flow completable?) · cross-module (full stack together?) · error at scale (behavior under stress?).

### Contract Tests (for APIs)
Schema promised = schema returned? · consumers get what they expect? · v1 still works for old clients?

## Anti-Patterns (What NOT to Do)

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Testing implementation details | Breaks on refactor | Test behavior |
| Mocking everything | Tests pass, real integration fails | Mock only I/O boundaries |
| Flaky tests | Erodes trust in test suite | Fix root cause or delete |
| Ice-cream cone (lots of E2E) | Slow, expensive, brittle | Push down to unit/integration |
| No negative testing | Misses error paths | Test what happens when things go wrong |
| Copy-paste test data | Maintenance burden | Use fixtures/factories |
| Asserting on everything | Brittle tests | Assert on behavior, not every field |

## Test Quality Checklist

Before declaring tests complete:
- [ ] Tests cover happy path
- [ ] Tests cover all error paths
- [ ] Tests cover edge cases (empty, null, boundary)
- [ ] Tests are independent (no shared mutable state)
- [ ] Tests are fast (unit <10ms, integration <1s)
- [ ] Tests assert on behavior, not implementation
- [ ] Test names describe what they test (not "test1")
- [ ] Each test has a clear Arrange-Act-Assert structure
- [ ] Tests can run in any order
- [ ] Tests don't depend on external services being up

## The Tester's Bias

**The tester's job is to break things gracefully.**

A tester does not trust code; a tester asks: what if the input is null? the API is down? two users act at once? the list is empty? the number is negative? the string is 10,000 chars?

The tester isn't the engineer's enemy but their best friend: bugs found now cost less than bugs found in production.

## Integration with Crew v2

The @tester bot: (1) reviews task acceptance criteria, (2) writes tests BEFORE engineering starts (or alongside), (3) verifies every module independently, (4) runs the full suite before declaring done, (5) reports coverage and gaps.

**BLOCK merge if:** critical-path tests missing · tests flaky · implementation-detail assertions · coverage below the task-type threshold.
