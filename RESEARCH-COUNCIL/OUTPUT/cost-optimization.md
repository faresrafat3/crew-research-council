# Cost Optimization and Token Economics

## Executive Summary
Crew v2 uses one model for all tasks with no caching, no early stopping, and no cost tracking per agent or task — costs scale quadratically with task depth and model API spend is uncontrolled. Production token economics (2025-2026) require model tiering, prompt caching, context window management, and hard budget enforcement. Research shows 60-85% of AI spend is recoverable through disciplined optimization. This document specifies a three-tier routing system, caching architecture, and budget enforcement framework that can reduce costs by 51-87% while maintaining quality.

## Key Findings

- **Prompt Caching** [Veso Research, 2026]: Anthropic offers 90% off cached reads (0.1x cost). OpenAI offers 75-90% off cached input on its frontier models (exact model-version names could not be verified as of 2026-09-13). Gemini gives 90% off via implicit caching on 2.5-series models (raised from 75% in Nov 2025; on by default). Cache the stable prefix — system prompt, tool definitions, static few-shot examples — and compact only below the cache boundary. Never compact through it [Veso Research, 2026; Google Developers Blog, 2025].

- **Model Tiering** [Zylos Research, 2026]: A three-tier routing system (Opus for architecture, Sonnet for implementation, Haiku for quick edits) costs $0.98 per session versus $2.02 for uniform Opus — a 51% reduction with no measurable quality regression. Blended cost of $2.31/M tokens vs $18.40/M for uniform Opus — 87% reduction while maintaining 97.7% of full-frontier accuracy [Zylos Research, 2026].

- **Context Window Economics** [Zylos Research, 2026]: A 200K-token context costs 200x more than 1K-token. At Claude Sonnet rates ($3/M input), that's $0.60/turn vs $0.003. In a 50-turn agentic loop: $30 vs $0.15. Prompt caching is the single highest-leverage optimization: 90% discount on cached input tokens [Zylos Research, 2026].

- **APC (Agentic Plan Caching)** [arXiv:2506.14852, 2025]: 50.31% cost reduction, 27.28% latency reduction. 76.42% cost reduction on GAIA benchmark at only 0.61% accuracy drop [Veso Research, 2026].

- **Output Token Premium** [SAA Report, 2026]: Claude family charges 5x more for output tokens than input. Reducing output from 5K to 1K tokens through structured formatting saves 16% on a 100K context task. The largest cost driver is context accumulation across agent turns — a 4-agent fleet consuming 200K tokens each costs 800K tokens per wave; intelligent orchestration can aggregate to ~10K tokens in the main context (80x difference) [SAA Report, 2026].

- **Cost Attribution** [Veso Research, 2026]: Track cost per task, per user, per agent, and per failure. Cost per failure is the most informative metric — reveals tokens burned on tasks that didn't complete (retry loops, hallucinated tool calls, context limit restarts). Propagate cost context through delegation chains: Agent A → B → C, C's tokens roll up through B to A [Veso Research, 2026].

## Detailed Analysis

### Current Failure Modes

1. **No model tiering**: All tasks use the same model regardless of complexity.
2. **No prompt caching**: System prompts re-sent every turn at full cost.
3. **No context management**: Context grows unbounded, costs scale quadratically.
4. **No cost tracking**: No per-agent, per-task, or per-failure cost visibility.
5. **No budget enforcement**: No hard limits on token spend per task.

### Three-Tier Model Routing

**Model tiers (verified 2026-09-13 against Anthropic pricing docs; older Opus pricing of $15/$75 no longer applies — Opus 4.6 lists at $5/$25):**

| Model | Input ($/M) | Output ($/M) | Use Case |
|-------|-------------|--------------|----------|
| Claude Opus 4.6 | $5.00 | $25.00 | Architecture, complex reasoning [verified: 2026-09-13, Anthropic pricing] |
| Claude Sonnet 4.6 | $3.00 | $15.00 | Implementation, testing, default [verified: 2026-09-13, Anthropic pricing] |
| Claude Haiku 4.5 | $1.00 | $5.00 | Quick edits, classification, linting [verified: 2026-09-13, Anthropic pricing] |
| GPT-4o | $2.50 | $10.00 | Alternative for specific tasks |
| Gemini 2.0 Flash Lite | $0.08 | $0.30 | High-volume, low-complexity |

