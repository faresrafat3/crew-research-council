# Multi-Agent Memory and Knowledge Management

## Executive Summary
Crew v2 has no systematic memory — each agent starts fresh, causing repeated research, lost context, and inability to learn from past failures. State-of-the-art multi-agent memory systems use hierarchical graph structures (G-Memory, 2025) or brain-inspired subsystems (BMAM, 2026) to enable cross-trial learning. This document proposes a four-tier memory architecture (per-task, per-agent, per-crew, cross-crew) with role-aware retrieval, rate-distortion compaction, and EWC-inspired catastrophic forgetting prevention, improving on Crew v2's current zero-memory baseline.

## Key Findings

- **G-Memory (NeurIPS 2025)** implements a three-tier graph hierarchy: insight graph (abstracted lessons), query graph (task metadata), interaction graph (raw trajectories). It improves MAS success rates by up to 20.89% and knowledge QA by 10.12% without framework modifications [G-Memory, 2025].
- **BMAM (ACL Findings 2026)** decomposes memory into episodic (timeline-indexed traces), semantic (knowledge graph), salience-aware (importance-weighted consolidation), and prefrontal (query routing + 10-item working buffer). Achieves 78.45% on LoCoMo, outperforming seven baselines. "Soul Portability Test" shows 87.5% identity integrity across export-clear-restore [BMAM, 2026].
- **LatentMem (2025)** addresses memory homogenization and information overload with a learnable memory composer that distills raw trajectories into fixed-length, role-aware latent memories. Achieves 19.36% performance gain over vanilla settings [LatentMem, 2025].
- **AMA (ACL Findings 2026)** uses four collaborating agents (Constructor, Retriever, Judge, Refresher) to manage memory across granularities (raw text, fact knowledge, episode) with consistency verification. Reduces token consumption by ~80% vs full-context methods [AMA, 2026].
- **Memory Compaction (arXiv 2607.08032, 2026)** unifies KV cache, prompt, architectural, and agent memory compaction under a rate-distortion objective: maximize I(Z;Y|Q) under budget B. Irreversible compaction causes super-linear error growth; reversible retrieval-backed memory stays flat [Colaco & Lahjouji, 2026].
- **MemoryAgentBench (2025)** identifies four memory competencies: Accurate Retrieval, Test-Time Learning, Long-Range Understanding, Selective Forgetting (resolving contradictions) [MemoryAgentBench, 2025].
- **Catastrophic Forgetting** in agent memory is mitigated by Elastic Weight Consolidation (EWC), which penalizes changes to important parameters while allowing new learning — adapted for memory stores as importance-weighted write protection [Huszár, 2018; Multiple Memory Systems, 2025].

## Detailed Analysis

### The Memory Hierarchy Problem

