# Research Queue — Pending Tasks

## How This Works

1. Research agents pick the highest priority task from this file
2. Research exhaustively
3. Write output to `OUTPUT/<topic>.md`
4. Move the task to "In Progress" with agent name
5. When complete, operator moves to "Completed"

## Priority Levels

- **P0**: Blocking implementation — must be done first
- **P1**: Critical — needed for v2 to function
- **P2**: Important — significantly improves quality
- **P3**: Nice to have — can be deferred

## Queue

### P0 — Testing Maturity Model
- **Question:** What are 5 maturity levels for AI agent testing, with measurable criteria?
- **Context:** We need to assess where Crew v2 is now and define a path forward.
- **Output:** `OUTPUT/testing-maturity-model.md`

### P0 — Role-Split TDD Protocol
- **Question:** What is the exact step-by-step procedure for multi-agent TDD?
- **Context:** Engineer and tester are different agents. They communicate asynchronously.
- **Output:** `OUTPUT/tdd-protocol.md`

### P0 — Blocking Authority and Governance
- **Question:** When can the tester block a release? How are disagreements resolved?
- **Context:** Tester must have bounded authority — not too strict, not too lenient.
- **Output:** `OUTPUT/blocking-authority.md`

### P1 — Testing Framework Specification
- **Question:** What are the concrete specifications for unit, integration, E2E, property-based, and mutation testing?
- **Context:** Need exact tools, configurations, and thresholds.
- **Output:** `OUTPUT/testing-framework-spec.md`

### P1 — Test Quality Metrics
- **Question:** What 15+ metrics should we track, with definitions and targets?
- **Context:** We need to measure test quality over time.
- **Output:** `OUTPUT/quality-metrics.md`

### P1 — CI/CD Integration
- **Question:** How do we integrate testing into the agent dispatch cycle?
- **Context:** Tests must run automatically when agents produce output.
- **Output:** `OUTPUT/cicd-integration.md`

### P1 — Tester Agent SOUL
- **Question:** What is the complete, implementable tester SOUL?
- **Context:** Must be executable instructions, not philosophy.
- **Output:** `OUTPUT/tester-soul.md`

### P1 — Engineer Agent SOUL Updates
- **Question:** What exact additions does the engineer SOUL need?
- **Context:** Must require tests before declaring done.
- **Output:** `OUTPUT/engineer-soul.md`

### P2 — Routing and Formation Integration
- **Question:** How does the tester integrate into formation selection?
- **Context:** firstmate must know when to activate the tester.
- **Output:** `OUTPUT/routing-integration.md`

### P2 — Implementation Roadmap
- **Question:** What is the phased implementation plan?
- **Context:** We need a sequence that delivers value at each step.
- **Output:** `OUTPUT/implementation-roadmap.md`

---

## In Progress

(None)

## Completed

(None — awaiting agent pickup)
