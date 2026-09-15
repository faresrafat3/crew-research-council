# Research Output

This directory contains completed research documents from all agents.

## File Naming Convention

`<topic-kebab-case>.md`

Examples:
- `testing-maturity-model.md`
- `tdd-protocol.md`
- `quality-metrics.md`

## Structure

Each file follows this format:

```markdown
# [TOPIC]

## Executive Summary
[3-5 sentences]

## Key Findings
[Bullet points, max 10 per section]

## Detailed Analysis
[Exhaustive, cited]

## Practical Recommendations
[Specific, implementable]

## Metrics and Targets
[With numbers]

## References
[Inline + references section]
```

## Deep Dives

When an agent goes deeper on an existing topic, append to the existing file with:

```markdown
## [DEEP DIVE]: [Specific Focus]
[New findings]
```

## Current Contents

24 research documents as of 2026-09-15: the 10 testing-discipline files (testing-maturity-model, tdd-protocol, blocking-authority, testing-framework-spec, quality-metrics, cicd-integration, tester-soul, engineer-soul, routing-integration, implementation-roadmap) and the 13 multi-agent-crew files (memory-architecture, communication-protocols, self-healing, production-deployment, multi-agent-security, scalability-patterns, human-in-the-loop, conflict-resolution, agent-embodiment, tool-differentiation, cost-optimization, evaluation-frameworks, explainability), plus gate-toolkit.

The authoritative, per-file inventory (contents, agents, deep-dive counts) is maintained in [`../STATUS.md` → Output Inventory](../STATUS.md#output-inventory) — this README intentionally does not duplicate it. Note: `testing-maturity-model.md` and `blocking-authority.md` had their base sections lost twice to local-state syncs (left appendix-only); both were restored additively with all appendices preserved on 2026-09-15 (see STATUS.md → dsh entry, commits 0546ea3 / 4bafbc2).
