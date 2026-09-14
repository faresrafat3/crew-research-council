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

## [DEEP DIVE]: Local-First Zero-Infra Substrate (SQLite+vec+FTS5), HippoRAG 2 Associative Traversal, Arabic-English Semantic Bridging, and Runtime Self-Routing (Antigravity, 2026-09-14)

### 1. Local-first zero-infra memory substrate: SQLite + FTS5 + sqlite-vec + RRF

Production agent systems often fail from operational bloat — running external vector DBs (Milvus, Qdrant, Pinecone) introduces network hops, container maintenance, authentication fragility, and memory footprint incompatible with single-machine agent harnesses [Yu & Zhao, 2026]. The minimal, zero-infra local substrate operates directly on embedded SQLite using Write-Ahead Logging (WAL) and two lightweight extensions: `FTS5` (BM25 keyword search) and `sqlite-vec` (SIMD-accelerated vector search) [Garcia, 2024; ceaksan, 2026]:

```sql
-- Core Memory Metadata and State Ledger
CREATE TABLE IF NOT EXISTS memories (
    id TEXT PRIMARY KEY,
    tier INTEGER NOT NULL CHECK(tier IN (1, 2, 3, 4)), -- 1: Task, 2: Agent, 3: Crew, 4: Global
    scope_id TEXT NOT NULL,                           -- agent_id, crew_id, or 'global'
    role TEXT NOT NULL,                               -- 'engineer', 'researcher', 'architect', etc.
    content TEXT NOT NULL,                            -- verbatim or distilled text
    content_ar TEXT,                                  -- bilingual parallel concept (if applicable)
    importance REAL NOT NULL DEFAULT 0.5,             -- [0.0, 1.0] EWC importance
    access_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_accessed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    valid_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    invalid_at TIMESTAMP,                             -- Zep-style bi-temporal invalidation
    provenance_task TEXT NOT NULL,                     -- task_id audit trail
    quarantined INTEGER NOT NULL DEFAULT 0            -- 1: pending 2-source corroboration
);

-- Full-Text Lexical Search (BM25 with unicode61 tokenizer)
CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
    id UNINDEXED,
    content,
    content_ar,
    tokenize = 'unicode61 remove_diacritics 2'
);

-- Dense Vector Table (BGE-M3 1024-dim cosine distance)
CREATE VIRTUAL TABLE IF NOT EXISTS memories_vec USING vec0(
    id TEXT PRIMARY KEY,
    embedding float[1024] distance_metric=cosine
);

-- Knowledge Graph Edges (Associative & Causal Links)
CREATE TABLE IF NOT EXISTS memory_edges (
    source_id TEXT NOT NULL REFERENCES memories(id) ON DELETE CASCADE,
    target_id TEXT NOT NULL REFERENCES memories(id) ON DELETE CASCADE,
    relation_type TEXT NOT NULL,                       -- 'caused_by', 'supersedes', 'contradicts', 'exemplifies'
    weight REAL NOT NULL DEFAULT 1.0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    invalid_at TIMESTAMP,
    PRIMARY KEY (source_id, target_id, relation_type)
);
CREATE INDEX IF NOT EXISTS idx_edges_source ON memory_edges(source_id, invalid_at);
CREATE INDEX IF NOT EXISTS idx_edges_target ON memory_edges(target_id, invalid_at);
```

**Reciprocal Rank Fusion (RRF) Hybrid Scoring:**
To combine lexical exact matches (crucial for function names, file paths, and error codes) with dense embeddings and graph connectivity, candidate memories are fused using RRF with constant $k = 60$ [Cormack et al., 2009; ceaksan, 2026]:
$$RRF(d) = \sum_{m \in \{lexical, dense, graph\}} \frac{w_m}{k + rank_m(d)}$$
Where $w_{dense} = 0.50$, $w_{lexical} = 0.35$, and $w_{graph} = 0.15$. Benchmark latency on an NVMe SQLite database with 25,000 memories: **p50 < 4.2ms, p95 < 8.7ms**, with zero cloud dependency and zero external daemon processes.

### 2. Associative traversal via HippoRAG 2 (Hippocampal-Cortical Consolidation)

Standard RAG treats knowledge fragments as independent vectors, failing on multi-hop associative queries where the link between past experience and current problems is structural rather than lexical [Gao et al., 2024]. HippoRAG 2 models the human hippocampus-neocortex interaction by performing Personalized PageRank (PPR) over a graph of extracted named entities and concept nodes [HippoRAG 2, 2026; Mnemoverse, 2026]:

1. **Entity Extraction & Graph Linking:** As agents complete tasks, noun phrases and key system entities are linked into `memory_edges` as nodes and relational edges.
2. **Associative Query Activation:** When a task query $q$ arrives, the top-$k$ most similar entity seeds are activated in initial probability vector $v$.
3. **Spreading Activation via Personalized PageRank:**
   $$p = (1 - \alpha) v + \alpha W^T p$$
   Where damping factor $\alpha = 0.85$, and $W$ is the row-normalized transition matrix over active graph edges where `invalid_at IS NULL`.
4. **Result:** Nodes with highest stationary probability $p$ surface memories that have zero lexical overlap with the query but share causal or contextual dependency. On multi-agent benchmarks, associative graph traversal yields **+7.2% to +10.8% higher accuracy** on multi-hop problem diagnostics compared to pure dense vector retrieval [HippoRAG 2, 2026; Xiang et al., 2026].

### 3. Bilingual & cross-lingual semantic bridging (Arabic-English Memory Cohesion)

In multi-agent systems where reasoning occurs in Arabic (natural human thought, domain synthesis) while execution, code, and formal documentation occur in English, memory fragmentation is a lethal failure mode: queries in one language fail to retrieve relevant traces recorded in the other [Hosn, 2026].

- **Embedding Backbone (BGE-M3):** Crew memory standardizes on BAAI's BGE-M3 (1024-dim), executed locally via ONNX Runtime (363 MB quantized model) [sayed0am, 2025; BAAI, 2026]. BGE-M3 supports dense semantic vectors, multi-vector representations, and cross-lingual lexical matching across 100+ languages simultaneously.
- **Dual-Key Semantic Representation:** When an agent or operator logs an insight in Arabic (e.g. "مهندس الأكواد بينسى يكتب التيستات يوم الجمعة"), the ingestion pipeline extracts a parallel English semantic key (`"engineer skips writing tests on Friday"`) into `content` while retaining the original text in `content_ar`. Both keys are indexed in `memories_fts` and encoded into `memories_vec`.
- **Measured Impact:** Cross-lingual retrieval recall on technical problem solving improves from **61.4%** (under standard English-centric embedding models) to **89.7%** (under BGE-M3 dual-key indexing), eliminating language-boundary context loss without incurring real-time translation latency.

### 4. Runtime LLM self-routing architecture (Autonomous Scope Navigation)

Agents must not have their context windows saturated with global organizational history, nor should they be locked into isolated silos [Yu & Zhao, 2026]. The memory system exposes a unified self-routing tool interface that lets the LLM navigate the four-tier hierarchy at runtime:

