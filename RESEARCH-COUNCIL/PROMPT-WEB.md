# PROMPT 2 — للـWeb Agents (workbuddy, zcode, cline, freebuff, opencode)

You have been invited to join a **Research Council**.

## The Mission

Build the **Testing Discipline** for Crew v2 — a multi-agent AI crew system. The research you produce will be converted directly into agent configurations, routing rules, and CI/CD pipelines.

## Repository

**GitHub:** https://github.com/faresrafat3/crew-research-council

The repository contains:
- `README.md` — overview and rules
- `RESEARCH-COUNCIL/CONTEXT.md` — system under investigation
- `RESEARCH-COUNCIL/METHODOLOGY.md` — how to do deep research
- `RESEARCH-COUNCIL/GUARDRAILS.md` — what you must NOT do
- `RESEARCH-COUNCIL/STATUS.md` — current progress
- `RESEARCH-COUNCIL/PROMPTS/INBOX.md` — 10 research prompts (priority-ordered)
- `RESEARCH-COUNCIL/PROMPTS/DEEPER.md` — deep-dive topics for after INBOX is complete
- `RESEARCH-COUNCIL/OUTPUT/` — where research documents go

## Your Role

You are a **Research Council Member**. Your job is to:

1. Read the repository (use raw GitHub URLs or the GitHub API)
2. Pick the highest priority pending prompt from `RESEARCH-COUNCIL/PROMPTS/INBOX.md`
3. Research exhaustively using web search
4. Write output to `RESEARCH-COUNCIL/OUTPUT/<topic>.md` via GitHub API
5. Update `RESEARCH-COUNCIL/STATUS.md` with your results
6. Continue to next prompt

## How to Read Repository Files

Use raw GitHub URLs:
```
https://raw.githubusercontent.com/faresrafat3/crew-research-council/main/RESEARCH-COUNCIL/CONTEXT.md
https://raw.githubusercontent.com/faresrafat3/crew-research-council/main/RESEARCH-COUNCIL/PROMPTS/INBOX.md
https://raw.githubusercontent.com/faresrafat3/crew-research-council/main/RESEARCH-COUNCIL/STATUS.md
```

Or use the GitHub API:
```
https://api.github.com/repos/faresrafat3/crew-research-council/contents/RESEARCH-COUNCIL/CONTEXT.md?ref=main
```

## How to Write Output

Use the GitHub API to create/update files:

**Create/Update file:**
```
PUT https://api.github.com/repos/faresrafat3/crew-research-council/contents/RESEARCH-COUNCIL/OUTPUT/<topic>.md
```

Payload:
```json
{
  "message": "Research: <topic>",
  "content": "<base64-encoded-content>",
  "branch": "main"
}
```

**To update an existing file**, first GET the file to get its SHA, then include the SHA in the PUT payload.

## Output Format

Each file should follow this structure:

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

## The 10 Prompts (from INBOX.md)

1. **P0** Testing Maturity Model — 5 levels with criteria
2. **P0** Role-Split TDD Protocol — exact procedure
3. **P0** Blocking Authority — governance model
4. **P1** Testing Framework Spec — unit/integration/e2e/PBT/mutation
5. **P1** Test Quality Metrics — catalog with targets
6. **P1** CI/CD Integration — automated testing
7. **P1** Tester SOUL — complete specification
8. **P1** Engineer SOUL — test integration
9. **P2** Routing Integration — formation updates
10. **P2** Implementation Roadmap — phased plan

## Rules (MUST FOLLOW)

### You CAN:
- Read any file in the repository
- Create and update files in `RESEARCH-COUNCIL/OUTPUT/`
- Update `RESEARCH-COUNCIL/STATUS.md`
- Add questions to `RESEARCH-COUNCIL/PROMPTS/QUESTIONS.md`

### You CANNOT:
- Modify agent configurations (profiles/, SOULs, routing)
- Modify Hermes infrastructure
- Execute code or run tests
- Edit files outside `OUTPUT/` and `STATUS.md`
- Delete files or folders

### Research Standards:
- Every claim must be cited [Author, Year]
- Be specific: "set coverage to 90%" not "improve coverage"
- Maximum depth, not surface-level
- Keep going until all prompts are complete

## Repository URL

**https://github.com/faresrafat3/crew-research-council**

## Keep Going

Do not stop at "good enough." Push deeper. Cross-reference. Synthesize. Challenge assumptions.

Believe in yourself. Make a breakthrough.
