# Production Deployment and Monitoring

## Executive Summary
Crew v2 runs on a single machine with no high availability, monitoring, or cost tracking — a single point of failure with no observability into agent behavior or system health. Production multi-agent systems require health checks, circuit breakers, rate limiting, cost monitoring, and agent drift detection. This document specifies a deployment architecture with MLflow-based observability, Datadog-style AI gateway controls, and the Agent Stability Index (ASI) for drift monitoring, adapted from production patterns at Google, Microsoft, and Datadog (2025-2026).

## Key Findings

- **Agent Drift** [arXiv, 2601.04170, 2026] is quantified via the Agent Stability Index (ASI) across 12 dimensions. Financial analysis shows 53.2% drift by 500 interactions; compliance 39.7%; enterprise automation 31.8%. Combined monitoring increases overhead 23% but extends completion time only 9%.
- **MLflow** [2026] provides out-of-the-box multi-agent tracing: `mlflow.<framework>.autolog()` instruments every agent step, tool call, and delegation decision. Full trace gives the "story" that individual input/output monitoring misses.
- **AI Gateway** [Datadog, 2025] centralizes cost controls: virtual keys per team/agent with spend ceilings, model routing with fallback, circuit breakers for provider failures. Budget enforcement is a config update, not a coordinated deployment.
- **Microsoft Agent Governance Toolkit** [2025] implements ring-based security: Ring 0 (Root, 100 req/s), Ring 1 (Privileged, 50 req/s), Ring 2 (Standard, 20 req/s), Ring 3 (Sandbox, 10 req/s). Breach detection auto-trips circuit breakers.
- **Reasoning Circuit Breakers** [hamley241/agent-reliability-patterns, 2025] detect confidence degradation before token waste: trip below 50% average confidence, at 80% context usage, with 30s recovery timeout.
- **Context overflow** [Factory AI, 2026] is gradual: tool outputs accumulate across dozens of steps until a single large response tips the model. Agents lose coherent access to original objectives by ~60% context mark without active compaction.
- **Six agent failure categories** [Microsoft, 2025]: tool misuse, context loss, goal drift, retry loops, cascading errors, silent quality degradation.

## Detailed Analysis

### Current Failure Modes

1. **No high availability**: Single machine failure = total crew failure.
2. **No health checks**: Operator doesn't know an agent is down until task fails.
3. **No cost tracking**: No per-agent, per-task, or per-token cost visibility.
4. **No drift detection**: Agent quality degrades silently over time.
5. **No circuit breakers**: One failing agent can cascade to entire crew.
6. **No rate limiting**: LLM API rate limits cause silent failures.

### Deployment Architecture

**Three-tier architecture:**

```
┌─────────────────────────────────────────────────────────┐
│  TIER 1: API GATEWAY / LOAD BALANCER                    │
│  - Rate limiting (token bucket per agent)               │
│  - Authentication (API keys per agent)                  │
│  - Request routing (model fallback)                     │
│  - Cost tracking (tokens per request)                   │
├─────────────────────────────────────────────────────────┤
│  TIER 2: AGENT ORCHESTRATOR                             │
│  - Health checks (per-agent heartbeat)                  │
│  - Circuit breakers (per-agent state machine)           │
│  - Task queue (priority-based)                          │
│  - Graceful degradation (5-level model)                 │
├─────────────────────────────────────────────────────────┤
│  TIER 3: AGENT POOL                                     │
│  - Agent instances (stateless, recoverable)             │
│  - Memory store (Redis/SQLite)                          │
│  - Tool execution sandbox (per-agent isolation)         │
│  - Observability (MLflow tracing)                       │
└─────────────────────────────────────────────────────────┘
```

### Health Checks

**Per-agent health check protocol:**

| Check | Frequency | Failure Threshold | Action |
|-------|-----------|-------------------|--------|
| Heartbeat | 30s | 3 consecutive misses | Mark agent unhealthy |
| Response time | Every request | >2x rolling average | Trigger circuit breaker |
| Error rate | Rolling 5min window | >10% errors | Mark agent unhealthy |
| Token usage | Per task | >150% budget | Alert operator |
| Memory usage | Per task | >90% context | Trigger compaction |