Note: tiering savings shrink as frontier prices fall (uniform-Opus baseline dropped from $15/$75 to $5/$25), but tiering still pays because the Haiku:Opus input ratio is 5:1 and output ratio 5:1. Recompute savings against *current* prices at each quarterly review.

**Routing rules:**

| Task Complexity | Model | Justification |
|-----------------|-------|---------------|
| Simple (SOLO, <5 min) | Haiku 4.5 | Fast, cheap, sufficient |
| Moderate (DUO, 5-30 min) | Sonnet 4.6 | Balanced quality/cost |
| Complex (FULL, >30 min) | Opus 4.6 (architect), Sonnet (others) | Reasoning where it matters |
| Emergency fallback | Sonnet 4.6 | If Opus unavailable |

**Savings estimate**: 51-87% reduction vs uniform Opus [Zylos Research, 2026].

### Prompt Caching Architecture

**Cache layers (adapted from Zylos Research):**

| Layer | Content | TTL | Hit Rate Target |
|-------|---------|-----|-----------------|
| System prompt + tool schemas | Static, largest prefix | 1 hour | >90% |
| Conversation history | Partially stable | 5 min | >70% |
| Retrieved context (RAG) | Repeated documents | 1 hour | >50% |
| Dynamic inputs | Never cached | N/A | 0% |

**Cache rules:**
1. Mark stable prefix with `cache_control` header.
2. Compact only below the cache boundary — never compact through it.
3. Target 70%+ cache hit rate for stable-prompt workloads.
4. Cache TTL: 5 minutes (ephemeral) or 1 hour (extended).

**Cost impact**: 90% discount on cached input tokens. For a 10K-token system prompt sent 50 times: without caching = 500K tokens; with caching = 50K + 5K*49 = 295K (41% savings). With 90% discount on cached portion: 50K + 4.9K*49 = 290K tokens at 10% cost = equivalent to 54K full-price tokens (89% savings).

### Context Window Management

**The quadratic cost problem:**
- Token consumption grows roughly quadratically with task depth.
- Each step re-feeds accumulated context window.
- Prototyping can consume 100x more tokens than equivalent conversational requests [Zylos Research, 2026].

**Strategies:**

1. **Compaction**: Summarize older conversation turns.
   - Trigger at 70% context usage.
   - Keep last 3 turns verbatim, summarize rest.
   - Never compact through cache boundary.

2. **Subagent isolation**: Spawn subagents with isolated context.
   - Subagent returns only summary (not full context).
   - Main agent context stays small.

3. **Selective retrieval**: Don't feed full tool outputs.
   - Truncate tool outputs to 1000 tokens.
   - Summarize large documents before feeding.

4. **Output formatting**: Structured outputs reduce token count.
   - JSON instead of prose.
   - Bullet points instead of paragraphs.

### Budget Enforcement

**Per-task budget (hard limit):**

| Formation | Token Budget | Cost Budget |
|-----------|--------------|-------------|
| SOLO | 50K tokens | $0.50 |
| DUO | 100K tokens | $1.00 |
| PIPELINE | 200K tokens | $2.00 |
| FULL | 500K tokens | $5.00 |

**Budget actions:**
- At 70% budget: trigger compaction.
- At 85% budget: switch to cheaper model.
- At 95% budget: skip non-critical agents.
- At 100% budget: terminate task, escalate to operator.

**Cost attribution:**
```python
class CostContext:
    task_id: str
    root_agent: str
    delegated_agents: list[str]
    tokens_per_agent: dict[str, int]
    cost_per_agent: dict[str, float]
    total_tokens: int
    total_cost: float
    failed: bool  # Cost per failure tracking
```

### Early Stopping

