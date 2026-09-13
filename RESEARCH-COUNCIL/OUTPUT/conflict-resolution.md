# Conflict Resolution and Decision Mechanisms

## Executive Summary
Crew v2 has an escalation ladder (tester → critic → human) but no systematic conflict resolution for other disagreements (architect vs. researcher, engineer vs. tester on non-blocking issues). Multi-agent systems require structured decision mechanisms: voting (majority, weighted, consensus), adjudication, and deadlock breaking. Research (2025-2026) shows majority voting is brittle under confabulation consensus, while structured debate with evidence-based adjudication outperforms simple voting. This document specifies a conflict resolution framework with RoundTable-inspired group decision-making, AGENTAUDITOR-style reasoning tree analysis, and DynaDebate-style dynamic path generation.

## Key Findings

- **RoundTable (arXiv, 2411.07161, 2024)** investigates group decision-making in multi-agent collaboration. Majority voting causes inefficient collaboration due to strict acceptance criteria. Unanimous voting gives 87% lower initial performance than the best-performing method. Adaptive voting with early stopping outperforms both [RoundTable, 2024].
- **AGENTAUDITOR (arXiv, 2602.09341, 2026)** moves beyond frequency-based aggregation by organizing agent traces into a Reasoning Tree that explicitly represents agreements and divergences. Structure-Adaptive Auditor performs localized adjudication at Critical Divergence Points (CDPs), converting global trace evaluation into targeted branch-level comparison. Outperforms majority voting and LLM-as-judge under confabulation consensus [AGENTAUDITOR, 2026].
- **DynaDebate (arXiv, 2601.05746, 2026)** addresses model homogeneity: agents with identical mental sets generate nearly identical responses, causing debate to collapse to simple majority voting. DynaDebate introduces dynamic path generation to break homogeneity and prevent false consensus. Agents assess peer responses based on evidence quality, not textual fluency [DynaDebate, 2026].
- **Multi-Agent Debate (MAD) Protocols (2025)** summarize decision mechanisms: majority/supermajority/unanimous voting, weighted/confidence-modulated aggregation (Dawid-Skene, calibrated weighting), sequential/simultaneous/hybrid turns. Consensus-based MAD faces conformity bias, error propagation, and high token cost [EmergentMind, 2025].
- **Beyond the Strongest LLM (2025)** shows multi-turn multi-agent orchestration matches or exceeds the strongest single model. Revealing authorship increases self-voting and ties; showing ongoing votes amplifies herding (speeds convergence but can yield premature consensus) [Beyond the Strongest LLM, 2025].

## Detailed Analysis

### Current Failure Modes

1. **Tester-engineer deadlock**: Tester says HOLD, engineer says it's fine. Only resolution is human escalation.
2. **No structured debate**: Agents don't systematically compare reasoning traces.
3. **No deadlock breaking**: If critic and tester disagree, no automatic resolution.
4. **No confidence weighting**: All agent opinions weighted equally.
5. **Premature consensus**: Agents converge on answer without sufficient exploration.

### Conflict Resolution Framework

**Three-tier resolution (adapted from RoundTable + AGENTAUDITOR):**

```
Tier 1: DIRECT RESOLUTION
    Agents exchange reasoning traces → identify divergence points
    If divergence is factual: check evidence, adopt evidence-based position
    If divergence is preference: escalate to Tier 2
    
Tier 2: STRUCTURED DEBATE
    Agents present arguments at Critical Divergence Points (CDPs)
    Each agent assigns confidence score (0.0-1.0)
    Weighted aggregation: sum(confidence * position) / sum(confidence)
    If weighted consensus > 0.7: adopt. Else: escalate to Tier 3.
    
Tier 3: ADJUDICATION
    Independent adjudicator (critic or external model) reviews reasoning tree
    Adjudicator selects branch with strongest evidence
    If adjudicator confidence < 0.6: escalate to human
```

### Voting Mechanisms

**Comparison (RoundTable + EmergentMind):**

| Mechanism | When to Use | Threshold | Performance |
|-----------|-------------|-----------|-------------|
| Majority | Quick decisions, low stakes | >50% agree | Brittle under confabulation |
| Supermoderity | Medium stakes | >66% agree | Better than majority |
| Unanimous | High stakes, safety-critical | 100% agree | 87% lower initial performance |
| Weighted | Agents have different expertise | Confidence-weighted sum | Best overall |
| Consensus-Progressive | Complex decisions | Heterogeneous pairwise → debate → weighted vote | Highest quality |

**Recommended: Weighted voting with confidence scores.**

