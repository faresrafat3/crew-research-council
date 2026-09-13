# Self-Healing and Self-Improvement Mechanisms

## Executive Summary
Crew v2 has coach and historian agents but no systematic self-improvement loop — escapes are tracked but not automatically converted to patches, and failures repeat across tasks. State-of-the-art self-healing systems (VIGIL 2025, ROAD 2025, Goal-Oriented Reliability 2025) use reflective runtimes that ingest behavioral logs, diagnose failures via structured protocols (Roses/Buds/Thorns), and propose prompt/code adaptations under guardrails. This document specifies a self-healing loop for Crew v2 with automated root cause analysis, self-patching with human approval, and graceful degradation patterns.

## Key Findings

- **VIGIL (2025)** is a reflective runtime that supervises a sibling agent: ingests behavioral logs, converts events into structured emotions (EmoBank with decay), derives Roses/Buds/Thorns (RBT) diagnosis, and generates prompt/code adaptations under guardrails. Achieves meta-procedural self-repair without source code inspection [VIGIL, 2025].
- **ROAD (2025)** treats optimization as dynamic debugging: an Analyzer performs root-cause analysis, an Optimizer aggregates patterns, and a Coach integrates strategies into Decision Tree Protocols. Achieves 5.6% success rate increase and 3.8% accuracy boost in 3 automated iterations [ROAD, 2025].
- **Goal-Oriented Reliability (ACM 2025)** introduces three components: Goal Decomposition Engine (verifiable sub-goals), Runtime Reliability Monitor (detects goal-level degradation), and Self-Improvement Loop (analyzes traces, proposes policy updates) [ACM, 2025].
- **Six failure categories unique to agents** [Microsoft, 2025]: tool misuse, context loss, goal drift, retry loops, cascading errors, silent quality degradation.
- **Multi-agent failure distribution** [Galileo, 2025]: specification failures 42%, coordination breakdowns 37%, verification gaps 21%.
- **Agent drift** [arXiv, 2601.04170, 2026]: quantified via Agent Stability Index (ASI) across 12 dimensions. Financial analysis shows 53.2% drift by 500 interactions. Combined monitoring increases overhead 23% but extends completion time only 9%.
- **Graceful degradation** [Zylos Research, 2026]: 5-level degradation model: FULL → SIMPLIFIED → CACHED → MINIMAL → REJECT. Pre-flight token estimation prevents context overflow.

## Detailed Analysis

### Current Failure Mode

Crew v2's self-improvement gap:
1. **No automated root cause analysis**: When a task fails, the operator manually reads logs.
2. **No self-patching**: Escapes are logged but not converted to SOUL patches.
3. **No regression testing for agent behavior**: Bugs recur because agent behavior isn't regression-tested.
4. **No graceful degradation**: When an agent fails, the task fails entirely.
5. **No drift detection**: Agent personality and performance degrade silently.

### Self-Healing Architecture

**Three-layer reflective runtime (adapted from VIGIL + ROAD):**

```
┌─────────────────────────────────────────────────────────┐
│  LAYER 1: INGESTION                                     │
│  - Behavioral logs from all agents                      │
│  - Task outcomes (success/failure, token usage, time)   │
│  - Message traces and verdicts                          │
├─────────────────────────────────────────────────────────┤
│  LAYER 2: DIAGNOSIS                                     │
│  - RBT (Roses/Buds/Thorns) analysis                    │
│  - Root cause classification (6 categories)             │
│  - Drift detection (ASI across 12 dimensions)           │
├─────────────────────────────────────────────────────────┤
│  LAYER 3: ADAPTATION                                    │
│  - Prompt update proposals (with human approval)        │
│  - SOUL patch proposals (with human approval)           │
│  - Formation adjustment proposals                       │
│  - Graceful degradation activation                      │
└─────────────────────────────────────────────────────────┘
```

### Ingestion Layer

**Data sources:**
1. **Behavioral logs**: Every agent message, tool call, and verdict.
2. **Task outcomes**: Success/failure, token usage, duration, escape count.
3. **Message traces**: Full inter-agent communication log.
4. **Verdict history**: Tester verdicts, critic reviews, appeals.