Crew v2's memory failure mode is structural: agents have no persistent state across tasks. The librarian curates solved cases but retrieval is manual. firstmate tracks expertise in JSONL but it's not indexed for fast lookup. This causes:
1. Repeated research: researcher re-searches topics already investigated.
2. Lost context: engineer forgets design decisions from previous tasks.
3. No organizational learning: escapes are tracked but not converted to patches.
4. Identity drift: agent personality erodes across sessions (BMAM's "soul erosion").

### Four-Tier Memory Architecture (Crew v2 Adaptation)

Based on G-Memory's three tiers and adding cross-crew scope for organizational learning:

```
┌─────────────────────────────────────────────────────────┐
│  TIER 4: Cross-Crew Knowledge (Knowledge Graph)         │
│  - Shared across all crews/crews in the organization   │
│  - Consolidates insights from multiple crews           │
│  - Updated weekly via salience-weighted consolidation  │
├─────────────────────────────────────────────────────────┤
│  TIER 3: Per-Crew Memory (Insight Graph)               │
│  - Crew v2's organizational memory                     │
│  - Stores: lessons learned, recurring patterns,        │
│    agent-specific quirks, formation effectiveness      │
│  - Updated after each task via distillation            │
├─────────────────────────────────────────────────────────┤
│  TIER 2: Per-Agent Memory (Role-Aware Latent)          │
│  - Agent-specific distilled memories                   │
│  - engineer: coding patterns, past bugs, style         │
│  - researcher: search strategies, trusted sources      │
│  - tester: common failure modes, oracle violations     │
│  - Updated per-task, filtered through agent profile    │
├─────────────────────────────────────────────────────────┤
│  TIER 1: Per-Task Memory (Interaction Graph)           │
│  - Raw task trajectories and messages                  │
│  - Episodic: timeline-indexed interaction traces       │
│  - Semantic: facts extracted from task execution       │
│  - Updated in real-time during task execution          │
└─────────────────────────────────────────────────────────┘
```

**Tier 1 — Per-Task Memory (Interaction Graph):**
- Stores raw message traces as a graph: nodes = agent utterances, edges = temporal/causal links.
- Episodic encoding: each task gets a timeline-indexed entry with entities, events, timestamps [BMAM, 2026].
- Semantic encoding: facts extracted from task execution (S-V, S-V-O, S-V-C, S-V-O-O, S-V-O-C patterns) [AMA, 2026].
- Capacity: all raw traces for current task (purged after compaction into Tier 2/3).
- Retrieval: bi-directional traversal from query graph to interaction graph [G-Memory, 2025].

**Tier 2 — Per-Agent Memory (Role-Aware Latent):**
- Learnable memory composer distills raw trajectories into fixed-length latent memories conditioned on agent role profiles [LatentMem, 2025].
- Each agent type has a dedicated memory profile that filters and weights stored information.
- engineer memory profile weights: code patterns > architectural decisions > testing issues.
- researcher memory profile weights: source quality > search queries > findings.
- Prevents memory homogenization: agents with different roles get different memories [LatentMem, 2025].

**Tier 3 — Per-Crew Memory (Insight Graph):**
- Abstracted, generalizable insights distilled from completed tasks.
- Insight format: {pattern, evidence, confidence, tasks_ref, agents_involved}.
- Updated via summarization function that identifies recurring patterns across tasks [G-Memory, 2025].
- Example: "Engineer forgets tests on Friday afternoons" → insight triggers proactive tester activation.

**Tier 4 — Cross-Crew Knowledge (Organizational Graph):**
- Aggregates insights from multiple crews/organizations.
- Stored as a knowledge graph with entity-relation-entity triples.
- Updated weekly via consolidation pipeline: cluster similar insights, merge evidence, prune outdated.
- Read-only for individual crews; write access requires operator approval.

### Memory Compaction (Rate-Distortion View)

Per Colaco & Lahjouji (2026), the compaction operator C_θ: H → Z maximizes:
  I(Z; Y | Q) subject to rate(Z) ≤ B

Where:
- I(Z; Y | Q) = mutual information between compact memory Z and task outcome Y given query Q
- rate(Z) = memory size in appropriate currency (tokens for agent memory, bytes for vector store)
- B = budget (token limit, storage limit)

**Compaction patterns by tier:**

| Tier | Budget (B) | Method | Reversibility |
|------|------------|--------|---------------|
| 1→2 | 500 tokens/agent/task | Role-aware distillation (LatentMem) | Reversible: raw traces retained for 7 days |
| 2→3 | 200 tokens/agent/task | Insight extraction (G-Memory summarization) | Irreversible: raw interactions purged |
| 3→4 | 1000 tokens/crew/week | Knowledge graph merge | Irreversible: source tasks anonymized |

**Critical insight:** Irreversible compaction causes super-linear error growth in end-task performance; reversible, retrieval-backed memory stays flat [Colaco & Lahjouji, 2026]. Therefore:
- Tier 1→2 compaction must retain raw traces for at least 7 days (rollback window).
- Tier 2→3 compaction must link insights back to source tasks (audit trail).
- Tier 3→4 compaction merges insights but preserves source references.

**Compaction triggers:**
- Tier 1→2: task completion + 24h cooling period (allow post-task corrections).
- Tier 2→3: weekly batch job (every Sunday 3 AM UTC).
- Tier 3→4: monthly batch job (first of month).

### Retrieval-Augmented Generation for Agents

**Retrieval pipeline (per BMAM [2026] + AMA [2026]):**

1. **Query routing** (Prefrontal component): classify incoming query along dimensions (temporal, identity, preference, factual) to determine which memory subsystems to consult.
2. **Coarse retrieval**: similarity search over vector store (cosine similarity, top-k=20).
3. **Hierarchical traversal**: upward (query → insight graph) for generalizable lessons; downward (query → interaction graph) for specific trajectories.
4. **Relevance filtering** (AMA Judge): discard memories with relevance score < 0.7; trigger retry if insufficient evidence.
5. **Conflict detection** (AMA Judge): identify contradictions; if found, invoke Refresher to update outdated entries.
6. **Selective forgetting** (MemoryAgentBench): when new evidence contradicts old, overwrite prior facts (prioritize newest fact).

**Retrieval triggers:**
- Per task start: retrieve relevant Tier 2 (agent) + Tier 3 (crew) memories.
- Per agent activation: retrieve agent-specific Tier 2 profile.
- Per message: optional Tier 1 retrieval for real-time context (disabled by default; enabled for complex tasks).

**Retrieval size budget:**
- Tier 1: max 1000 tokens of raw trajectory.
- Tier 2: max 500 tokens of agent profile.
- Tier 3: max 300 tokens of crew insights.
- Tier 4: max 200 tokens of cross-crew knowledge.
- Total: max 2000 tokens per retrieval event (well within context window).

### Preventing Catastrophic Forgetting

**Three mechanisms adapted from EWC [Huszár, 2018] and memory research:**

1. **Importance-weighted write protection**: Each memory entry has an importance score I(entry). Writes that would modify high-I entries require higher confidence threshold. Prevents important patterns from being overwritten by noise.

2. **Elastic consolidation**: After each task, update memory with:
   - New entries: importance initialized to 0.5.
   - Reinforced entries (used successfully): importance += 0.1, max 1.0.
   - Contradicted entries: importance -= 0.3, min 0.0 (pruned at 0.1).

3. **Periodic replay**: Weekly, replay 10 randomly selected past tasks to reinforce memory traces. Analogous to hippocampal replay in neuroscience.

**Anti-forgetting rules:**
- Tier 3 insights can only be deleted by operator (never auto-pruned).
- Tier 2 agent profiles must retain at least 50 entries per agent (even if low importance).
- Tier 1 raw traces are retained for 7 days minimum (enables rollback and audit).

### Memory Access Control

| Tier | Read Access | Write Access | Audit |
|------|-------------|--------------|-------|
| 1 (Per-Task) | All agents in task | Auto (message trace) | Full |
| 2 (Per-Agent) | Agent itself + firstmate | Auto (distillation) + agent self-edit | Full |
| 3 (Per-Crew) | All crew members | Auto (weekly) + operator | Full |
| 4 (Cross-Crew) | All crews (read-only) | Operator only | Full |

### Implementation Stack

| Component | Tool | Justification |
|-----------|------|---------------|
| Vector store | ChromaDB (embedded) | Zero-config, local, fast enough for 81-agent crew |
| Graph store | NetworkX → Neo4j (scale) | NetworkX for prototype; Neo4j for production scale |
| Embedding model | text-embedding-3-small | Cheap, fast, good enough for retrieval |
| Distillation | LLM summarization | Extract insights from raw traces |
| Importance scoring | Learned (init: heuristic) | Start with heuristic; train on task outcomes |
| Compaction scheduler | Cron (weekly/monthly) | Tier 2→3 and 3→4 batch jobs |

## Practical Recommendations

| Recommendation | Implementation | Tools | Threshold |
|----------------|----------------|-------|-----------|
| Tier 1 interaction graph | Store raw message traces per task | ChromaDB + SQLite | All tasks |
| Tier 2 per-agent latent | Distill per-task traces into agent profiles | LatentMem-style composer | 500 tokens/agent |
| Tier 3 insight graph | Weekly extraction of patterns from Tier 2 | G-Memory summarization | 200 tokens/agent/week |
| Tier 4 cross-crew KG | Monthly merge of Tier 3 insights | Knowledge graph merge | 1000 tokens/crew/month |
| Retrieval pipeline | Bi-directional traversal + relevance filter | Prefrontal router + Judge | Max 2000 tokens/query |
| Catastrophic forgetting | Importance-weighted write + EWC consolidation | Heuristic init → learned | Min 50 entries/agent |
| Compaction reversibility | Retain raw Tier 1 for 7 days; link Tier 2→3 to sources | Cron + TTL | 7-day TTL on Tier 1 |
| Selective forgetting | Judge detects contradictions; prioritize newest | AMA-style Judge | Overwrite on conflict |

## Metrics Catalog

| Metric | Definition | How to Measure | Target | Warning |
|--------|-----------|----------------|--------|---------|
| Retrieval recall | Relevant memories retrieved / total relevant | Benchmark queries | >90% | <80% review embedding model |
| Retrieval precision | Relevant memories / total retrieved | Benchmark queries | >85% | <70% tighten relevance filter |
| Compaction ratio | Compressed size / original size | Token count | <30% | >50% losing too much info |
| Forgetting rate | Lost important memories / total important | Weekly audit | <5% | >10% raise importance weights |
| Insight utility | Tasks where insight was used / total tasks | Ledger tracking | >30% | <10% improve extraction |
| Memory homogeneity | Similarity between agent profiles | Cosine similarity | <0.6 | >0.8 role drift |
| Retrieval latency | Time to retrieve + filter | Timer | <500ms | >2s optimize index |
| Storage per agent | Memory entries per agent | DB count | 50-500 | >1000 compact Tier 2 |
| Soul erosion score | Personality drift across sessions | BMAM-style portability test | >80% integrity | <70% reinforce Tier 2 |
| Cross-crew transfer | Insights adopted from other crews | Usage tracking | >5/quarter | 0 increase integration |

## References

1. [G-Memory, 2025] G-Memory: Tracing Hierarchical Memory for Multi-Agent Systems. NeurIPS 2025. github.com/bingreeky/GMemory.
2. [BMAM, 2026] BMAM: Brain-inspired Multi-Agent Memory Framework. ACL Findings 2026. github.com/innovation64/BMAM.
3. [LatentMem, 2025] LatentMem: Learnable Multi-Agent Memory via Latent Representations. arXiv:2602.03036.
4. [AMA, 2026] AMA: Adaptive Memory via Multi-Agent Collaboration. ACL Findings 2026.
5. [Colaco & Lahjouji, 2026] What to Keep, What to Forget: A Rate–Distortion View of Memory Compaction in LLMs and Agents. arXiv:2607.08032.
6. [MemoryAgentBench, 2025] Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions. arXiv:2507.05257.
7. [Huszár, 2018] Elastic Weight Consolidation. DeepMind / Imperial College London.
8. [Multiple Memory Systems, 2025] Multiple Memory Systems for Enhancing the Long-term Memory of Agent. arXiv:2508.15294.
9. [CrewAI, 2025] How we built Cognitive Memory for Agentic Systems. blog.crewai.com.
10. [IBM, 2025] What Is AI Agent Memory? IBM Think.

## [DEEP DIVE]: Production Memory Systems, Context Rot, Sleep-Time Consolidation, Memory Poisoning, and Benchmark Validation (freebuff, 2026-09-13)

### 1. Production memory systems validate the four-tier design — and supply the exact mechanics

Three production-grade systems independently converged on tiered memory, and each maps onto one crew tier:

- **Mem0 (arXiv:2504.19413, ECAI 2025)** runs a two-phase pipeline: an *extraction phase* (LLM extracts candidate memories from the recent exchange, asynchronously) and an *update phase* where an LLM decides per candidate: ADD / UPDATE / DELETE / NOOP against similar existing memories. Results: +26% accuracy over full-context OpenAI baselines, **91% lower p95 latency, >90% token savings**; the graph variant Mem0g adds ~2% accuracy over Mem0 at ~1.7x p95 latency [Mem0, 2025]. This is exactly the Tier 1→2 compaction operation — adopt the four update verbs as the compaction operator's decision set, and run extraction **asynchronously** (never in the task's critical path).
- **Zep/Graphiti (arXiv:2501.13956)** uses a *bi-temporal* knowledge graph: every edge carries `valid_at` (when true in the world) and `invalid_at` (when it stopped being true), separate from ingestion time. An LLM extract-step **invalidates** contradicted edges rather than deleting them — history stays queryable, current state stays clean. Results: up to **+18.5% accuracy on LongMemEval with 90% latency reduction** vs full-context baselines; up to +11.6% on DMR [Zep, 2025]. This is the concrete mechanism for Tier 3/4 "selective forgetting": replace the spec's "overwrite on conflict" with *edge invalidation* — mark the old insight `invalid_at = now`, never delete.
- **Letta/MemGPT** formalizes *memory blocks*: bounded in-context blocks (core memory, edited by the agent itself via tools) plus external archival/recall stores [Letta, 2025]. This justifies Tier 2's shape: per-agent profile = a fixed set of named blocks with hard character limits, edited by the agent, not by an invisible batch job.

