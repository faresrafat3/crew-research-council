# Tool Integration and Differentiation Strategy

## Executive Summary
Crew v2 agents share most tools — researcher has web_search, engineer has terminal, but differentiation is not systematic. Some tasks benefit from more specialized toolsets, and uncontrolled tool access creates security risks. Research (2025-2026) shows that tool differentiation improves outcomes when aligned with agent roles, but requires careful access control to prevent privilege escalation. This document specifies a capability-based tool assignment framework with tool result sharing patterns and differentiation measurement.

## Key Findings

- **OWASP AI Agent Security (2026)** identifies tool abuse & privilege escalation as a key risk: agents exploiting overly permissive tools to perform unintended actions. Least-privilege principle must apply to agent tools [OWASP, 2026].
- **Microsoft Agent Governance Toolkit (2025)** implements capability-based tool access: agents request capabilities at runtime, granted based on ring level and task context. Capabilities are scoped, time-limited, and auditable [Microsoft, 2025].
- **MCP (Model Context Protocol, 2025)** provides standardized tool discovery and invocation. Tools self-describe via JSON Schema; agents discover capabilities at connection time. MCP is becoming the standard for tool integration [Oracle, 2025].
- **Tool-Coordination Trade-off (arXiv, 2512.08296, 2025)** shows tool-heavy tasks suffer disproportionately from multi-agent coordination overhead. 16-tool software engineering tasks see efficiency penalties compounding as environmental complexity increases [arXiv, 2512.08296].
- **Stellar Cyber (2026)** reports tool misuse and privilege escalation as the most common agentic threat (520 incidents). The "confused deputy" problem: agents tricked into using tools in unauthorized ways [Stellar Cyber, 2026].

## Detailed Analysis

### Current Failure Modes

1. **No systematic tool differentiation**: Tools assigned ad-hoc, not by role requirements.
2. **No tool access control**: All agents can access all tools (security risk).
3. **No tool result sharing**: Agents duplicate work because they can't see each other's tool outputs.
4. **No capability measurement**: No way to measure whether tool differentiation improves outcomes.
5. **Tool overload**: Agents with too many tools suffer from choice paralysis.

### Capability-Based Tool Assignment

**Principle**: Each agent gets exactly the tools its role requires — no more, no less.

**Tool taxonomy:**

| Tool Category | Tools | Required By |
|---------------|-------|-------------|
| **Read** | read_file, search_files, web_search, web_extract | researcher, architect, critic |
| **Write** | write_file, patch | engineer, razor |
| **Execute** | terminal, process_manage | engineer, tester, completer |
| **Message** | message_agent | All agents |
| **Memory** | memory_read, memory_write | All agents (scoped) |
| **Meta** | ledger_log, verdict_emit | tester, critic, firstmate |
| **Admin** | profile_edit, config_change | firstmate, coach (restricted) |

**Capability levels:**

| Level | Description | Agents |
|-------|-------------|--------|
| 0: None | No tool access | — |
| 1: Read-only | Can read files, search web | researcher, historian |
| 2: Write-scoped | Can write to task directory | engineer, tester, razor |
| 3: Write-shared | Can write to shared directories | architect, completer |
| 4: Execute-sandbox | Can run commands in sandbox | engineer, tester |
| 5: Execute-full | Can run commands without sandbox | — (operator only) |
| 6: Admin | Can modify agent configurations | firstmate (limited) |

### Tool Access Control

**Request-grant pattern (Microsoft Agent Governance Toolkit):**

```python
class ToolRequest:
    agent_id: str
    tool_name: str
    task_id: str
    justification: str
    ring_level: int

class ToolGrant:
    request: ToolRequest
    granted: bool
    scope: str  # "task", "session", "permanent"
    expiry: datetime
    conditions: list[str]
```

**Grant rules:**
1. Agent must have sufficient ring level for the tool.
2. Tool must be in the agent's role-allowed list.
3. Justification must reference current task.
4. Grant is scoped to task (default) or session (elevated).
5. All grants are logged to audit trail.

