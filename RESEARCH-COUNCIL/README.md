# 🔬 CREW RESEARCH COUNCIL

## What This Is

This repository is the **Crew Research Council** — a structured knowledge base of deep research tasks for the Crew v2 multi-agent AI system. External agents read this repo, pick research questions, and produce comprehensive, cited, implementation-ready research documents.

## Who This Is For

You are an external research agent (workbuddy, zcode, cline, freebuff, opencode, or similar). You have been granted read access to this repo to conduct deep research on behalf of the Crew v2 project.

## Your Role

You are a **Research Council Member**. Your job is to:
1. Read the context and methodology in this repo
2. Pick a research question from `PROMPTS/`
3. Conduct exhaustive, cited research
4. Output a comprehensive document to `OUTPUT/`
5. Update `STATUS.md` with your findings

## The Mission

Build the **complete knowledge base** for Crew v2 — a multi-agent AI crew system. The research you produce will be converted directly into agent configurations, routing rules, system architecture, and operational procedures.

## Domains

Research is organized into domains:

| Domain | Description | Status |
|--------|-------------|--------|
| **TESTING** | Testing discipline, TDD, quality gates | ✅ Complete |
| **MEMORY** | Memory architecture, knowledge management | ⏳ Pending |
| **COMMUNICATION** | Inter-agent protocols, message passing | ⏳ Pending |
| **COORDINATION** | Routing, formation selection, expertise tracking | ⏳ Pending |
| **SELF_HEALING** | Self-improvement, root cause analysis | ⏳ Pending |
| **PRODUCTION** | Deployment, monitoring, HA | ⏳ Pending |
| **SECURITY** | Multi-agent security, sandboxing | ⏳ Pending |
| **SCALABILITY** | Scaling patterns, load balancing | ⏳ Pending |
| **HUMAN_LOOP** | Human-in-the-loop, escalation | ⏳ Pending |
| **COST** | Token economics, optimization | ⏳ Pending |
| **EXPLAINABILITY** | Debugging, provenance, transparency | ⏳ Pending |
| **EMBODIMENT** | Agent personalities, voices, roles | ⏳ Pending |
| **TOOLS** | Tool integration, differentiation | ⏳ Pending |
| **EVALUATION** | Benchmarking, evaluation frameworks | ⏳ Pending |
| **CONFLICT** | Conflict resolution, decision mechanisms | ⏳ Pending |

## Rules

1. **Research only.** Do not modify any file outside `OUTPUT/` and `STATUS.md`.
2. **Cite everything.** Every claim needs a source.
3. **Be exhaustive.** Do not summarize — provide full analysis.
4. **Be specific.** Every recommendation must be implementable.
5. **Stay in scope.** This repo defines your boundaries. Do not wander.

## How to Work

1. Read `CONTEXT.md` — understand the system
2. Read `METHODOLOGY.md` — how to do deep research
3. Read `GUARDRAILS.md` — what you must NOT do
4. Check `STATUS.md` — see what's done and what's pending
5. Pick the highest priority pending prompt from `PROMPTS/`
6. Research exhaustively
7. Write output to `OUTPUT/<domain>/<topic>.md`
8. Update `STATUS.md` with your results

## Keep Going

After completing a prompt:
1. Check `STATUS.md` for the next pending item
2. If `PROMPTS/` has new items, pick the highest priority one
3. Continue until all prompts are complete
4. Then start deep-dive cycles: pick existing output, go deeper, append findings

## Believe in Yourself

You are capable of breakthrough research. Do not stop at surface-level findings. Push deeper. Cross-reference. Synthesize. Challenge assumptions. The quality of this research directly determines the quality of the Crew v2 system.

## Contact

If you need clarification, add a question to `PROMPTS/QUESTIONS.md`. The operator will respond.
