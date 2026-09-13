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

### P1 — Multi-Agent Memory and Knowledge Management
- **Question:** How should a multi-agent crew manage shared memory, per-agent memory, and organizational knowledge? What are the patterns for memory hierarchy (per-task, per-agent, per-crew, cross-crew), memory compaction, retrieval-augmented generation for agents, and preventing catastrophic forgetting?
- **Context:** Crew v2 has no systematic memory. Each agent starts fresh. librarian shelves solved cases but there's no retrieval mechanism. firstmate tracks expertise in JSONL but it's not structured for fast lookup.
- **Output:** `OUTPUT/memory-architecture.md`

### P1 — Agent Communication Protocol Optimization
- **Question:** What is the optimal communication protocol for async multi-agent systems? How do you handle message ordering, duplicate detection, priority queuing, backpressure, and dead letter queues? What are the patterns for request-response vs fire-and-forget in agent workflows?
- **Context:** Crew v2 uses message_agent() which is fire-and-forget. There's no ordering guarantee, no duplicate detection, no priority. Complex tasks can have race conditions.
- **Output:** `OUTPUT/communication-protocols.md`

### P1 — Self-Healing and Self-Improvement Mechanisms
- **Question:** How should a multi-agent crew detect its own failures and heal itself? What are the patterns for automated root cause analysis, self-patching, regression testing for agent behavior, and graceful degradation? How do you implement a "coach" that improves the crew without human intervention?
- **Context:** Crew v2 has coach and historian but no systematic self-improvement loop. Escapes are tracked but not automatically converted to patches.
- **Output:** `OUTPUT/self-healing.md`

### P2 — Production Deployment and Monitoring
- **Question:** How do you deploy a multi-agent crew to production with high availability? What are the patterns for health checks, circuit breakers, rate limiting, cost monitoring, and alerting? How do you monitor agent "drift" over time?
- **Context:** Crew v2 runs on a single machine. No HA, no monitoring, no cost tracking per agent.
- **Output:** `OUTPUT/production-deployment.md`

### P2 — Security and Safety in Multi-Agent Systems
- **Question:** What are the unique security risks in multi-agent systems? How do you prevent prompt injection between agents, privilege escalation, data exfiltration via agent outputs, and agent "going rogue"? What are the patterns for sandboxing, capability-based security, and audit logging?
- **Context:** Crew v2 agents share a filesystem, can execute arbitrary code, and trust each other's outputs. No inter-agent security boundary.
- **Output:** `OUTPUT/multi-agent-security.md`

### P2 — Scalability Patterns for Multi-Agent Crews
- **Question:** How do you scale a multi-agent crew from 8 agents to 80 to 800? What are the patterns for agent pooling, load balancing, task routing at scale, and preventing coordination overhead from dominating? When should you split a monolithic crew into micro-crews?
- **Context:** Crew v2 has 81 agents but they all share one machine, one context window, one terminal. This won't scale.
- **Output:** `OUTPUT/scalability-patterns.md`

### P2 — Human-in-the-Loop Integration
- **Question:** How do you design the human-agent handoff in a multi-agent crew? What should be escalated to humans vs handled automatically? How do you present agent state for human review efficiently? What are the patterns for "approval gates," "adjudication queues," and "operator dashboards"?
- **Context:** Crew v2 has human escalation but no structured interface. Operator gets raw logs, not a dashboard.
- **Output:** `OUTPUT/human-in-the-loop.md`

### P3 — Cost Optimization and Token Economics
- **Question:** How do you optimize token usage across a multi-agent crew? What are the patterns for model tiering (cheap model for simple tasks, expensive for complex), caching strategies, context window management, and early stopping? How do you measure and optimize "value per token"?
- **Context:** Crew v2 uses one model for all tasks. No caching, no early stopping, no cost tracking per agent/task.
- **Output:** `OUTPUT/cost-optimization.md`

### P3 — Testing Multi-Agent Interactions
- **Question:** How do you test the interaction between agents, not just individual agents? What are the patterns for integration testing agent workflows, chaos engineering for crews, and simulating edge cases in multi-agent communication?
- **Context:** COORD-01 tested individual formations but not agent-to-agent handoffs under failure conditions.
- **Output:** `OUTPUT/multi-agent-testing.md`

### P3 — Explainability and Debugging for Agent Crews
- **Question:** How do you explain why a multi-agent crew made a specific decision? What are the patterns for decision provenance, replay debugging, and "why did agent X do Y" traceability? How do you make the crew's reasoning transparent to operators?
- **Context:** Crew v2 has message history but no structured provenance. When something goes wrong, debugging requires reading hundreds of messages.
- **Output:** `OUTPUT/explainability.md`

---

## In Progress

(None)

## Completed

### Researcher (Internal) — 2026-09-13
- 10 INBOX prompts completed (611 lines)
- Testing discipline framework delivered

### Scout — 2026-09-13
- 6 DEEP DIVE topics completed (866 lines)
- Testing discipline deepened with exact configs, state machines, calibration

### Web Agents (freebuff, cline, opencode, workbuddy, zcode) — 2026-09-13
- Cycle 1: Testing discipline synthesis (testing-maturity-model.md deepened)
- Cycle 2: Implementation roadmap operationalized (implementation-roadmap.md deepened)
- Cycle 3: TDD protocol state machine formalized (tdd-protocol.md deepened)
- Cycle 4: CI/CD integration detailed (cicd-integration.md deepened)
- Cycle 5: Quality metrics calibrated (quality-metrics.md deepened)
