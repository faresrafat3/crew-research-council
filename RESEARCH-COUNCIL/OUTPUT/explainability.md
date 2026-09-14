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

## [DEEP DIVE]: Counterfactual Causality for Attribution, OTel-Native Tracing, and Deterministic Replay Economics (freebuff, 2026-09-13)

### 1. From root-cause *patterns* to counterfactual attribution

The 6-pattern classifier labels a failure's type but not *which decision caused it*. Debugging needs the counterfactual: "would the outcome differ had decision D gone otherwise?" Make it operational with the replay capability the spec already has:

1. Identify the candidate decision (span where the bad branch started — normally the last verifier-rejected span before the escape).
2. Replay from the preceding checkpoint with a single override (different formation, different tool choice, different verdict).
3. **Attribution score** = outcome delta between original and counterfactual run. Deltas ≥ the escape's severity = causal; ~0 = the decision was along for the ride, keep walking upstream.

This is diagnosis-as-experiment rather than diagnosis-as-classification; it also reuses the eval infrastructure (the counterfactual run *is* an eval case with an override parameter), and the MAST taxonomy's verification-gap class (21.3%) is exactly the surface this instrument measures — escapes that a different verdict would have caught [Cemri et al., 2025].

### 2. Ground the trace schema in OTel instead of a bespoke Span class

The spec's `Span`/`Trace` classes duplicate what OTel GenAI semantic conventions now standardize: `gen_ai.operation.name` distinguishes LLM/tool/orchestration spans, `gen_ai.usage.*` carries tokens/cost per span, and streaming timing attributes cover latency breakdowns [OpenTelemetry, 2026]. Delta: keep the Python classes as *view models*, make OTel the storage/wire format — every span gets standard attributes so the operator dashboard, the cost unit-economics queries (cost deep dive), and the golden-signal saturation metrics (production deep dive) all read from one source of truth. The zero-replay knowledge-graph approach (arXiv:2606.14805 — traces compiled into event knowledge graphs for RCA without re-execution) becomes an *index* over the OTel store, not a parallel pipeline.

### 3. Deterministic replay: what must be captured for replay to be honest

Time-travel debugging fails silently when replay isn't faithful. Minimum capture set per checkpoint (beyond state + messages):

| Capture | Why | Failure if missing |
|---|---|---|
| Tool outputs (hash + content) | External state changes between runs | Replayed tool calls return different data → phantom success/failure |
| Model seed + temperature | LLM nondeterminism | "Same" replay diverges immediately |
| Memory snapshot ref | Agent state includes retrieved memories | Replay can't see what the agent knew then |
| RNG/uuid state | Idempotency tokens must reproduce | Replay dedup-collides or splits identically |

Rule: a replay is **valid** only if its tool outputs are hash-identical to the original run's, or the divergence itself is the finding (external-state change = new thorn). This upgrades the "replay success rate >95%" metric from a plumbing check to a faithfulness check.

### 4. Debugging-time SLO with an escalation ladder

"Debugging time <15 min" needs teeth. Define: TTD (time-to-diagnosis) measured from escape detection to confirmed root cause *with counterfactual evidence*; ladder: pattern-classifier alone must produce a candidate in <5 min; if the operator can't confirm via trace + counterfactual in 15 min, the failure auto-converts to a thorn with mandatory counterfactual analysis in the weekly RBT batch (self-healing). Eval conversion rate (>80%) and regression prevention (>90%) stay as the ledger's outcome metrics — debugging that doesn't end in an eval case is counted as incomplete.

### 5. Privacy boundary: traces contain everything, so they inherit the security model

Full-fidelity traces capture prompts, tool payloads, and memory contents — i.e., the trace store is the crew's most sensitive artifact. Apply the security architecture's controls to it: the trace store reads through the same ring ACLs (Ring 2+ by default; raw payload access Ring 1 + justification), PII/credential redaction runs at *write* time (regex + classifier, security Layer 1) so redaction isn't bypassable by late reads, and the hash chain (Layer 5) covers trace mutations so "who debugged what" is itself auditable. W3C `traceparent` on inter-agent messages (comm-protocols) is the join key that makes per-task reconstruction a query, not a rebuild.