**Delta to the architecture:** Tier 1→2 compaction gets the Mem0 four-verb operator (async); Tier 3/4 contradictions get Zep-style edge invalidation with bitemporal fields; Tier 2 becomes explicit named blocks with size caps.

### 2. Context rot: the empirical reason retrieval budgets are accuracy-critical, not just cost-saving

Chroma's context-rot study tested 18 state-of-the-art models (GPT-4.1, Claude-4 families, Gemini 2.5, Qwen, Gemma) on repetitive/simple synthetic tasks and found performance **degrades as input tokens grow even when nothing else changes** — degradation worsens with task complexity, grows with irrelevant "distractor" content, and needle position effects are non-uniform and model-specific [Chroma, 2025]. This converts the spec's 2000-token retrieval budget from a cost heuristic into an *accuracy* requirement: every extra retrieved token risks degrading the very task the memory was meant to help. Practical consequence: the budget stays at 2000 tokens; raising it requires a measured win on the benchmark below, per model, not a default assumption that "more context = better."

### 3. Sleep-time compute: restructure compaction from cron schedule to idle-time agents

Sleep-time compute lets a model "think" offline about contexts before queries arrive: the same accuracy is reached with **~5x less test-time compute**; scaling sleep-time compute adds up to **+13% (Stateful GSM-Symbolic) and +18% (Stateful AIME)** accuracy; amortized across multiple queries per context, average cost per query drops **2.5x**; efficacy correlates with how predictable the queries are [Lin et al., 2025]. Letta operationalizes this as sleep-time agents that **rewrite other agents' memory state** during idle periods [Letta, 2025].

