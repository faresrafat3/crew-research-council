# TESTING COUNCIL — Deep Design Document

## Philosophy

**Testing is not a phase — it is a way of thinking about correctness.**

The purpose of testing is not to prove code works. It is to **discover the ways code can fail** before users do. A test that passes is a test that found nothing. A test that fails is a test that taught you something.

## Core Principles

### 1. Test Behavior, Not Implementation
- What does the function return? → TEST THAT
- How does it compute it? → DON'T TEST THAT
- If you refactor internals and tests break → tests are wrong

### 2. Test at the Right Level
| Level | Tests | Speed | Cost | Use When |
|-------|-------|-------|------|----------|
| Unit | 70% | ms | low | Pure logic, functions, edge cases |
| Integration | 20% | sec | medium | Component interaction, DB, API calls |
| E2E | 10% | min | high | Critical user flows, revenue paths |

### 3. Independent Tests
- No test depends on another test's state
- No test depends on execution order
- Each test sets up its own data and tears it down

### 4. Repeatable Tests
- Same input → same output, every time
- No flakiness from timing, randomness, or external state
- If a test is flaky → fix it or delete it, don't ignore it

### 5. Fast Feedback
- Unit tests run in milliseconds
- Full suite runs in minutes, not hours
- If CI takes 30+ minutes → tests are too high-level

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
- Pure functions: given input → expected output
- Edge cases: empty, null, zero, negative, max
- Error paths: invalid input, missing data, boundary
- No mocking of core logic — mock only I/O

### Integration Tests (@tester + @engineer)
- Module interaction: does A correctly call B?
- Database: do queries return correct data?
- External API: does the integration handle real responses?
- Cache: does TTL work? Does invalidation work?

### E2E Tests (@tester + @executor)
- Critical user journey: can a user complete the core flow?
- Cross-module: does the full stack work together?
- Error at scale: what happens when the system is under stress?

### Contract Tests (for APIs)
- Does the API return the schema it promises?
- Do consumers get what they expect?
- Version compatibility: does v1 still work for old clients?

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

A tester does not trust code. A tester asks:
- "What if this input is null?"
- "What if this API is down?"
- "What if two users do this at the same time?"
- "What if this list is empty?"
- "What if this number is negative?"
- "What if this string is 10,000 characters?"

The tester is not the enemy of the engineer. The tester is the engineer's best friend — finding bugs now is cheaper than finding them in production.

## Integration with Crew v2

The @tester bot:
1. Reviews task acceptance criteria
2. Writes tests BEFORE engineering starts (or alongside)
3. Verifies every module independently
4. Runs the full suite before declaring done
5. Reports coverage and gaps

The @tester has authority to BLOCK merge if:
- Tests are missing for critical paths
- Tests are flaky
- Tests assert on implementation details
- Coverage is below threshold for the task type