```python
def weighted_vote(positions, confidences):
    """
    positions: list of agent positions (0 or 1 for binary, or continuous)
    confidences: list of agent confidence scores (0.0-1.0)
    """
    weighted_sum = sum(p * c for p, c in zip(positions, confidences))
    total_confidence = sum(confidences)
    return weighted_sum / total_confidence if total_confidence > 0 else 0.5
```

### Reasoning Tree Construction

**AGENTAUDITOR pattern for Crew v2:**

1. **Collect traces**: Each agent produces reasoning trace for the decision.
2. **Identify CDPs**: Find points where agents diverge (different conclusions from same evidence).
3. **Branch-level comparison**: At each CDP, compare evidence quality of competing branches.
4. **Localized adjudication**: Adjudicator evaluates each CDP independently.
5. **Aggregate**: Combine CDP-level decisions into final verdict.

**Example: Architect vs. Researcher on system design**

```
CDP 1: Database choice
    Architect branch: PostgreSQL (evidence: ACID compliance, complex queries)
    Researcher branch: MongoDB (evidence: flexibility, rapid prototyping)
    Adjudicator: Evaluate evidence quality → PostgreSQL wins (task requires ACID)
    
CDP 2: API style
    Architect branch: REST (evidence: simplicity, tooling)
    Researcher branch: GraphQL (evidence: flexible queries)
    Adjudicator: Evaluate evidence → REST wins (team familiarity)
    
Final: PostgreSQL + REST
```

### Deadlock Breaking

**When agents disagree and no consensus emerges:**

1. **Evidence-based**: Agent with stronger evidence wins. Evidence quality scored by adjudicator.
2. **Track record**: Agent with better historical accuracy on similar decisions wins.
3. **Conservatism**: For safety-critical decisions, conservative option wins.
4. **Human escalation**: If deadlock persists after 3 rounds, escalate to human.

**Deadlock detection:**
- If weighted consensus < 0.6 after 3 rounds → deadlock.
- If adjudicator confidence < 0.6 → deadlock.
- If agents cycle through same arguments → deadlock.

### Preventing Premature Consensus

**Anti-herding measures (DynaDebate + Beyond the Strongest LLM):**

1. **Anonymous voting**: Hide agent identities during voting to prevent self-bias.
2. **Independent generation**: Agents generate answers before seeing peer responses.
3. **Dynamic path generation**: If agents converge too quickly, introduce new perspectives (different model, different prompt).
4. **Evidence requirement**: Agents must cite evidence, not just state position.
5. **Devil's advocate**: Assign one agent to argue against the emerging consensus.

## Practical Recommendations

| Recommendation | Implementation | Tools | Threshold |
|----------------|----------------|-------|-----------|
| Weighted voting | Confidence-weighted aggregation | Custom | All multi-agent decisions |
| Reasoning tree | AGENTAUDITOR-style CDP analysis | Custom | Complex disagreements |
| Deadlock breaking | Evidence → track record → conservatism → human | Custom | After 3 rounds |
| Anti-herding | Anonymous voting + independent generation | Custom | All debates |
| Adjudication | Critic or external model as tie-breaker | Custom | Split decisions |
| Early stopping | Stop debate at consensus stabilization | Custom | 3 rounds max |

## Metrics Catalog

| Metric | Definition | How to Measure | Target | Warning |
|--------|-----------|----------------|--------|---------|
| Conflict resolution rate | Resolved without human / total conflicts | Counter | >80% | <60% review mechanisms |
| Decision quality | Correct decisions / total | Log review | >90% | <75% review adjudication |
| Debate rounds to consensus | Average rounds to reach decision | Timer | <3 | >5 simplify |
| Premature consensus rate | Decisions with insufficient exploration | Audit | <10% | >25% add anti-herding |
| Human escalation rate | Escalated to human / total conflicts | Counter | <20% | >40% review mechanisms |
| Adjudicator agreement | Adjudicator agrees with final decision | Counter | >85% | <70% review adjudicator |

## References

1. [RoundTable, 2024] RoundTable: Investigating Group Decision-Making Mechanism in Multi-Agent Collaboration. arXiv:2411.07161.
2. [AGENTAUDITOR, 2026] Auditing Multi-Agent LLM Reasoning Trees Outperforms Majority Vote and LLM-as-Judge. arXiv:2602.09341.
3. [DynaDebate, 2026] DynaDebate: Breaking Homogeneity in Multi-Agent Debate with Dynamic Path Generation. arXiv:2601.05746.
4. [EmergentMind, 2025] Multi-Agent Debate (MAD) Protocols. emergentmind.com/topics.
5. [Beyond the Strongest LLM, 2025] Beyond the Strongest LLM: Multi-Turn Multi-Agent Orchestration. arXiv:2509.23537.
