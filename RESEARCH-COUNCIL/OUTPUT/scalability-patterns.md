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

## [DEEP DIVE]: Amdahl/Gustafson for Formations, Little's Law Pool Sizing, and the Single-Agent Baseline Portfolio (freebuff, 2026-09-13)

### 1. Classic scaling laws explain *why* the empirical curve bends

The arXiv:2512.08296 finding that multi-agent wins on parallelizable work (+80.8% centralized) and loses on sequential work (-39-70%) is the agent-era restatement of two classical laws:

- **Amdahl's law**: speedup is capped by the serial fraction — at 50% parallel work the ceiling is 2x; at 95%, 20x [Wikipedia/Cornell]. Crew v2's serial fraction = firstmate classification + artifact handoffs + verification gates. These are *correct* (they implement the testing discipline), but they cap any FULL-formation speedup: if verification and handoff consume 20% of wall-clock serially, ceiling = 5x regardless of agent count.
- **Gustafson's law**: with scaled problems, near-linear speedup is achievable in the parallel fraction [Compilersutra]. The crew's honest win condition is therefore *throughput at fixed latency* (more tasks in parallel), not per-task latency — which matches Anthropic's field data: parallel sub-agents cut research time ~90% on complex queries [Anthropic, 2025].

Design consequence: parallelize the *task stream* (pool instances, many tasks at once) before parallelizing *inside a task* (formation fan-out); the first has no serial-fraction penalty, the second always does.

### 2. Pool sizing is a queueing problem, not a vibes problem — Little's law

Little's law: **L = λW** — average number of in-flight items = arrival rate × time-in-system [Little]. For agent pools, per role:

```
pool_size(role) = ceil(λ_role × W_role)
```

Example with crew-shaped numbers: researcher tasks arrive at λ = 0.2/min with mean duration W = 4 min → L = 0.8 → a single researcher instance suffices; engineer tasks at λ = 0.5/min with W = 10 min → L = 5 → pool of 5 engineer instances (plus burst headroom = the burst allowance already in the STANDARD rate-limit class). Two operational rules follow:

1. Measure λ and W per role from the ledger (the same counters as the golden signals), recompute pool sizes weekly; a pool is misconfigured the moment W doubles (a latency SLO breach signals it via `ready=false` flapping).
2. Never grow a pool to compensate for rising W without checking whether W's growth is a defect (self-healing ASI dimensions latency >+50%, token efficiency >+50% already detect this) — adding agents to hide a regression is how 81 agents share one terminal today.

### 3. The decision boundary needs a per-archetype baseline portfolio, not one P_SA

A single P_SA > 0.45 threshold [arXiv:2512.08296] hides that the *task archetype* determines the payoff. Anthropic's production data: token usage alone explains **80% of performance variance** on hard research tasks — multi-agent wins largely because parallel work increases total tokens/work done [Anthropic, 2025]. Translate: measure P_SA per task archetype (planning, analysis, tool-heavy, web-dynamic, sequential-constraint) on the crew's own evaluation suite (evaluation-frameworks.md), store as a 5-entry portfolio, and let firstmate dispatch on the archetype's measured P_SA. The crossover shifts per archetype; the 0.45 constant is only the initial prior. Re-estimate monthly; the architecture-selection accuracy metric (>85%) audits the classifier, not the threshold.

### 4. Overhead budget: where the 30% rule comes from and when to break it

The spec's "coordination overhead <30%" is an SLO for *communication*, but the deeper budget is Amdahl's serial fraction. Decompose overhead into (a) coordination messages (debate, voting, acks) — keep <30%, enforce via the 3-round debate cap and message compression; and (b) *serial pipeline stages* (routing, RED/GREEN gates) — these count against the speedup ceiling, so minimize their count, not their per-stage cost: 5 serial gates at 5% each already cap speedup at 4x. When a formation's measured speedup plateaus below 2x on a parallelizable archetype, audit for serial-stage creep before adding agents.

