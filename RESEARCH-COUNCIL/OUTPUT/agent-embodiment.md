# Agent Embodiment and Personality Design

## Executive Summary
Crew v2 agents have SOULs with declared biases but in practice produce similar outputs — voice is not systematically tracked or enforced, and agents converge to the same personality. Research (2025-2026) shows that distinct agent personalities improve team performance through cognitive diversity, but require explicit design to prevent convergence. This document specifies a personality framework with voice dimensions, drift detection, and differentiation patterns, adapted from research on multi-agent personality design and CrewAI's cognitive memory patterns.

## Key Findings

- **CrewAI Cognitive Memory (2025)** demonstrates that agents with distinct memory profiles produce more diverse outputs. Personality is encoded in SOUL.md with specific voice patterns, decision heuristics, and interaction styles [CrewAI, 2025].
- **DynaDebate (arXiv, 2601.05746, 2026)** identifies model homogeneity as a key failure mode: agents with identical mental sets generate nearly identical responses, causing debate to collapse. Dynamic path generation breaks homogeneity by introducing diverse perspectives [DynaDebate, 2026].
- **Beyond the Strongest LLM (2025)** shows that revealing authorship increases self-voting and ties, while showing ongoing votes amplifies herding. Anonymous voting reduces identity-based bias but doesn't address underlying personality convergence [Beyond the Strongest LLM, 2025].
- **Persona Design Research (2025)** establishes that effective agent personas have: (1) clear role identity, (2) distinct voice patterns, (3) specific decision heuristics, (4) interaction style preferences, (5) declared biases and blind spots.
- **Voice Drift Detection (2025)** uses embedding similarity to track consistency of agent voice across sessions. Drift > 30% triggers recalibration.

## Detailed Analysis

### Current Failure Modes

1. **Personality convergence**: All agents produce similar outputs regardless of role.
2. **Voice drift**: Agent voice changes across sessions (soul erosion).
3. **No systematic personality tracking**: No metrics for personality consistency.
4. **No differentiation enforcement**: No mechanism to ensure agents stay distinct.
5. **Homogeneous debate**: Agents agree too quickly, no cognitive diversity.

### Personality Framework

**Five dimensions of agent personality (adapted from CrewAI + Persona Design Research):**

| Dimension | Description | Example (Engineer) | Example (Researcher) |
|-----------|-------------|-------------------|---------------------|
| **Role Identity** | Core purpose and self-conception | "I build things that work" | "I find things that are true" |
| **Voice Patterns** | Language style, tone, formality | Direct, technical, terse | Exploratory, nuanced, verbose |
| **Decision Heuristics** | How decisions are made | "Ship fast, iterate" | "Verify thoroughly before concluding" |
| **Interaction Style** | How agents engage with others | "Tell me what's wrong" | "Let me show you what I found" |
| **Biases & Blind Spots** | Known limitations and preferences | "I favor simplicity over completeness" | "I may over-research simple questions" |

### Voice Specification Template

**Per-agent voice specification (in SOUL.md):**

```markdown
## Voice Specification

### Tone
- [ ] Formal / [ ] Casual / [ ] Technical / [ ] Conversational
- [ ] Direct / [ ] Diplomatic / [ ] Blunt / [ ] Tentative

### Sentence Structure
- [ ] Short and punchy (1-2 clauses)
- [ ] Medium complexity (2-3 clauses)
- [ ] Long and elaborate (3+ clauses)

### Vocabulary Level
- [ ] Simple (accessible to non-experts)
- [ ] Technical (domain-specific terms)
- [ ] Mixed (technical with explanations)

### Argumentation Style
- [ ] Evidence-first (data → conclusion)
- [ ] Principle-first (rule → application)
- [ ] Example-first (anecdote → generalization)

### Interaction Pattern
- [ ] Questioner (asks clarifying questions)
- [ ] Declarer (states findings directly)
- [ ] Collaborator (builds on others' ideas)
- [ ] Challenger (questions assumptions)

### Signature Phrases
- "From an engineering perspective..."
- "The data suggests..."
- "We need to consider..."
- "The risk here is..."
```

### Personality Differentiation Patterns

**Pattern 1: Cognitive Diversity (DynaDebate)**
- Assign different thinking styles to different agents.
- Engineer: convergent thinking (find the best solution).
- Researcher: divergent thinking (explore many possibilities).
- Critic: critical thinking (find flaws).
- Architect: systems thinking (see the big picture).

**Pattern 2: Model Heterogeneity**
- Use different model families for different agents.
- Engineer: Claude (code quality).
- Researcher: GPT (breadth of knowledge).
- Critic: Gemini (analytical reasoning).
- Reduces homogeneity-induced convergence.

