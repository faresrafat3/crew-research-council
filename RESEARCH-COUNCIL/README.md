# Crew Research Council

This repo is the research arm of Crew v2, a multi-agent crew system. External agents research one question at a time and write the result into `OUTPUT/`. The operator turns those documents into agent configurations, routing rules, architecture decisions, and procedures. Nothing here runs; it is all input to that work.

## Who this is for

External research agents: workbuddy, zcode, cline, freebuff, opencode, or whichever agent the operator points at this repo. You need read access and nothing else. You do not run the crew.

## What you do

1. Read `CONTEXT.md` for the system, then `METHODOLOGY.md` for how research is done here.
2. Read `GUARDRAILS.md`. It is short, and breaking it wastes the work.
3. Open `STATUS.md`, which records what is finished. If `PROMPTS/INBOX.md` still lists something open, take the highest-priority one. If everything is finished, go deeper instead.
4. Research it and cite what you use.
5. Write the document to `OUTPUT/<topic>.md`, following the format in `OUTPUT/README.md`.
6. Record it in `STATUS.md`.

## What exists

Every domain below has at least one document. Per-file status, contents, and deep-dive counts live in `STATUS.md` under `## Output Inventory`. This page does not repeat them.

| Domain | Covers | Start with |
|---|---|---|
| Testing | Test discipline, TDD, gates, quality metrics | `tdd-protocol.md` |
| Memory | Memory architecture, knowledge management | `memory-architecture.md` |
| Communication | Inter-agent protocols, message passing | `communication-protocols.md` |
| Coordination | Routing, formation selection, expertise tracking | `routing-integration.md` |
| Self-healing | Self-improvement, root cause analysis | `self-healing.md` |
| Production | Deployment, monitoring, high availability | `production-deployment.md` |
| Security | Multi-agent security, sandboxing | `multi-agent-security.md` |
| Scalability | Scaling patterns, load balancing | `scalability-patterns.md` |
| Human loop | Human in the loop, escalation | `human-in-the-loop.md` |
| Cost | Token economics, optimization | `cost-optimization.md` |
| Explainability | Debugging, provenance, transparency | `explainability.md` |
| Embodiment | Agent personalities, voices, roles | `agent-embodiment.md` |
| Tools | Tool integration, differentiation | `tool-differentiation.md` |
| Evaluation | Benchmarking, evaluation frameworks | `evaluation-frameworks.md` |
| Conflict | Conflict resolution, decision mechanisms | `conflict-resolution.md` |

All files sit directly in `OUTPUT/`, not in per-domain folders.

## Rules

1. Research only. Write to `OUTPUT/*.md`, `STATUS.md`, and `PROMPTS/QUESTIONS.md`; do not run code, tests, or deployments. Everything else is read-only.
2. Cite every claim. If you cannot verify something, say so in the document instead of smoothing over it.
3. No summaries. "Set line coverage to 90%" is useful. "Improve coverage" is not.
4. Every recommendation has to be buildable by someone reading it cold.

## Going deeper

When the topic is already covered, do not open a second file. Append to the existing one:

```markdown
## [DEEP DIVE]: <specific focus>
```

Say what the dive adds that the base document does not. Repeating the base in different words is not a deep dive.

## When you are stuck

Add the question to `PROMPTS/QUESTIONS.md` and keep working on something clear. Do not stop and wait.

## The bar

A document is finished when another agent could build from it without asking you anything. If it needs a conversation to be useful, it is not done.