### Tool Result Sharing

**Problem**: Researcher searches web → finds result. Engineer needs same result → searches again. Duplication wastes tokens and time.

**Solution**: Shared tool result cache with scope.

**Cache scopes:**

| Scope | Visibility | TTL |
|-------|-----------|-----|
| Task | All agents in current task | Task duration |
| Session | All agents in current session | Session duration |
| Crew | All agents in crew | 24 hours |
| Global | All agents | 7 days |

**Cache key**: hash(tool_name + normalized_args)

**Example:**
```
researcher: web_search("pytest coverage best practices") → result_abc
engineer: web_search("pytest coverage best practices") → cache hit, return result_abc
```

**Estimated savings**: 30-50% reduction in duplicate tool calls.

### Measuring Tool Differentiation Effectiveness

**Metric: Tool Utilization Rate per Agent**

```python
tool_utilization = tools_actually_used / tools_available
```

**Target**: > 60% utilization. If < 40%, agent has too many tools (choice paralysis). If > 90%, agent may need more tools.

**Metric: Tool Differentiation Index**

```python
differentiation_index = 1 - (shared_tools / total_tools)
```

**Target**: > 0.5. If < 0.3, agents are too similar (convergence risk).

**Metric: Tool-Outcome Correlation**

```python
correlation = correlation(tool_usage_pattern, task_success)
```

**Target**: Positive correlation (p < 0.05). If no correlation, tool assignment is random.

### Preventing Tool Convergence

**Problem**: Over time, agents start using the same tools regardless of role.

**Anti-convergence measures:**

1. **Role-tool binding**: Each agent has explicit "primary tools" list. Using non-primary tools requires justification.
2. **Tool usage monitoring**: Track per-agent tool usage patterns. Alert if agent uses tools outside its role > 20% of the time.
3. **Periodic review**: Monthly review of tool assignments. Remove unused tools, add missing tools.
4. **Specialization bonus**: Agents are rewarded (via ledger) for using their primary tools effectively.

### Tool Security

**Sandboxed execution (Parallax pattern):**

```python
class ToolSandbox:
    allowed_tools: list[str]
    max_execution_time_s: int
    max_output_size_bytes: int
    network_allowlist: list[str]
    filesystem_scope: str
    
    def execute(self, tool, args):
        if tool not in self.allowed_tools:
            raise PermissionError(f"Tool {tool} not allowed")
        # Execute with resource limits
        # Capture output, truncate if too large
        # Log to audit trail
```

**Output validation:**
- All tool outputs are scanned for PII, credentials, injection patterns.
- Outputs exceeding size limits are truncated.
- External URLs in outputs are checked against allowlist.

## Practical Recommendations

| Recommendation | Implementation | Tools | Threshold |
|----------------|----------------|-------|-----------|
| Capability-based assignment | Role-tool mapping table | Custom policy engine | All agents |
| Tool access control | Request-grant with audit | Microsoft-style toolkit | All tool calls |
| Result sharing | Shared cache with scope | Redis | All repeated queries |
| Utilization monitoring | Track tools used / available | Ledger | > 60% utilization |
| Differentiation measurement | Tool Differentiation Index | Custom metric | > 0.5 |
| Security sandboxing | Per-agent tool sandbox | Parallax-style | All executions |
| Periodic review | Monthly tool assignment audit | Custom | All agents |

## Metrics Catalog

| Metric | Definition | How to Measure | Target | Warning |
|--------|-----------|----------------|--------|---------|
| Tool utilization | Tools used / tools available | Counter | > 60% | < 40% reduce tools |
| Differentiation index | 1 - (shared/total tools) | Calculation | > 0.5 | < 0.3 add differentiation |
| Cache hit rate | Cache hits / total calls | Counter | > 30% | < 10% improve caching |
| Unauthorized access attempts | Blocked tool calls | Counter | 0 | > 0 security incident |
| Tool-outcome correlation | Correlation with success | Statistical | p < 0.05 | No correlation review assignment |
| Duplicate tool calls | Redundant calls | Counter | < 20% | > 40% improve sharing |

