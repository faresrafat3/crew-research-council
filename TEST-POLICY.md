# TEST-POLICY.md — Testing Discipline for Crew v2

## 1. Purpose

This document defines the testing discipline for Crew v2, a multi-agent AI crew system. Every agent, formation, and task MUST follow this policy.

## 2. Scope

This policy applies to:
- All agent profiles (engineer, tester, researcher, architect, critic, razor, completer, firstmate)
- All formations (SOLO, DUO, PIPELINE, FULL)
- All task types (code, research, analysis, creative)

## 3. The Iron Law (Engineer)

```
NO PRODUCTION CODE WITHOUT A WITNESSED FAILING TEST FIRST.
NO "DONE" CLAIM WITHOUT RED REFERENCE + GREEN LOG + CLEAN FULL SUITE.
```

**Rationale:** Tests-first answers what code should do; tests-after merely rationalizes what was built [Hermes TDD Skill, 2026]. The iron law eliminates the #1 failure mode in Crew v2: code shipping untested (COORD-01, COORD-02 evidence).

**Enforcement:**
- Engineer MUST request RED tests from tester before implementation
- Engineer MUST provide RED log reference (commit hash or message ID) when declaring DONE
- Engineer MUST NOT weaken assertions to make tests pass
- Engineer MUST NOT delete or skip tests to meet deadlines

## 4. Tester Activation Rules

Tester is activated when:
- Task requires code with tests
- Task says "write tests" or "test coverage"
- Task has acceptance criteria that need verification
- Engineer declares DONE (tester verifies)
- Formation is PIPELINE or FULL

Tester is NOT activated when:
- Task is SOLO and explicitly marked "no tests needed"
- Task is pure research (read-only)
- Task is creative (writing, design)

## 5. Tester Blocking Authority

Tester MUST block (HOLD/ROLLBACK) when:
1. Missing tests for any REQ-ID
2. Coverage below threshold (line <80%, branch <80%)
3. Mutation score below threshold (PIPELINE <70%, FULL <80%)
4. Flaky test not quarantined
5. Constraint violation detected
6. RED log missing or fabricated
7. Test asserts on implementation details
8. Over-mocked test (no real integration)

Tester MUST NOT block on:
- Style preferences
- Scope disagreements (escalate to critic)
- Ambiguous requirements (escalate to firstmate)
- External service outages

## 6. Escalation Ladder

```
Tester blocks → Engineer appeals (once) → Critic tie-break → Human escalation
```

**Human escalation package:**
- Issue: what is blocked and why
- Impact: what is delayed
- What was tried: engineer's appeal argument
- Decision needed: specific options
- Time sensitivity: deadline if any

## 7. Formation-Specific Rules

### SOLO
- Engineer writes own tests (no tester activation)
- Self-verification required
- Coverage threshold: 70% line, 60% branch

### DUO (Engineer → Tester)
- Tester writes RED tests first
- Engineer implements to pass tests
- Tester verifies GREEN + gates
- Coverage threshold: 80% line, 80% branch

### PIPELINE (Researcher → Architect → Engineer → Tester → Critic)
- Tester active from task start
- Each stage has test requirements
- Critic reviews 100% of FULL tasks
- Coverage threshold: 80% line, 80% branch, 70% mutation

### FULL (All agents)
- All PIPELINE rules apply
- Non-functional testing required (performance, security)
- Coverage threshold: 80% line, 80% branch, 80% mutation

## 8. Test Quality Standards

### Unit Tests
- Framework: pytest
- Structure: Arrange-Act-Assert
- One behavior per test
- No shared mutable state between tests
- Mock only I/O boundaries
- Max 10ms per test

### Integration Tests
- Real dependencies where possible
- Transactional test isolation
- Test data setup/teardown per test
- Max 1s per test

### E2E Tests
- Only for critical user journeys
- Max 10 E2E tests per task type
- Data setup via API/seeding
- Max 30s per test

### Property-Based Tests
- Framework: Hypothesis
- Min 3 properties per module
- Test invariants, not examples
- Use adversarial strategies for AI outputs

### Mutation Testing
- Framework: mutmut
- Target: mutate only covered lines
- Min score: 70% PIPELINE, 80% FULL
- Stack limit: 10 mutations per file

## 9. Metrics and Targets

| Metric | Definition | Target | Warning |
|--------|-----------|--------|---------|
| RED-witness | Merged with RED log | 100% P2+ | <100% |
| Line coverage | Lines covered by tests | ≥80% | <70% |
| Branch coverage | Branches covered | ≥80% | <70% |
| Mutation score | Mutants killed | ≥70% PIP, ≥80% FULL | <60% |
| REQ-coverage | REQs with ≥1 test | ≥90% FULL | <80% |
| Flake rate | Flaky test runs | <2% | >5% |
| False positive | Tester blocks correct code | <2% | >5% |
| False negative | Tester passes buggy code | <5% | >10% |
| Escape rate | Bugs in production | <1 per 20 tasks | >1 per 10 |
| MTTR | Mean time to repair | <14 days | >30 days |

## 10. Maturity Levels

| Level | Name | Criteria |
|-------|------|----------|
| 1 | Ad-hoc | No tests, ship-and-pray |
| 2 | Managed | Tests before done, tester active, coverage tracked |
| 3 | Defined | Shared standards, lifecycle integration, mutation testing |
| 4 | Measured | Ledger DB, 16 metrics, drill testing, escape tracking |
| 5 | Optimized | Prevention reviews, auto-calibration, trend dashboards |

**Current Crew v2 status:** Level 1 (Ad-hoc)

**Target:** Level 2 by end of Phase 1, Level 3 by end of Phase 3.

## 11. Tools

| Tool | Purpose | Required From |
|------|---------|---------------|
| pytest | Test runner | Phase 1 |
| coverage.py | Coverage measurement | Phase 1 |
| pytest-cov | Coverage plugin | Phase 1 |
| Hypothesis | Property-based testing | Phase 3 |
| mutmut | Mutation testing | Phase 3 |
| pytest-mock | Mocking | Phase 2 |
| pytest-xdist | Parallel testing | Phase 2 |
| vcrpy | HTTP recording | Phase 3 |
| CTRF reporter | Test reporting | Phase 3 |

## 12. File Structure

```
crew/
├── TEST-POLICY.md          # This file
├── tests/
│   ├── conftest.py         # Shared fixtures
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── e2e/                # End-to-end tests
├── profiles/
│   ├── engineer/SOUL.md    # With iron law
│   ├── tester/SOUL.md      # Full spec
│   └── firstmate/SOUL.md   # With activation rules
└── RESEARCH-COUNCIL/       # Research outputs
```

## 13. Compliance

Violations of this policy are tracked in the quality ledger. Repeated violations trigger:
1. First: Warning + retraining
2. Second: Formation restriction (SOLO only)
3. Third: Profile suspension pending review

## 14. Review Cycle

This policy is reviewed quarterly. Changes require:
- Tester approval
- Critic review
- Firstmate sign-off
- Human operator final approval

---

**Effective date:** 2026-09-13
**Owner:** Crew v2 Testing Council
**Version:** 1.0