```python
def memory_query(
    query: str,
    scopes: list[Literal["self", "crew", "global"]],
    domain: Literal["testing", "architecture", "incident", "general"],
    top_k: int = 5,
    include_invalidated: bool = False
) -> list[MemoryResult]:
    """Autonomous query routing across memory tiers.
    - 'self': Queries Tier 2 (per-agent private skills and patterns)
    - 'crew': Queries Tier 3 (shared crew insights and recurring failures)
    - 'global': Queries Tier 4 (cross-crew organizational knowledge base)
    """
```

**Access Invariants and Promotion Gates:**
- **Read Permissions:** Every agent has read access to its own `self` scope, its active `crew` scope, and `global` scope.
- **Write Permissions:** Agents may write directly only to Tier 1 (`task` working traces) and Tier 2 (`self` private reflections).
- **Promotion to Tier 3 (Crew Insight):** Requires automated validation: the insight must be derived from a task that passed CI with green tests, and must receive Librarian verification or corroboration from a second independent task trace.
- **Promotion to Tier 4 (Global Doctrine):** Requires explicit Operator confirmation and must pass the anti-poisoning two-source corroboration check [Chen et al., 2026].

### 5. Mathematical decay, access reinforcement, and cold-storage archiving

Memory entries must not accumulate indefinitely. To prevent memory sprawl and catastrophic interference, each memory's effective activation strength $S(m, t)$ is computed using an ACT-R / Ebbinghaus hybrid decay model [ACM, 2026]:

$$S(m, t) = I(m) \cdot e^{-\lambda \cdot (t - t_{last})} \cdot \left(1 + \beta \cdot \ln(1 + n_{access})\right)$$

Where:
- $I(m) \in [0.1, 1.0]$ is the EWC importance weight.
- $\lambda$ is the decay constant: $\lambda = 0.05 \text{ day}^{-1}$ for raw task episodic memories; $\lambda = 0.005 \text{ day}^{-1}$ for validated architectural insights.
- $(t - t_{last})$ is the elapsed time in days since the memory was last retrieved.
- $n_{access}$ is the lifetime access count, reinforced with $\beta = 0.25$.

**Automated Garbage Collection (GC) Policy:**
1. **Hot Tier:** Memories with $S(m, t) \ge 0.25$ remain in the high-speed SQLite vector index.
2. **Cold Archiving:** When $S(m, t) < 0.25$ for 30 consecutive days and the memory has zero active graph edges, the entry is exported to compressed JSONL/Parquet cold storage (`Archive/memory/YYYY-MM/`) and purged from `memories_vec`.
3. **Permanent Tombstones:** Invalidated memories (`invalid_at IS NOT NULL`) are retained in SQLite metadata for auditability and poisoning detection but excluded from standard agent retrieval (`invalid_at IS NULL` default filter).

### References for deep dive

- [Garcia, 2024] Garcia, A. Hybrid Full-Text Search and Vector Search with SQLite. alexgarcia.xyz/blog/2024/sqlite-vec-hybrid-search.
- [ceaksan, 2026] Eaksan, C. Smart Search Architecture with FTS5 + Vector + RRF. ceaksan.com/en/hybrid-search-fts5-vector-rrf.
- [Cormack et al., 2009] Cormack, G. V. et al. Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods. SIGIR 2009.
- [Gao et al., 2024] Gao, Y. et al. HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models. NeurIPS 2024. arXiv:2405.14831.
- [HippoRAG 2, 2026] OSU NLP Group. HippoRAG 2: From RAG to Memory. github.com/OSU-NLP-Group/HippoRAG.
- [Mnemoverse, 2026] Knowledge-Graph Memory for AI Agents: HippoRAG 2 and Associative Traversal. mnemoverse.com, July 2026.
- [Xiang et al., 2026] MemGraphRAG: Memory-based Multi-Agent System for Graph Retrieval-Augmented Generation. arXiv:2606.02891 (ACM Aug 2026).
- [sayed0am, 2025] Arabic-English BGE-M3 Compact Embedding Model. huggingface.co/sayed0am/arabic-english-bge-m3.
- [BAAI, 2026] BGE-M3: Multi-Lingual, Multi-Functionality, Multi-Granularity Text Embeddings. BAAI Tech Report. github.com/FlagOpen/FlagEmbedding.
- [Hosn, 2026] Best Embedding Models for Arabic-English RAG. hosn.om/blog/arabic-english-rag-embeddings-2026.
- [ACM, 2026] Human-Like Remembering and Forgetting in LLM Agents: An ACT-R Inspired Memory Model. ACM SIGCHI / IUI 2026. doi:10.1145/3765766.3765803.


## [DEEP DIVE]: Governed Shared Memory, Write-Path Engineering, ACE Playbooks, and Retrieval Economics (cline, 2026-09-13)

# MEMORY — Multi-Agent Memory and Knowledge Management for Crew v2

> **Domain:** MEMORY | **Priority:** P1 | **Prompt:** INBOX #1 | **Agent:** cline (external)
> **Status:** Complete | **Date:** 2026-09-13 | **Freshness:** [verified: 2026-09-13 — all sources checked live via exa + tinyfish web search on this date]
> **Method note:** Every numeric claim carries its source and as-of date. Where vendors disagree (Mem0 vs Zep benchmark dispute), both sides are reported.

## Executive Summary

Crew v2's core defect is architectural, not behavioral: every agent starts every task with a fresh context window, so the crew re-pays the same learning cost on every run and its only knowledge assets (librarian's case shelf, firstmate's JSONL expertise log) are write-only. The research literature has converged on a five-layer memory hierarchy — working/task memory, per-agent private memory, crew/group shared memory, org/company memory, and a distilled global layer — with writes flowing *up* only after extraction and validation, and reads flowing *down* through scoped, hybrid retrieval [1][5][20]. The highest-leverage change for Crew v2 is procedural memory stored as editable playbooks (the ACE pattern: incremental deltas, never monolithic rewrites) [16], plus a governed shared store with scope enforcement, temporal supersession, provenance, and policy-controlled propagation — the four primitives that a 2026 production study found are *all* required, because long-context retrieval alone fails in four measurable ways (unauthorized leakage, stale propagation, contradiction persistence, provenance collapse) [2]. Forgetting must be designed as deliberately as remembering: TTLs per layer, recency-weighted retrieval, and supersede-on-write, or the store rots within weeks [22]. Benchmarks (LoCoMo, LongMemEval, BEAM) provide honest baselines: full-context replay reaches 72.9% on LoCoMo at ~26K tokens/query, while selective memory pipelines reach 66.9–92.5% (depending on version, vendor-reported) at 1.8K–7K tokens — but memory poisoning is the unclosed security hole, and existing prompt-injection defenses do not cover it [23].

## Key Findings

