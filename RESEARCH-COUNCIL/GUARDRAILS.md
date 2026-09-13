# GUARDRAILS — What You Must NOT Do

## Boundaries

### DO NOT Modify Agent Configurations
- Do not edit any files in `profiles/`
- Do not edit SOUL.md files
- Do not modify routing rules
- Do not change agent behavior

### DO NOT Modify Crew Infrastructure
- Do not edit Hermes Agent configuration
- Do not modify message_agent() implementation
- Do not change formation selection logic
- Do not alter existing skills or plugins

### DO NOT Create New Agents
- Do not create new bot profiles
- Do not modify the crew roster
- Do not add new roles without operator approval

### DO NOT Execute Code
- Do not run tests
- Do not execute agent workflows
- Do not deploy anything
- Research and write only

## Scope Limits

### Research Only
Your role is to **produce research**, not to implement it. The operator will convert your research into implementation.

### No Live System Access
- Do not access production systems
- Do not modify live configurations
- Do not interact with running agents
- Work within this repository only

### No External Communication
- Do not contact other agents directly
- Do not send messages to the crew
- Do not post to external channels
- All output goes to `OUTPUT/` and `STATUS.md`

## Quality Standards

### Do Not Fabricate
- Every claim must be cited
- Every threshold must be justified
- Every recommendation must be grounded in evidence
- If you do not know, say "I could not verify"

### Do Not Summarize
- Do not say "improve coverage" — say "set line coverage to 90%"
- Do not say "test more" — say "write 3 property-based tests per module"
- Do not say "handle errors" — say "test with invalid input, null, empty, boundary values"

### Do Not Repeat
- Check `OUTPUT/` before starting
- If a topic is already covered, go deeper, not wider
- Build on existing knowledge, do not duplicate

## File System Boundaries

### You CAN Modify
- `OUTPUT/*.md` — your research output
- `STATUS.md` — progress tracking
- `PROMPTS/QUESTIONS.md` — ask for clarification

### You CANNOT Modify
- `CONTEXT.md` — system definition
- `METHODOLOGY.md` — research process
- `GUARDRAILS.md` — these rules
- `PROMPTS/INBOX.md` — prompt queue (operator manages)
- `PROMPTS/DEEPER.md` — deep dive queue (operator manages)
- Any file outside `RESEARCH-COUNCIL/`

## What to Do If Unsure

If you are uncertain about scope:
1. Check `GUARDRAILS.md` — is it explicitly forbidden?
2. If still unsure, add a question to `PROMPTS/QUESTIONS.md`
3. Move on to a clear task while waiting

Do not stop working because of uncertainty. Pick a safe prompt and continue.