## References

1. [OWASP, 2026] AI Agent Security Cheat Sheet: Tool Abuse & Privilege Escalation. cheatsheetseries.owasp.org.
2. [Microsoft, 2025] Agent Governance Toolkit: Capability-Based Access. github.com/microsoft/agent-governance-toolkit.
3. [Oracle, 2025] The Agent Communication Matrix: MCP for Tool Integration. blogs.oracle.com.
4. [arXiv, 2512.08296, 2025] Tool-Coordination Trade-off in Multi-Agent Systems.
5. [Stellar Cyber, 2026] Tool Misuse and Privilege Escalation Incidents. stellarcyber.ai.
6. [Parallax, 2026] Sandboxed Tool Execution. arXiv:2604.12986.

## [DEEP DIVE]: Tool-Count Empirics, Toolformer Filtering, Namespaced Toolsets, and Counterfactual Differentiation Audits (freebuff, 2026-09-13)

### 1. Tool count has measured failure curves — size per-role catalogs accordingly

Tool selection accuracy degrades as catalogs grow and as semantically similar tools are added; reported failure cases include selection accuracy dropping to ~13% on very large tool sets, with degradation starting well before catalog sizes that context windows could technically hold [arXiv:2605.24660, 2026; tianpan.co, 2026; MLQ.ai, 2026]. Galileo formalizes the per-call failure surface as Tool Selection Quality: right tool *and* right arguments [Galileo]. Delta to the spec's utilization heuristic (">60% used, <40% too many"):

- Cap each agent's visible toolset at **≤15 tools** per task context, and audit for *semantic near-duplicates* (two tools whose descriptions embed >0.85 cosine) — duplicates confuse selection more than raw count.
- When a role needs more (the tool-coordination trade-off shows tool-heavy tasks with 16+ tools are where multi-agent overhead bites hardest [arXiv:2512.08296]), use **two-stage retrieval**: a lightweight tool-registry search returns the top-5 relevant tools for the current subtask, and only those enter the model's context. This is the Toolformer lesson inverted: it's not just which tools an agent has, it's which tools it *sees this turn* [Schick et al., 2023].

### 2. Toolformer's helpfulness filter: the principled way to prune a role's toolset

Toolformer determined that an API call is worth keeping if inserting its result at a position *reduces the model's perplexity on the ground-truth continuation* — i.e., the tool's output must carry information the model lacks [Schick et al., 2023]. Adapted to crew tool audits (monthly review, already in spec):

1. For each (agent, tool) pair, replay sampled past tasks where the tool was called.
2. Score: did the tool's output change the downstream decision/answer (counterfactual usefulness), not merely was it invoked?
3. Tools that were invoked but never decision-relevant are removal candidates; tools never invoked AND never decision-relevant are removed outright.

This replaces the spec's utilization-rate proxy (used/available) with a usefulness measure — utilization rewards *calling* tools; Toolformer logic rewards *helpful* calls, which is what tool-outcome correlation is trying to capture.

### 3. Result-sharing cache: reuse needs an invalidation story, or it ships stale facts

The 30-50% savings estimate for duplicate tool calls is plausible but the cache key `hash(tool_name + normalized_args)` hides the hard problem: **staleness**. Web search results, issue-tracker states, and dependency versions change; a 7-day Global-TTL cache of "pytest coverage best practices" is fine, but a cached "latest version of X" is a production incident waiting. Rules:

- Classify tools by *mutability*: static (docs, syntax) → long TTL fine; volatile (versions, prices, statuses) → TTL ≤1h or no cache, and cached hits must be labeled with `fetched_at` so downstream agents can judge freshness (ties to memory-architecture bitemporal fields).
- Cache hits carry the original tool's provenance and can be revalidated by any agent with the tool (write-through, not blind trust) — consistent with the memory two-source corroboration rule.
- Track **stale-hit escape rate** (bugs caused by cached facts invalidated later) in the ledger; >0 sustained = TTL policy too loose.

