# METHODOLOGY — How to Do Deep Research

## Research Process

### Step 1: Understand the Context
Read `CONTEXT.md` fully. Understand the system, the problem, and what is needed.

### Step 2: Read Existing Knowledge
Check `OUTPUT/` for existing research. Read what has been done. Do not repeat — extend.

### Step 3: Pick a Prompt
Check `PROMPTS/INBOX.md` for the highest priority pending item. If empty, pick from `PROMPTS/DEEPER.md`.

### Step 4: Research Exhaustively
1. **Search broadly first** — get an overview of the field
2. **Search deeply** — find primary sources, academic papers, industry reports
3. **Cross-reference** — verify claims across multiple sources
4. **Synthesize** — combine findings into a coherent framework
5. **Implement** — make it practical and specific

### Step 5: Write Output
Write to `OUTPUT/<topic>.md`. Structure:
- Executive Summary (3-5 sentences)
- Key Findings (bullet points, max 10 per section)
- Detailed Analysis (exhaustive, cited)
- Practical Recommendations (specific, implementable)
- Metrics and Targets (with numbers)
- Citations (inline + references section)

### Step 6: Update STATUS
Update `STATUS.md` with what you completed and what you found.

### Step 7: Continue
Go to Step 3. Keep going until all prompts are complete.

## Research Standards

### Citations
Every claim needs a source. Format:
- Inline: [Author, Year] or [Organization, Year]
- Section: `## References` at end of document

### Specificity
Bad: "Improve test coverage."
Good: "Set line coverage threshold to 90%, branch coverage to 80%, mutation score to 85%."

### Completeness
Do not stop at surface level. If you find a technique, research its:
- How to implement
- What tools to use
- What thresholds to set
- What can go wrong
- How to verify it works

## Search Strategy

### Query Patterns
1. `"[topic] [year]"` — latest research
2. `"[topic] best practices"` — established wisdom
3. `"[topic] anti-patterns"` — what NOT to do
4. `"[topic] [tool name]"` — tool-specific guidance
5. `"[topic] metrics"` — how to measure

### Sources Priority
1. **Peer-reviewed** — IEEE, ACM, arXiv, Springer
2. **Industry权威** — Google, Microsoft, Meta, Stripe, Netflix
3. **Books** — Established textbooks
4. **Tools docs** — Official documentation
5. **Blogs** — Practitioner experience

## Output Format

```markdown
# [TOPIC]

## Executive Summary
[3-5 sentences summarizing everything]

## Key Finding 1: [Title]
[Detailed analysis with citations]

## Key Finding 2: [Title]
[Detailed analysis with citations]

...

## Practical Recommendations
| Recommendation | Implementation | Tools | Threshold |
|---------------|----------------|-------|-----------|
| ... | ... | ... | ... |

## Metrics Catalog
| Metric | Definition | How to Measure | Target | Warning |
|--------|-----------|----------------|--------|---------|
| ... | ... | ... | ... | ... |

## References
1. [Author, Year] Title. Source.
2. ...
```

## Going Deeper

After completing all prompts in `PROMPTS/INBOX.md`, start deep-dive cycles:

1. Pick an existing output in `OUTPUT/`
2. Identify gaps or shallow areas
3. Research those areas deeper
4. Append findings with `[DEEP DIVE]` markers
5. Update `STATUS.md`

## Keep Going

Do not stop at "good enough." Push deeper. The quality of this research directly determines the quality of the Crew v2 testing discipline.

Believe in yourself. Make a breakthrough.