**Health check endpoint (per agent):**
```python
class AgentHealth:
    agent_id: str
    status: str  # "healthy", "degraded", "unhealthy"
    last_heartbeat: datetime
    tasks_completed: int
    tasks_failed: int
    avg_response_time_ms: float
    token_usage_24h: int
    error_rate_5min: float
    circuit_breaker_state: str  # "closed", "open", "half_open"
```

### Circuit Breakers

**Per-agent circuit breaker (adapted from Microsoft + hamley241):**

| State | Trigger | Behavior |
|-------|---------|----------|
| CLOSED | Normal confidence | All tasks accepted |
| OPEN | Confidence < 50% OR context > 80% OR 3 consecutive failures | Tasks rejected, agent marked unhealthy |
| HALF_OPEN | After 30s recovery timeout | Limited tasks (1 at a time) for testing |

**Anomaly score thresholds (Microsoft Agent Governance Toolkit):**

| Score | Severity | Circuit Breaker |
|-------|----------|-----------------|
| ≥ 20.0 | CRITICAL | Trips immediately |
| ≥ 10.0 | HIGH | Trips after 2 consecutive |
| ≥ 5.0 | MEDIUM | Logs warning |
| ≥ 2.0 | LOW | No action |

### Rate Limiting

**Token bucket per agent (Datadog AI Gateway pattern):**

| Ring | Rate (req/s) | Burst | Use Case |
|------|--------------|-------|----------|
| 0 (Root) | 100 | 200 | Infrastructure, system agents |
| 1 (Privileged) | 50 | 100 | High-trust agents (firstmate, coach) |
| 2 (Standard) | 20 | 40 | Default for most agents |
| 3 (Sandbox) | 10 | 20 | New/untested agents |

**Backpressure signals:**
- Queue depth > 80% capacity: NACK to sender.
- Queue depth = 100%: reject with `buffer_full`.
- Process time > 2x average: enter HALF_OPEN.

### Cost Monitoring

**Cost tracking dimensions (Datadog pattern):**

| Dimension | Granularity | Alert Threshold |
|-----------|-------------|-----------------|
| Per-agent | Per task | >150% of agent's avg |
| Per-task | Per task | >200% of task's budget |
| Per-model | Per hour | >$X (operator-defined) |
| Per-crew | Per day | >$Y (operator-defined) |

**Virtual keys (Datadog AI Gateway):**
- Each agent gets a unique API key with spend ceiling.
- Budget enforcement at gateway level.
- Model fallback: if primary model throttled, retry with next-best.

**Cost optimization strategies:**
1. **Model tiering**: Cheap model (GPT-3.5) for simple tasks, expensive (GPT-4) for complex.
2. **Caching**: Cache identical prompts for 1 hour.
3. **Early stopping**: Stop generation if confidence > 0.95.
4. **Context compaction**: Reduce prompt size at 70% context usage.

### Agent Drift Monitoring

**Agent Stability Index (ASI) — 12 dimensions [arXiv, 2601.04170]:**

| Dimension | Metric | Warning | Critical |
|-----------|--------|---------|----------|
| Response consistency | Output quality variance | >20% | >40% |
| Tool usage patterns | Deviation from baseline | >30% | >60% |
| Reasoning pathway | Steps variance | >25% | >50% |
| Inter-agent agreement | Consensus rate | <70% | <50% |
| Token efficiency | Tokens/task | >50% | >100% |
| Latency | Time to completion | >50% | >100% |
| Error rate | Errors/task | >10% | >20% |
| Escape rate | Bugs/task | >5% | >10% |
| Appeal rate | Appeals/HOLD | >10% | >20% |
| Memory utilization | Entries/task | >100% | >200% |
| Personality drift | Voice deviation | >30% | >60% |
| Goal alignment | Spec vs outcome | <80% | <60% |

**Drift detection frequency:**
- Per task: lightweight checks (token usage, latency, error rate).
- Daily: medium checks (tool usage, reasoning pathway, agreement rate).
- Weekly: full ASI computation across all 12 dimensions.

**Drift response:**
- ASI < 2.0: Normal operation.
- ASI 2.0-5.0: Log warning, increase monitoring frequency.
- ASI > 5.0: Trigger investigation, propose recalibration.
- ASI > 10.0: Pause agent, escalate to operator.

### Observability with MLflow

**Instrumentation:**
```python
import mlflow
mlflow.crewai.autolog()  # or mlflow.langchain.autolog()

# All agent steps, tool calls, and delegation decisions are traced.
```

