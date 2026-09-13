# CREW v2 — Architecture Redesign

## Core Principle
**The crew is not a pipeline — it's a collective that assembles the right formation for each task.**

## The Problem with v1
- All agents share the same model and tools → no real diversity
- Fixed pipeline → overhead on simple tasks, insufficient on complex ones
- No expertise tracking → no learning from success/failure
- Gate verifies with the same knowledge as executor → catches nothing new
- Razor violates constraints → anti-bloat becomes bloat

## v2 Design: Dynamic Formation with Expertise Tracking

### 1. The Router (firstmate)
- Analyzes task type, complexity, and constraints
- Picks formation from: SOLO → DUO → PIPELINE → FULL
- Sets explicit success criteria
- Tracks which formations succeed on which task types

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

**SOLO** (simple, well-scoped):
- One agent with the right toolset
- No overhead, no coordination cost
- Used for: grammar fixes, simple lookups, single-file edits

**DUO** (needs verification):
- Executor + Verifier
- Verifier has different tools than executor
- Used for: code with tests, research with fact-checking

**PIPELINE** (sequential decomposition):
- researcher → architect → engineer → critic
- Each stage has different tools
- Used for: build features, write systems, complex analysis

**FULL** (maximum capability):
- All specialists + router + meta-tracker
- Used for: unknown complexity, high-stakes, novel problems

### 4. Expertise Tracking
Every task records:
- Which formation was used
- Which agents participated
- Success/failure against criteria
- Time and token cost

This builds a **track record** that informs future routing.

### 5. Constraint Respect
- Explicit constraints in briefs are **inviolable**
- Anti-bloat (razor) only removes redundancy, never changes meaning
- Completer checks constraint compliance before FINAL

### 6. Verification Independence
The critic/verifier must have **different tools** than the executor:
- Executor writes code → Verifier runs tests
- Executor writes analysis → Verifier checks sources
- Executor writes summary → Verifier checks original text

## Implementation

### Phase 1: Router Upgrade
- firstmate SOUL rewritten as router
- Task classification logic
- Formation selection algorithm

### Phase 2: Specialist Tool Differentiation
- Each specialist gets a toolset profile
- SOULs updated to reflect real capabilities
- Track record fields added

### Phase 3: Dynamic Pipeline
- New pipeline script assembles formations per task
- Expertise tracker records results
- Feedback loop improves routing

### Phase 4: Verification Independence
- Critic gets terminal + test execution tools
- Verifier gets web_extract + fact-checking tools
- Gate becomes a real independent check

## Success Metrics
- **SOLO tasks**: v2 SOLO = v1 PIPELINE quality, 1/3 the tokens
- **Complex tasks**: v2 FULL > v1 PIPELINE (real expertise leveraging)
- **Constraint violation**: 0% (razor respects constraints)
- **Routing accuracy**: >80% correct formation selection after 20 tasks