**Delta to the architecture:** replace the "weekly Sunday 3 AM" Tier 2→3 batch with *idle-triggered* sleep-time agents — whenever a queue goes idle (see communication-protocols backpressure metrics), a sleep agent distills that agent's recent traces. Also add pre-task priming: before firstmate dispatches, a sleep agent pre-computes the top-3 relevant insights per assignee (queries are highly predictable per task type, which is the regime where sleep-time compute works best [Lin et al., 2025]). Cost note: sleep tokens run in batch/off-peak lanes at BULK priority; they buy down latency-critical STANDARD-lane tokens at a measured 2.5-5x ratio [Lin et al., 2025].

### 4. Memory poisoning: the threat model the original spec missed

- **Agent Poisoning (arXiv:2409.20283)** demonstrated persistent memory poisoning: poisoning **<0.15% of memory** achieves >50% backdoor success rate *persistently across sessions* — the poisoned entry is few-shot context for future retrievals [Zeng et al., 2024].
- **Unit42 (Oct 2025)** showed indirect prompt injection can write injected instructions into long-term memory where they persist and later trigger exfiltration [Unit42, 2025].
- **Systematic study (arXiv:2606.04329)** catalogs four memory *write channels* and nine structural poisoning mechanisms; **MemPoison (arXiv:2605.29960)** plants trojans through memory-sharing mechanisms with attack success rates up to **0.95** [Chen et al., 2026].