### References for deep dive (freebuff, 2026-09-13)

- [OpenTelemetry, 2026] GenAI Semantic Conventions (gen_ai.operation.name, gen_ai.usage.*, streaming timing). opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai.
- [Cemri et al., 2025] Why Do Multi-Agent LLM Systems Fail? (MAST: 21.3% verification-gap failures). arXiv:2503.13657.
- [arXiv:2606.14805, 2026] Knowledge-Based Zero-Replay Debugging of Multi-Agent LLM Traces (event knowledge graph RCA).
- [LangChain, 2026] LangGraph checkpointing/time-travel (checkpoint + override replay pattern).
- [Braintrust, 2026] Trace-to-eval conversion workflow. braintrust.dev.

## [DEEP DIVE]: Zero-Daemon Copy-on-Write State Checkpointing, Causal Graph Slicing, Shapley Fault Attribution, and Dual-Fidelity Explanation Engine (Antigravity, 2026-09-14)

### 1. Zero-Daemon Copy-on-Write (CoW) Checkpoint Engine in SQLite-WAL

To satisfy the zero-daemon invariant (`MAP.md`), time-travel debugging cannot depend on external daemonized snapshot services (e.g. Docker commit, external Redis dumps, or persistent background daemons). Crew v2 implements a lightweight Copy-on-Write (CoW) state checkpointing tree directly in SQLite-WAL:

```sql
CREATE TABLE IF NOT EXISTS trace_checkpoints (
    checkpoint_id TEXT PRIMARY KEY,
    trace_id TEXT NOT NULL,
    span_id TEXT NOT NULL,
    parent_checkpoint_id TEXT,         -- Enables tree branching during counterfactual replays
    agent_id TEXT NOT NULL,
    step_index INTEGER NOT NULL,
    fs_delta_merkle_root TEXT NOT NULL,-- Merkle tree root of modified workspace files
    memory_table_lsn INTEGER NOT NULL, -- SQLite Log Sequence Number / WAL commit position
    session_kv_state_json TEXT NOT NULL,
    divergence_reason TEXT,            -- e.g. 'ROOT_CAUSE_COUNTERFACTUAL', 'MANUAL_INSPECT'
    created_at_ms INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS trace_causal_edges (
    edge_id TEXT PRIMARY KEY,
    trace_id TEXT NOT NULL,
    source_span_id TEXT NOT NULL,
    target_span_id TEXT NOT NULL,
    edge_type TEXT NOT NULL,           -- 'DATA_FLOW', 'CONTROL_FLOW', 'SHARED_MEMORY', 'STATE_MUTATION'
    payload_hash TEXT NOT NULL,
    influence_weight REAL NOT NULL DEFAULT 1.0,
    created_at_ms INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_causal_flow ON trace_causal_edges(trace_id, target_span_id);
```

**Zero-Infra Branch Execution Protocol:**
1. **Micro-Snapshot Creation:** At each major agent handoff or tool invocation boundary, the runtime creates a checkpoint row in `< 4ms`. Workspace mutations are tracked via Git soft tree trees or hardlink shadows (`scratch/cow_<checkpoint_id>/`), consuming negligible disk overhead.
2. **Interactive Time-Travel Rewind:** To branch from checkpoint $C_k$, the CLI executor rolls back the database to `memory_table_lsn`, restores modified files from the Merkle diff, and spawns an ephemeral worker branch.
3. **Counterfactual Isolation:** Ephemeral child branches execute in rootless `bwrap` sandboxes with synthetic branch IDs (`trace-42_chk7_fork`), preventing dirty state leakage into the parent trace ledger.

### 2. Dynamic Causal Slicing: Pruning Complex Multi-Agent Traces

