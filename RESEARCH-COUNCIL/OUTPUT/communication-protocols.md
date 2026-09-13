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

## [DEEP DIVE]: Standards Alignment (A2A, MCP), Delivery-Semantics Correction, Ordering Keys, Jittered Retries, and Trace Propagation (freebuff, 2026-09-13)

### 1. Adopt A2A's task lifecycle as the standard state vocabulary

The A2A specification defines tasks as addressable, resumable objects that progress through an explicit lifecycle: **submitted → working → input-required / auth-required → completed / failed / canceled**, with completed/failed/canceled as terminal states, over JSON-RPC with SSE streaming and web-hook push notifications for long-running work [A2A, 2025]. The crew's Pattern-3 "task delegation" schema should adopt these exact state names and the terminal-state rule:

- Every task message MUST reach a terminal state within its `ttl_ms`; a task still in `working` at TTL expiry is moved to DLQ as `failed` (closes the "lost task" hole in the current spec, where only messages fail — tasks could linger forever).
- `input-required` gives tester HOLD and clarifying questions a first-class state instead of overloading responses.
- Agents already running `message_agent()` can keep the transport and adopt only the state machine — the vocabulary is implementable in the existing Pydantic schema as a `task_state` field.

### 2. Delivery semantics: drop "exactly-once", implement "effectively-once"

Correction to the original spec's "Exactly-once" claim. Kafka's exactly-once semantics are a per-partition guarantee built from an **idempotent producer** (broker de-duplicates retried produces using a producer ID + per-partition sequence number) plus **transactions** for atomic multi-partition writes; end-to-end EOS still requires the consumer side to be idempotent, and ordering is guaranteed **only within a partition** [Confluent, 2017; AutoMQ, 2025; Strimzi, 2023]. The honest wording for Crew v2:

- Delivery is **at-least-once** (retries guarantee it).
- Processing is **effectively-once** via the idempotency-token handler — which the spec already specifies, and which is the same mechanism Kafka itself relies on downstream.
- Implementation detail from Kafka practice: idempotence/sequence tracking is per-connection and per-partition — a handler restart must re-load the dedup table (the Redis dedup cache with TTL is the right store; a purely in-memory dict loses dedup state exactly when duplicates are most likely) [AutoMQ, 2025].

### 3. Ordering: partition by task, never promise global order

Per-partition ordering [Confluent, 2017] translates to: order is guaranteed **per task_id (or correlation_id), zero guarantees across tasks**. Practical rules for the router:

1. Key the stream partition on `task_id` — all RED/GREEN/DONE/HOLD messages for one task are consumed in order.
2. Within a task, a tester verdict arriving before the RED log it references becomes structurally impossible — the exact COORD failure mode.
3. Do not add global sequence numbers or a global serial queue to "fix" cross-task order; it serializes the whole crew for no correctness benefit (tasks are independent by design).

### 4. Retries: full jitter with a cap, not bare exponential backoff

AWS's canonical guidance: with plain exponential backoff, simultaneous failures retry in lockstep and stampede the recovering agent; **full jitter** (`sleep = random_between(0, min(cap, base * 2 ** attempt))`) cuts total completion time with less total work than fixed or equal jitter; **decorrelated jitter** (`sleep = min(cap, random_between(base, prev * 3))`) is preferred when individual callers must make progress quickly [AWS, 2015]. Concretely for the crew:

| Parameter | Value | Rationale |
|---|---|---|
| base delay | 100ms | Sub-second roundtrips for agent-to-agent |
| cap | 20s | Keeps 5-retry worst case ≤ ~40s total |
| retries | 5 | Matches existing DLQ trigger |
| jitter | full (default) | Prevents synchronized retry storms after a circuit breaker closes |
| decorrelated | tester/critic lanes | Verification agents should not wait behind long random delays |

Jitter applies to the *agent retrying a busy peer* and to *circuit-breaker HALF_OPEN probes* — the probe schedule should itself be jittered so 81 agents don't all probe the same recovered agent in the same millisecond.