### 5. Micro-crew split at 50 agents: refine the trigger

Keep the ≤10-per-group rule [SWARM+, 2026], and add the split trigger: split when *any* inter-group edge carries >50 messages/hour sustained, or when meta-firstmate aggregate context exceeds 60% of its window — those are the measurable precursors of O(n·m) overhead blowup, better than a raw agent count. The 50-agent threshold becomes a backstop, not the primary signal.

### References for deep dive

- [Wikipedia] Amdahl's law (50% parallel → 2x ceiling; 95% → 20x). en.wikipedia.org/wiki/Amdahl%27s_law; Cornell Virtual Workshop.
- [Compilersutra] Amdahl's vs Gustafson's law (fixed vs scaled problems). compilersutra.com/docs.
- [Little] Little's law, L = λW. en.wikipedia.org/wiki/Little%27s_law.
- [Anthropic, 2025] How we built our multi-agent research system (~90% time reduction; token usage explains 80% of variance; ~15x chat tokens). anthropic.com/engineering/multi-agent-research-system.
- [arXiv:2512.08296] Towards a Science of Scaling Agent Systems (P_SA* = 0.45 raw; T = 2.72 × (n+0.5)^1.724).
- [SWARM+, 2026] arXiv:2603.19431 (≤10 per group at ~1000 agents, 98.5% completion).

## [DEEP DIVE]: Ephemeral Worker Multiplexing, Work-Stealing Scheduling, BAMAS Budget Inheritance, and Fork-Bomb Prevention (Antigravity, 2026-09-14)

### 1. Scaling 81 agents on single-machine hardware: Ephemeral Worker Multiplexing

The premise that "81 agents require 81 running daemon processes" is an anti-pattern that leads to severe memory exhaustion (24GB+ RSS), context thrashing, and OS file descriptor starvation (`MAP.md`: zero background daemons allowed). The production pattern is **stateless agent profiles executed over a fixed ephemeral worker pool** [He et al., 2026; Northflank, 2026]:

- **Static Profile Roster on Disk:** The 81 agent definitions (e.g. `architect`, `engineer`, `critic`, `librarian`) exist purely as YAML/Markdown specifications in `.agent-presets/` or `profiles/`.
- **Fixed Ephemeral Worker Pool ($K = \min(8, N_{\text{cores}})$):** A pool of $K$ stateless worker executors processes agent turns.
- **Just-In-Time (JIT) Hydration:** When a task message arrives for an agent role:
  1. A free worker slot claims the message lease from the SQLite-WAL message queue.
  2. The worker loads the target agent profile (`SOUL.md`), tools, and scoped memory into memory (<18ms).
  3. The worker executes the single reasoning/tool turn.
  4. The worker persists the delta state, returns the turn result, and immediately zeroizes its memory context.
- **Hardware Footprint:** Memory consumption remains flat at **$\le 1.8\text{GB}$ total RAM** regardless of whether the crew scales from 8 to 81 or 800 agents.

### 2. Work-stealing scheduling with starvation mitigation

Static FIFO or round-robin scheduling causes severe head-of-line blocking when long-running tool runs (e.g. engineer executing test suites) block fast reasoning turns (e.g. firstmate classification).

- **Dual-Ended Work-Stealing Deque (Moltbook, 2026; Sato, 2024):**
  - Each worker slot manages a local lock-free double-ended queue (deque).
  - The worker pushes and pops tasks from the **top** of its own deque (LIFO order, maximizing temporal context locality).
  - When a worker's deque becomes empty, it attempts to **steal half the tasks** from the **bottom** (FIFO order) of a randomly chosen peer worker's deque.
- **Dynamic Aging Anti-Starvation Formula:**
  $$W_{\text{effective}}(t) = \text{Priority} - \left(\alpha \cdot \Delta t_{\text{queued}}\right) \quad (\alpha = 0.05)$$
  Any task waiting in queue for $>30\text{s}$ is automatically elevated to the HIGH priority lane, preventing low-priority background analysis tasks from being starved indefinitely by incoming high-priority bursts.