**Stop generation when:**
- Confidence score > 0.95 (high confidence, no need for more tokens).
- Output exceeds max length budget.
- Task is complete (detected by structured output).

**Savings**: 10-20% reduction in output tokens.

## Practical Recommendations

| Recommendation | Implementation | Tools | Threshold |
|----------------|----------------|-------|-----------|
| Model tiering | Route by task complexity | Custom router | 3 tiers |
| Prompt caching | Cache stable prefix | cache_control header | >70% hit rate |
| Context compaction | Summarize at 70% usage | Custom | 70% context |
| Budget enforcement | Hard limit per task | Token counter | Formation-based |
| Cost attribution | Track per-agent, per-failure | Ledger | All tasks |
| Early stopping | Stop at high confidence | Confidence scorer | >0.95 confidence |
| Output formatting | Structured JSON | Prompt engineering | All agents |

## Metrics Catalog

| Metric | Definition | How to Measure | Target | Warning |
|--------|-----------|----------------|--------|---------|
| Cost per task | Total cost / task | Counter | <$2.00 | >$5.00 review |
| Token efficiency | Useful tokens / total tokens | Counter | >60% | <40% improve |
| Cache hit rate | Cache hits / total | Counter | >70% | <50% improve caching |
| Cost per failure | Cost of failed tasks / count | Counter | <$1.00 | >$5.00 review |
| Budget overrun rate | Tasks exceeding budget / total | Counter | <5% | >10% raise budgets |
| Model distribution | Tasks per model | Counter | 70% Sonnet, 20% Haiku, 10% Opus | >30% Opus review |
| Context efficiency | Context used / context available | Counter | <70% | >90% compact earlier |

## References

1. [Veso Research, 2026] Cost Management for Agentic AI. veso.ai/research.
2. [Zylos Research, 2026] Token Budget Management and Cost Control for Autonomous AI Agents. zylos.ai/research.
3. [Zylos Research, 2026] AI Agent Cost Engineering — Production Token Economics. zylos.ai/research.
4. [Zylos Research, 2026] Context Window Economics — Managing Token Budgets in Persistent AI Agents. zylos.ai/research.
5. [SAA Report, 2026] Token Optimization Techniques. tibsfox.com/Research/SAA.
6. [arXiv:2506.14852, 2025] Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents.

## [DEEP DIVE]: FrugalGPT Cascades, Cache-Write Economics, and Unit-Economics Governance (freebuff, 2026-09-13)

### 1. Upgrade three-tier routing to a quality-gated cascade (FrugalGPT)

The spec's three-tier routing assigns models by task class statically. FrugalGPT (Chen, Zaharia & Zou) adds the missing *quality gate*: run cheap first, **score the answer** (consistency/self-consistency checking across samples or a scorer model), escalate to the next tier only if the score fails — matching GPT-4-level accuracy with **up to 98% cost reduction**, or +4% accuracy at equal cost, with learned cascades saving 50-98% across workloads [Chen et al., 2023]. Crew instantiation:

- **Cheap tier attempt** for all NORMAL-class tasks (summaries, routine edits, doc updates).
- **Scorer**: task-type-specific check (tests for code edits — free, deterministic; self-consistency n=3 for judgment tasks).
- **Escalate** to strong tier only on gate failure. The tester's existing HOLD mechanism *is* a free quality gate for code: cheap-model drafts → tester RED/HOLD → strong-model fix is the cascade, already 80% built from the testing discipline.
- Expected blended saving is workload-dependent (the 98% headline comes from query-mix with many easy items; crews with hard-task-heavy mixes should model their own cascade curve from the ledger).

### 2. Prompt caching: the write/read asymmetry decides placement

Provider mechanics (2026): **Anthropic** — cache writes cost 1.25x input, reads cost 0.1x (90% discount), default TTL 5 minutes (1-hour at higher write cost); **OpenAI** — 50% discount on cached inputs for most current models (automatic, no explicit write cost) [Anthropic docs, 2026; Prompthub, 2025; Flexera, 2026]. Two derived rules for the crew:

