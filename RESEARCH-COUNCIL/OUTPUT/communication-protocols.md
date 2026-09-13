# Agent Communication Protocol Optimization

## Executive Summary
Crew v2 uses fire-and-forget `message_agent()` with no ordering guarantees, duplicate detection, priority queuing, or backpressure — causing race conditions, lost messages, and unbounded token costs. Industry best practices (2025-2026) converge on event-driven architecture (EDA) with hybrid sync/async patterns: synchronous request-response for tool calls within an agent, EDA for inter-agent communication. This document specifies a protocol with exactly-once semantics, priority lanes, circuit breakers, and dead letter queues, adapted from SW4RM, A2A, and production multi-agent systems.

## Key Findings

- **Event-Driven Architecture (EDA) is the consensus for multi-agent systems** [Zylos Research, 2026]. LangGraph 1.0 uses Pregel/BSP where state updates ARE events. AutoGen v0.4 rebuilt around an actor model with typed message passing. Google's A2A protocol uses Server-Sent Events for long-running tasks.
- **SW4RM Protocol (2026)** specifies a central Scheduler with priority-based task ordering (-19 to 20), three communication classes (PRIVILEGED, STANDARD, BULK), and explicit lifecycle management with idempotency tokens and deduplication windows [SW4RM, 2026].
- **A2A Protocol (Google, 2025)** distinguishes `tasks/send` (sync quick calls) from `tasks/sendSubscribe` (long-running via SSE) from webhooks (fully async). Tasks are addressable, resumable, and have observable state machines [Oracle, 2025].
- **Hybrid pattern**: Synchronous request-response at edges (user-facing API, tool calls within an agent), event-driven internally (agent-to-agent, cross-system, long-running workflows) [Zylos Research, 2026; Oracle, 2025].
- **Backpressure strategies**: Queue depth monitoring, semaphore-based concurrency limits, token bucket rate limiting, reactive actor model (agents that can't keep up don't acknowledge) [Zylos Research, 2026].
- **Idempotency**: At-least-once delivery requires idempotent handling. Azure Service Bus deduplicates by ID within a configurable window. Event sourcing provides natural idempotency: events recorded before execution, replay reconstructs state [Zylos Research, 2026].
- **Dead Letter Queues (DLQ)**: Isolate failures without blocking the workload. ML-based automated DLQ triage classifies failure types and routes to remediation workflows [Zylos Research, 2026].

## Detailed Analysis

### Current Failure Modes in Crew v2

1. **No ordering guarantee**: Messages arrive out of order. Engineer receives tester verdict before RED log.
2. **No duplicate detection**: Same task dispatched twice → duplicate work.
3. **No priority**: Critical tester verdict competes with routine researcher updates.
4. **No backpressure**: 81 agents can flood a single agent with messages.
5. **No dead letter queue**: Failed messages are lost, not quarantined.
6. **No retry with backoff**: Transient failures cause permanent message loss.

### Protocol Specification

**Message Schema (adapted from SW4RM + Agentplace):**

```python
class AgentMessage:
    # Identity
    message_id: str          # UUID v4, unique per message
    correlation_id: str      # Links request-response pairs
    idempotency_token: str   # {producer_id}:{operation_type}:{hash}
    
    # Routing
    from_agent: str
    to_agent: str | list[str] | "*"  # broadcast
    message_type: str        # "request", "response", "event", "task"
    
    # Content
    payload: dict
    content_type: str        # "application/json"
    
    # Delivery control
    priority: int            # -19 (CRITICAL) to 20 (BULK), default 0
    ttl_ms: int              # Time-to-live in milliseconds
    requires_ack: bool       # Whether acknowledgment is required
    
    # Metadata
    timestamp: datetime
    version: str             # Protocol version
    task_id: str             # Associated task
    metadata: dict           # Extension fields
```

**Priority Levels (SW4RM adaptation):**

| Priority | Class | Use Case | Lane |
|----------|-------|----------|------|
| -19 to -10 | CRITICAL | System failures, kill switches, security breaches | Immediate |
| -9 to 0 | HIGH | Tester verdicts, critic reviews, blocking issues | Expedited |
| 1 to 10 | NORMAL | Standard task messages, progress updates | Standard |
| 11 to 20 | LOW | Background sync, logging, non-urgent notifications | Bulk |