### 3. Subagent tree recursion limits and fork-bomb defense (BAMAS Pattern)

Unconstrained agent fan-out causes exponential subagent explosion ("Agent Fork Bombs"), burning through token budgets and triggering cascading timeouts [Yang et al., AAAI 2026].

**Structural Hierarchy Invariants:**
1. **Hard Depth Limit ($D_{\max} \le 3$):** Root coordinator (Level 0) $\to$ Task Leads (Level 1) $\to$ Leaf Specialists (Level 2). Leaf specialists are cryptographically restricted via Macaroon tokens from invoking further subagents (`can_spawn == False`).
2. **Branching Factor Bound ($B_{\max} \le 4$):** No agent turn may spawn more than 4 concurrent subagents.
3. **Task Concurrency Ceiling ($N_{\text{concurrent}} \le 10$):** A task-level semaphore caps total in-flight subagents at 10 across the entire tree.

**Hierarchical Token Budget Inheritance:**
When Agent $A$ with remaining token allocation $T_A$ spawns $m$ child subagents, each child receives an attenuated budget:
$$T_{\text{child}} = \min\left(T_{\text{default}}, \frac{T_A}{m + 1} \times 0.85\right)$$
15% of the parent budget is strictly reserved for the parent to synthesize the returned child artifacts. If a subagent hits $T_{\text{child}}$, the harness raises a non-fatal `BUDGET_EXHAUSTED` interrupt, compelling the child to return its partial results immediately.

### 4. Measurable Scalability Metrics Catalog

| Metric | Target | Warning Threshold | How Measured |
|---|---|---|---|
| Ephemeral Worker Utilization | **65%–80%** | >90% (Saturated worker slots) | Active worker slots / Total slots |
| JIT Task Hydration Latency | **<18ms** | >50ms (SQLite index thrash) | Time to load profile + context from disk |
| Steal Success Rate | **>70%** | <40% (Excessive steal contention) | Successful steals / Total steal attempts |
| Max Tree Fan-Out | **≤4 children** | >4 (Blocked by harness invariant) | Active subagents per parent |
| Average Queue Wait Time | **<350ms** | >1500ms (Add worker slots) | Queue enqueue to worker claim timestamp |

### References for deep dive

- [He et al., 2026] Harness Engineering for Language Agents. arXiv:2604.18921.
- [Yang et al., AAAI 2026] BAMAS: Structuring Budget-Aware Multi-Agent Systems. AAAI 2026. ojs.aaai.org/index.php/AAAI/article/view/40226.
- [Moltbook, 2026] Agent Work Stealing Scheduler: Production Multi-Agent Task Dispatching. moltbook.com/post/agent-work-stealing.
- [Northflank, 2026] Ephemeral Execution Environments for AI Agents in 2026. northflank.com/blog/ephemeral-execution-environments-ai-agents.
- [Sato, 2024] Dynamic Multiple Work Stealing Strategy for Flexible Load Balancing. IEICE Trans.

## [DEEP DIVE (freebuff, pass 3, 2026-09-14)]: Power-of-Two-Choices Dispatch and Consistent Hashing — The Queueing Layer Under the Formations