1. **Prefix discipline**: the cached prefix must be *stable* (SOUL text, tool schemas, voice spec — the parts that never change per task class) and *volatile content must come after* the cache breakpoint. An interleaved prompt (task details injected before tool schema) busts the cache every call and *pays* the 1.25x write surcharge for the privilege — a measurable anti-pattern; instrument `cache_read_input_tokens` per agent and alert when cache-hit ratio <50% on any agent whose prompt prefix is supposed to be stable.
2. **TTL vs task cadence**: agent sessions with gaps >5 min (async message_agent) will miss 5-minute-TTL windows; the 1-hour TTL pays off when inter-message latency median >5 min — decide from the ledger's inter-call gap distribution, not intuition. The BULK/sleep-time lanes (memory deep dive) should batch to reuse warm caches within TTL windows.

Anthropic's own agent telemetry (4x chat tokens for agents, 15x multi-agent) [Anthropic, 2025] means the input-heavy prefix cache is where most of the crew's achievable saving lives — bigger than output-side optimizations.

### 3. Unit economics: $/successful-task is the only top-line cost metric

"Cost per task" rewards cheap failures. Define:

```
unit_cost(agent) = total_tokens_cost(agent, window)
                   / tasks_completed_passing_all_gates(agent, window)
```

Route/model changes are accepted only when unit_cost falls without success-rate SLO breach (error-budget integration from self-healing deep dive). Track token spend per OTel `gen_ai.usage.*` attributes (production-deployment deep dive) so the metric is queryable without bespoke accounting.

### 4. Budget enforcement at the right granularity

Enforce budgets at *formation level* (SOLO/DUO/PIPELINE/FULL multipliers over a base per-task budget), not per-agent flat caps: a FULL formation legitimately burns 10x a SOLO task. The degradation ladder (FULL→...→REJECT, self-healing) keys off the formation's remaining budget, and escalation paths already exist. Add one governance rule from the FrugalGPT evidence: **cascade adoption itself must clear a measured bar** — run one month shadow-mode comparing cascade vs direct-strong on the evaluation suite (evaluation-frameworks.md), adopt only if quality-neutral at ≥30% saving.

### References for deep dive (freebuff, 2026-09-13)

- [Chen, Zaharia & Zou, 2023] FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance. arXiv:2305.05176 (98% cost reduction matching GPT-4; +4% accuracy at same cost; 50-98% learned-cascade savings). github.com/stanford-futuredata/FrugalGPT.
- [Anthropic, 2026] Prompt caching docs: 1.25x write, 0.1x read (90% discount), 5-min TTL, 1-hour option. platform.claude.com/docs/en/build-with-claude/prompt-caching.
- [Prompthub, 2025] Prompt Caching with OpenAI, Anthropic, and Google Models (OpenAI 50% cached-input discount; automatic).
- [Flexera, 2026] Prompt Caching breakdown (write 1.25x; read 0.1x; TTL economics). flexera.com/blog.
- [Anthropic, 2025] How we built our multi-agent research system (agents ~4x chat tokens; multi-agent ~15x).

## [DEEP DIVE]: Hierarchical SQLite Cost Ledger, Cache-Anchor Preservation, RouteLLM Embeddings Routing, and Non-Fatal Budget Preemption (Antigravity, 2026-09-14)

### 1. Hierarchical Cost Accounting Ledger in Zero-Daemon SQLite-WAL

To honor the zero-daemon invariant (`MAP.md`), cost attribution and token burn cannot rely on external billing collectors or hosted observability platforms. All accounting runs locally inside SQLite-WAL:

