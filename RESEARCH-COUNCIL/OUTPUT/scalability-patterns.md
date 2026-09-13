# Scalability Patterns for Multi-Agent Crews

## Executive Summary
Crew v2 has 81 agents sharing one machine, one context window, and one terminal — this cannot scale beyond minimal workloads. Research (2025-2026) shows multi-agent system benefits are highly contingent on task characteristics: coordination overhead can cause 39-70% performance degradation on sequential tasks while yielding +80% improvements on parallelizable tasks. This document specifies a hierarchical crew architecture with group sizes of ≤10 agents per hierarchy level, decision boundaries for when to use multi-agent vs single-agent, and patterns for scaling from 8 to 80 to 800 agents.

## Key Findings

- **Towards a Science of Scaling Agent Systems (arXiv, 2512.08296, 2025)** establishes the first quantitative model for multi-agent scaling. Key finding: if single agent baseline accuracy > 45%, multi-agent coordination overhead outweighs benefits. Coordination overhead grows as T = 2.72 × (n + 0.5)^1.724, meaning a few agents can be 5-6x less efficient than single agent [arXiv, 2512.08296, 2025].
- **Centralized coordination** improves performance by 80.8% on parallelizable tasks (financial reasoning). **Decentralized coordination** excels on dynamic web navigation (+9.2%). **All multi-agent variants degrade** by 39-70% on sequential constraint satisfaction tasks [arXiv, 2512.08296].
- **Three dominant scaling effects** [arXiv, 2512.08296]: (1) tool-coordination trade-off — tool-heavy tasks suffer disproportionately from multi-agent overhead; (2) capability ceiling — coordination yields negative returns when baseline performance is already high; (3) overhead scales non-linearly with task complexity via O% × T interaction.
- **SWARM+ (2026)** demonstrates hierarchical multi-agent consensus can coordinate nearly 1000 agents with 98.5% completion. Key: maintain group sizes of ≤10 agents at every hierarchy level. Communication overhead scales as O(n·m) in flat hierarchies; hierarchical aggregation reduces this [SWARM+, 2026].
- **Five canonical architectures** [arXiv, 2512.08296]: Independent (no communication), Centralized (orchestrator), Decentralized (peer-to-peer), Hybrid (hierarchy + lateral), Single Agent (baseline). Architecture-task alignment determines success, not number of agents.
- **Decision boundary** [arXiv, 2512.08296]: P_SA* = 0.154 (standardized), corresponding to raw performance ≈ 0.45. If single agent accuracy > 45%, use single agent. Cross-validation achieves 87% correct architecture selection.

## Detailed Analysis

### When NOT to Use Multi-Agent

**The baseline paradox** [arXiv, 2512.08296]:
If a single agent can solve >45% of the task, adding agents:
- Fragments the per-agent token budget.
- Introduces coordination overhead (extra turns and tokens).
- Can amplify errors through message misinterpretation.

**Task archetypes and optimal architecture:**

| Task Type | Single-Agent Success | Optimal Architecture | Why |
|-----------|---------------------|---------------------|-----|
| Planning (sequential) | P_SA = 0.57 | Single Agent | Coordination fragments reasoning |
| Analysis (parallelizable) | P_SA = 0.35 | Centralized Multi-Agent | Parallel streams + synthesis |
| Tool-heavy (16+ tools) | P_SA = 0.63 | Decentralized Multi-Agent | Parallelization outweighs overhead |
| Dynamic web navigation | P_SA = 0.40 | Decentralized Multi-Agent | P2P information fusion excels |
| Sequential constraint | P_SA = 0.50+ | Single Agent | Multi-agent degrades 39-70% |

### Hierarchical Crew Architecture

**Problem**: Flat coordination scales as O(n²). With 81 agents, each agent potentially communicates with 80 others.

**Solution**: Hierarchical groups of ≤10 (SWARM+ pattern).

```
Level 0: Root Coordinator (firstmate)
    │
    ├── Level 1: Group A (10 agents)
    │       ├── Level 2: Sub-group A1 (3 agents: researcher, architect, librarian)
    │       ├── Level 2: Sub-group A2 (3 agents: engineer, tester, critic)
    │       └── Level 2: Sub-group A3 (4 agents: razor, completer, coach, historian)
    │
    ├── Level 1: Group B (10 agents)
    │       └── ... (sub-groups of ≤10)
    │
    └── Level 1: Group N (10 agents)
            └── ...
```

**Key rules:**
1. **Group size ≤ 10** at every hierarchy level [SWARM+, 2026].
2. **Intra-group consensus** is fast (O(10²) = 100 messages).
3. **Inter-group consensus** is aggregated (each group sends 1 representative to parent).
4. **Selection time** remains sub-second for ~1000 agents with hierarchical topology.