**Communication Classes:**

| Class | Rate Limit | Burst | Use Case |
|-------|------------|-------|----------|
| PRIVILEGED | 100 req/s | 200 | System-critical, kill switches, security |
| STANDARD | 50 req/s | 100 | Default agent-to-agent |
| BULK | 20 req/s | 40 | Background, logging, non-urgent |

### Delivery Patterns

**Pattern 1: Request-Response (synchronous, for tool calls):**
```
Agent A → request(message_id, correlation_id, payload)
Agent B → process → response(correlation_id, result)
Agent A waits with timeout (default 5s, max 30s)
```

**Pattern 2: Fire-and-Forget (async, for events):**
```
Agent A → event(message_id, payload)
No response expected. Message logged to event bus.
```

**Pattern 3: Task Delegation (async with state machine):**
```
Agent A → task_submit(task_id, payload)
Agent B → task_update(task_id, state="working")
Agent B → task_update(state="completed", result=...)
Task is addressable and resumable.
```

**Pattern 4: Pub-Sub (broadcast):**
```
Agent A → publish(topic="tester.verdict", payload)
All agents subscribed to topic receive message.
Topics: tester.verdict, critic.review, engineer.done, etc.
```

### Duplicate Detection and Idempotency

**Idempotency token format:** `{producer_id}:{operation_type}:{deterministic_hash}`

Example: `tester:verdict:task-42` — only one verdict per task from tester.

**Deduplication window:** 3600 seconds (configurable per operation type).

**Implementation:**
```python
class IdempotentHandler:
    def __init__(self, dedup_window_s=3600):
        self.processed = {}  # token → expiry_time
    
    def handle(self, message):
        token = message.idempotency_token
        if token in self.processed:
            if time.now() < self.processed[token]:
                return  # Duplicate, ignore
        # Process message
        self.processed[token] = time.now() + self.dedup_window
```

### Backpressure and Rate Limiting

**Token bucket rate limiter per agent:**
```python
class TokenBucket:
    def __init__(self, rate_per_sec, burst):
        self.rate = rate_per_sec
        self.burst = burst
        self.tokens = burst
        self.last_refill = time.now()
    
    def consume(self, cost=1):
        self.refill()
        if self.tokens >= cost:
            self.tokens -= cost
            return True
        return False  # Rate limited
```

**Backpressure signals:**
- `router.inbound_queue_depth{agent_id}`: current queue depth
- `router.enqueue_rejects_total{agent_id,reason}`: rejects by reason
- `agent.process_time_seconds{agent_id}`: service time per message
- `router.oldest_enqueued_age_seconds{agent_id}`: age of oldest message

**Backpressure actions:**
1. When queue depth > 80% capacity: send NACK to sender.
2. When queue depth = 100%: reject with `buffer_full` error.
3. When process time > 2x average: trigger circuit breaker (HALF_OPEN).

### Dead Letter Queue

**DLQ triggers:**
- Max retries exceeded (default 5)
- TTL expired
- Invalid message format
- Authentication/authorization failure

**DLQ processing:**
1. Message moved to DLQ with failure reason and timestamp.
2. Alert sent to operator.
3. Automated triage classifies failure type:
   - Transient (network timeout): retry with backoff.
   - Permanent (invalid format): escalate to operator.
   - Rate limit: pause sender for 60 seconds.

**DLQ schema:**
```python
class DeadLetterMessage:
    original_message: AgentMessage
    failure_reason: str
    failure_type: str  # "transient", "permanent", "rate_limit"
    retry_count: int
    first_failure: datetime
    last_failure: datetime
```

### Circuit Breaker

**States:**
- CLOSED: Normal operation. Requests pass through.
- OPEN: Failure threshold exceeded. Requests blocked.
- HALF_OPEN: Testing recovery. Limited requests allowed.

**Thresholds (adapted from Microsoft Agent Governance Toolkit, 2025):**