Defenses, mapped onto the existing tiers (all implementable without new infrastructure):

| Defense | Mechanism | Tier |
|---|---|---|
| Provenance mandatory | Every entry stores {source_task, agent, tool, timestamp}; entries without provenance are unqueryable | 1-4 |
| Two-source corroboration | Tier 3/4 insights stay *quarantined* until two independent agents derive the same insight from different tasks | 3-4 |
| Write rate limits | Per-agent memory-write budget via the existing token bucket (e.g., 20 writes/hour) — blunts flood-poisoning | 1-2 |
| Invalid-not-delete | Zep-style edge invalidation keeps poison visible and auditable for rollback instead of silently overwriting | 3-4 |
| Weekly provenance audit | The existing "periodic replay" doubles as a poison sweep: re-derive sampled insights from cited sources; mismatch → invalidate upstream | 2-3 |

The importance-weighted write protection already specified [Council OUTPUT, 2026] blocks *accidental* overwrites but not *malicious inserts* — poison enters as new high-relevance entries, which is why corroboration + provenance are the load-bearing controls.

### 5. Benchmark validation plan: hold the memory system to LongMemEval

**LongMemEval (arXiv:2410.10813, ICLR 2025)** is the standard: 500 questions over seven question types testing five abilities — information extraction, multi-session reasoning, temporal reasoning, knowledge updates, and *abstention* (refusing to answer what isn't in memory) [Wu et al., 2024]. Its key operating finding: even strong long-context models lose **more than 30% accuracy** as the haystack expands from 2 hours to 7 days of interaction [Wu et al., 2024] — which is the baseline case our memory layer must beat.

**Crew v2 validation protocol (monthly regression gate):**
1. Run LongMemEval-S (500 questions) against the crew's memory stack with 10 representative task-history replays as the haystack.
2. Report accuracy overall + per ability; the five abilities map 1:1 to crew failure modes already observed (e.g., knowledge updates = stale API facts researcher re-cites; abstention = fabricating "past incidents" that never happened).
3. Pass gate: memory-augmented accuracy ≥ no-memory baseline **+10 points**, and retrieval latency within the existing <500ms target. Below that, the memory system's complexity is not paying for itself.
4. Track MemoryAgentBench's four competencies (accurate retrieval, test-time learning, long-range understanding, selective forgetting) as the per-quarter drill [MemoryAgentBench, 2025].

### References for deep dive

- [Mem0, 2025] Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory. arXiv:2504.19413 (ECAI 2025). github.com/mem0ai/mem0.
- [Zep, 2025] Rasmussen et al. Zep: A Temporal Knowledge Graph Architecture for Agent Memory. arXiv:2501.13956. github.com/getzep/graphiti.
- [Letta, 2025] Memory Blocks / Agent Memory. letta.com/blog/memory-blocks; letta.com/blog/agent-memory.
- [Lin et al., 2025] Sleep-time Compute: Beyond Inference Scaling at Test-time. arXiv:2504.13171. github.com/letta-ai/sleep-time-compute.
- [Chroma, 2025] Hong et al. Context Rot: How Increasing Input Tokens Impacts LLM Performance. research.trychroma.com/context-rot.
- [Zeng et al., 2024] Zeng, Y. et al. How to Steal an LLM Agent? (Agent Poisoning: memory poisoning, <0.15% poison → persistent backdoor). arXiv:2409.20283.
- [Unit42, 2025] When AI Remembers Too Much: indirect prompt injection poisons long-term agent memory. unit42.paloaltonetworks.com, Oct 2025.
- [Chen et al., 2026] A Systematic Study of Memory Poisoning Attacks in LLM-based Agents. arXiv:2606.04329; MemPoison (Hijacking Agent Memory). arXiv:2605.29960.
- [Wu et al., 2024] LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory. arXiv:2410.10813 (ICLR 2025). github.com/xiaowu0162/LongMemEval.
- [MemoryAgentBench, 2025] Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions. arXiv:2507.05257.