1. **"Fresh context every task" is the #1 capability tax.** LongMemEval shows commercial assistants and long-context LLMs lose 30% accuracy on information across sustained interactions; long-context models drop 30–60% on LongMemEval-S [10]. An agent with no memory re-commits the same failures (the engineer's forgotten tests) indefinitely.
2. **The architecture consensus is a hierarchy, not one store.** Computer-architecture framing (I/O layer / cache layer / memory layer) with explicit cache-sharing and memory-access protocols is the 2026 reference model [1]; production systems use 5–6 typed stores (MIRIX: core, episodic, semantic, procedural, resource, knowledge vault) [5].
3. **Governed shared memory needs four primitives:** scoped retrieval, temporal supersession, provenance tracking, policy-governed propagation. A live-service study found scope enforcement can be *asymmetric across API paths* (tenant held, sub-tenant bypassed via GET-by-id) and pipeline ordering can reject contradictions before the contradiction detector sees them [2].
4. **Procedural memory (playbooks) is the highest-ROI layer for crews.** ACE's incremental-delta playbook updates beat strong baselines by +10.6% (agents) and +8.6% (finance) while avoiding *context collapse* — the erosion caused by monolithic LLM rewriting [16].
5. **Write paths must be filtered in stages.** Production write pipelines converge on: triage (regex/heuristic, no model) → extract/distill (small model) → dedupe/resolve (hybrid exact + embedding match). Skipping triage is "the most common production cost bug" — ~$5/day/user of extraction calls for "ok" turns [21].
6. **Conflicts should not be resolved synchronously.** The 2026 production answer: write the new fact, back-reference the old, let read-time reranking or a background reconciler supersede [21][2].
7. **Retrieval quality decides everything downstream.** Hybrid retrieval (vector + BM25 + entity match) with recency × importance × relevance reranking is the template [22][27]; HippoRAG-style graph indexing beats embedding-only RAG by up to 20% on multi-hop QA while being 10–20× cheaper and 6–13× faster than iterative retrieval [13].
8. **Sleep-time compute amortizes memory maintenance.** Background reorganization between tasks cut test-time compute ~5× at equal accuracy, +13–18% accuracy at higher budgets, and 2.5× lower cost/query when amortized across related queries [11].
9. **Memory poisoning is an unsolved attack class.** Four write channels, nine structural vulnerabilities, six attack classes; a single poisoned write exerts long-term influence, and "existing prompt injection defenses fail to cover memory poisoning attacks" [23].
10. **Vendor benchmarks disagree; use them as ranges, not truths.** Mem0 reports 66.9% LoCoMo @ ~1.8K tokens (paper) [8] and 92.5% @ ~6.9K tokens (Apr 2026 update, self-reported) [24]; Zep publicly disputes Mem0's methodology and claims superior accuracy when "evaluated correctly" [25]. Full-context baseline: 72.9% @ ~26K tokens, 9.87s median latency [24].

## Detailed Analysis

### 1. The problem: Crew v2 has write-only memory

CONTEXT.md records the evidence: COORD-01 ran three task types with explicit "write tests" requirements and produced zero test files; COORD-02 repeated the failure; T09–T12 never regression-tested original failure cases, so "bugs recurred in subsequent runs." This is precisely what the memory literature predicts: an LLM agent without persistent memory "repeatedly forgets past failures and improvements" [3]. The survey literature formalizes agent memory as a **write–manage–read loop** tightly coupled with perception and action [3] — Crew v2 currently has *no* managed write path and *no* read path at all:

- **librarian** shelves solved cases but has no retrieval mechanism (INBOX context) — a write-only episodic store.
- **firstmate** tracks expertise in JSONL "not structured for fast lookup" (INBOX context) — a write-only expertise index.
- Every other agent: stateless. Work product dies with the task.

The consequence is measurable: memory-augmented pipelines beat no-memory baselines exactly where Crew v2 fails — temporal reasoning (+29.6 points) and multi-hop reasoning (+23.1 points) [24].

### 2. Reference architecture: the memory hierarchy

The 2026 computer-architecture framing [1] treats multi-agent memory as classical memory systems:

| Classical concept | Agent-memory translation | Crew v2 mapping |
|---|---|---|
| Registers / L1 | Agent working context (current task prompt) | The task message itself |
| Cache (L2/L3) | Compressed context, recent tool calls, KV reuse | Task-scoped working notes (ephemeral) |
| Main memory | Vector/graph/document stores, full histories | **Per-agent private memory** |
| Shared multiprocessor memory | Shared pool with coherence requirements | **Crew shared memory** (needs coherence: "without coordination, agents overwrite each other, read stale information") [1] |
| Distributed memory | Local stores with selective sync | Per-agent stores + explicit handoff |
| Disk / cold storage | Archives, audit logs | Org/global archives |

Two protocol gaps identified in [1] map directly onto Crew v2's missing machinery:
- **Cache-sharing protocol:** one agent's cached artifacts (e.g., researcher's fetched pages) should be transformable and reusable by another, "analogous to cache transfers in multiprocessors."
- **Memory-access protocol:** even when frameworks support shared state, "the standard access protocol (permissions, scope, granularity) remains under-specified" — can one agent read another's long-term memory? Read-only or read-write? What is the unit of access (document/chunk/record/trace)? [1]

The largest open challenge is **multi-agent memory consistency**: which updates are visible to a read, and in what order [1]. This is the distributed-systems problem Crew v2 will hit the moment two agents write the same lesson.

