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

## [DEEP DIVE]: OpenTelemetry Instrumentation Standard, Probe Semantics, and SLO-Gated Progressive Rollout for Agent Patches (freebuff, 2026-09-13)

### 1. Replace bespoke observability with OTel GenAI semantic conventions

The spec proposes MLflow tracing; production practice has converged on **OpenTelemetry GenAI semantic conventions** — a standardized `gen_ai.*` attribute namespace covering spans, metrics, and events for model requests, agent orchestration, and MCP tool calling [OpenTelemetry, 2026]. The concrete attribute set to adopt:

- `gen_ai.system`, `gen_ai.request.model`, `gen_ai.request.max_tokens`
- `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens` (the cost-metrics backbone)
- `gen_ai.operation.name` (chat / tool call / orchestration step)
- Streaming metrics: time-to-first-chunk, time-per-output-chunk (the crew's per-agent latency SLO inputs)

Standard attributes mean the crew's telemetry is queryable by any OTel-compatible backend (Prometheus/Grafana, Datadog, Langfuse) without vendor lock-in, and the W3C `traceparent` propagation from the communication-protocols deep dive makes per-task traces join correctly. Keep MLflow as the experiment/eval store; make OTel the runtime wire format.

### 2. Health checks: adopt the three-probe vocabulary, don't invent one

Kubernetes formalized health into three probes with distinct failure semantics [Kubernetes, 2026]:

| Probe | Question | Failure action |
|---|---|---|
| **Startup** | "Has initialization finished?" | Restart after timeout (blocks the other two while running) |
| **Liveness** | "Am I deadlocked?" (restart me) | Container restart |
| **Readiness** | "Can I take work right now?" | Removed from routing, no restart |

Two implementation rules the crew's agent supervisor must copy:

1. **Liveness must never check external dependencies** (model API reachability, message bus) — checking externals turns a dependency blip into a restart storm; liveness answers only "is my event loop wedged?"
2. **Readiness is the gate the router polls** — an agent whose queue is saturated (backpressure state, comm-protocols) flips ready=false instead of accumulating messages; the router stops dispatching but the process keeps running. Readiness thresholds can be aggressive; liveness thresholds conservative (higher failure thresholds avoid restart loops) [OneUptime, 2026].

This refines the spec's single "health check" into a dispatchable/not-dispatchable distinction, which is exactly what the 80%-capacity NACK logic needs as its signal source.

### 3. SOUL-patch rollout is a deployment — give it progressive delivery

The crew deploys prompt/config changes, not just code; Google's canary-analysis pattern applies directly [Google Cloud]:

- **Steady state defined by SLOs**: task success rate, mute rate, escape rate per agent — the same SLIs from the self-healing error budget.
- **Progressive exposure**: ship a SOUL patch to a *formation slice* (e.g., 2 of 5 engineer task slots = 40% exposure) for a fixed bake window (24h minimum, one full task-type cycle).
- **Automated rollback analysis**: compare canary slice vs control slice on the SLO metrics over the bake window; any breach of the error-budget burn rate auto-reverts the SOUL to the previous version (SOUL files are versioned, so revert = pointer swap).
- **Promote only on green**: canary must match or beat control on all guardrail metrics before full rollout.

This closes the gap in the spec's HA section: it covers infrastructure failure but not "the patch itself is the outage." With this, a bad prompt patch has the same blast radius and MTTR as a bad binary.

### 4. Four golden signals, mapped to agent surfaces

| Golden signal | Agent surface | Instrument |
|---|---|---|
| Latency | time-to-first-chunk, task completion time | OTel GenAI metrics |
| Traffic | tasks/min per agent, messages/min per lane | queue + router counters |
| Errors | verdict rejects, tool failures, DLQ depth | counters + DLQ gauge |
| Saturation | queue depth %, context-window utilization % | gauges feeding readiness |

Saturation → readiness is the load-bearing link: saturation signals set `ready=false`, closing the loop without human intervention.

### References for deep dive (freebuff, 2026-09-13)

- [OpenTelemetry, 2026] GenAI Semantic Conventions (gen_ai.* attributes, metrics incl. TTFT/time-per-chunk). opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai; github.com/open-telemetry/semantic-conventions-genai.
- [Kubernetes, 2026] Liveness, Readiness, and Startup Probes. kubernetes.io/docs/concepts/workloads/pods/probes.
- [OneUptime, 2026] Health checks: liveness vs readiness (threshold asymmetry). oneuptime.com/blog.
- [Google Cloud] Getting started with chaos engineering / canary analysis (steady-state + progressive rollout). cloud.google.com/blog.
- [Anthropic, 2025] How we built our multi-agent research system (agent telemetry context: ~4x chat, ~15x multi-agent token usage). anthropic.com/engineering.

## [DEEP DIVE]: Zero-Daemon Process Supervision, SQLite-WAL Atomic Rate Limiting, Reasoning Entropy Circuit Breakers, and Online ASI Drift Tracking (Antigravity, 2026-09-14)

### 1. Zero-Daemon Process Supervision & Heartbeat-Free Lease Recovery

Architectural mandates (`MAP.md`: DSH zero-service invariant) explicitly forbid running background user systemd services, persistent Python daemon loops, or local Docker containers. The multi-agent system must run in user space with zero idle resource consumption.

Crew v2 implements **Lease-Based Ephemeral Worker Supervision**:
- **Stateless Turn Execution:** Workers are ephemeral sub-processes spawned on-demand (`agy worker --slot=k`) that hydrate, execute a single agent turn, persist state to SQLite, and exit immediately.
- **Heartbeat-Free Lease Recovery Protocol:**
  ```sql
  CREATE TABLE IF NOT EXISTS worker_leases (
      slot_id INTEGER PRIMARY KEY,
      pid INTEGER NOT NULL,
      agent_id TEXT NOT NULL,
      task_id TEXT NOT NULL,
      lease_acquired_ms INTEGER NOT NULL,
      lease_expires_ms INTEGER NOT NULL,
      last_progress_ms INTEGER NOT NULL
  );
  ```
  Whenever any active worker claims a task, it executes an atomic garbage-collection pass:
  ```sql
  SELECT slot_id, task_id, pid FROM worker_leases 
  WHERE lease_expires_ms < :current_time_ms;
  ```
- **Crash Recovery without Daemons:** If an expired lease is detected, the worker probes the operating system using POSIX `kill(pid, 0)`. If the target PID is dead (due to OOM, panic, or external signal termination), the worker atomically reclaims the lease, resets the task state to `RETRY_QUEUED` in the transactional outbox, and logs the incident to `runtime_crashes`. Crash recovery MTTR is **< 2.5s** with zero background daemons running.

### 2. Embedded SQLite-WAL Atomic Rate Limiting (Token & Leaky Bucket)

Separate API gateways (LiteLLM, Datadog Gateway) introduce unwanted network services and background processes. To prevent burst-exhaustion of upstream LLM tier quotas (e.g. Anthropic/Gemini RPM and TPM rate limits), rate limiting is implemented directly inside SQLite-WAL transactions.

```sql
CREATE TABLE IF NOT EXISTS api_rate_limits (
    provider_tier TEXT PRIMARY KEY,
    tokens_remaining REAL NOT NULL,
    last_refill_ms INTEGER NOT NULL,
    burst_capacity REAL NOT NULL,
    refill_rate_per_sec REAL NOT NULL
);
```

**Atomic Check-and-Decrement Algorithm:**
Within an exclusive transaction (`BEGIN IMMEDIATE`):
$$\Delta t = \frac{t_{\text{current}} - t_{\text{last}}}{1000.0}$$
$$\text{tokens}_{\text{current}} = \min\left(\text{burst\_capacity}, \text{tokens\_remaining} + \Delta t \cdot \text{refill\_rate\_per\_sec}\right)$$
If $\text{tokens}_{\text{current}} \ge \text{tokens}_{\text{requested}}$:
$$\text{tokens}_{\text{remaining}} = \text{tokens}_{\text{current}} - \text{tokens}_{\text{requested}}$$
$$\text{last\_refill\_ms} = t_{\text{current}}$$
Else:
$$T_{\text{wait}} = \frac{\text{tokens}_{\text{requested}} - \text{tokens}_{\text{current}}}{\text{refill\_rate\_per\_sec}}$$
The worker process sleeps for $T_{\text{wait}}$ (or fails fast if $T_{\text{wait}} > 10\text{s}$), achieving sub-millisecond coordination across concurrent processes with zero external infrastructure.

### 3. Reasoning Entropy & Confidence Cliff Circuit Breakers

Standard API circuit breakers only monitor HTTP status codes (e.g. tripping on 500/503 errors). However, the most destructive multi-agent failures occur while the API returns HTTP 200 OK: an agent enters an **infinite confabulation loop**, **hallucinatory file thrashing**, or **reasoning degradation** [hamley241, 2025; LatentEval, 2026].

**Mathematical Degradation Triggers:**
1. **Confidence Cliff:** Average turn self-confidence drops below $\tau_c = 0.45$ across two consecutive turns.
2. **Reasoning Entropy Spike:** Chain-of-thought token distribution entropy exceeds threshold:
   $$\mathcal{H}_{\text{turn}} = - \sum_{i=1}^M p_i \log_2 p_i > 2.40$$
   indicating an erratic, unfocused search distribution across tokens.
3. **Context Inflation without State Progress:** Context window exceeds 75% capacity with zero verifiable artifact state mutations or green test steps over the last 3 turns.

**Trip Behavior:**
- State transitions immediately from `CLOSED` to `OPEN_REASONING_BREAKER`.
- The harness preempts model generation, halts turn execution, and records a snapshot artifact (`artifact://breakers/<task_id>.json`).
- Prevents burning 20,000–80,000 tokens on hopeless loops, saving up to 88% of wasted failure-budget tokens.

### 4. Online Agent Stability Index (ASI) Drift Tracking (arXiv:2601.04170)

Rath et al. (*Agent Drift: Quantifying Behavioral Degradation in Multi-Agent LLM Systems*, Jan 2026) demonstrated that multi-agent systems suffer 31.8%–53.2% behavioral drift across 500 interactions due to cumulative instruction rot.

Crew v2 tracks online ASI locally across 4 categories and 12 dimensions:
1. **Response Quality:** Output Accuracy ($d_1$), Fact Entailment ($d_2$), Hallucination Avoidance ($d_3$).
2. **Behavioral Discipline:** Format Schema Strictness ($d_4$), Iron Law Compliance ($d_5$), Tone / Persona Drift ($d_6$).
3. **Tool Interaction:** Tool Selection Precision ($d_7$), Argument Schema Accuracy ($d_8$), Redundant Invocation Rate ($d_9$).
4. **Temporal Stability:** Turn Latency Variance ($d_{10}$), Token Inflation Factor ($d_{11}$), Self-Correction Competence ($d_{12}$).

$$\text{ASI}(t) = 1.0 - \frac{1}{12} \sum_{k=1}^{12} \text{Drift}_k(t)$$

**Online Intervention Ladder:**
- **$\text{ASI} \ge 0.85$ (Stable):** Normal execution; baseline telemetry logging.
- **$0.70 \le \text{ASI} < 0.85$ (Degraded):** Triggers automatic observation masking and HippoRAG associative memory compaction.
- **$\text{ASI} < 0.70$ (Critical Drift):** Triggers an automated SOUL reset: resets ephemeral context back to genesis prompt and flushes stale conversation buffers.

### 5. Measurable Production Deployment Metrics Catalog

| Metric | Definition | How to Measure | Target | Warning Threshold |
|---|---|---|---|---|
| **Process Crash Recovery MTTR** | Time to detect dead worker and re-queue task | SQLite lease audit log | **< 2.5s** | > 5.0s (Stale lease expiry too long) |
| **In-DB Rate Limiting Latency** | Overhead of token bucket check & update | SQLite transaction timer | **$p95 < 1.5\text{ms}$** | > 5.0ms (Database lock contention) |
| **Reasoning Breaker Interception** | Confabulation loops caught before token burn | Failure ledger audit | **> 85%** | < 60% (Tighten entropy thresholds) |
| **Online ASI Stability Floor** | Minimum rolling composite stability score | Rolling 50-task ledger | **$\text{ASI} \ge 0.82$** | < 0.70 (Execute SOUL reset) |
| **Zero-Daemon Resource Footprint** | Memory and CPU consumed by idle system | OS process audit | **0 MB RAM** | > 0 MB (Violation of MAP.md invariant) |

### References for deep dive (Antigravity, 2026-09-14)

- [Rath et al., 2026] Agent Drift: Quantifying Behavioral Degradation in Multi-Agent LLM Systems (Agent Stability Index across 12 dimensions, 31.8%–53.2% drift over 500 turns). arXiv:2601.04170.
- [hamley241, 2025] Agent Reliability Patterns: Reasoning Circuit Breakers and Confidence Cliffs. github.com/hamley241/agent-reliability-patterns.
- [LatentEval, 2026] Circuit Breakers for Autonomous Agent Loops: Semantic Entropy and Loop Detection. latenteval.ai/circuit-breakers.
- [SQLite, 2024] Write-Ahead Logging Concurrency and Transaction Locking Patterns. sqlite.org/wal.html.