**Key metrics to track:**
- `agent.tasks_completed{agent_id}`: Counter of successful tasks.
- `agent.tasks_failed{agent_id}`: Counter of failed tasks.
- `agent.token_usage{agent_id, model}`: Token consumption.
- `agent.latency_seconds{agent_id}`: Task completion time.
- `agent.error_rate{agent_id}`: Rolling error rate.
- `agent.drift_score{agent_id}`: ASI composite.

**Alerting rules:**
- Error rate > 10% over 5 minutes: PagerDuty alert.
- Token usage > 150% of daily budget: Slack alert.
- Drift score > 5.0: Email operator.
- Circuit breaker trips > 3/week: Investigation required.

### High Availability

**Single-machine HA (immediate):**
- Process supervisor (systemd) auto-restarts crashed agents.
- Health check endpoint monitored every 30s.
- Circuit breaker prevents cascade failures.

**Multi-machine HA (future):**
- Stateless agents: any instance can handle any task.
- Shared state: Redis for message bus, PostgreSQL for ledger.
- Load balancer: round-robin with health checks.
- Failover: if machine A fails, machine B takes over tasks.

## Practical Recommendations

| Recommendation | Implementation | Tools | Threshold |
|----------------|----------------|-------|-----------|
| Health checks | Per-agent heartbeat + response time | Custom endpoint | 30s interval |
| Circuit breakers | Per-agent state machine | Custom | Trip on 3 consecutive failures |
| Rate limiting | Token bucket per agent | Custom | Ring-based (10-100 req/s) |
| Cost tracking | Per-agent, per-task, per-model | Datadog-style gateway | Virtual keys with ceilings |
| Drift detection | ASI across 12 dimensions | Weekly batch | ASI > 5.0 warning |
| Observability | MLflow tracing + custom metrics | MLflow + Grafana | Full trace per task |
| Graceful degradation | 5-level model | Token budget monitor | 70/85/95/99% thresholds |
| HA (immediate) | Process supervisor + health checks | systemd + custom | Auto-restart on crash |
| HA (future) | Stateless agents + shared state | Redis + PostgreSQL | Multi-machine failover |

## Metrics Catalog

| Metric | Definition | How to Measure | Target | Warning |
|--------|-----------|----------------|--------|---------|
| Agent uptime | Healthy time / total time | Health check log | >99.9% | <99% investigate |
| Task success rate | Completed / total | Ledger | >95% | <90% investigate |
| Mean time to detect | Failure to detection | Timestamp diff | <5 min | >30 min review |
| Mean time to recover | Detection to recovery | Timestamp diff | <15 min | >1 hour review |
| Token cost per task | Tokens used / task | Counter | <$X | >$1.5X review |
| Drift score (ASI) | Composite drift | 12-dimension | <2.0 | >5.0 investigate |
| Circuit breaker trips | State changes to OPEN | Counter | 0/week | >3/week review |
| Rate limit hits | Rejected requests | Counter | 0 | >10/hour review |
| Context overflow rate | Tasks hitting limit | Counter | <1% | >5% compact earlier |

## References

1. [arXiv, 2601.04170, 2026] Agent Drift: Quantifying Behavioral Degradation in Multi-Agent LLM Systems.
2. [MLflow, 2026] AI Observability for Production: Multi-Agent Systems. mlflow.org/blog.
3. [Datadog, 2025] AI Gateway Best Practices: Model Routing, Reliability, Budget Controls. datadoghq.com/blog.
4. [Microsoft, 2025] Agent Governance Toolkit: Kill Switch and Rate Limiting. github.com/microsoft/agent-governance-toolkit.
5. [hamley241, 2025] Agent Reliability Patterns: Circuit Breakers for Reasoning Failures. github.com/hamley241/agent-reliability-patterns.
6. [Factory AI, 2026] Long-Running Session Context Overflow Research.
7. [Microsoft, 2025] AI Agent Failure Modes: Six Failure Categories. Whitepaper.
8. [LangChain, 2026] State of Agent Engineering Report. 89% observability adoption.
9. [Google, 2025] A2A Protocol: Agent-to-Agent Communication.
10. [Confluent, 2025] Four Canonical Multi-Agent Patterns on Pub/Sub.