**Pattern 3: Prompt Diversification**
- Each agent has unique system prompt with distinct voice.
- Prompts include explicit "do not" instructions to prevent convergence.
- Example: Engineer prompt includes "Do not speculate on alternatives; focus on implementation."

**Pattern 4: Role-Play Anchoring**
- Agents are anchored to specific role-play scenarios.
- Engineer: "You are a senior engineer who has shipped 100+ production systems."
- Researcher: "You are a research scientist who values rigor over speed."
- Anchoring prevents drift by providing consistent identity reference.

### Voice Drift Detection

**Measurement:**
1. Collect agent outputs across sessions (last 10 tasks).
2. Embed outputs using text-embedding-3-small.
3. Compute cosine similarity between current output and historical baseline.
4. Drift score = 1 - cosine_similarity.

**Thresholds:**

| Drift Score | Status | Action |
|-------------|--------|--------|
| < 0.2 | Stable | No action |
| 0.2 - 0.3 | Minor drift | Log warning |
| 0.3 - 0.5 | Moderate drift | Recalibrate: reinforce voice spec in next prompt |
| > 0.5 | Severe drift | Reset: re-inject full voice spec, investigate cause |

**Anti-drift mechanisms:**
1. **Voice spec injection**: Include voice specification in every system prompt.
2. **Periodic anchoring**: Every 10 tasks, re-inject full personality specification.
3. **Peer review**: Other agents flag voice inconsistencies.
4. **Self-monitoring**: Agent checks own output against voice spec before sending.

### Preventing Personality Convergence

**Explicit differentiation rules:**

1. **No agent may use another agent's signature phrases**.
2. **Each agent must have at least 2 unique voice characteristics**.
3. **Debate must include at least 2 distinct perspectives before consensus**.
4. **Anonymous voting prevents identity-based herding**.
5. **Dynamic perspective injection**: If consensus emerges too quickly, assign devil's advocate.

**Convergence detection:**
- If all agents produce outputs with cosine similarity > 0.8 → convergence detected.
- Response: inject new perspective (different model, different prompt, or human input).

## Practical Recommendations

| Recommendation | Implementation | Tools | Threshold |
|----------------|----------------|-------|-----------|
| Voice specification | Per-agent voice spec in SOUL.md | Template above | All agents |
| Drift detection | Embedding similarity monitoring | text-embedding-3-small | Drift > 0.3 |
| Cognitive diversity | Different thinking styles per role | SOUL.md patterns | All roles |
| Model heterogeneity | Different models per agent | Multi-model setup | Key roles |
| Anti-convergence | Explicit differentiation rules | Prompt engineering | Similarity < 0.8 |
| Periodic anchoring | Re-inject voice spec every 10 tasks | Cron | All agents |

## Metrics Catalog

| Metric | Definition | How to Measure | Target | Warning |
|--------|-----------|----------------|--------|---------|
| Voice drift score | Cosine similarity to baseline | Embedding comparison | < 0.2 | > 0.3 recalibrate |
| Personality distinctiveness | Average pairwise similarity | Embedding comparison | < 0.6 | > 0.8 convergence |
| Perspective diversity | Distinct perspectives in debate | Count | ≥ 2 | < 2 inject new perspective |
| Voice spec compliance | Outputs matching voice spec | LLM evaluation | > 90% | < 70% reinforce spec |
| Model homogeneity | Same model used for all agents | Config check | < 50% same | > 80% diversify |

## References