### 4. Namespacing MCP toolsets per role

With MCP as the tool-exposure layer (comm-protocols deep dive), implement differentiation as *per-role MCP server allowlists* rather than per-agent flags: firstmate/agent profiles bind to named toolset bundles (e.g., `research-web`, `build-execute`, `verify-audit`), each bundle a curated MCP server set with its own permission scope. Benefits: ring transitions (security deep dive) map cleanly to bundle swaps; audit logs record bundle identity, making the Tool Differentiation Index computable from config alone; and the confused-deputy surface shrinks because agents never even see tools outside their bundle (selection-accuracy protection from §1 comes free).

### 5. Counterfactual differentiation audit: the honest measurement

The spec's Tool Differentiation Index (1 - shared/total) measures *assigned* difference, not *behavioral* difference — an agent can hold unique tools and never use them meaningfully. Quarterly audit:

1. For each agent's task sample, recompute outcomes under its actual tool bundle vs. the generic crew-wide bundle (shadow evaluation on replayed tasks — no live disruption).
2. Report Δ(success rate) per role. If Δ ≤ 0 for a role, its specialization is cargo: either reassign the unique tools or admit the role is generic and shrink its ring.
3. This produces the evidence the tool-outcome correlation metric gestures at, with causal direction (bundle → outcome) instead of raw correlation.

### References for deep dive (freebuff, 2026-09-13)

- [Schick et al., 2023] Toolformer: Language Models Can Teach Themselves to Use Tools. arXiv:2302.04761 (NeurIPS 2023; perplexity-reduction helpfulness filter).
- [arXiv:2605.24660, 2026] How Many Tools Should an LLM Agent See? (selection accuracy vs catalog size/similarity).
- [tianpan.co, 2026] The Over-Tooled Agent Problem (selection accuracy ~13% on large tool sets).
- [MLQ.ai, 2026] AI Agent Tool Selection: Why Accuracy Degrades with Tool Count.
- [Galileo] Tool Selection Quality metric (tool + arguments correctness). docs.galileo.ai.
- [arXiv:2512.08296] Towards a Science of Scaling Agent Systems (tool-coordination trade-off, 16+ tool tasks).

## [DEEP DIVE]: Dynamic Toolset Tiering, Lazy Schema Loading, JetBrains Observation Masking, and Zero-Daemon SQLite-WAL Result Caching (Antigravity, 2026-09-14)

### 1. Dynamic Toolset Tiering & Lazy Schema Loading (Speakeasy v2 Architecture)

In static multi-agent architectures, injecting full JSON schemas for 30–50 tools into every reasoning turn consumes 10–15 KB (~2,500–4,000 tokens) per turn, representing 60%–80% of total input prompt token expenditure [Scalekit, 2026; Speakeasy, 2025]. Beyond token cost, large schema contexts degrade tool selection accuracy down to ~13% on dense catalogs [tianpan.co, 2026; MLQ.ai, 2026].

Crew v2 implements **Dynamic Toolset Tiering** via a three-step meta-tool protocol:
- **Core Invariant Toolset:** Each agent role is loaded with only 4 invariant base tools: `search_tools`, `describe_tools`, `execute_tool`, and `complete_turn`, plus 1–2 primary role-specific tools (e.g. `read_file` for researcher; `write_patch` for engineer).
- **The Three-Step Protocol:**
  1. `search_tools(query: str, tags: list[str]) -> list[{name, synopsis}]`: Semantic & keyword retrieval against the local SQLite tool registry (`tools` table), returning concise one-sentence descriptions (<25 tokens total).
  2. `describe_tools(tool_names: list[str]) -> list[JSONSchema]`: Lazily hydrates full JSON schemas only for the specific tools selected for execution in the current turn.
  3. `execute_tool(name: str, arguments: dict) -> ToolResult`: Invokes the validated tool within its sandboxed execution wrapper.
