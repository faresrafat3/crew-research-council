# Routing and Formation Integration

## Executive Summary
Tester joins DUO as verifier, PIPELINE as pre-engineering RED author plus final gate, and FULL as mandatory gate with critic review; SOLO stays lightweight. Activation triggers on testability, acceptance criteria, DONE claims, source touches, or complex formations. Message flows carry SPEC, RED, GREEN, suite evidence, critic review, and verdict artifacts in order, with large tests scheduled async so gates stay under 10 minutes [SQRBOK, 2025].

## Key Findings
- DUO is executor plus verifier, PIPELINE is sequential specialists, FULL is all agents [Council Context, 2026].
- Classification axes are complexity, verifiability, and tool needs [Council Context, 2026].
- Tester activation gaps (no formation table, no artifact or message flow) block implementation [Council Context, 2026].
- Pyramid discipline keeps most tests small and fast [SQRBOK, 2025].
- Small-immediate, medium-queued, large-parallel scheduling protects feedback speed [SQRBOK, 2025].
- Handoff agents with explicit prompts transfer cleanly between phases [Microsoft, 2026].
- Independent verification needs separation from implementation rationale [IJECS, 2026].
- Evidence-bound verdicts (inputs, outputs, traces, policy) make gates auditable [QABattle, 2025].
- E2E bloat belongs capped and pushed down to unit and integration [KnowMBA, 2025].
- Async large suites prevent gate timeouts on complex tasks [ArXiv, 2026].

## Detailed Analysis
New table: SOLO unchanged (tester-lite lint advisory); DUO engineer-then-tester with unit plus PBT sample and pytest-fail BLOCK only; PIPELINE researcher-architect-engineer-tester-critic-tester with RED before GREEN and 70% mutation BLOCK; FULL all-agents with mandatory critic plus 80% mutation and 90% req-coverage BLOCKs. Activate tester when testable, criteria exist, DONE claimed, `src/` touched, formation is PIPELINE/FULL, or nightly/drill/appeal/human requests. Skip tester for pure read-only research, trivial sub-5-line SOLO, infra outages (defer), and diff-free redispatches. DUO flow: SPEC, REQUEST_TESTS, RED, ENGINEER_DONE, verdict. PIPELINE adds architect outputs, suite evidence, critic review, final verdict. Artifacts per edge: REQ-IDs, test files plus RED log, impl plus GREEN log, JUnit plus coverage plus mutation plus lints plus flake snapshot, critic pass/fail, PROMOTE/HOLD/ROLLBACK plus ledger entry.

## Practical Recommendations
| Recommendation | Implementation | Tools | Threshold |
|---|---|---|---|
| Publish formation table | firstmate SOUL patch | SOUL | all dispatches |
| Tag needs_tester | testable OR criteria OR done OR src OR complex | classifier | 100% PIPE/FULL |
| Enforce message order | SPEC-RED-GREEN-suite-review-verdict | message_agent | no skips |
| Pass artifacts | paths+logs+reports at each edge | ledger/S3 | 100% present |
| Async large tests | nightly E2E/full mutation | scheduler | gate <10 min |

## Metrics and Targets
| Metric | Definition | How to Measure | Target | Warning |
|---|---|---|---|---|
| Activation recall | complex tasks with tester | ledger | 100% PIPE/FULL | <100% fix rules |
| Activation precision | tester runs with value | verdict audit | >80% gated | <50% loosen |
| Handoff completeness | required artifacts present | CI check | 100% | <100% HOLD |
| Gate duration | SPEC to verdict | timer | <10 min block | >10 min async |
| Misroute rate | wrong formation selected | review | <5% | >5% retune |

## References
1. [Council Context, 2026] Crew v2 formations and classification axes.
2. [SQRBOK, 2025] Pyramid and tiered scheduling.
3. [Microsoft, 2026] Handoff agents pattern.
4. [IJECS, 2026] Independent verification with HITL.
5. [QABattle, 2025] Evidence-bound verdicts.
6. [KnowMBA, 2025] E2E caps and budgets.
7. [ArXiv, 2026] Self-testing gates at scale.