**Log format (adapted from VIGIL's EmoBank):**
```python
class BehaviorEvent:
    timestamp: datetime
    agent_id: str
    task_id: str
    event_type: str  # "message", "tool_call", "verdict", "error"
    payload: dict
    outcome: str     # "success", "failure", "timeout"
    emotion: str     # "rose" (win), "bud" (opportunity), "thorn" (failure)
    importance: float  # 0.0-1.0, decay over time
```

**Emotional Bank (EmoBank):**
- Stores behavior events with decay policy: importance *= 0.95 per day.
- Events with importance < 0.1 are pruned weekly.
- Max 1000 events per agent (FIFO eviction).

### Diagnosis Layer

**RBT Diagnosis (Roses/Buds/Thorns):**

| Category | Definition | Action |
|----------|------------|--------|
| **Roses** | Stable wins: patterns that consistently succeed | Reinforce, document as best practice |
| **Buds** | Emerging opportunities: patterns with potential | Monitor, test in safe context |
| **Thorns** | Systematic failures: patterns that consistently fail | Root cause analysis, propose patch |

**Root cause classification (6 categories from Microsoft, 2025):**

| # | Category | Symptoms | Detection |
|---|----------|----------|-----------|
| 1 | Tool misuse | Wrong tool, wrong args, missing args | Tool call validation |
| 2 | Context loss | Agent forgets earlier decisions | Cross-reference with memory |
| 3 | Goal drift | Agent pursues different objective | Compare task spec vs actions |
| 4 | Retry loops | Same action repeated >3 times | Loop detection in message log |
| 5 | Cascading errors | One failure triggers chain | Dependency graph analysis |
| 6 | Silent degradation | Quality drops without hard failure | ASI trend analysis |

**Agent Stability Index (ASI) — 12 dimensions:**

| Dimension | Metric | Warning Threshold |
|-----------|--------|-------------------|
| Response consistency | Variance in output quality | >20% increase |
| Tool usage patterns | Deviation from established patterns | >30% change |
| Reasoning pathway stability | Variance in reasoning steps | >25% increase |
| Inter-agent agreement rate | Consensus on decisions | <70% agreement |
| Token efficiency | Tokens per task | >50% increase |
| Latency | Time to completion | >50% increase |
| Error rate | Errors per task | >10% increase |
| Escape rate | Bugs per task | >5% increase |
| Appeal rate | Appeals per HOLD | >10% increase |
| Memory utilization | Memory entries per task | >100% increase |
| Personality drift | Voice/style deviation | >30% change |
| Goal alignment | Task spec vs outcome match | <80% match |

### Adaptation Layer

**Self-patching protocol (with human approval):**

1. **Thorn detected**: Systematic failure pattern identified.
2. **Root cause analysis**: Classify into 1 of 6 categories.
3. **Patch proposal**: Generate specific SOUL or prompt change.
4. **Safety check**: Verify patch doesn't violate guardrails.
5. **Human approval**: Operator reviews and approves/rejects.
6. **Apply patch**: Update SOUL, log to ledger.
7. **Regression test**: Run 5 past failure cases to verify fix.

**Patch proposal format:**
```python
class PatchProposal:
    thorn_id: str
    root_cause_category: str
    affected_agent: str
    current_behavior: str
    proposed_change: str  # SOUL delta
    evidence: list[str]   # Task IDs where failure occurred
    risk_level: str       # "low", "medium", "high"
    rollback_plan: str    # How to revert if patch causes issues
```

**Guardrails for self-patching:**
- No patch can remove blocking authority.
- No patch can disable testing requirements.
- No patch can grant new tool access without operator approval.
- All patches are versioned and reversible.
- Patches affecting >3 agents require operator approval.

### Graceful Degradation

**5-level degradation model (adapted from Zylos Research, 2026):**

| Level | Trigger | Behavior |
|-------|---------|----------|
| FULL | Normal | All agents active, full reasoning |
| SIMPLIFIED | Token budget > 70% | Reduce reasoning depth, skip optional steps |
| CACHED | Token budget > 85% | Use cached results, skip research |
| MINIMAL | Token budget > 95% | Only critical path, no verification |
| REJECT | Token budget > 99% | Task rejected, escalate to operator |

**Agent-level degradation:**
- If agent times out: retry once with simplified prompt.
- If agent fails twice: escalate to human.
- If agent drifts: reset to last known good state (memory replay).

### Regression Testing for Agent Behavior

**Problem**: Agent behavior changes (SOUL patches, model updates) can cause regressions.

**Solution**: Maintain a regression test suite of past failure cases.

**Regression test format:**
```python
class RegressionTest:
    test_id: str
    description: str
    task_spec: str
    expected_outcome: str
    failure_mode: str  # What this test prevents
    agents_involved: list[str]
    last_passed: datetime
```

**Regression test execution:**
- Run full suite weekly (nightly CI job).
- Run targeted suite after every SOUL patch.
- If any test fails: alert operator, propose rollback.

### Implementation Stack

| Component | Tool | Justification |
|-----------|------|---------------|
| Behavioral logging | Structured logging → SQLite | Durable, queryable |
| EmoBank | In-memory + SQLite | Fast access, persistent storage |
| RBT diagnosis | LLM-based analysis | Pattern recognition in logs |
| Root cause analysis | Rule-based + LLM hybrid | Fast classification, deep analysis |
| Patch proposal | LLM-generated SOUL deltas | Specific, actionable |
| Human approval | Operator dashboard | Safety guardrail |
| Regression testing | pytest-style test runner | Automated, repeatable |
| Drift detection | ASI computation | Quantified, trend-based |

## Practical Recommendations

| Recommendation | Implementation | Tools | Threshold |
|----------------|----------------|-------|-----------|
| Behavioral logging | Structured events per agent | SQLite | All agent actions |
| RBT diagnosis | Weekly analysis of EmoBank | LLM | All tasks |
| Root cause analysis | 6-category classification | Rule-based + LLM | On every failure |
| Self-patching | Patch proposals with human approval | LLM-generated SOUL deltas | Thorns only |
| Graceful degradation | 5-level model | Token budget monitor | 70/85/95/99% thresholds |
| Regression testing | Past failure cases as tests | pytest-style runner | Weekly + post-patch |
| Drift detection | ASI across 12 dimensions | Trend analysis | Weekly |
| Kill switch | Immediate agent stop | Microsoft-style circuit breaker | Anomaly score ≥ 20 |

## Metrics Catalog

| Metric | Definition | How to Measure | Target | Warning |
|--------|-----------|----------------|--------|---------|
| Thorn detection rate | Thorns identified / total failures | RBT log | >90% | <70% review diagnosis |
| Patch success rate | Patches that fixed issue / total patches | Regression test | >80% | <50% review proposal quality |
| Mean time to detect (MTTD) | Failure occurrence to detection | Timestamp diff | <1 hour | >24 hours review monitoring |
| Mean time to repair (MTTR) | Detection to patch applied | Timestamp diff | <7 days | >14 days review process |
| Regression rate | Regressions / total patches | Test suite | <5% | >10% tighten guardrails |
| Drift score (ASI) | Composite drift metric | 12-dimension trend | <2.0 | >5.0 trigger investigation |
| Graceful degradation rate | Tasks degraded / total | Counter | <5% | >20% review capacity |
| Self-healing coverage | Thorns with patches / total | Counter | >80% | <50% review resources |

## References

1. [VIGIL, 2025] VIGIL: A Reflective Runtime for Self-Healing Agents. arXiv:2512.07094.
2. [ROAD, 2025] ROAD: Reflective Optimization via Automated Debugging for Zero-Shot Agent Alignment. arXiv:2512.24040.
3. [ACM, 2025] Goal-Oriented Reliability and Self-Improvement for Multi-Agent Systems. Proceedings of the ACM Conference on AI and Agentic Systems.
4. [Microsoft, 2025] AI Agent Failure Modes: Six Failure Categories. Whitepaper.
5. [Galileo, 2025] Multi-Agent Production Deployment Analysis. 42% spec, 37% coordination, 21% verification.
6. [arXiv, 2601.04170, 2026] Agent Drift: Quantifying Behavioral Degradation in Multi-Agent LLM Systems.
7. [Zylos Research, 2026] AI Agent Self-Healing and Failure Recovery. zylos.ai/research.
8. [Microsoft, 2025] Agent Governance Toolkit: Kill Switch and Rate Limiting. github.com/microsoft/agent-governance-toolkit.
9. [LangChain, 2026] State of Agent Engineering Report. 89% observability adoption.
10. [Factory AI, 2026] Long-Running Session Context Overflow Research.

## [DEEP DIVE]: Optimizer-Grade Patch Generation (GEPA/TextGrad), Error-Budget Governance, and Chaos Drills for Agents (freebuff, 2026-09-13)

### 1. Replace ad-hoc patch proposals with reflective prompt evolution (GEPA)

The self-patching protocol currently says "LLM-generated SOUL deltas" — the state of the art makes this concrete and measured. **GEPA** (Genetic-Pareto) evolves textual components (prompts/rules) via LLM reflection on *traceback-like* execution traces, maintaining a Pareto frontier of candidates scored on a held-out metric. Results: **beats GRPO (RL) by 10% on average across four tasks (up to 20%) while using up to 35x fewer rollouts**, and beats the leading prompt optimizer MIPROv2 by over 10% across two pipelines; on six tasks it beats GRPO by 6% on average with the same rollout advantage [Agarwal et al., 2025]. For the coach agent this means:

- A patch proposal is never a single candidate — generate 2-4 SOUL deltas, score each against the regression suite (the existing past-failure tests), keep the Pareto-nondominated set, promote only a candidate that dominates the incumbent SOUL on the failure cases without regressing the success cases.
- Reflection inputs = the thorn's evidence bundle (task IDs, traces, root-cause category) — exactly the "traceback" signal GEPA's reflect step consumes.
- The 35x fewer rollouts number is what makes this economical for an 8-agent crew: patch generation is an occasional, high-value operation, not a background RL loop.

### 2. TextGrad as the mechanism for localized, attributable patches

**TextGrad** implements "backpropagation through text": LLM-generated textual feedback is propagated along the compound system's computation graph to improve individual components; the framework treats prompts, tool specs, and even code as differentiable-in-text variables [Yuksekgonul et al., 2024]. Crew mapping: the SOUL file is the variable; escape traces are the loss signal; the "gradient" is a specific, localized critique ("rule X causes behavior Y in situation Z — change rule X"). Practical use: run TextGrad-style critique *before* GEPA-style candidate generation, so each candidate patch carries an explicit causal story linking it to the failing behavior — this is what makes the PatchProposal `proposed_change` field reviewable by the operator in minutes rather than an hour.

### 3. Patch governance via error budgets: when the coach is *allowed* to act

The original spec gates patches on human approval but has no quantitative trigger — patches happen whenever someone notices. Google SRE's error-budget policy supplies the trigger logic [Google SRE Workbook]:

- Define the SLI (task success rate) and SLO (start: 95%), giving a **5% escape budget** per 4-week window.
- Policy: a **single incident consuming >20% of the error budget** (i.e., one failure class burning ≥1% of all tasks in 4 weeks) triggers a mandatory postmortem with at least one concrete action item [Google SRE Workbook].
- Budget exhausted → feature work freezes and the crew enters a reliability sprint (patches only) until budget is restored. This is the automated "coach that improves the crew without human intervention" — within guardrails: the coach can *force* the patch pipeline to run, but never merge without operator approval.
- Pair with the SRE toil cap (<50% of agent/operator time on mechanical toil) as a standing health metric for the self-healing loop itself [Google SRE Workbook].

This also fixes the MTTR target's vagueness: MTTR <7 days becomes an SLO with its own budget, and repeat escapes (same thorn re-opened) count double against the budget — the economic incentive that makes regression-testing patches non-optional.

### 4. Chaos drills for agent systems: formalize the existing break drills

The Principles of Chaos Engineering: (1) build a hypothesis around **steady-state** behavior measured in outputs, (2) vary **real-world events**, (3) run experiments in **production** (or a faithful staging), (4) **minimize blast radius** with automatic rollback [Principles of Chaos]. The crew already runs "break drills" informally (STATUS: quality tracking lints) — formalize as a monthly GameDay with this experiment catalog:

| Experiment | Injected fault | Steady-state hypothesis | Expected crew response |
|---|---|---|---|
| Kill-the-verifier | Critic process terminated mid-task | Task completes with bounded delay | Retry once simplified → escalate; graceful degradation L2 |
| Duplicate-verdict | Same tester verdict replayed 3x | Verdict applied once | Idempotency token dedup (comm-protocols) |
| Poisoned-message | Malformed/oversized payload on bus | No task affected | Validation reject → DLQ, alert |
| Token-shock | Simulate 95% budget consumption | Task degrades, never silently | Level MINIMAL banner + operator notify |
| Memory-poison | Contradictory high-relevance memory insert | Insight quarantined | Two-source corroboration blocks propagation (memory-architecture deep dive) |

Rules: one experiment per GameDay, hypothesis written before injection, automatic rollback on steady-state violation, every finding becomes either a regression test or a thorn — closing the loop back into Layer 2 diagnosis.

### 5. Failure-class weighting for the ASI

The MAST taxonomy (150+ traces: 41.8% spec, 36.9% inter-agent, 21.3% verification) [Cemri et al., 2025] implies the 12-dimension ASI should be weighted by observed class frequency: specification drift and inter-agent misalignment deserve ~2x the weight of verification gaps, because they are ~2x more frequent in the field. Rebalance quarterly as the crew's own failure ledger accumulates — the ASI is a living instrument, not a fixed checklist.

### References for deep dive

- [Agarwal et al., 2025] GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning. arXiv:2507.19457. github.com/gepa-ai/gepa.
- [Yuksekgonul et al., 2024] TextGrad: Automatic "Differentiation" via Text. arXiv:2406.07496. github.com/zou-group/textgrad.
- [Google SRE Workbook] Error Budget Policy for Service Reliability; Implementing SLOs. sre.google/workbook.
- [Principles of Chaos] principlesofchaos.org (steady-state hypothesis, blast radius, rollback).
- [Google Cloud, 2026] Getting started with chaos engineering. cloud.google.com/blog.
- [Cemri et al., 2025] Why Do Multi-Agent LLM Systems Fail? arXiv:2503.13657.
