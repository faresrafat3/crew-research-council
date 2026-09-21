# CREW v2 — Architecture Redesign

## Core Principle
**The crew is not a pipeline — it's a collective that assembles the right formation for each task.**

## The Problem with v1
Shared model/tools for all agents → no real diversity · fixed pipeline → overhead on simple tasks, insufficient on complex ones · no expertise tracking · gate shares the executor's knowledge → catches nothing new · razor violates constraints → anti-bloat becomes bloat.

## v2 Design: Dynamic Formation with Expertise Tracking

### 1. The Router (firstmate)
Analyzes task type/complexity/constraints · picks formation (SOLO → DUO → PIPELINE → FULL) · sets explicit success criteria · tracks which formations succeed on which task types.

### 2. Specialist Pool (Real Diversity)
Each specialist has a **different toolset configuration**, not just a different SOUL:

| Role | Primary Tools | Model Config | Track Record Weight |
|------|--------------|--------------|-------------------|
| researcher | web_search, web_extract, read_file | default | evidence quality |
| engineer | terminal, read_file, write_file, patch | default | code correctness |
| architect | read_file, search_files, write_file | default | design quality |
| critic | terminal, read_file, web_search | default | bug-finding rate |
| verifier | terminal, read_file, web_extract | default | verification accuracy |

### 3. Formation Rules

**SOLO** (simple, well-scoped): one agent with the right toolset; no overhead/coordination cost. Used for grammar fixes, simple lookups, single-file edits.

**DUO** (needs verification): executor + verifier, verifier with different tools. Used for code with tests, research with fact-checking.

**PIPELINE** (sequential decomposition): researcher → architect → engineer → critic, each stage different tools. Used for build features, write systems, complex analysis.

**FULL** (maximum capability): all specialists + router + meta-tracker. Used for unknown complexity, high-stakes, novel problems.

### 4. Expertise Tracking
Every task records: formation used · agents participating · success/failure against criteria · time and token cost.

This builds a **track record** that informs future routing.

### 5. Constraint Respect
Explicit brief constraints are **inviolable** · razor removes redundancy only, never meaning · completer checks constraint compliance before FINAL.

### 6. Verification Independence
Critic/verifier must have **different tools** than the executor: code written → verifier runs tests · analysis written → verifier checks sources · summary written → verifier checks original text.

## Implementation

### Phase 1: Router Upgrade
firstmate SOUL rewritten as router · task classification logic · formation selection algorithm.

### Phase 2: Specialist Tool Differentiation
Per-specialist toolset profile · SOULs updated to real capabilities · track-record fields added.

### Phase 3: Dynamic Pipeline
Pipeline script assembles formations per task · expertise tracker records results · feedback loop improves routing.

### Phase 4: Verification Independence
Critic gets terminal + test execution · verifier gets web_extract + fact-checking · gate becomes a real independent check.

## Success Metrics
- **SOLO tasks**: v2 SOLO = v1 PIPELINE quality, 1/3 the tokens
- **Complex tasks**: v2 FULL > v1 PIPELINE (real expertise leveraging)
- **Constraint violation**: 0% (razor respects constraints)
- **Routing accuracy**: >80% correct formation selection after 20 tasks
