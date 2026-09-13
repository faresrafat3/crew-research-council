# Human-in-the-Loop Integration

## Executive Summary
Crew v2 has human escalation but no structured interface — operators get raw logs, not a dashboard, and approval flows are ad-hoc. Production multi-agent systems require explicit approval gates, adjudication queues, and operator dashboards with full context. The EU AI Act (August 2026) mandates human oversight for high-risk agentic systems. This document specifies a HITL architecture with confidence-based routing, SLA-bound approval queues, and cryptographic payload locking, adapted from Sphinx, Aegis, and production patterns (2025-2026).

## Key Findings

- **Sphinx (2026)** is an open-source HITL control plane: unified approval queue for every framework, SLA with auto-degradation (escalate/auto-approve/auto-reject on timeout), decision log with delta diffing, and tamper-evident capture (SHA3-256 hash chain + Ed25519 signatures). Governance KPIs: escalation rate, timeout rate, correction rate, reviewer agreement, error escape rate, SLA compliance [Sphinx, 2026].
- **Aegis (CloudMatos, 2025)** implements inline approvals with short-lived Ed25519-signed override tokens, threshold tiers (Tier1: ≤$5k auto; Tier2: $5k-$50k approval_needed), debounce windows (30-300s), and OpenTelemetry spans for every decision [Aegis, 2025].
- **Agent Native (2026)** specifies the approval flow pattern: intent classifier → policy engine → confidence threshold → durable approval queue → operator review surface → cryptographic payload lock → execution worker → immutable audit trail. EU AI Act mandates human oversight for high-risk systems effective August 2, 2026 [Agent Native, 2026].
- **Weir (2026)** treats approvers as finite-capacity resources with pressure-aware queuing: Normal → Elevated → Critical states based on decision latency and queue depth. Governance agent is proposal-only; deterministic policy engine validates all decisions [Weir, 2026].
- **KLA Decision Desk (2026)** provides a triage inbox with four dimensions: Priority, Team, Agent, State. Every decision is captured as an OpenTelemetry span and written to a cryptographic ledger (ImmuDB) for audit [KLA, 2026].

## Detailed Analysis

### Current Failure Modes

1. **No structured approval flow**: Human escalation is ad-hoc, no SLA.
2. **No operator dashboard**: Operators read raw logs, not a curated queue.
3. **No payload locking**: Approved actions can mutate between approval and execution.
4. **No confidence routing**: All escalations treated equally, no prioritization.
5. **No audit trail**: No immutable record of who approved what and when.

### HITL Architecture

**Six-stage flow (adapted from Agent Native + Sphinx):**

```
Stage 1: ACTION DETECTION
    Agent proposes action → emit structured metadata (intent, risk, confidence)
    
Stage 2: POLICY EVALUATION
    Policy engine evaluates: action type (CUD vs read), risk level, confidence, compliance scope
    
Stage 3: ROUTING DECISION
    If confidence < threshold OR action in protected category → route to approval queue
    Else → auto-execute
    
Stage 4: APPROVAL QUEUE
    Durable store with payload, context window summary, reasoning trace, uncertainty signals
    SLA deadline stamped (configurable per risk tier)
    
Stage 5: OPERATOR REVIEW
    Reviewer sees: action description, parameters, confidence, risk, reasoning trace
    Actions: Approve / Reject / Edit / Escalate
    
Stage 6: EXECUTION
    Approved payload cryptographically locked (HMAC signature)
    Execution worker verifies signature before running
    Full sequence persisted to immutable audit log
```

### Confidence-Based Routing

**Per-action-type thresholds (Agent Native):**

| Action Type | Auto-Execute Threshold | Approval Required If |
|-------------|----------------------|---------------------|
| Read-only | confidence > 0.95 | confidence < 0.95 |
| Write (task dir) | confidence > 0.90 | confidence < 0.90 |
| Write (shared) | confidence > 0.85 | confidence < 0.85 |
| External communication | confidence > 0.95 | confidence < 0.95 |
| Code deployment | Never auto | Always approval |
| Financial transaction | Never auto | Always approval |

**Risk tiers (Aegis pattern):**

| Tier | Threshold | Behavior |
|------|-----------|----------|
| Low | ≤$5k equivalent | Auto-execute if confidence > 0.90 |
| Medium | $5k-$50k | Approval required |
| High | >$50k | Dual approval required |
| Critical | Irreversible | Named approver + dual verification |

### Approval Queue Design

**SLA with auto-degradation (Sphinx pattern):**

| Risk Level | SLA | On Timeout |
|------------|-----|------------|
| Low | 300s | Auto-approve |
| Medium | 1800s | Escalate to senior reviewer |
| High | 3600s | Auto-reject |
| Critical | 7200s | Escalate + alert operator |

