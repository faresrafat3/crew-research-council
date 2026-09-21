# TEST-POLICY.md — Testing Discipline for Crew v2

## 1. Purpose

Testing discipline for Crew v2 (multi-agent crew); binding on every agent, formation, and task.

## 2. Scope

Applies to all agent profiles (engineer, tester, researcher, architect, critic, razor, completer, firstmate) · all formations (SOLO, DUO, PIPELINE, FULL) · all task types (code, research, analysis, creative).

## 3. The Iron Law (Engineer)

```
NO PRODUCTION CODE WITHOUT A WITNESSED FAILING TEST FIRST.
NO "DONE" CLAIM WITHOUT RED REFERENCE + GREEN LOG + CLEAN FULL SUITE.
```

**Rationale:** Tests-first answers what code should do; tests-after rationalizes what was built [Hermes TDD Skill, 2026]. The iron law kills Crew v2's #1 failure mode: untested code shipping (COORD-01/02 evidence).

**Enforcement:** engineer MUST (a) request RED tests from tester before implementation, (b) provide a RED log reference (commit hash / message ID) when declaring DONE; MUST NOT (c) weaken assertions to force a pass, (d) delete or skip tests for deadlines.

## 4. Tester Activation Rules

**Activated:** task requires code with tests · says "write tests"/"test coverage" · acceptance criteria need verification · engineer declares DONE (tester verifies) · formation is PIPELINE/FULL.
**NOT activated:** SOLO explicitly marked "no tests needed" · pure research (read-only) · creative (writing, design).

## 5. Tester Blocking Authority

**MUST block (HOLD/ROLLBACK):** (1) missing tests for any REQ-ID · (2) coverage <80% line/branch · (3) mutation <70% PIPELINE / <80% FULL · (4) unquarantined flaky test · (5) constraint violation · (6) missing/fabricated RED log · (7) implementation-detail assertions · (8) over-mocked test (no real integration).
**MUST NOT block on:** style · scope disagreements (→ critic) · ambiguous requirements (→ firstmate) · external outages.

## 6. Escalation Ladder

```
Tester blocks → Engineer appeals (once) → Critic tie-break → Human escalation
```

**Human escalation package:** issue (what/why blocked) · impact (what's delayed) · what was tried (engineer's appeal) · decision needed (options) · time sensitivity (deadline).

## 7. Formation-Specific Rules

### SOLO
Engineer writes own tests (no tester) · self-verification · coverage 70% line / 60% branch.

### DUO (Engineer → Tester)
Tester writes RED tests first · engineer implements to pass · tester verifies GREEN + gates · coverage 80% line / 80% branch.

### PIPELINE (Researcher → Architect → Engineer → Tester → Critic)
Tester active from task start · per-stage test requirements · critic reviews 100% of FULL tasks · coverage 80% line / 80% branch, 70% mutation.

### FULL (All agents)
All PIPELINE rules · non-functional testing required (performance, security) · coverage 80% line / 80% branch, 80% mutation.

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

Violations tracked in the quality ledger; repeated: (1) warning + retraining, (2) formation restriction (SOLO only), (3) profile suspension pending review.

## 14. Review Cycle

Reviewed quarterly; changes require tester approval · critic review · firstmate sign-off · human operator final approval.

---

**Effective date:** 2026-09-13
**Owner:** Crew v2 Testing Council
**Version:** 1.0