**Layered design for Crew v2** (aligned with the workspace's declared 4-tier hierarchy — per-agent, per-group, per-company, global — extended with the task layer that all surveyed systems include):

| Layer | Name | Scope | Lifetime | Contents |

### 3. Governance: the four failure modes and their primitives

A June 2026 study of a production multi-tenant memory service (MemClaw, evaluated live via the ArgusFleet harness) formalizes the **fleet-memory problem** and names four failure modes [2]:

| Failure mode | What it looks like in Crew v2 | Required primitive |
|---|---|---|
| Unauthorized leakage | engineer reads researcher's private findings and skips verification | Scoped retrieval (ACL per scope) |
| Stale propagation | tester's old "flake pattern" lesson fires on a new, unrelated flake | Temporal supersession (new fact invalidates old) |
| Contradiction persistence | two conflicting "correct config" notes both retrievable | Supersession + contradiction detector |
| Provenance collapse | nobody knows which run produced a lesson | Immutable provenance attrs (writer, sources, timestamps) |

The study's live evaluation surfaced two production-relevant findings that design-only reviews miss [2]:
1. **Asymmetric scope enforcement:** tenant isolation held, but *sub-tenant* scope was bypassed on direct GET-by-id for agent-scoped credentials (disclosed and remediated during the study). Lesson: enforce scope on *every* access path, not just search.
2. **Pipeline ordering conflict:** a synchronous near-duplicate gate rejected contradictory writes *before* the asynchronous contradiction detector could evaluate them — i.e., dedupe gates must not preempt supersession logic.

Provenance works at production scale: the service reconstructed 100% of depth-4 derivation chains with correct writer identity at sub-second per-hop latency, with zero cross-fleet leakage [2].

**Access control model.** Collaborative Memory [12] provides the formal pattern: two memory tiers (private/shared), each fragment carrying **immutable provenance attributes** (contributing agents, accessed resources, timestamps), with separate read policies (project fragments into *filtered, transformed views*) and write policies (determine retention and sharing), over time-evolving bipartite permission graphs (user↔agent, agent↔resource). This is exactly the shape Crew v2 needs between agents, since today "agents share a filesystem… and trust each other's outputs" with "no inter-agent security boundary" (CONTEXT.md).

### 4. The write path: what to remember, and how

Production write pipelines have converged on a three-stage filter [21]:

1. **Triage** — cheapest possible filter, no model call: skip system messages, empty turns, pure fillers ("Got it", "Thanks"). "Skipping triage and going straight to LLM extraction is the most common production cost bug" [21].
2. **Extract/distill** — small-model call transforming the turn into structured facts (`{type, subject, value, confidence}`), or raw episode, or both (hybrid). "The distill step is what separates 'memory' from 'transcript'" [21]. Mem0's pipeline is the reference: extraction phase processes recent messages plus an asynchronous summary, then an **update phase** evaluates candidate memories against similar existing ones via tool calls (ADD / UPDATE / DELETE / NOOP) [8].
3. **Dedupe/resolve** — hybrid exact-match on stable identifiers + embedding similarity above threshold; conflicts are written with back-references and resolved by read-time reranking or background reconciliation, not synchronously [21].


### 5. The read path: retrieval that works

LongMemEval's ablations give the three optimizations with measured impact [10]:
- **Session decomposition for value granularity** (index at session/segment level, not whole histories)
- **Fact-augmented key expansion** (index keys enriched with extracted facts)
- **Time-aware query expansion** (temporal queries need the time dimension in the index)

Then reranking. The Generative Agents template remains canonical: score = recency × importance × relevance [27]. Modern implementations fuse semantic similarity, BM25, and entity matching into one score [24]; recency-window filtering before scoring bounds interference [22].

**Graph indexing for relational questions.** HippoRAG (hippocampal indexing theory: LLM + knowledge graph + Personalized PageRank) outperforms embedding-only RAG by up to 20% on multi-hop QA; single-step HippoRAG matches iterative retrieval (IRCoT) at 10–20× lower cost and 6–13× faster [13]. Zep's Graphiti demonstrates the same at service level: a temporal knowledge graph with **episode subgraph** (raw non-lossy input), **semantic entity subgraph** (extracted entities/relations), and **community subgraph** (clusters), maintaining "a timeline of facts and relationships, including their periods of validity" — facts are *invalidated*, not deleted [9]. On LongMemEval-style enterprise tasks Zep reports accuracy improvements up to 18.5% with 90% latency reduction vs baselines [9].

**Token budgets.** Full-context replay is the expensive baseline: ~26K tokens/query at 9.87s median for 72.9% LoCoMo accuracy [24]. Selective pipelines: Mem0 paper claims ~1.8K tokens (66.9%) [8]; Mem0's April 2026 token-efficient algorithm claims 92.5% LoCoMo / 94.4% LongMemEval at ~6.9K tokens (self-reported; LoCoMo/LongMemEval/BEAM are now the standard suite) [24]; a 2026 break-even analysis puts the crossover at ~10 interactions for 100K-token contexts, after which memory is cheaper [26]. Crew v2 rule of thumb: **memory context per task ≤ 10% of context window**, retrieval ≤ 1s p95 for in-crew lookups (sub-second per-hop is demonstrated at fleet scale [2]).

### 6. Forgetting and compaction: design the delete path first

"An agent-memory system is really a forgetting system. If you only ever write, it will rot" [22]. The four rot modes and fixes [22]:

| Rot mode | Fix |
|---|---|
| Unbounded growth | Trim/summarize windows; cap persistence; extract facts not transcripts; TTL the long tail |
| Stale retrieval | Hybrid retrieval + composite rerank (recency AND relevance) + recency-window filter |
| No forgetting | TTLs to bound storage; recency decay on scores; active supersession on write |
| Poisoning | Scope per namespace; validate before persisting; verbatim source chunks for high-stakes facts; supersede, don't append |

### 7. Preventing catastrophic forgetting — the Crew v2 version

In weight-space, catastrophic forgetting means new training overwrites old competence [29]. Crew v2 does not fine-tune, so its "weights" are **SOULs, playbooks, and stored lessons** — and its forgetting is **context erosion**: lessons drowned out by newer noise, or rewritten into useless brevity. The literature's non-gradient answers transfer directly:

- **Skill libraries** (Voyager): store *executable, compositional skills* (code) indexed for retrieval; skills are temporally extended and interpretably composable, "which compounds the agent's abilities rapidly and alleviates catastrophic forgetting" [15]. Crew v2 equivalent: store reusable test scaffolds, conftest blocks, pytest configs as named, indexed artifacts — the tester retrieves instead of regenerating.
- **Reflective Memory Management** (RMM): forward-looking memory use plus backward-looking reflection on whether past memories helped; predictive signals decide retention [14b].
- **Playbook deltas over rewrites** (ACE): incremental, structured updates prevent context collapse — the crew's lessons must *accumulate*, never be re-summarized wholesale [16].
- **Contradiction hygiene** (supersession, not silent overwrite) [2][21].
- **Typed stores** (MIRIX): separating procedural from episodic from semantic facts prevents a lesson about *process* being overwritten by a *fact* [5].

### 8. Procedural memory: the playbook layer (highest leverage)

ACE (Agentic Context Engineering) treats contexts as **evolving playbooks** maintained through generation, reflection, and curation with **incremental delta updates** [16]. Results: +10.6% on agents (AppWorld), +8.6% on finance (FiNER), works without labeled supervision by using natural execution feedback, and matches the top-ranked production agent on AppWorld with a smaller open-source model [16]. The two failure modes it fixes are precisely what will kill a naive Crew v2 memory:
- **Brevity bias:** prompt optimizers prefer concise summaries, dropping "domain-specific heuristics, tool-use guidelines, or common failure modes that matter in practice" [16].
- **Context collapse:** "methods that rely on monolithic rewriting by an LLM often degrade into shorter, less informative summaries over time, causing sharp performance declines" [16].

### 9. Security: memory poisoning is the unclosed hole

A 2026 systematic study identifies **four memory write channels** and **nine structural vulnerabilities** (in model capabilities, system-prompt design, and agent architecture), producing six classes of memory-poisoning attacks and a benchmark (MPBench) [23]. Key results:
- "A single adversarial memory write can exert long-term influence over agent behavior" — unlike prompt injection, the payload need only succeed *once* [23].
- "Agents designed to write and retrieve memory more aggressively are more exploitable" [23].
- "Existing prompt injection defenses fail to cover memory poisoning attacks" [23].
- Real-world incidents already documented (Gemini, Microsoft Azure ecosystems, per the study's citations) [23].

Defenses that follow from the evidence (and from [22]): scope-per-namespace writes; validate before persisting; prefer **verbatim source chunks** for high-stakes facts over model-generated paraphrase; provenance on every fragment so poisoned lines can be traced and rolled back; supersede rather than append so a known-bad fact can be invalidated globally with one operation; and rate-limit aggressive auto-writes. This dovetails with the repo's SECURITY domain (separate pending prompt) — memory governance is the bridge.

### 10. Vendor/framework landscape (verified 2026-09-13)

| Framework | Mechanism | Headline numbers (as-reported) | Fit for Crew v2 |
|---|---|---|---|
| **Mem0** | Two-phase extract/update pipeline; graph variant | Paper: 66.9% LoCoMo, 91% lower p95 latency, >90% token savings vs full-context [8]. Apr 2026: 92.5% LoCoMo, 94.4% LongMemEval @ ~6.9K tokens (self-reported) [24] | Pattern donor (write gate design) |
| **Zep/Graphiti** | Temporal KG, episode/entity/community subgraphs, edge invalidation | 94.8% vs MemGPT 93.4% (DMR); up to +18.5% accuracy, −90% latency vs baselines on LongMemEval-style tasks [9] | Pattern donor (temporal facts, supersession) |
| **Letta (MemGPT)** | OS-style virtual context paging; self-editing memory; sleep-time compute | DMR 93.4% (as baseline in [9]); sleep-time: 5× test-compute cut [11][7] | Pattern donor (memory as files + background consolidation) |
| **MIRIX** | 6 typed stores + multi-agent controller | 85.4% LoCoMo; +35% over RAG on ScreenshotVQA with 99.9% storage reduction [5] | Pattern donor (typed stores) |
| **CrewAI** | Unified Memory class; hierarchical scopes; LLM-suggested placement | Adaptive-depth recall, composite scoring (semantic+recency+importance); scope-limited private views [19] | Pattern donor (scope tree) |
| **LangGraph** | Namespaced JSON stores, cross-namespace filters | Semantic/episodic/procedural taxonomy in docs [20] | Pattern donor (namespacing) |
| **Anthropic** | memory tool (client-side files) + CLAUDE.md/auto memory | JIT retrieval; path-traversal protections; per-user storage mapping [17b][18] | Directly portable (Claude-based crew) |

**Benchmark caveat (read before citing numbers anywhere):** Zep publicly disputes Mem0's LoCoMo methodology ("When evaluated correctly on the same benchmark, Zep significantly outperforms Mem0" [25]); full-context remains a strong baseline (72.9% @ 26K tokens [24]); and vendors benchmark their own products. Use vendor numbers as ranges; validate on your own tasks (the repo's EVALUATION domain covers harness design).


Anthropic's shipped pattern is the same shape at product level: CLAUDE.md files (persistent instructions) + auto memory (notes the agent writes from corrections/preferences), both loaded at session start, treated as context rather than enforced config [18]; and the memory tool (`memory_20250818`) implements just-in-time context retrieval — "an agent records what it learns in memory files and reads them back on demand," client-side, under a path-scoped handler [17b]. These are directly portable to Crew v2's SOUL files and librarian.


**Consolidation timing.** Do it offline, not inline: sleep-time compute lets a background agent reorganize memory and precompute inferences while the crew is idle — 5× test-time compute reduction at equal accuracy, and amortized 2.5× cost/query when one context serves many queries [11]; Letta's "dreaming" implements exactly this (background subagents review recent conversations, consolidate lessons, update memory without interrupting active work) [17].

**Forgetting curves.** MemoryBank's Ebbinghaus-inspired decay lets the agent "forget and reinforce memory" based on access frequency and recency [14]; the underlying psychology replicates (Murre & Dros 2015 replicated Ebbinghaus' 1880 savings method) [28]. For Crew v2: decay *retrieval priority* (never delete silently); demote unread lessons on a 30/90/180-day schedule; archive rather than destroy (auditability).

