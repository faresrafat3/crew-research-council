# Deep Dive Queue — Go Deeper on Existing Research

## How This Works

After all prompts in `PROMPTS/INBOX.md` are complete, pick a topic from this file to research at greater depth. These are follow-up questions that build on initial research.

## Queue

### Testing Maturity Model — Deep Dives
- What are the exact assessment questions for each level?
- What tools are needed at each level?
- How long does it typically take to move between levels?
- What are the common failure modes at each level?

### TDD Protocol — Deep Dives
- How to handle flaky tests in the TDD cycle?
- What is the state machine for the protocol?
- How to handle async communication delays?
- What happens when the tester itself has bugs?

### Testing Framework — Deep Dives
- What are the exact pytest configuration options?
- How to structure a conftest.py for AI agent outputs?
- What Hypothesis strategies are most effective for AI outputs?
- What mutation operators catch the most AI-specific bugs?

### Quality Metrics — Deep Dives
- What are industry benchmarks for each metric?
- How to set team-specific targets?
- How to visualize test quality over time?
- What leading indicators predict test effectiveness?

### Blocking Authority — Deep Dives
- What are real-world examples of tester blocking abuse?
- How to calibrate tester strictness automatically?
- What is the optimal escalation time?
- How to handle tester-critic collusion?

### CI/CD — Deep Dives
- What is the exact GitHub Actions workflow configuration?
- How to parallelize test execution?
- What artifact retention policy to use?
- How to handle secrets in test environments?

---

## Completed Deep Dives

- Testing Maturity Model — assessment questions, tools per level, level timelines, failure modes (scout, 2026-09-13)
- TDD Protocol — flake handling, state machine, async delays, tester bugs (scout, 2026-09-13)
- Testing Framework — pytest config, conftest.py, Hypothesis strategies, mutation operators (scout, 2026-09-13)
- Quality Metrics — benchmarks, target-setting, visualization, leading indicators (scout, 2026-09-13)
- Blocking Authority — abuse examples, calibration, escalation time, collusion (scout, 2026-09-13)
- CI/CD — workflow YAML, parallelization, artifact retention, secrets (scout, 2026-09-13)
- Tester SOUL — oracle quality, assertion strength taxonomy, determinism harness, verdict provenance fields (freebuff, 2026-09-13 — appended in OUTPUT/tester-soul.md)
- Tester SOUL — production mutation deployment (Google/Meta), agent-test value under scrutiny, suite-evolution hazards (cline, 2026-09-13 — appended in OUTPUT/tester-soul.md)
