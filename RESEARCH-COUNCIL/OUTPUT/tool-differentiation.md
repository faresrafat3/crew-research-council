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

### References for deep dive

- [Schick et al., 2023] Toolformer: Language Models Can Teach Themselves to Use Tools. arXiv:2302.04761 (NeurIPS 2023; perplexity-reduction helpfulness filter).
- [arXiv:2605.24660, 2026] How Many Tools Should an LLM Agent See? (selection accuracy vs catalog size/similarity).
- [tianpan.co, 2026] The Over-Tooled Agent Problem (selection accuracy ~13% on large tool sets).
- [MLQ.ai, 2026] AI Agent Tool Selection: Why Accuracy Degrades with Tool Count.
- [Galileo] Tool Selection Quality metric (tool + arguments correctness). docs.galileo.ai.
- [arXiv:2512.08296] Towards a Science of Scaling Agent Systems (tool-coordination trade-off, 16+ tool tasks).