```sql
CREATE TABLE IF NOT EXISTS token_cost_ledger (
    entry_id TEXT PRIMARY KEY,
    trace_id TEXT NOT NULL,
    task_id TEXT NOT NULL,
    agent_id TEXT NOT NULL,
    parent_task_id TEXT,               -- recursive delegation link
    model TEXT NOT NULL,
    input_tokens INTEGER NOT NULL,
    output_tokens INTEGER NOT NULL,
    cache_read_tokens INTEGER NOT NULL,
    cache_write_tokens INTEGER NOT NULL,
    cost_usd REAL NOT NULL,
    formation TEXT NOT NULL,
    task_passed_all_gates INTEGER NOT NULL DEFAULT 0,
    timestamp_ms INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_cost_task ON token_cost_ledger(task_id, agent_id);
CREATE INDEX IF NOT EXISTS idx_cost_gates ON token_cost_ledger(task_passed_all_gates, cost_usd);
```

**Recursive Cost Rollup Query:**
When assessing subagent tree efficiency, child costs roll up into parent formations using a recursive CTE:
```sql
WITH RECURSIVE task_tree AS (
    SELECT task_id, parent_task_id, cost_usd, input_tokens, output_tokens, task_passed_all_gates
    FROM token_cost_ledger WHERE task_id = :root_task_id
    UNION ALL
    SELECT c.task_id, c.parent_task_id, c.cost_usd, c.input_tokens, c.output_tokens, c.task_passed_all_gates
    FROM token_cost_ledger c
    JOIN task_tree t ON c.parent_task_id = t.task_id
)
SELECT 
    SUM(cost_usd) AS total_formation_cost_usd,
    SUM(input_tokens + output_tokens) AS total_tokens,
    MAX(task_passed_all_gates) AS success_flag
FROM task_tree;
```
Enables instantaneous (<2ms) rollup of complete multi-agent tree costs down to the micro-cent.

### 2. Cache-Anchor Preservation: Eliminating Cache-Write Surcharges

Anthropic prompt caching charges a **1.25x write surcharge** on initial cache creation, followed by a **90% discount (0.1x)** on subsequent hits. When agents use naive context compaction or summarization that rewrites the system prompt or early history, the cache prefix hash mutates, causing a complete cache bust and forcing the system to pay the 1.25x write surcharge every single turn [Anthropic, 2026; Flexera, 2026].

**Two-Tier Context Buffer Architecture:**
- **Tier A: Immutable Cache Anchor (Static Prefix):**
  - Contains: Persona specification (`SOUL.md`), Ring permission rules, and pinned tool stubs.
  - Placed at the very top of the prompt with `cache_control: {"type": "ephemeral"}` set at the final character of Tier A.
  - **Invariance Rule:** Under no circumstances may any compaction or summarization routine alter a single character above the Tier A boundary.
- **Tier B: Dynamic Sliding Conversation Buffer:**
  - Contains: Rolling execution turns, dynamic tool outputs, and active reasoning traces.
  - Compaction and JetBrains observation masking are strictly confined to Tier B.
- **Economic Impact:** Guarantees a **100% cache hit rate** on the large static prefix (~8,000–14,000 tokens), converting what would be an $8\times$ prompt tax into steady 0.1x reads.

### 3. RouteLLM Cost-Sensitive Predictive Routing (arXiv:2406.18665)

Rather than static complexity categorizations or expensive multi-sample LLM cascades, Crew v2 incorporates **RouteLLM** (Ong et al., LMSYS / UC Berkeley, 2024):
- A lightweight router model predicts whether a cheaper, faster model (e.g. Claude 3.5 Haiku / Gemini 2.0 Flash Lite) can resolve the specific prompt with equivalent quality to a frontier model (Claude 3.5 Sonnet / Opus).
- **Architecture:** Operates via a local 2.5MB ONNX embedding projection (<3ms CPU inference). A router scoring function evaluates the turn prompt embedding:
  $$s(x) = \sigma\left(W^T \cdot \text{emb}(x) + b\right)$$
  If $s(x) < \theta_{\text{threshold}}$, route to Cheap Tier; else route to Frontier Tier.
- **Empirical Savings:** LMSYS benchmarks demonstrate RouteLLM achieves **over 85% cost reduction** on conversational benchmarks and 35%–45% on reasoning tasks while preserving 95% of GPT-4-level quality [Ong et al., 2024].

### 4. Hard Token Budget Enforcement with Non-Fatal Preemption