| Anomaly Score | Severity | Circuit Breaker |
|---------------|----------|-----------------|
| ≥ 20.0 | CRITICAL | Trips |
| ≥ 10.0 | HIGH | Trips |
| ≥ 5.0 | MEDIUM | No trip |
| ≥ 2.0 | LOW | No trip |

**Recovery:** After `recovery_timeout` (default 30s), circuit enters HALF_OPEN. If next request succeeds, close. If fails, reopen.

### Implementation Stack

| Component | Tool | Justification |
|-----------|------|---------------|
| Message bus | Redis Streams (prototype) → Kafka (production) | Redis for single-machine; Kafka for multi-machine scale |
| Message schema | Pydantic models | Type safety, validation |
| Rate limiter | Token bucket per agent | Prevents agent flood |
| DLQ | Redis list + SQLite | Durable, queryable |
| Circuit breaker | Custom (per agent state) | Adapted from Microsoft toolkit |
| Idempotency | Redis cache with TTL | Fast dedup lookup |
| Observability | MLflow tracing + custom metrics | Full trace across agents |

## Practical Recommendations

| Recommendation | Implementation | Tools | Threshold |
|----------------|----------------|-------|-----------|
| Adopt EDA internally | Event bus for agent-to-agent | Redis Streams | All inter-agent messages |
| Sync at edges | Request-response for tool calls | Direct function call | Within single agent |
| Priority lanes | 3-class system (PRIVILEGED/STANDARD/BULK) | Token bucket per class | Rate limits per class |
| Idempotency | Token-based dedup with 1h window | Redis cache | All messages |
| Backpressure | Queue depth monitoring + NACK | Metrics + alerts | 80% capacity warning |
| DLQ | Quarantine failed messages | Redis list + SQLite | Max 5 retries |
| Circuit breaker | Per-agent state machine | Custom | Trip on 3 consecutive failures |
| Exactly-once | Idempotent handler + dedup | Redis | 3600s window |

## Metrics Catalog

| Metric | Definition | How to Measure | Target | Warning |
|--------|-----------|----------------|--------|---------|
| Message delivery rate | Delivered / sent | Message log | >99.9% | <99% review bus |
| Duplicate rate | Duplicates / total | Dedup log | <0.1% | >1% review idempotency |
| Queue depth | Messages waiting | Redis LLEN | <10/agent | >50/agent backpressure |
| End-to-end latency | Send to receive | Timer | <2s NORMAL | >5s review priority |
| DLQ depth | Messages in DLQ | Redis LLEN | 0 | >0 alert operator |
| Circuit breaker trips | Breaker state changes | Counter | 0/week | >3/week review |
| Backpressure events | NACKs sent | Counter | 0 | >10/hour review load |
| Retry rate | Retries / total | Counter | <5% | >20% review reliability |

## References

1. [Zylos Research, 2026] Event-Driven Architecture for AI Agent Systems. zylos.ai/research.
2. [SW4RM, 2026] RFC: SW4RM - Interruptible, Message-Driven Agent Coordination Protocol. sw4rm.ai/protocol/spec.
3. [Oracle, 2025] The Agent Communication Matrix: When MCP, A2A, and Plain REST Each Win. blogs.oracle.com.
4. [Agentplace, 2026] Agent Communication Protocols: Building Effective Inter-Agent Messaging. agentplace.io/blog.
5. [Microsoft, 2025] Agent Governance Toolkit: Kill Switch and Rate Limiting. github.com/microsoft/agent-governance-toolkit.
6. [Microsoft, 2025] AI Agent Failure Mites: Six Failure Categories. Whitepaper.
7. [Galileo, 2025] Multi-Agent Production Deployment Analysis. 42% spec, 37% coordination, 21% verification.
8. [LangChain, 2026] State of Agent Engineering Report. 89% observability adoption.
9. [MLflow, 2026] AI Observability for Production: Multi-Agent Systems. mlflow.org/blog.
10. [Datadog, 2025] AI Gateway Best Practices: Model Routing, Reliability, Budget Controls. datadoghq.com/blog.