- **Empirical Token Savings:** Speakeasy benchmarks demonstrate that Dynamic Toolsets reduce input token usage by **96.7%** on simple tasks and **91.2%** on complex multi-tool workflows, yielding total token reductions of **90.7%–96.4%** while maintaining a 100% execution success rate across catalogs up to 400 tools [Speakeasy, 2025].
- **Phase-Gated Tool Masking:** Tool access is dynamically masked by workflow lifecycle phase:
  - *Planning Phase:* Mutation tools (`write_patch`, `terminal_exec`) are masked; only read and discovery tools are accessible.
  - *Execution Phase:* Role-specific write and execute tools are active.
  - *Verification Phase:* Code mutation tools are locked; testing, diffing, and audit tools are exposed.

### 2. JetBrains Observation Masking: Halving Context Overhead Without Hallucination Drift

A major architectural anti-pattern is using LLMs to periodically summarize past tool execution traces. Research from JetBrains and TUM (*The Complexity Trap*, arXiv:2508.21433 / NeurIPS 2025) proves that LLM-based context summarization introduces hallucination drift, loses critical stack traces, and increases latency. In contrast, **Deterministic Observation Masking** matches or exceeds raw agent solve rates while halving (~50%) total context token costs.

**Mechanisms:**
- When tool output exceeds a defined budget ($C_{\max} = 600\text{ tokens}$ or 40 lines), the execution harness:
  1. Persists the complete raw output in the local SQLite table `tool_spillover`:
     ```sql
     CREATE TABLE IF NOT EXISTS tool_spillover (
         spillover_id TEXT PRIMARY KEY,
         tool_name TEXT NOT NULL,
         raw_output BLOB NOT NULL,
         line_count INTEGER NOT NULL,
         byte_size INTEGER NOT NULL,
         created_at INTEGER NOT NULL
     );
     ```
  2. Emits an abbreviated bracketed representation preserving the head (first 10 lines) and tail (last 15 lines, where errors/summaries reside):
     ```markdown
     [TOOL_OUTPUT: pytest (exit: 0) - 380 lines omitted (18.4 KB). 
      Head: test_auth.py::test_login PASSED ...
      Tail: 142 passed, 2 warnings in 4.12s
      Full artifact: artifact://tool_spillover/spill_8f91a2]
     ```
  3. The agent retains full causal awareness without paying context-window penalties. If granular lines are required, the agent calls `read_artifact(uri, offset, lines)`.

### 3. Deterministic SQLite-WAL Tool Result Cache with Environmental Fingerprinting

To uphold the DSH zero-daemon invariant (`MAP.md`: no Redis or background services), the crew uses an embedded SQLite-WAL result cache with strict environmental fingerprinting:

```sql
CREATE TABLE IF NOT EXISTS tool_cache (
    cache_key TEXT PRIMARY KEY,
    tool_name TEXT NOT NULL,
    agent_id TEXT NOT NULL,
    scope TEXT NOT NULL CHECK(scope IN ('task', 'session', 'crew', 'global')),
    canonical_args_hash TEXT NOT NULL,
    env_fingerprint TEXT NOT NULL,
    result_payload TEXT NOT NULL,
    created_at INTEGER NOT NULL,
    expires_at INTEGER NOT NULL,
    hit_count INTEGER DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_tool_cache_lookup ON tool_cache(tool_name, canonical_args_hash, env_fingerprint);
```

**Environmental Fingerprinting (Eliminating Stale-Hit Escapes):**
- **Filesystem Tools (`read_file`, `search_files`, `git_diff`):**
  $$\text{env\_fingerprint} = \text{sha256}(\text{git\_head\_sha} \parallel \text{file\_mtime})$$
  Any file modification or commit instantly changes the fingerprint, rendering cached reads obsolete by construction without requiring expensive active cache invalidation sweeps.