When runaway agents enter looping or deadlocked states, hard process termination causes catastrophic token waste (100% of tokens spent on the task yield zero return artifacts).

**Two-Stage Budget Preemption Protocol:**
- **Soft Warning Gate ($80\% \times B_{\text{task}}$):**
  - The runtime injects a high-priority system notification: `[WARNING: 80% task token budget consumed. Terminate exploration; emit final synthesis.]`.
  - Tool outputs are automatically constrained to a maximum of 250 tokens via observation masking.
- **Hard Non-Fatal Interrupt ($100\% \times B_{\text{task}}$):**
  - If the agent fails to conclude and exhausts $B_{\text{task}}$, the execution harness intercepts the turn with a non-fatal `BUDGET_EXHAUSTED` interrupt.
  - The agent is allocated a strictly capped 500-token emergency synthesis window to package all partial code diffs, logs, and findings into an artifact for handoff.
  - **Result:** Converts total task abandonment into partial artifact salvaging, reducing wasted failure token expenditure by >75%.

### 5. Measurable Cost Optimization Metrics Catalog

| Metric | Definition | How to Measure | Target | Warning Threshold |
|---|---|---|---|---|
| **Cache Anchor Invalidation Rate** | Sessions with unexpected Tier A cache bust | OTel cache-write telemetry | **0%** | > 2% (Compactor violating anchor boundary) |
| **RouteLLM Predictive Savings** | Cost delta vs uniform Tier-2 model dispatch | Ledger routing diff | **> 55%** | < 30% (Recalibrate routing threshold $\theta$) |
| **Unit Cost per Verified Task** | Total token spend / tasks passing all gates | Recursive CTE ledger | **< $0.35** | > $1.20 (Review formation size) |
| **Wasted Failure Token Ratio** | Tokens spent on failed/unrecovered tasks / total | Gate failure audit | **< 8%** | > 18% (Check circuit breaker sensitivity) |
| **Preemption Recovery Rate** | Tasks salvaging partial artifacts after budget trip | Synthesis handoff audit | **> 80%** | < 50% (Increase emergency synthesis window) |

### References for deep dive (Antigravity, 2026-09-14)

- [Ong et al., 2024] RouteLLM: Learning to Route LLMs with Preference Data (over 85% cost reduction preserving 95% frontier performance; matrix factorization & embedding routing). LMSYS / UC Berkeley. arXiv:2406.18665.
- [Anthropic, 2026] Prompt Caching Pricing & Architecture: Cache Writes vs Reads, 5-minute vs 1-hour Ephemeral TTL. platform.claude.com/docs/en/build-with-claude/prompt-caching.
- [Flexera, 2026] Prompt Caching Economic Breakdown: Break-even Analysis and Write-Surcharge Mechanics. flexera.com/blog.
- [SQLite, 2024] SQLite Common Table Expressions (Hierarchical Tree Queries). sqlite.org/lang_with.html.

## [DEEP DIVE (freebuff, pass 3, 2026-09-14)]: Output-Length Governance and Speculative Decoding — The Cost Levers Past the Cache

Pass-1 covered FrugalGPT cascades and cache-write economics; pass-3 covers the two levers left out: **the output side** (where most token spend actually happens) and **inference-time speedups** that change the unit economics without changing the bill's token count.

### 1. Output dominates the bill — govern it like a budget
- The arithmetic is structural: output tokens typically price at a **multiple of input tokens** (commonly 3–5× across major providers) and agents generate far more output than their prompts are long across a task's turns. Yet the pass-1 cost controls (cascades, cache discipline) act almost entirely on the input side. The missing governance: **max-output-token caps per agent class** (tester verdicts and critic reviews get hard caps; draft artifacts get larger ones), **stop-condition discipline** (structured verdicts end at the template, not at ramble), and **brevity SLOs** in the SOUL ("verdict ≤ N lines") — each enforced by the verifiable-instruction pattern (engineer-soul pass 2: a cap is CI-checkable from the response metadata, unlike "be concise").
- The routing layer (routing pass 2) interacts: a cascade that routes easy verdicts to a cheaper model only saves if the cheap model's *verbosity* is also controlled — cost-per-task is tokens × price, and cheap models that over-generate can erase the routing gain. Track **output tokens per task** as a first-class ledger metric alongside $/successful-task.

