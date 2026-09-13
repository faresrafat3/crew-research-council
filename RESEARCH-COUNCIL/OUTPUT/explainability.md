# Explainability and Debugging for Agent Crews

## Executive Summary
Crew v2 has message history but no structured provenance — when something goes wrong, debugging requires reading hundreds of messages. Production multi-agent systems require decision provenance, replay debugging, and "why did agent X do Y" traceability. Research (2025-2026) shows debugging must shift from trace inspection to regression prevention, converting production failures into enforced quality gates. This document specifies a provenance framework with structured traces, time-travel debugging, and automated root cause analysis.

## Key Findings

- **Braintrust (2026)** captures complete traces across model calls, tool invocations, and retrieval steps in an expandable tree of nested spans. Each span shows inputs, outputs, timing, cost, and evaluation scores. One-click trace-to-eval conversion: production failure → eval case → CI gate [Braintrust, 2026].

- **NHI Mgmt Group (2026)** reports that production agent failures often look healthy in monitoring while hiding step-level execution mistakes. An agent can return a successful status code after selecting the wrong tool, fetching the wrong context, or using the wrong parameters. Debugging must capture the decision path, not just system status [NHI Mgmt Group, 2026].

- **Knowledge-Based Zero-Replay Debugging (arXiv, 2606.14805, 2026)** frames trace debugging as a knowledge-based decision-support problem. Each trace is compiled into a structured event knowledge graph over routing, enabling root-cause analysis without replay [arXiv, 2606.14805].

- **AgentOps (2026)** supports 400+ LLMs with time-travel debugging and session replay. DevOps principles applied to agentic systems: rewind and replay agent runs with point-in-time precision [Galileo, 2026].

- **LangGraph Checkpointing (2026)** enables pause/resume, time-travel debugging, and human-in-the-loop interrupts via AsyncPostgresSaver. Durable execution survives process restarts [Zylos Research, 2026].

- **Maxim AI (2026)** provides distributed tracing at session, trace, and span levels with visual replay and automated evaluation. Visual map of agent-to-agent communication for failure attribution [Maxim AI, 2026].

## Detailed Analysis

### Current Failure Modes

1. **No structured provenance**: Messages are flat, not a decision tree.
2. **No replay capability**: Can't rewind to see what agent was thinking.
3. **No root cause automation**: Operator manually reads hundreds of messages.
4. **No decision attribution**: Can't trace which agent caused a downstream failure.
5. **No eval integration**: Production failures not converted to regression tests.

### Provenance Framework

**Structured trace (adapted from Braintrust):**

```python
class Trace:
    trace_id: str
    task_id: str
    root_agent: str
    spans: list[Span]
    outcome: str
    total_tokens: int
    total_cost: float
    duration_ms: int

class Span:
    span_id: str
    parent_span_id: str | None
    agent_id: str
    span_type: str  # "llm_call", "tool_call", "message", "decision"
    inputs: dict
    outputs: dict
    timestamp: datetime
    duration_ms: int
    tokens: int
    cost: float
    evaluation_score: float | None
    metadata: dict
```

**Trace tree visualization:**
```
Trace: task-42 (FULL formation, 45s, $1.23)
├── Span: firstmate.classify (LLM, 2s, $0.01)
│   └── Output: formation=PIPELINE, complexity=moderate
├── Span: researcher.search (Tool, 5s, $0.05)
│   └── Input: query="pytest coverage"
│   └── Output: 3 sources found
├── Span: architect.design (LLM, 3s, $0.02)
│   └── Input: sources + task spec
│   └── Output: design document
├── Span: engineer.implement (LLM+Tool, 20s, $0.50)
│   └── Input: design document
│   └── Output: 4 modules, 135 lines
│   └── Span: engineer.terminal (Tool, 5s, $0.01)
│       └── Command: pytest
│       └── Output: 0 tests collected
├── Span: tester.verify (LLM, 3s, $0.02)
│   └── Input: code + test results
│   └── Output: HOLD (0 tests)
└── Span: engineer.patch (LLM+Tool, 7s, $0.30)
    └── Output: 11 tests added
```

### Decision Provenance

**"Why did agent X do Y?" traceability:**

```python
class DecisionRecord:
    decision_id: str
    agent_id: str
    task_id: str
    timestamp: datetime
    decision_type: str  # "tool_call", "verdict", "formation_choice"
    inputs: dict
    reasoning: str  # Agent's stated reasoning
    evidence: list[str]  # Supporting facts
    confidence: float
    outcome: str
    downstream_effects: list[str]  # What this decision caused
```

**Query interface:**
```python
# Why did the tester issue HOLD?
decisions.query(agent="tester", decision_type="verdict", outcome="HOLD")

# What decisions led to this escape?
decisions.trace(escape_id="esc-001")

# Which agent caused the cascade failure?
decisions.root_cause(task_id="task-42", failure_type="cascade")
```

### Time-Travel Debugging

**LangGraph checkpoint pattern:**

```python
# Save checkpoint after every agent action
checkpoint = {
    "task_id": task_id,
    "agent_id": agent_id,
    "state": current_state,
    "messages": message_history,
    "timestamp": datetime.now()
}

# Restore to any point in time
restore_checkpoint(checkpoint_id="span-42-end")

# Replay from that point with different parameters
replay_from(checkpoint_id="span-42-end", override={"model": "sonnet"})
```