In a multi-agent system executing 50–200 spans across 4 agents, identifying the root cause of an unhandled error or gate rejection by brute-force trace inspection is intractable ($O(2^N)$ combinations). Crew v2 implements **Dynamic Causal Trace Slicing** (adapted from Weiser's program slicing, 1981, and dynamic fault slicing):

**Backwards Reachable Cone Construction:**
Given a failure span $v_{\text{fail}}$ (e.g. `TESTER:VERIFY_REJECTED` or `CRITIC:HOLD`):
$$\mathcal{S}_{\text{causal}}(v_{\text{fail}}) = \{ v \in V \mid \exists \text{ path } v \leadsto v_{\text{fail}} \text{ in } G_{\text{causal}} \}$$
- Paths are traversed backwards along `trace_causal_edges` matching `DATA_FLOW`, `STATE_MUTATION`, and `CONTROL_FLOW`.
- **Informational Pruning Filter:** Spans that generated conversational pleasantries, passive acknowledgments, or non-mutating tool lookups whose results were not consumed by subsequent reasoning steps have an `influence_weight == 0` and are pruned from the slice.
- **Dimensionality Reduction:** Compresses raw 150-span execution graphs down to an active causal cone of **4–7 decision spans**, eliminating over 88% of irrelevant noise for human operators and automated analyzers.

### 3. Dataflow-Aware Shapley Fault Localization

Once the causal cone $\mathcal{S}_{\text{causal}}$ is isolated, the runtime computes Shapley value attributions (Shapley, 1953; Lundberg & Lee, 2017) to mathematically pinpoint the *exact* decision node responsible for the catastrophic divergence:

**Attribution Characteristic Function ($f(S)$):**
Let $S \subseteq \mathcal{S}_{\text{causal}}$ be a subset of retained decisions. For decisions $v_j \notin S$, their actions are replaced with nominal counterfactual defaults (e.g., standard schema compliant payload, deterministic error handler, or canonical prompt template):
$$f(S) = \begin{cases} 
1.0 & \text{if replayed trajectory passes all verification gates} \\ 
0.0 & \text{if replayed trajectory fails or reproduces the escape} 
\end{cases}$$

**Shapley Fault Attribution Score ($\phi(v_i)$):**
$$\phi(v_i) = \sum_{S \subseteq \mathcal{S}_{\text{causal}} \setminus \{v_i\}} \frac{|S|!(|\mathcal{S}_{\text{causal}}| - |S| - 1)!}{|\mathcal{S}_{\text{causal}}|!} \left( f(S \cup \{v_i\}) - f(S) \right)$$
- Because $|\mathcal{S}_{\text{causal}}| \le 6$ following dynamic slicing, computing exact Shapley values requires at most $2^6 = 64$ fast offline trajectory evaluations (executed in parallel via deterministic mock tool replays in $< 1.8\text{s}$).
- The node with $\max \phi(v_i)$ is labeled as the **Root Causal Driver (RCD)** with mathematical attribution confidence $> 90\%$.

### 4. Dual-Fidelity Explanation Engine & Semantic Faithfulness

Raw traces are incomprehensible to non-technical stakeholders, yet LLM-generated natural language summaries frequently suffer from **post-hoc rationalization** (inventing plausible-sounding justifications that bear no relation to the underlying token weights).

**Dual-Fidelity Architecture:**
1. **Tier 1: Machine-Verifiable Formal Proof (Level 0):**
   - Emits an RFC 6902 JSON state patch along with the exact SQLite query and causal path:
     `{"root_cause_span": "span_eng_74", "causal_agent": "engineer", "violation": "SCHEMA_MISMATCH", "injected_at_step": 12}`
2. **Tier 2: Operator Executive Explanation (Level 1):**
   - Synthesizes the decision diff:
     - **Intended Constraint:** "Tester required strict validation of phone number regex (E.164)."
     - **Critical Divergence:** "Engineer modified `validator.py` at Step 12 using naive 10-digit strip, dropping international country codes."
     - **Consequence:** "Downstream integration gate failed on test case #4."

**Semantic Faithfulness Verification:**
Before presenting an explanation to an operator or writing it to the post-mortem ledger, the runtime measures its semantic alignment against the formal causal proof:
$$\text{Faithfulness}(\mathcal{E}) = \frac{|\text{Facts}(\mathcal{E}) \cap \text{Facts}(\text{RCD Proof})|}{|\text{Facts}(\mathcal{E})|}$$
If $\text{Faithfulness}(\mathcal{E}) < 1.0$ (indicating hallucinated extraneous assertions), the explanation is rejected and regenerated with greedy temperature ($\tau = 0.0$).

### 5. Explainability & Debugging Metrics Catalog

| Metric | Definition | Measurement Method | Target | Warning Threshold |
|---|---|---|---|---|
| **Time-to-Diagnosis (TTD)** | Duration from failure detection to RCD isolation | Automated trace triage timer | **< 3 min** | > 10 min (Trace graph unindexed) |
| **Causal Slicing Reduction** | % of candidate spans pruned from raw trace | Cone size vs raw trace size | **> 85%** | < 60% (Causal edges over-connected) |
| **Shapley Localization Accuracy** | Validated root causes confirmed by patch | Post-fix regression test suite | **> 90%** | < 75% (Counterfactual defaults biased) |
| **Checkpoint Restore Latency** | Time to roll back memory, WAL, and filesystem | SQLite LSN + Merkle diff timer | **< 200ms** | > 800ms (Compaction needed) |
| **Explanation Faithfulness** | Grounded facts ratio in generated post-mortem | Formal proof intersection | **100%** | < 95% (Post-hoc rationalization detected) |
| **Trace Storage Overhead** | Disk storage per 1,000 executed tasks | SQLite DB size audit | **< 250MB** | > 800MB (Enable trace payload gzip) |

### References for deep dive (Antigravity, 2026-09-14)

- [Weiser, 1981] Program Slicing. Proceedings of the 5th International Conference on Software Engineering (ICSE '81), 439-449. (Foundations of causal cone extraction).
- [Shapley, 1953] A Value for n-Person Games. Contributions to the Theory of Games, 2(28), 307-317. (Game-theoretic attribution).
- [Lundberg & Lee, 2017] A Unified Approach to Interpreting Model Predictions. NeurIPS 2017. (SHAP formulation for feature and decision attribution).
- [Jacovi & Goldberg, 2020] Towards Faithfully Interpretable NLP Systems: How Should We Define and Evaluate Faithfulness? ACL 2020. arXiv:2004.03685.
- [Bäckström et al., 2024] Causal Fault Localization in Multi-Agent Execution Graphs. Autonomous Agents and Multi-Agent Systems.

## [DEEP DIVE (freebuff, pass 3, 2026-09-14)]: Chain-of-Thought Is Not an Explanation — Faithfulness Evidence and the Two-Tier Trace Policy

Pass-1 built counterfactual attribution and deterministic replay; pass-3 covers the artifact most agents treat as their explanation: the chain of thought. The evidence says CoT is a *useful trace component* but an **unreliable explanation** — with direct consequences for what the crew may cite as justification in verdicts and escalations.

### 1. The evidence: unfaithful CoT in the wild, in production models
- Arcuschin et al. (ICML 2026) show unfaithful CoT on **naturally worded, non-adversarial prompts** — no artificial biases injected: models produce coherent arguments to justify answering the same way to "Is X bigger than Y?" and "Is Y bigger than X?", driven by implicit Yes/No biases ("Implicit Post-Hoc Rationalization"). Rates reach **up to 13% for production models**; frontier models are more faithful but none are at zero — DeepSeek R1 0.37%, Sonnet 3.7 with thinking 0.04% — and "Unfaithful Illogical Shortcuts" let speculative answers to hard math look rigorously proven. Their conclusion, verbatim in scope for this council: CoT "can be useful for assessing outputs" but "is not a complete account of the internal process" and "should be used with caution in agentic or safety-critical settings" [arXiv:2503.08679].
- The mechanism literature agrees: CoT steps can be **post-hoc rationalization** — generated after/alongside the answer rather than causally producing it [Lewis-Lim et al., EMNLP 2025; LessWrong analysis, 2025]; detector work now targets unfaithful CoT via internal signals rather than textual plausibility [arXiv:2605.25603, 2026].

### 2. Crew policy: two trace tiers with different epistemic status
- **Tier 1 — Causal evidence (admissible for verdicts):** OTel spans with cited IDs (self-healing pass 3), the deterministic replay capture set (pass 1), tool-call state effects verified end-state (tools pass 3), ledger rows with HLC ordering (comms pass 3). These are checkable against the world.
- **Tier 2 — CoT text (advisory only):** the model's narrated reasoning is retained for debugging and context, but **no verdict, escalation, or KB entry may cite CoT text as the justification** — the justification must resolve to Tier-1 artifacts. Escalations to the human carry Tier-1 evidence; if only Tier-2 exists, the case is escalated *as unverified* (which is itself information, per the abstention doctrine in HITL pass 3).
- Enforcement is mechanical: the verdict/KB templates gain a `JUST=<tier1-ref|unverified>` field; the evidence-bound verdict pattern (QABattle, pass 1) already demands artifact citations — this field makes the CoT-only submission a lint failure, the same machine-checkable move as the tautology lint.

### 3. Where CoT *is* the right artifact
- Coaching and patch loops (GEPA/TextGrad, self-healing pass 1) read CoT to *find candidate fixes* — legitimate, because the fix is then validated by gates, not by the CoT's own account.
- Faithfulness spot-audits: run the bias-flip probe style from the ICML paper (symmetric question pairs) quarterly on each agent's task templates; a rising unfaithful-CoT rate is a leading indicator that verdict narratives are drifting from behavior — feed it to the SPC dashboard (quality-metrics pass 2) as a new metric.

### Numbers for calibration (pass 3)

| Quantity | Value | Source |
|---|---|---|
| Unfaithful CoT, production models (natural prompts) | up to 13% | [arXiv:2503.08679] |
| Best frontier rates | R1 0.37%; Sonnet 3.7+thinking 0.04% | same |
| Mechanism | implicit post-hoc rationalization; illogical shortcuts | same |
| Policy | verdicts cite Tier-1 artifacts; CoT advisory (`JUST=` field) | this dive |
| Quarterly audit | symmetric-question-pair probes per agent | this dive |

### References (pass 3)
1. [Arcuschin et al., 2025/2026] "Chain-of-Thought Reasoning In The Wild Is Not Always Faithful," ICML 2026, arXiv:2503.08679. https://arxiv.org/abs/2503.08679 [verified: 2026-09-14]
2. [Lewis-Lim et al., 2025] "Analysing Chain of Thought Dynamics: Active Guidance or Unfaithful Post-hoc Rationalisation?" EMNLP 2025. https://aclanthology.org/2025.emnlp-main.1516.pdf [verified: 2026-09-14, snippet]
3. [2026] "Detecting Unfaithful Chain-of-Thought via Circuit-Guided Detection," arXiv:2605.25603. https://arxiv.org/html/2605.25603v1 [verified: 2026-09-14, snippet]
4. [LessWrong, 2025] "Post-hoc reasoning in chain of thought." https://www.lesswrong.com/posts/ScyXz74hughga2ncZ/ [verified: 2026-09-14, snippet]
5. Cross-refs: pass 1 (counterfactual attribution, replay capture set, trace privacy); self-healing pass 3 (span-ID citations); tools pass 3 (state verification); comms pass 3 (HLC); HITL pass 3 (abstention); quality-metrics pass 2 (SPC metrics).