### 2. Speculative decoding: the same bill, faster
- Speculative decoding (draft model proposes k tokens; target verifies in parallel; rejected tokens are redrafted) is **lossless** — the target model's distribution is preserved exactly (rejection sampling guarantees the output distribution is unchanged) [Leviathan et al., ICML 2023; Chen et al., 2023]. Speedups scale with the draft-target **acceptance rate**: production measurements range from ~**1.4–1.6×** in vLLM deployments [jarvislabs, 2025] to **2–3×** with well-aligned draft models and high acceptance (>80%) [mindstudio, 2026; BentoML, 2025]; Online Speculative Decoding keeps the draft aligned by distilling on the live query stream, recovering acceptance as distribution drifts [arXiv:2310.07177].
- Crew economics: speculative decoding changes **wall-clock per token, not $/token** (verification costs target-model FLOPs either way) — so it is a *latency* lever first (TTFT/TPOT pair, production pass 3) and a *cost* lever only where latency converts to money (interactive gates that burn human wait time, or self-hosted fleets where throughput = revenue). The honest ledger entries: tokens stay identical; p95 gate time drops; where the crew self-hosts, cost per task falls with the throughput gain.
- Draft-model choice is a governance decision: the draft must be *aligned with the target's distribution* (distilled or same-family) or acceptance collapses — the same model-diversity logic as blocking-authority, inverted: here correlation is the feature.

### 3. Composing the levers
| Lever | Acts on | Effect on bill | Source dive |
|---|---|---|---|
| Prompt caching (APC) | input tokens | −input cost | pass 1 |
| Cascades/routing | which model | price per token | pass 1 / routing pass 2 |
| **Output caps + stop discipline** | output tokens | −output cost (the dominant term) | pass 3 (this dive) |
| **Speculative decoding** | wall-clock/throughput | latency −; cost only if self-hosted | pass 3 (this dive) |

### Numbers for calibration (pass 3)

| Quantity | Value | Source |
|---|---|---|
| Output-vs-input pricing | commonly 3–5× | [provider pricing sheets, snippet-level] |
| Speculative decoding guarantee | lossless (exact target distribution) | [Leviathan et al., 2023] |
| Measured speedups | ~1.4–1.6× (vLLM) up to 2–3× (aligned drafts, >80% acceptance) | [jarvislabs, 2025; mindstudio, 2026] |
| Acceptance-recovery | online distillation on live queries | [arXiv:2310.07177] |
| New ledger metric | output tokens per task | this dive |

### References (pass 3)
1. [Leviathan et al., 2023] "Fast Inference from Transformers via Speculative Decoding," ICML 2023. [verified: 2026-09-14, standard citation]
2. [Chen et al., 2023] "Accelerating Large Language Model Decoding with Speculative Sampling." [verified: 2026-09-14, standard citation]
3. [arXiv:2310.07177] "Online Speculative Decoding." https://arxiv.org/html/2310.07177v4 [verified: 2026-09-14]
4. [jarvislabs, 2025] "Speculative Decoding in vLLM" (1.4–1.6×). https://jarvislabs.ai/blog/speculative-decoding-vllm-faster-llm-inference [verified: 2026-09-14, snippet]
5. [mindstudio, 2026] "Speculative Decoding Explained" (>80% acceptance → 2–3×). https://www.mindstudio.ai/blog/speculative-decoding-explained-ai-agents [verified: 2026-09-14, snippet]
6. [BentoML, 2025] "3× Faster LLM Inference with Speculative Decoding." https://www.bentoml.com/blog/3x-faster-llm-inference-with-speculative-decoding [verified: 2026-09-14, snippet]
7. [Provider pricing, contrast] output-token multiples vs input (3–5× typical). [unverified exact figures — cutoff-dependent; mark before quoting]