**Queue dimensions (KLA Decision Desk):**
- **Priority**: Critical escalations surface first.
- **Team**: Route to owning team (finance, legal, engineering).
- **Agent**: Isolate by agent ID for debugging.
- **State**: Open vs resolved for triage.

**Anti-fatigue measures (Aegis):**
- Debounce window: 30-300s (collapse similar requests).
- Batch approval: 5-20 ops per batch for low-risk.
- Shadow mode: run policies in shadow for 7-14 days before enforcement.
- Routing by severity: low-risk to auto-approver, high-risk to named approvers.

### Operator Dashboard

**Governance KPIs (Sphinx):**

| Metric | Definition | Target |
|--------|-----------|--------|
| Escalation rate | Escalated / total created | <5% |
| Timeout rate | SLA auto-decided / decided | <2% |
| Correction rate | Human reviews that changed payload / human reviews | >10% |
| Reviewer agreement | Human reviews confirming agent unchanged | >80% |
| Error escape rate | Approved actions with negative outcome | <1% |
| SLA compliance | Decisions before SLA deadline | >95% |
| Decision latency | Avg / p50 / p95 review time | <5 min p50 |

**Dashboard views:**
1. **Approval Queue**: Pending requests sorted by priority + SLA countdown.
2. **Decision Log**: Searchable history with delta diffs (agent proposed X, human changed to Y).
3. **Governance Metrics**: Real-time KPI dashboard.
4. **Agent Health**: Per-agent escalation rate, error rate, drift score.

### Cryptographic Payload Locking

**Problem**: Payload can mutate between approval and execution (agent modifies after approval).

**Solution (Agent Native):**
1. On approval: compute HMAC-SHA256(payload + timestamp + approver_id).
2. Store signature with approved payload.
3. Before execution: recompute HMAC and verify match.
4. If mismatch: reject and re-route to review.

**Override tokens (Aegis):**
- Short-lived (2-15 min), single-use Ed25519-signed tokens.
- Token minted on approval, verified on execution.
- Prevents replay attacks and ties approval to single retry.

### EU AI Act Compliance

**Requirements effective August 2, 2026:**
- Human oversight as verifiable technical control (not just stated principle).
- Approval queues, confidence routing, audit trails available to regulators.
- Penalties: up to €40M or 7% of global turnover for violations.

**Compliance checklist:**
- [ ] Approval queue with SLA and auto-degradation.
- [ ] Confidence-based routing with per-action-type thresholds.
- [ ] Immutable audit trail with hash chain and signatures.
- [ ] Operator dashboard with governance KPIs.
- [ ] Payload locking to prevent mutation.
- [ ] Dual verification for highest-risk categories.

## Practical Recommendations

| Recommendation | Implementation | Tools | Threshold |
|----------------|----------------|-------|-----------|
| Confidence routing | Per-action-type thresholds | Policy engine | 0.85-0.95 |
| Approval queue | SLA-bound with auto-degradation | Sphinx-style | Risk-based SLA |
| Payload locking | HMAC-SHA256 signature | Custom | All approved actions |
| Override tokens | Ed25519-signed, short-lived | Aegis-style | 2-15 min TTL |
| Operator dashboard | Real-time KPI + queue | React + WebSocket | <5 min latency |
| Anti-fatigue | Debounce + batch + shadow mode | Aegis-style | 30-300s debounce |
| EU AI Act compliance | Full audit trail + human oversight | All above | August 2026 deadline |

## Metrics Catalog

| Metric | Definition | How to Measure | Target | Warning |
|--------|-----------|----------------|--------|---------|
| Escalation rate | Escalated / total actions | Counter | <5% | >10% review policy |
| Approval latency | Request to decision | Timer | <5 min p50 | >15 min p50 |
| Payload mutation rate | Lock failures / total | Counter | 0 | >0 immediate investigation |
| Override token reuse | Reused tokens / total | Counter | 0 | >0 security incident |
| SLA compliance | Decisions before deadline | Timer | >95% | <90% review capacity |
| Reviewer agreement | Confirmations / reviews | Counter | >80% | <60% review context quality |

## References

1. [Sphinx, 2026] Sphinx: Human-in-the-Loop Control Plane. github.com/LandslideLab/Sphinx.
2. [Aegis, 2025] Aegis: Human-in-Loop Approvals for Agentic AI. cloudmatos.ai/blog.
3. [Agent Native, 2026] Human-in-the-Loop Approval Flow Pattern. agentnative.dev/patterns.
4. [Weir, 2026] Weir: Admission Control for Human Approval. github.com/VampiricCyborg/Weir.
5. [KLA, 2026] Decision Desk: Human-in-the-Loop Control Point. kla.digital/docs.
6. [EU AI Act, 2026] High-Risk AI Systems — Human Oversight Requirements. artificialintelligenceact.eu.