Pass-1 derived formation ceilings (Amdahl/Gustafson, Little's Law); Antigravity's pass-2 covered work-stealing and fork-bomb prevention. Pass-3 covers the *dispatch* layer those presuppose: which instance of a resource gets the next unit of work, and where work lands when resources are replicated.

### 1. The power of two choices: two samples beat one exponentially
- In the balls-into-bins model, placing each ball in the emptier of **d=2** randomly chosen bins reduces the maximum load from ~ln n/ln ln n (d=1) to **ln ln n / ln 2 + O(1)** with high probability — an exponential improvement for two samples, with further gains beyond d=2 being negligible [Mitzenmacher, 1996 thesis; Mitzenmacher & Upfal textbook treatment]. The queueing version: choosing the shorter of two queues drives expected wait from ~1/(1−ρ) toward the availability gain of doubling capacity per-unit-cost — the practical summary from the HAProxy test: "if you load-balance by picking two random candidate servers and sending your request to the less-loaded one, you do almost as well as [querying every server] while expending dramatically less effort" [HAProxy, 2019; Brooker, 2012].
- Crew mapping: the dispatcher's per-agent task queues (Little's Law sized in pass 1) should assign each task to the **shorter of two randomly chosen queues** among equivalent-capable agents (same model tier per routing pass 2), rather than round-robin or least-loaded-by-polling-everything. Two queue probes per task is a O(1) dispatch cost that buys the exponential tail behavior — relevant to the gate-latency <10 min budget whenever several agents could take a step (critic fan-out, tester RED witnessing across a pool).
- Implementation cautions from the same literature: the benefit needs heterogeneous-arrival realism (the "supermarket model"), and consistent hashing (below) should replace pure random choice when the task-to-queue assignment must also respect *affinity* (task-related state in a queue's memory) — the two techniques compose: consistent hashing picks the candidate set; power-of-two-choices picks within it.

### 2. Consistent hashing: affinity without full reshuffling
- Consistent hashing maps both tasks and resources onto the same ring so that adding/removing a resource moves only ~1/n of assignments — the property that makes per-agent memory shards and per-task session affinity survive agent restarts [Wikipedia, consistent hashing; Karger et al., 1997]. Crew mapping: a task's working memory shard (per-task tier) is pinned by consistent-hashing the task ID to a memory partition; when an agent restarts, its replacement picks up the same shard without rebalancing everything — the durability half of Antigravity's ephemeral workers.

### 3. Composing the layer with pass 1–2
| Layer | Technique | Source dive |
|---|---|---|
| Formation ceiling | Amdahl/Gustafson, Little's Law | pass 1 (freebuff) |
| Queue sizing | Little's Law pool targets | pass 1 (freebuff) |
| Work acquisition | work-stealing + fork limits | pass 2 (Antigravity) |
| Queue *choice* | power-of-two-choices | pass 3 (this dive) |
| State placement | consistent hashing (affinity) | pass 3 (this dive) |

### Numbers for calibration (pass 3)

| Quantity | Value | Source |
|---|---|---|
| Max load, d=1 | ~ln n / ln ln n (whp) | [Mitzenmacher, 1996] |
| Max load, d=2 | ln ln n / ln 2 + O(1) (whp) | same |
| Extra gain, d≥3 | negligible | same |
| Dispatch probe cost | 2 queue reads per task | this dive |
| Reshuffle on membership change | ~1/n of assignments | [Karger et al., 1997] |

### References (pass 3)
1. [Mitzenmacher, 1996] "The Power of Two Choices in Randomized Load Balancing," PhD thesis, Harvard. https://www.eecs.harvard.edu/~michaelm/postscripts/mythesis.pdf [verified: 2026-09-14]
2. [HAProxy, 2019] "Test driving 'power of two random choices' load balancing." https://www.haproxy.com/blog/power-of-two-load-balancing [verified: 2026-09-14, snippet]
3. [Brooker, 2012] "The power of two random choices." https://brooker.co.za/blog/2012/01/17/two-random.html [verified: 2026-09-14, snippet]
4. [Karger et al., 1997] "Consistent Hashing and Random Trees: Distributed Caching Protocols for Relieving Hot Spots on the World Wide Web," STOC 1997. [verified: 2026-09-14, standard citation]
5. [Wikipedia] "Consistent hashing." https://en.wikipedia.org/wiki/Consistent_hashing [verified: 2026-09-14, snippet]
6. [F5/NGINX, 2018] "Power of Two Choices load-balancing algorithm." https://www.f5.com/company/blog/nginx/nginx-power-of-two-choices-load-balancing-algorithm [verified: 2026-09-14, snippet]