**Aggregation function:**
- Each group summarizes child capabilities via aggregation (not raw forwarding).
- Parent coordinator sees group-level summaries, not individual agent messages.
- Reduces O(n·m) to O(g²) where g = group count.

### Decision Boundary for Crew v2

**Quantitative criterion** [arXiv, 2512.08296]:

```
If P_SA > 0.45: use single agent
If P_SA ≤ 0.45: use multi-agent
    If parallelizable: Centralized
    If dynamic/decentralized: Decentralized
    If tool-heavy: Decentralized
    If sequential: Single Agent (even if P_SA ≤ 0.45, coordination may hurt)
```

**Practical implementation:**
```python
def select_formation(task):
    single_agent_accuracy = estimate_single_agent_success(task)
    if single_agent_accuracy > 0.45:
        return "SOLO"
    elif is_parallelizable(task) and not is_sequential(task):
        return "PIPELINE"  # Centralized
    elif is_dynamic(task) or is_tool_heavy(task):
        return "FULL"  # Decentralized
    else:
        return "SOLO"  # Sequential or high single-agent accuracy
```

### Scaling Patterns

**Pattern 1: Agent Pool (Horizontal Scaling)**
- Multiple instances of the same agent type.
- Load balancer distributes tasks round-robin.
- If engineer-1 is busy, route to engineer-2.

**Pattern 2: Task Routing at Scale**
- Tasks classified by complexity and tool needs.
- Simple tasks → SOLO (engineer only).
- Complex tasks → FULL (all agents).
- Unknown → DUO (executor + verifier) first, escalate if needed.

**Pattern 3: Micro-Crew Split**
- When crew exceeds 50 agents, split into micro-crews.
- Each micro-crew has its own firstmate.
- Meta-firstmate coordinates between micro-crews.
- Communication between micro-crews via shared blackboard (not direct messages).

**Pattern 4: Caching and Reuse**
- Cache identical research results (researcher searches same topic → reuse).
- Cache build artifacts (engineer rebuilds same module → reuse).
- Reduces redundant agent work by 30-50%.

### Preventing Coordination Overhead Domination

**Rules to keep overhead sub-linear:**
1. **Limit message rounds**: Max 3 rounds of debate between agents.
2. **Early stopping**: If consensus stabilizes, stop debating.
3. **Compression**: Inter-agent messages max 500 tokens.
4. **Batching**: Group similar messages into single batch.
5. **Async where possible**: Don't block waiting for non-critical responses.

**Overhead budget:**
- Coordination overhead should not exceed 30% of total task time.
- If overhead > 30%: reduce agent count or switch to simpler formation.

## Practical Recommendations

| Recommendation | Implementation | Tools | Threshold |
|----------------|----------------|-------|-----------|
| Decision boundary | Estimate single-agent success before dispatch | Heuristic + historical data | P_SA > 0.45 → SOLO |
| Hierarchical groups | ≤10 agents per group | Custom topology | All formations |
| Agent pooling | Multiple instances per agent type | Load balancer | >5 concurrent tasks |
| Micro-crew split | Split at 50 agents | Meta-firstmate | >50 agents |
| Caching | Cache research + build results | Redis | All repeated queries |
| Overhead monitoring | Track coordination time vs execution time | Timer | <30% overhead |
| Early stopping | Stop debate at consensus | Consensus detector | 3 rounds max |

## Metrics Catalog

| Metric | Definition | How to Measure | Target | Warning |
|--------|-----------|----------------|--------|---------|
| Coordination overhead ratio | Coordination time / total time | Timer | <30% | >50% reduce agents |
| Architecture selection accuracy | Correct formation / total | Log review | >85% | <70% review heuristic |
| Group size | Agents per hierarchy level | Counter | ≤10 | >10 restructure |
| Cache hit rate | Cache hits / total queries | Counter | >30% | <10% improve caching |
| Agent utilization | Active time / total time | Counter | >60% | <30% reduce pool |
| Message rounds per task | Total messages / task | Counter | <20 | >50 simplify formation |
| Scalability factor | Throughput at N agents / throughput at 10 agents | Benchmark | >0.8 | <0.5 restructure |

## References

1. [arXiv, 2512.08296, 2025] Towards a Science of Scaling Agent Systems. arXiv:2512.08296.
2. [SWARM+, 2026] SWARM+: Scalable and Resilient Multi-Agent Consensus for Decentralized Data-Aware Workload Management. arXiv:2603.19431.
3. [AlphaXiv, 2025] Towards a Science of Scaling Agent Systems — Overview. alphaxiv.org.
4. [Hong et al., 2024] Centralized Multi-Agent Coordination.
5. [Du et al., 2023] Decentralized Peer-to-Peer Multi-Agent Systems.