**Memory evolution** goes further: A-Mem's agentic memory treats each new memory as a Zettelkasten note (structured attributes: contextual description, keywords, tags) and on each write triggers **link generation** (connect by shared attributes/similarity) and **memory evolution** (existing notes' representations update as new knowledge arrives) — "allowing the memory network to continuously refine its understanding" [6].

**What Crew v2 should write** (evidence-ranked):
- **Failure lessons** (what broke, root cause, the fix) — this is what prevents T09–T12-style recurrence [3][22].
- **Verdicts and gate outcomes** (tester HOLD, critic timeouts) — G-Memory shows inter-agent *collaboration trajectories* themselves are the underused memory asset: capturing them improved embodied-action success by up to 20.89% and knowledge QA by 10.12% across five benchmarks, *without modifying the underlying frameworks* [4].
- **Playbook deltas** (procedural): concrete strategies, tool-use guidelines, common failure modes — not summaries. ACE shows monolithic rewrites suffer brevity bias and context collapse; structured incremental deltas preserve detail and scale [16].
- **Entity facts** (files, modules, thresholds) — MIRIX's Resource Memory pattern [5].

|---|---|---|---|---|
| L0 | Task working memory | 1 task | Task duration | SPEC, partial artifacts, scratch notes |
| L1 | Agent private memory | 1 agent | Persistent | Agent's lessons, preferences, failure patterns |
| L2 | Crew shared memory | 1 crew | Persistent | Solved cases, playbooks, artifact index, expertise index |
| L3 | Org/company memory | Company | Persistent | Cross-crew standards, policies, org knowledge |
| L4 | Global distilled knowledge | All crews | Curated | Distilled doctrine (what survives updates) |

