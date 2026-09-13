# CONTEXT — The System You Are Researching

## What is Crew v2?

Crew v2 is a multi-agent AI crew — a system of specialized AI agents that work together on tasks. It is built on the Hermes Agent framework (https://hermes-agent.nousresearch.com).

## Architecture

### Agents and Their Roles

| Agent | Role | Tools | Limitation |
|-------|------|-------|------------|
| **firstmate** | Router — classifies tasks, selects formations | message_agent | None known |
| **researcher** | Searches web/sources, gathers evidence | web_search, web_extract | None known |
| **engineer** | Writes code, tests it, ships it | terminal, read_file, write_file | **FORGETS TO WRITE TESTS** |
| **architect** | Designs systems before code | read_file, search_files, write_file | None known |
| **critic** | Independent verification of work | terminal, read_file | **TIMES OUT on complex tasks** |
| **tester** | Writes and runs tests, gates releases | TBD | **Does not exist yet** |
| **razor** | Removes redundancy, preserves meaning | read_file, write_file | **BREAKS CONSTRAINTS** |
| **completer** | Final check before release | read_file, terminal | **Does not block on missing tests** |

### Formations (selected per task)

```
SOLO   = One agent (engineer OR researcher)
DUO    = executor → verifier
PIPELINE = researcher → architect → engineer → critic
FULL   = All agents working together
```

### Task Classification

Every task is classified on three axes:

| Axis | Values |
|------|--------|
| **Complexity** | simple / moderate / complex / unknown |
| **Verifiability** | self-evident / testable / external-source / unverifiable |
| **Tool needs** | read-only / write / execute / mixed |

## The Problem We Must Solve

### Core Failure Mode

**The engineer agent consistently forgets to write tests.**

This is not a minor issue — it is the #1 cause of quality failures in the crew.

### Consequences

1. Code ships untested — bugs reach users
2. The critic (verification agent) times out on large tasks
3. No agent has authority to block code that lacks tests
4. The "anti-bloat" agent (razor) actively makes things worse by changing wording when tasks say "do not change wording"

### Empirical Evidence

**Trial: COORD-01 (runs IC1/EA1/OH1)**
- Three task types: logic puzzle, bug finding, grammar correction
- Engineer produced code for all three — **zero test files**
- "Write tests" was an explicit task requirement — ignored

**Trial: COORD-02 (currency converter)**
- Task: Build a multi-module CLI currency converter with 4 modules
- Engineer built all 4 modules (135 lines total)
- **Zero test files produced**
- Operator had to write 11 tests manually — all passed

**Trial: T09-T12 (correction-class probes)**
- Engineer implemented fixes to system rules
- Never regression-tested the original failure cases
- Bugs recurred in subsequent runs

### Root Cause Analysis

1. **Engineer SOUL has no test requirement.** Nothing in the agent's instructions says "write tests before declaring done."
2. **Critic SOUL lacks timeout configuration.** It dies on complex tasks.
3. **Critic SOUL lacks path awareness.** It searches in wrong directories.
4. **Completer SOUL has no test execution requirement.** It does not run tests.
5. **No blocking authority exists.** No agent can say "no, this is not done."

## What Currently Exists

### TESTING-COUNCIL.md (High-Level Philosophy)

Defines WHAT and WHY but not HOW:
- Core principles (test behavior not implementation)
- Testing lifecycle per feature
- Test types (unit/integration/e2e)
- Anti-patterns checklist

### tester SOUL (Incomplete)

Defines role but not implementation. Missing:
- Exact activation conditions
- Operating procedure
- Blocking conditions
- Output format
- Calibration rules

### firstmate SOUL (Updated)

Has tester activation rules but:
- No formation selection table with tester
- No artifact flow specification
- No message flow specification

### The Gap

**We have philosophy but no implementation.** We know WHAT we want and WHY we want it, but not HOW to build it, MEASURE it, or IMPROVE it.

## Your Mission

Build the **implementation-ready testing discipline** for Crew v2. Your research must answer:

1. What exactly should the tester do, step by step?
2. What exactly should the engineer do before declaring done?
3. What metrics should we track?
4. What thresholds should we set?
5. How do we gate releases on test results?
6. How do we handle disagreements?
7. How do we calibrate the tester over time?

## Success Criteria

Your research is successful if a developer can read your output and immediately:
1. Write the tester SOUL
2. Update the engineer SOUL
3. Configure CI/CD gates
4. Measure test quality
5. Run a maturity self-assessment

## Sources to Consult

- Academic: IEEE, ACM, arXiv on software testing
- Industry: Google, Microsoft, Meta, Stripe testing practices
- Books: Kent Beck TDD, Martin Fowler testing, Freeman & Pryce GOOS
- Tools: pytest, Hypothesis, mutmut, coverage.py
- Recent: AI-generated code testing (2024-2026)