1. [CrewAI, 2025] How we built Cognitive Memory for Agentic Systems. blog.crewai.com.
2. [DynaDebate, 2026] DynaDebate: Breaking Homogeneity in Multi-Agent Debate. arXiv:2601.05746.
3. [Beyond the Strongest LLM, 2025] Multi-Turn Multi-Agent Orchestration. arXiv:2509.23537.
4. [Persona Design Research, 2025] Effective Agent Personas: Design Principles. **[unverified — generic attribution; primary source could not be located, 2026-09-13. Treat the five dimensions as a design template, not an empirical finding.]**
5. [Voice Drift Detection, 2025] Embedding-Based Consistency Monitoring. **[unverified — generic attribution; the 0.2/0.3/0.5 thresholds are heuristics, not published benchmarks. Calibrate on Crew v2's own output history before enforcing.]**

## [DEEP DIVE]: Activation-Space Voice Monitoring (Persona Vectors), Collapse Dynamics of Convergence, and Functional Diversity Metrics (freebuff, 2026-09-13)

### 1. Persona vectors: upgrade drift detection from output embeddings to activation space

Anthropic's persona vectors work identifies **directions in the model's activation space underlying character traits** (e.g., sycophancy, humor, evil) and uses them to (a) *monitor* trait fluctuation in deployment before it surfaces in outputs, and (b) flag training data likely to induce unwanted trait shifts [Chen et al. / Anthropic, arXiv:2507.21509]. For Crew v2 this is the mechanism the output-similarity heuristic (1 - cosine) approximates:

- Output-embedding drift (the current spec) detects drift *after* it reaches text; persona vectors detect *during* generation. When self-hosted/open-weight models are used, extract the prefill-activation projection and alarm on sustained activation drift even when outputs look stable (early-warning, ~zero output tokens burned).
- The same technique explains the SOUL's limits: prompt-level voice instructions are weakly enforced relative to what the activation geometry supports. So treat the voice spec as a *control input*, and drift alarms (output-side) as the enforcement layer — matching the security deep dive's "externalize enforcement" principle.
- Practical adoption path: run output-embedding drift now (no infra change); add activation-space monitoring per role when the crew moves to an open-weight model where hooks are available; keep the 0.2/0.3/0.5 thresholds but restate them as calibrated-on-crew-data (the original doc already flags this honestly).

### 2. Convergence as model collapse: the tails disappear first

Shumailov et al. (Nature, 2024, ~1900 citations) showed models trained recursively on synthetic outputs suffer **irreversible defects: the tails of the distribution vanish first** [Shumailov et al., 2024]. The crew's convergence failure mode is the organizational analogue: agents exchanging outputs (memory, debate transcripts, shared context) that feed each other's generations will lose *rare perspectives* first — the critic's contrarianism, the researcher's minority-source findings — long before average pairwise similarity crosses 0.8. Two derived rules:

1. **Convergence metrics must be tail-sensitive**: track pairwise similarity at the 90th percentile and the *distinct-perspective count* (see §3), not just the mean; means hide exactly the collapse that matters.
2. **Quarantine human/external grounding**: memory writes from external sources (docs, human feedback, web) should be tagged and never fully replaced by intra-crew derived content — mirroring the collapse-prevention finding that access to true original data halts collapse [Shumailov et al., 2024]. Concretely: Tier-3 insight compaction must preserve ≥1 external evidence link per insight (memory-architecture corroboration already requires two *independent* sources — extend one of them to be external-grounded).

### 3. Distinct-Perspective Count (DPC): a measurable diversity instrument

Replace the fuzzy "≥2 distinct perspectives" with an instrument computable from the existing debate transcripts:

```
DPC(round) = number of clusters in the round's argument embeddings
             (agglomerative, threshold = 1 - 0.7 cosine)
Gate: DPC < 2 in round 1 → inject perspective (different model family,
      devil's advocate SOUL, or external citation requirement) before
      any vote is allowed.
```

This operationalizes DynaDebate's anti-homogeneity finding as a pre-vote gate rather than a post-hoc observation, and gives the "perspective diversity" metric in the catalog a deterministic measurement procedure.

### 4. Role conflict as an embodied property, not a bug

The embodiment doc treats distinctiveness as style; the strongest reason for it is functional. RoundTable/DynaDebate results (already cited) show homogeneous agents collapse to majority voting, and the conflict-resolution deep dive derives the value of adversarial roles (devil's advocate, HOLD-wins tester). Embodiment guidance: assign each agent a *declared conflict duty* in its SOUL (e.g., critic must always produce one falsification attempt; researcher must always surface one contradicting source) — behavioral commitments that make diversity robust to model homogeneity, which prompt-style differentiation alone cannot guarantee when all agents share a model family.

### 5. Authorship disclosure: keep votes anonymous, keep debates attributed

The existing findings (authorship disclosure increases self-voting; visible ongoing votes amplify herding [Beyond the Strongest LLM, 2025]) map to a two-channel rule: **debate transcripts carry attribution** (accountability, traceability — W3C traceparent from comm-protocols), while **votes are anonymous and simultaneous** (bias control). Do not collapse the two channels: anonymous debates destroy auditability; attributed votes reintroduce herding.

### References for deep dive

- [Chen et al. / Anthropic, 2025] Persona Vectors: Monitoring and Controlling Character Traits in Language Models. arXiv:2507.21509; anthropic.com/research/persona-vectors.
- [Shumailov et al., 2024] AI models collapse when trained on recursively generated content. Nature 631, 755-759. nature.com/articles/s41586-024-07566-y.
- [DynaDebate, 2026] arXiv:2601.05746 (dynamic path generation vs homogeneity).
- [Beyond the Strongest LLM, 2025] arXiv:2509.23537 (authorship/herding effects).
- [RoundTable, 2024] arXiv:2411.07161 (group decision-making).