### 5. Wire-level standards: borrow, don't invent

- **A2A** for inter-crew / external agent interop (JSON-RPC, SSE for streaming, push for long tasks, per-task auth states) [A2A, 2025].
- **MCP Streamable HTTP** (spec 2025-03-26, superseding the deprecated HTTP+SSE transport) for tool sessions: single-endpoint POST, optional SSE streaming responses, explicit session header for resumability, OAuth 2.1 authorization [MCP, 2025]. When Crew v2 exposes tools to outside agents, expose them as MCP servers rather than a bespoke HTTP API.
- Inside the crew, Redis Streams remains correct — the point is that the *schemas and states* are standard so nothing is crew-locked.

### 6. Trace propagation: make every message traceable by default

The W3C Trace Context specification defines the `traceparent` header format (`00-<32-hex trace-id>-<16-hex span-id>-<2-hex flags>`) and `tracestate` for vendor extensions, enabling end-to-end distributed tracing; OpenTelemetry implements it as its default propagator [W3C, 2022; OpenTelemetry, 2026]. The spec's `metadata` dict should carry `traceparent` on every message, with the router validating the format and rejecting (to DLQ) malformed trace IDs. This makes the explainability stack (OUTPUT/explainability.md) a free side effect: task timelines reconstruct from trace-id grouping without a separate provenance pipeline.

### 7. Communication failures are the measured #1 class — size the DLQ and metrics accordingly

The MAST taxonomy (why multi-agent LLM systems fail) analyzed 150+ traces across 7 frameworks and found **41.8% specification issues, 36.9% inter-agent misalignment, 21.3% task verification** failures [Cemri et al., 2025] — matching the 42/37/21 split already cited from Galileo, now anchored to the primary source. Inter-agent misalignment (information asymmetry, invalid/incorrect acts, misaligned or ignorable instructions, transaction failures) is precisely the message-flow surface this protocol governs. Consequences:

1. Budget the DLQ for ~1/3 of failure volume being coordination-type, not transport-type — triage must classify "message delivered but wrong/ignored" not just "message lost."
2. Track the MAST-named metrics: ignorable-instruction rate (messages never acked) and information-asymmetry events (consumer missing context the producer had) as first-class counters, alongside delivery rate.
3. Token economics reinforce priority lanes: agents use ~4x chat tokens and multi-agent systems ~15x [Anthropic, 2025] — BULK-lane discipline (background sync, non-urgent notifications at reduced rate) is the single cheapest lever on that multiplier.

### References for deep dive

- [A2A, 2025] Agent2Agent (A2A) Protocol Specification. github.com/a2aproject/A2A/blob/main/docs/specification.md.
- [MCP, 2025] Model Context Protocol Specification 2025-03-26: Transports (Streamable HTTP, OAuth 2.1, sessions). modelcontextprotocol.io/specification/2025-03-26/basic/transports.
- [Confluent, 2017] Exactly-Once Semantics Are Possible: Here's How Apache Kafka Does It. confluent.io/blog.
- [AutoMQ, 2025] Kafka Exactly-Once Semantics Implementation: Idempotence and Transactional Messages. automq.com/blog.
- [Strimzi, 2023] Exactly-once semantics with Kafka transactions. strimzi.io/blog.
- [AWS, 2015] Exponential Backoff and Jitter. aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter.
- [W3C, 2022] Trace Context — W3C Recommendation. w3.org/TR/trace-context.
- [OpenTelemetry, 2026] Context Propagation. opentelemetry.io/docs/concepts/context-propagation.
- [Cemri et al., 2025] Why Do Multi-Agent LLM Systems Fail? (MAST taxonomy, 150+ traces, 7 frameworks). arXiv:2503.13657.
- [Anthropic, 2025] How we built our multi-agent research system. anthropic.com/engineering/multi-agent-research-system.