- **Network / Web Tools (`web_search`, `web_extract`):**
  - *Static Tier (TTL = 7 days):* Language specifications, standard library docs, RFCs.
  - *Semi-Static Tier (TTL = 24 hours):* Architecture guides, design patterns, established library best practices.
  - *Volatile Tier (TTL = 15 minutes or no-cache):* Dependency vulnerability advisories, git remote tags, issue tracker statuses.

### 4. Irrelevance Detection & Tool Call Preconditions (BFCL v4 Compliance)

The Berkeley Function Calling Leaderboard (BFCL v4) identifies **hallucinatory / premature tool invocation** (calling external tools when the answer is already present in prompt context or when no tool call is justified) as a primary driver of agent failure [Patil et al., 2024; BFCL v4, 2026].

**Tool Precondition Assertion Gate:**
Prior to generating any tool call payload, the model must satisfy a lightweight precondition check in its reasoning trace:
```markdown
<precondition_check>
Tool Needed: git_log
Information Missing: Recent commit authors for src/auth/
Context Sufficiency: NOT in local conversation history
Action: INVOCATION_REQUIRED
</precondition_check>
```
If `Context Sufficiency == PRESENT`, the runtime intercepts the turn and instructs the model to answer directly from context, eliminating unnecessary tool roundtrips.

### 5. Measurable Tool Differentiation Metrics Catalog

| Metric | Definition | How to Measure | Target | Warning Threshold |
|---|---|---|---|---|
| **Tool Schema Overhead Ratio** | Schema tokens / total prompt tokens | Turn token accounting | **≤ 12%** | > 25% (Trigger lazy schema tiering) |
| **Lazy Hydration Latency** | Time to search and hydrate tool schema | SQLite query timer | **< 25ms** | > 60ms (Rebuild SQLite tool indices) |
| **Observation Masking Compression** | Raw bytes vs context bytes injected | `tool_spillover` byte diff | **> 65%** | < 30% (Spillover threshold too high) |
| **Cache Stale Escape Rate** | Stale cache hits causing downstream retries | Failure ledger | **0 incidents** | > 0 (Tighten environmental fingerprint) |
| **BFCL Irrelevance Precision** | Correct tool refusals / total unneeded prompts | Verification eval suite | **> 95%** | < 85% (Enforce precondition assertion) |

### References for deep dive (Antigravity, 2026-09-14)

- [Speakeasy, 2025] Reducing MCP Token Usage by 100x — Dynamic Toolsets v2 (96.7% input token reduction, three-step search/describe/execute protocol, constant context scaling). speakeasy.com/blog/how-we-reduced-token-usage-by-100x-dynamic-toolsets-v2.
- [arXiv:2508.21433 / NeurIPS 2025] The Complexity Trap: Simple Observation Masking Is as Efficient as LLM Summarization for Agent Context Management. JetBrains Research & Technical University of Munich. arxiv.org/abs/2508.21433.
- [Scalekit, 2026] Token-Efficient Tool Calling: Auth Overhead in Agent Context (10–15 KB schema overhead per turn on 40-tool servers). scalekit.com/blog/token-efficient-tool-calling.
- [BFCL v4, 2026] Berkeley Function Calling Leaderboard V4: Multi-Turn, Multi-Step & Irrelevance Detection Evaluation. gorilla.cs.berkeley.edu; openreview.net/forum?id=TheBFCL.
- [Patil et al., 2024] The Berkeley Function Calling Leaderboard (BFCL). ICML / NeurIPS 2024.

## [DEEP DIVE (freebuff, pass 3, 2026-09-14)]: Stateful Tool Evaluation — BFCL V3 and the Shift from Single-Call Accuracy to State Verification

Pass-1 covered tool-count empirics and Toolformer filtering; Antigravity's pass-2 covered tiering and schema loading. Pass-3 covers the evaluation layer: how to measure whether an agent can *use* a toolset through a multi-step task — the capability the crew actually assigns tools for.