**Capabilities:**
1. **Rewind**: Go back to any point in the trace.
2. **Replay**: Re-execute from that point with same or different parameters.
3. **Branch**: Explore "what if" scenarios (what if architect chose different design?).
4. **Compare**: Side-by-side comparison of two execution paths.

### Root Cause Analysis

**Automated root cause detection:**

```python
class RootCauseAnalyzer:
    def analyze(self, trace):
        # Check for known failure patterns
        if self.is_tool_misuse(trace):
            return "tool_misuse", self.get_evidence(trace)
        if self.is_context_loss(trace):
            return "context_loss", self.get_evidence(trace)
        if self.is_goal_drift(trace):
            return "goal_drift", self.get_evidence(trace)
        if self.is_retry_loop(trace):
            return "retry_loop", self.get_evidence(trace)
        if self.is_cascading_error(trace):
            return "cascading_error", self.get_evidence(trace)
        if self.is_silent_degradation(trace):
            return "silent_degradation", self.get_evidence(trace)
        return "unknown", []
```

**Failure pattern signatures:**

| Pattern | Signature | Detection |
|---------|-----------|-----------|
| Tool misuse | Wrong tool or args for task | Tool call validation |
| Context loss | Agent references info not in context | Cross-reference with message history |
| Goal drift | Actions don't match task spec | Compare task spec vs actual actions |
| Retry loop | Same action >3 times | Loop detection in trace |
| Cascading error | One failure triggers chain | Dependency graph analysis |
| Silent degradation | Quality drops without hard failure | ASI trend analysis |

### Trace-to-Eval Conversion (Braintrust Pattern)

**Workflow:**
1. **Capture**: Production failure → save full trace.
2. **Annotate**: Operator annotates failure type and root cause.
3. **Create eval**: Convert trace into evaluation case.
4. **Enforce**: Add to CI/CD regression suite.
5. **Block merge**: If eval fails, block SOUL patch.

**Eval case format:**
```python
class EvalCase:
    eval_id: str
    source_trace_id: str
    failure_type: str
    task_spec: str
    expected_outcome: str
    agents_involved: list[str]
    evaluation_prompt: str  # LLM-as-judge prompt
    threshold: float  # Minimum score to pass
```

### Operator Dashboard

**Debugging views:**

1. **Trace Tree**: Expandable tree of all agent actions (Braintrust-style).
2. **Decision Graph**: Visual graph of which agent decided what.
3. **Timeline**: Chronological view of agent interactions.
4. **Cost Breakdown**: Per-agent, per-span token cost.
5. **Evaluation Scores**: Per-span quality scores.
6. **Failure Clusters**: Group similar failures for pattern detection.

**Dashboard features:**
- Filter by agent, task, failure type, date range.
- Search by keyword in inputs/outputs.
- Side-by-side comparison of two traces.
- Export trace for offline analysis.

## Practical Recommendations

| Recommendation | Implementation | Tools | Threshold |
|----------------|----------------|-------|-----------|
| Structured traces | Nested span tree | Braintrust-style | All tasks |
| Decision provenance | Per-decision record | Custom | All decisions |
| Time-travel debugging | Checkpoint after every action | LangGraph-style | All agents |
| Root cause automation | 6-pattern detection | Custom | All failures |
| Trace-to-eval conversion | Production failure → eval case | Braintrust-style | All failures |
| Operator dashboard | Trace tree + decision graph | React + WebSocket | Real-time |
| Failure clustering | Group similar failures | Embedding similarity | Weekly |

## Metrics Catalog

| Metric | Definition | How to Measure | Target | Warning |
|--------|-----------|----------------|--------|---------|
| Trace coverage | Tasks with full traces / total | Counter | 100% | <100% fix instrumentation |
| Debugging time | Time to root cause | Timer | <15 min | >1 hour improve traces |
| Root cause accuracy | Correct root cause / total | Log review | >85% | <70% improve detection |
| Eval conversion rate | Failures converted to evals / total | Counter | >80% | <50% improve workflow |
| Regression prevention | Caught in CI / total regressions | Counter | >90% | <70% improve evals |
| Replay success rate | Successful replays / total | Counter | >95% | <90% fix checkpointing |

## References

1. [Braintrust, 2026] 7 Best Tools for Debugging AI Agents. braintrust.dev.
2. [NHI Mgmt Group, 2026] AI Agent Debugging Tools Expose the Gap. nhimg.org.
3. [arXiv, 2606.14805, 2026] Knowledge-Based Zero-Replay Debugging of Multi-Agent LLM Traces.
4. [Galileo, 2026] 8 Best AI Agent Debugging & Root Cause Analysis Tools. galileo.ai.
5. [Maxim AI, 2026] Agent Tracing for Debugging Multi-Agent AI Systems. getmaxim.ai.
6. [Zylos Research, 2026] Event-Driven Architecture for AI Agent Systems. zylos.ai.
7. [LangChain, 2026] LangGraph Checkpointing and Time-Travel Debugging.