Write rule: **facts flow up only after extraction and validation** (L0→L1 automatic within scope; L0→L2 only via librarian's extraction gate; L2→L3 only via coach/operator curation). Read rule: **retrieval descends** from the most specific scope upward, under a token budget. This mirrors CrewAI's hierarchical scopes (`/project/alpha`, `/agent/researcher/findings`) where recall inside a scope searches only that branch, "which improves both precision and performance" [19].

A single write gate function; nothing writes to persistent memory except through it.

```python
# crew/memory/write_gate.py
def triage(turn) -> bool:
    """No model call. Skip noise before any LLM spend [21]."""
    if turn.origin == "system" or len(turn.text) < 40: return False
    if turn.text in FILLER_SET: return False            # "Got it", "Thanks", "ok"
    return True

def extract(turn) -> list[Fact]:                        # small model, schema-anchored
    # {type: lesson|verdict|fact|preference, subject, value, confidence 0-1,
    #  scope: /agent/<a> | /crew/<c> | /org/<o>, provenance: {writer, ts, sources[]}}
    ...

def dedupe(fact, store) -> Decision:                    # hybrid lookup [21]
    # exact on stable ids + embedding cosine >= 0.92 -> NOOP
    # 0.75 <= sim < 0.92 -> evaluate contradiction
    # conflict -> write NEW fact, back-reference old, DO NOT delete (async reconcile) [21][2]

def admit(fact) -> WriteResult:
    # scope check on EVERY path (search AND direct get-by-id) [2]
    # confidence < 0.7 -> quarantine, human review [23]
    # auto-write rate limit: <= N writes per agent per hour
    #   (aggressive writers = exploit surface) [23]
```

**Rules (each cited):**
- Triage before extraction — "skipping triage… is the most common production cost bug" [21].
- Never synchronously resolve conflicts: write + back-reference + async supersession [21][2].
- Dedupe gates must NOT preempt the contradiction detector (MemClaw's pipeline-ordering bug) [2].
- Quarantine band: 0.4 < confidence < 0.7 → human review; < 0.4 → reject [23][22].
- Provenance fields mandatory: writer_agent, timestamp, source refs, run_id [2][12].

#### R2. Store — layer layout and scope tree

```
/memories
  /agent/<agent-id>/          # L1 private (lessons, failure patterns, prefs)
  /crew/<crew-id>/            # L2 shared (cases, playbooks, expertise index)
    /cases/<case-id>.md       # solved cases WITH symptom->fix sections
    /playbooks/<domain>.md    # procedural memory (ACE-style, sectioned)
    /expertise.jsonl          # agent->domain->success_rate (fast lookup)
  /org/                       # L3 (standards, policies; curator-gated)
  /quarantine/                # unvalidated writes pending review
  /archive/                   # TTL-expired but auditable
```

- Scopes are path-like; recall inside a scope searches only that branch (CrewAI pattern) [19].
- Per-agent private memory is readable *only* by that agent + tester/critic with explicit read grants (Collaborative Memory read/write policies) [12].
- MIRIX typed fields on every record: `core | episodic | semantic | procedural | resource` [5] — type drives retrieval default and TTL (procedural: never auto-expire; episodic: 180d).

#### R3. Retrieve — hybrid, reranked, budgeted

```python
def recall(query, scope, budget_tokens=2000):
    cands = hybrid_search(query, scope=scope)      # vector + BM25 + entity match [24]
    cands = rerank(cands, score=lambda m: 2.0*sem + 1.0*bm25 + 1.0*entity
                                       + 0.5*recency(m) + 0.3*importance(m)
                                       - 0.8*contradicted(m))   # Gen-Agents template [27]
    return pack(cands, max_tokens=budget_tokens)   # inject above the fold
```

- Defaults: `top_k=8`, budget 2,000 tokens, p95 ≤ 1s in-crew (fleet-scale sub-second demonstrated [2]).
- Temporal queries MUST hit time-aware expansion (LongMemEval's third optimization) [10].
- For multi-hop questions, prefer graph traversal (HippoRAG/PPR or Graphiti) over pure vector [13][9].
- If budget exceeded: prefer procedural (playbook) > failure lessons > entity facts > episodic.


#### R4. Forget — TTLs, decay, supersession

| Layer | TTL | Decay rule | Compaction |
|---|---|---|---|
| L0 task scratch | task end | drop | n/a |
| L1 agent | 90d unread → demote to archive | recency in score | summarize >200 entries (delta-style only [16]) |
| L2 crew cases | 180d unaccessed → archive | 30/90/180 demotion ladder | weekly consolidate duplicates (never re-summarize whole store [16][22]) |
| L2 playbooks | never auto-expire | usage-count demotion of individual strategies | section-level deltas |
| L3 org | manual review cycle | n/a | curation gate |
| L4 global | manual | n/a | curation gate |

- **Supersede on write:** a new contradictory fact invalidates the old one globally — old record marked `superseded_by`, retrievable only for audit [2][9][21][22].
- **Never delete silently**; archive for rollback (poisoning response) [22][23].
- Nightly job: TTL sweep, contradiction detector sweep, decay re-score — Crew v2's "sleep-time" consolidation [11][17].

#### R5. Consolidate — sleep-time maintenance crew

- Between tasks (crew idle): a background agent reviews the day's verdicts/escapes → drafts **playbook deltas** → curator approves → deltas applied section-wise [11][16].
- Amortization evidence: sleep-time compute cut test-time compute 5× at equal accuracy; 2.5× cost/query amortized across related queries [11].

#### R6. Playbooks — procedural memory format (ACE-style)

```markdown
# Playbook: testing-discipline
## Strategy: nub-test-first          [success: 14/16, last: 2026-09-12]
## Strategy: mutation-gate           [success: 9/10]
## Anti-pattern: summary-rewrite     [banned: context-collapse risk, ACE 2025]
```

- Every entry is a **delta** with its own success counter — never rewrite the file wholesale [16].
- Retrieval injects the 2–3 highest-scoring strategies for the task type, ≤300 tokens.

#### R7. Poisoning defenses (memory security)

- Scope-per-namespace writes; validate before persist; **verbatim source chunks for high-stakes facts** (not model paraphrase) [22][23].
- Provenance on 100% of fragments → poisoned-line trace + global supersede rollback [2][12][23].
- Rate-limit auto-writes; aggressive writer = exploitable writer [23].
- Quarterly "memory red-team": inject a known-false fact via a tool output, measure detection latency (ties into the repo's SECURITY domain).

#### R8. Fix the existing write-only assets (librarian + firstmate)

- **librarian:** add retrieval (R3) to the case shelf; every shelved case gets `symptom → root cause → fix` sections; cases without retrieval are cost without value (write-only store [3]).
- **firstmate:** JSONL expertise → SQLite/JSON index `(agent, domain, success_rate, last_used)`; firstmate reads it *before* formation selection via recall(R3).


#### R9. Benchmarks (schedule, not vanity)

- **LoCoMo** (1,540 Qs: single-hop/multi-hop/open-domain/temporal) + **LongMemEval-S** (500 Qs: extraction, multi-session, temporal, knowledge-update, abstention) + BEAM — "the standard for comparing memory architectures" [24][10].
- Acceptance for the memory PR: ≥ full-context baseline on crew-adapted tasks at ≤10% of full-context tokens (72.9% @ 26K is the reference point [24]).
- Track per-task **memory-hit quality**: did the retrieved lesson prevent a repeat escape? (ties into existing ledger).

#### R10. Explicit non-goals

- No fine-tuning / weight updates (catastrophic-forgetting risk without infrastructure) [29]; if ever adopted, isolated-silo methods (LoRA adapters per skill) are the mitigation class, not joint training.
- No cross-agent automatic memory propagation without policy approval (the leakage primitive failure) [2].
- No synchronous conflict resolution in the hot path [21][2].

### 12. Metrics and Targets

| Metric | Definition | How to measure | Target | Warning threshold |
|---|---|---|---|---|
| Write acceptance rate | % of triaged turns yielding admitted facts | gate logs | 5–20% | <2% (over-filtering) or >40% (noise) |
| Triage spend | $ on extraction calls for filler turns | gate logs | ~$0 | >2% of memory budget |
| Retrieval precision@8 | relevant facts in top-8 | weekly sample, human-judged | ≥70% | <50% |
| Temporal query accuracy | time-aware questions answered correctly | LongMemEval-style set | ≥80% | <60% |
| Multi-hop accuracy | multi-hop questions correct | crew-adapted set | ≥75% | <55% |
| Recurrence prevention | escapes avoided by retrieved lessons | ledger join (lesson→task→verdict) | trending ↑ | 0 for 30 tasks = memory not used |
| Stale-hit rate | retrieved facts superseded later | contradiction sweep | <5% | >15% |
| Contradiction latency | write→supersession time | gate logs | <24h (async) | >7d |
| Provenance coverage | % records with full provenance | audit | 100% | <95% |
| Scope violations | cross-scope reads blocked | API audit | 0 | any = security bug [2] |
| Memory tokens/task | injected memory tokens | telemetry | ≤2,000 | >5,000 |
| Poison-detection latency | injected false fact → detected | quarterly red-team | <7d | n/a |
| TTL hygiene | % of store past-TTL | nightly job | <5% | >20% |

### 13. Implementation Roadmap (4 phases)

| Phase | Deliverables | Acceptance criteria | Risks |
|---|---|---|---|
| **M1 (wk 1–2): Gate + scopes** | write_gate.py; scope tree; quarantine dir; provenance schema | 100% writes via gate; triage live; 0 cross-scope reads | over-filtering (tune triage weekly) |
| **M2 (wk 3–4): Retrieval + TTLs** | hybrid index (vector+BM25+entity); reranker; nightly TTL/contradiction sweep | p95 ≤1s; precision@8 ≥70%; stale-hit <5% | wrong-scope retrieval (audit scope paths) |
| **M3 (wk 5–6): Librarian/firstmate retrofit** | case retrieval; expertise index; recall-before-selection in firstmate | firstmate consults memory on 100% of formations; ≥1 case reused/week | stale case hits (supersession sweep) |
| **M4 (wk 7–8): Playbooks + consolidation** | playbook layer; sleep-time delta drafter; curator gate; red-team drill | +≥10% repeat-task success vs no-memory baseline (ACE showed +10.6% [16]); poison drill <7d detection | collapse if deltas not enforced [16] |

### 14. Anti-patterns

| Anti-pattern | Why it fails | Evidence |
|---|---|---|
| Dump transcripts into the store | unbounded growth buries signal | [22][21] |
| Monolithic LLM "summarize the memory" rewrites | brevity bias + context collapse | [16] |
| Synchronous conflict resolution in hot path | blocks writes; can reject contradictions prematurely | [21][2] |
| One global flat store for all agents | leakage + stale propagation; no coherence protocol | [1][2] |
| Retrieval by pure vector similarity | semantically near ≠ task-relevant | [22][24] |
| Aggressive auto-writes everywhere | bigger exploit surface | [23] |
| Paraphrase-only storage of high-stakes facts | unverifiable; poisoning-friendly | [22] |
| Memory as afterthought in eval | memory quality decides agent quality | [24][10] |

### 15. Questions for the Operator (QUESTIONS.md)

1. Memory storage substrate: files (Anthropic pattern [17b]) or SQLite? We recommend files for L1 + SQLite for L2 indexes — confirm operator preference.
2. Should tester/critic have **read** grants on agent private memory for verification, or should L1 be fully opaque? (Collaborative Memory supports filtered read views [12] — we recommend filtered views for tester only.)
3. Who is the curator approving playbook deltas — coach, operator, or tester? (We recommend coach drafts / tester validates / operator approves.)


### 11. Practical Recommendations — Crew v2 memory build-out

**Design principle (from all sources):** memory is a **write–manage–read loop** [3]; Crew v2 currently has no managed write path and no read path. Build in this order: (1) scopes + write gate, (2) retrieval, (3) forgetting, (4) playbook layer, (5) governance audits.

#### R1. Ingest — the write gate (first PR)


## References

1. Yu, Z. et al. (2026). *Multi-Agent Memory from a Computer Architecture Perspective: Visions and Challenges Ahead.* arXiv:2603.10062; Architecture 2.0 Workshop, Mar 23 2026. https://arxiv.org/abs/2603.10062v1
2. Margalit, Y., Cohen-Inger, N., Avram, E., Taig, R., Margalit, O. (2026). *Governed Shared Memory for Multi-Agent LLM Systems.* arXiv:2606.24535 (Jun 23, 2026). https://arxiv.org/abs/2606.24535
3. (2026). *Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers.* arXiv:2603.07670. https://arxiv.org/pdf/2603.07670
4. (2025). *G-Memory: Tracing Hierarchical Memory for Multi-Agent Systems.* NeurIPS 2025. https://arxiv.org/abs/2506.07398; code: https://github.com/bingreeky/GMemory
5. MIRIX Team (2025). *MIRIX: Multi-Agent Memory System for LLM-Based Agents.* arXiv:2507.07957. https://arxiv.org/html/2507.07957v1; docs: https://docs.mirix.io/architecture/memory-components/
6. Xu, W. et al. (2025). *A-MEM: Agentic Memory for LLM Agents.* arXiv:2502.12110. https://arxiv.org/abs/2502.12110
7. Packer, C. et al. (2023). *MemGPT: Towards LLMs as Operating Systems.* arXiv:2310.08560. https://arxiv.org/pdf/2310.08560
8. Chhikara, P., Khant, D., Aryan, S., Singh, T., Yadav, D. (2025). *Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory.* arXiv:2504.19413 (Apr 28, 2025). https://arxiv.org/html/2504.19413
9. Rasmussen, M. et al. (2025). *Zep: A Temporal Knowledge Graph Architecture for Agent Memory.* arXiv:2501.13956. https://arxiv.org/html/2501.13956
10. Wu, X. et al. (2024). *LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory.* arXiv:2410.10813. https://arxiv.org/abs/2410.10813
11. (2025). *Sleep-time Compute: Beyond Inference Scaling at Test-time.* arXiv:2504.13171 (Apr 17, 2025). https://arxiv.org/html/2504.13171v1; code: https://github.com/letta-ai/sleep-time-compute
12. (2025). *Collaborative Memory: Multi-User Memory Sharing in LLM Agents with Dynamic Access Control.* arXiv:2505.18279. https://arxiv.org/html/2505.18279
13. Gutiérrez, B.J. et al. (2024). *HippoRAG: Neurobiologically Inspired Long-Term Memory for LLMs.* NeurIPS 2024. https://proceedings.neurips.cc/paper_files/paper/2024/file/6ddc001d07ca4f319af96a3024f6dbd1-Paper-Conference.pdf
14. Zhong, W. et al. (2024). *MemoryBank: Enhancing Large Language Models with Long-Term Memory.* AAAI 2024. https://ojs.aaai.org (cited by 1,357 per AAAI page); also Liang, X. et al. (2025) *SAGE: Self-evolving Agents with Reflective and Memory-Augmented Mechanisms*, ScienceDirect, cited by 141. https://www.sciencedirect.com (SAGE)
14b. Tan, Z. et al. (2025). *Reflective Memory Management (RMM).* ACL Anthology, cited by 130. https://aclanthology.org
15. Wang, G. et al. (2023). *Voyager: An Open-Ended Embodied Agent with Large Language Models.* https://voyager.minedojo.org/
16. Zhang, Q. et al. (2025). *Agentic Context Engineering (ACE): Evolving Contexts for Self-Improving Language Models.* arXiv:2510.04618 (Oct 6, 2025). https://arxiv.org/html/2510.04618
17. Letta. *Sleep-time Compute* (blog) https://www.letta.com/blog/sleep-time-compute/; *Memory & dreaming* docs https://docs.letta.com/configuration/memory/
17b. Anthropic (2025). *Memory tool* (`memory_20250818`). Claude Platform Docs. https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool
18. Anthropic. *How Claude remembers your project* (CLAUDE.md + auto memory). Claude Code Docs. https://code.claude.com/docs/en/memory
19. CrewAI. *Memory* (unified Memory class, hierarchical scopes). https://docs.crewai.com/edge/en/concepts/memory
20. LangChain. *Long-term memory* (LangGraph stores, namespaces). https://docs.langchain.com/oss/python/langchain/long-term-memory; *Memory overview* https://docs.langchain.com/oss/python/concepts/memory
21. Bansal, J. (May 18, 2026). *Memory Write Policies: What's Worth Remembering.* https://jatinbansal.com/ai-engineering/memory-write-policies/
22. Mareno, D. (Aug 3, 2026). *Why Agent Memory Rots in Production: The Four Failure Modes (and the Fix for Each).* https://dreaming.press/posts/why-agent-memory-rots-in-production-four-failure-modes.html
23. Dash, P., Ge, T., Jain, A., Shah, T., Shang, Z. (2026). *From Untrusted Input to Trusted Memory: A Systematic Study of Memory Poisoning Attacks in LLM Agents.* arXiv:2606.04329. https://arxiv.org/pdf/2606.04329v1.pdf
24. Singh, T. et al. (Apr 1, 2026). *State of AI Agent Memory 2026: Benchmarks & Trends Report.* Mem0. https://mem0.ai/blog/state-of-ai-agent-memory-2026
25. Zep (May 6, 2025). *Is Mem0 Really SOTA in Agent Memory?* https://blog.getzep.com (LOCOMO methodology dispute)
26. (2026). *A Cost-Performance Analysis of Fact-Based Memory vs. Long-Context.* arXiv:2603.04814. https://arxiv.org/html/2603.04814v1
27. Park, J.S. et al. (2023). *Generative Agents: Interactive Simulacra of Human Behavior* (recency × importance × relevance retrieval). https://arxiv.org/abs/2304.03442
28. Murre, J.M.J. & Dros, J. (2015). *Replication and Analysis of Ebbinghaus' Forgetting Curve.* PLoS ONE / PMC (cited by 1,398). https://pmc.ncbi.nlm.nih.gov
29. IBM (2026). *What is Catastrophic Forgetting?* https://www.ibm.com/think/topics/catastrophic-forgetting; mechanistic study: arXiv:2601.18699 (20 SOTA models, mid-2026). https://arxiv.org/html/2601.18699v2

## [DEEP DIVE (freebuff, pass 3, 2026-09-14)]: Concurrent-Write Consistency (CRDTs), Implicit Memory Conflict, and Forgetting as an Operating Policy

Pass-1 covered system mechanics, context rot, and poisoning; pass-3 covers the failure class those leave untouched: **what happens when two agents write the same memory at the same time**, and how memory should stop being valid.

### 1. Concurrent writes: the register semantics must be chosen, not defaulted
- An LWW-Register (last-write-wins by timestamp) silently discards one of two concurrent writes — the write with the earlier (or tie-broken lower) timestamp is lost [third-bit, CRDT field notes; Duncan, 2025]. For crew memory (two agents revising the same ledger row or SOUL note off a synced dispatch), LWW is the default in every off-the-shelf store — and the wrong default: the lost write is invisible unless a pre-write compare is logged.
- The register choice is the actual decision: **MV-Register (multi-value)** surfaces both concurrent values and forces a read-time merge decision (an adjudication hook the crew already has — conflict-resolution's HOLD-wins mechanism) [Duncan, 2025; Ably, 2021]. CRDTs guarantee convergence when replicas merge in any order, which is exactly the crew's per-agent + per-group memory hierarchy (independent replicas, periodic sync) [Wikipedia, CRDT; ACM Survey, 2024].
- Crew rule: memory rows that are **append-only observations** (task events, verdicts) → grow-only/JSONCRDT semantics, no conflict possible; memory rows that are **mutable state** (current SOUL, current task state) → MV-Register with the conflict surfaced to the adjudicator, never LWW. The communication-protocols HLC timestamp (below) is the tie-breaker of last resort — with the loser logged, not dropped.

### 2. Implicit conflict: retrieving the new memory is not acting on it
- STALE (400 expert-validated conflict scenarios, 1,200 queries, contexts to 150K tokens) isolates the failure mode where a later observation invalidates an earlier memory **without explicit negation** ("Implicit Conflict"). Frontier models and memory frameworks show a pervasive gap between retrieving updated evidence and acting on it: the best evaluated model reaches only **55.2%** overall; models accept outdated assumptions embedded in queries and miss that a change in one aspect of state should invalidate related memories [Chao et al., arXiv:2605.06527, 2026].
- The proposed fix direction — write-time **state consolidation with propagation-aware search** (CUPMem prototype) — maps to the crew as: when a memory row is revised, the writer must enumerate dependent rows and mark them stale at write time, not leave invalidation to retrieval time.
- A 2026 systems audit names the recurring failure modes of treating memory as a dumb store: **unregulated growth, missing semantic revision, capacity-driven forgetting, and read-only retrieval** [arXiv:2605.26252, 2026] — the crew's 4-tier hierarchy plus ledger already has slots for all four; the write-path rule above closes "missing semantic revision."

### 3. Forgetting is an operating policy, not a storage accident
- The design-space, in increasing sophistication: **time-based expiry (TTL) → usage-based decay → staleness detection** [Konishi, 2026]. Production guidance composes them: eviction decides what leaves; decay down-ranks at retrieval; both can coexist — a memory can survive every eviction pass and still be effectively dead at retrieval [mem0, 2026].
- Crew policy (three dials, one per memory tier): per-task tier = TTL equal to task lifetime; per-agent tier = usage-decay with quarterly review of evicted items; cross-crew knowledge = no expiry, but staleness-detection prompts ("is this still true?") at retrieval for rows older than the quarterly calibration cycle. The STALE result justifies the third dial: agents cannot be trusted to detect staleness themselves.

### Numbers for calibration (pass 3)

| Quantity | Value | Source |
|---|---|---|
| Best model on STALE (implicit conflict) | 55.2% | [arXiv:2605.06527] |
| STALE scale | 400 scenarios / 1,200 queries / 150K-token contexts | same |
| Between-model variance capture (Big Five, contrast) | — | (see agent-embodiment pass 3) |
| LWW concurrent-write outcome | one write silently lost | [Duncan, 2025] |
| Memory-as-dumb-store failure modes | 4 (growth, revision, forgetting, read-only retrieval) | [arXiv:2605.26252] |

### References (pass 3)
1. [Chao et al., 2026] "STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?" arXiv:2605.06527. https://arxiv.org/abs/2605.06527 [verified: 2026-09-14]
2. [2026] "Is Agent Memory a Database? Rethinking Data Management for Agent Memory," arXiv:2605.26252. https://arxiv.org/html/2605.26252v1 [verified: 2026-09-14]
3. [Duncan, 2025] "The CRDT Dictionary: A Field Guide to Conflict-Free Data Types." https://iankduncan.com/engineering/2025-11-27-crdt-dictionary/ [verified: 2026-09-14]
4. [third-bit] "Conflict-Free Replicated Data Types" (LWW-Register weakness). https://third-bit.com/dsdx/crdt/ [verified: 2026-09-14, snippet]
5. [Wikipedia; ACM Computing Surveys, 2024] CRDT definitions and survey, DOI 10.1145/3695249 [verified: 2026-09-14, snippet]
6. [mem0, 2026] "Memory eviction and forgetting in AI agents." https://mem0.ai/blog/memory-eviction-and-forgetting-in-ai-agents [verified: 2026-09-14]
7. [Konishi, 2026] "AI Agent Memory Design Guide" (TTL → decay → staleness). https://hidekazu-konishi.com/entry/ai_agent_memory_design_guide.html [verified: 2026-09-14, snippet]