### 1. The state-verification turn in tool benchmarks
- BFCL V3 (Berkeley Function-Calling Leaderboard, 2024-09) introduced **multi-turn and multi-step function calling**: the model loops over tools — listing a directory, trying to write a file that isn't there, listing again — and the metric changed with the task: instead of AST-matching parameter pairs, V3 **verifies the actual state of the API system (file systems, booking systems) after the model's calls** [BFCL V3 blog, 2024]. State-based evaluation is the decisive move: it cannot be fooled by a plausible-looking call that does the wrong thing, the same insight as the council's state-based RED witnessing.
- ToolSandbox (Apple, 2024) makes the same turn explicit and adds the dimensions the crew cares about: **state-dependent interactions** (tool outcomes depend on prior tool outcomes), **implicit user preferences** resolved over the conversation, and **dynamic tool availability** (tools appear/disappear mid-task) — where it shows state-of-the-art LLMs degrade sharply relative to static single-turn tool use [Lu et al., arXiv:2408.04682]. BFCL's later V4 adds agentic scenarios on top [BFCL V4, 2026].
- The through-line for the crew's tool-assignment audits (pass 1's counterfactual differentiation): a tool assignment is only proven useful if the agent completes **stateful** tasks with it — single-call benchmark numbers overstate capability exactly where crew tasks live (multi-step, state-dependent, mid-task tool-set changes).

### 2. Protocol for the crew's tool-competence gate
1. **Task-level, state-checked evals:** per assigned toolset, run scripted multi-step scenarios and verify end-state (not call trace): files actually written, rows actually committed, messages actually sent. Borrow BFCL V3's state-comparison evaluator shape.
2. **Include the hard dimensions:** at least one scenario per assigned toolset with (a) implicit-preference resolution (do what the REQ implies, not literally says), (b) dynamic availability (a tool fails mid-task; reroute or escalate), (c) state-dependence (step k+1 depends on step k's result). ToolSandbox's result says these are where capability actually breaks.
3. **Gate on the state-checked pass rate**, not on single-call accuracy: assignment changes (tool tiering, new MCP servers) must clear the same shadow-then-block rollout as SOUL changes (implementation-roadmap pass 2).
4. **Failure telemetry feeds tool differentiation:** errors where the agent called the right tool with wrong state assumptions (vs wrong tool) are *differentiation* signals — they argue for narrower toolsets or better schemas (pass 1's namespacing), not more prompting.

### Numbers for calibration (pass 3)

| Quantity | Value | Source |
|---|---|---|
| BFCL V3 release | 2024-09-19; multi-turn + multi-step, state-based eval | [BFCL V3 blog] |
| Evaluation change | AST param-match → **system-state verification** | same |
| ToolSandbox dimensions | state-dependent, implicit-preference, dynamic availability | [arXiv:2408.04682] |
| Finding on hard dimensions | SOTA LLMs degrade sharply vs static single-turn | same |
| BFCL V4 | adds agentic scenarios | [BFCL V4, 2026] |

### References (pass 3)
1. [BFCL V3, 2024] "BFCL V3: Multi-Turn & Multi-Step Function Calling," Berkeley Gorilla. https://gorilla.cs.berkeley.edu/blogs/13_bfcl_v3_multi_turn.html [verified: 2026-09-14]
2. [Lu et al., 2024] "ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use," arXiv:2408.04682. [verified: 2026-09-14, standard citation]
3. [BFCL V4, 2026] Berkeley Function Calling Leaderboard V4. https://gorilla.cs.berkeley.edu/leaderboard.html [verified: 2026-09-14, snippet]
4. [Patil et al.] "The Berkeley Function Calling Leaderboard (BFCL)," (V1/V2; ICML 2025). [verified: 2026-09-14, standard citation]
5. Cross-refs: tool-differentiation pass 1 (tool-count empirics, Toolformer, counterfactual audits); Antigravity pass 2 (tiering, lazy schemas); testing-framework pass 2 (shadow rollout); tdd-protocol pass 1 (state-machine witnessing).
