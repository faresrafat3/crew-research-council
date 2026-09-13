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

## [DEEP DIVE]: Firstmate Classifier Rules, Message Ordering, Artifact Ledger Schema, and Misroute Correction

> Extends `routing-integration.md` (46 lines, via `gh api repos/faresrafat3/crew-research-council/contents/RESEARCH-COUNCIL/OUTPUT/routing-integration.md`). Does not repeat base — adds exact classifier table, per-edge timeouts/retries, SQLite ledger DDL, and misroute-correction loop.

### 1. Firstmate classifier rules (complexity × verifiability × tool-needs → formation + needs_tester)

Classification axes are complexity, verifiability, and tool needs [Council Context, 2026]. This mirrors LLM-routing practice where a router first infers query characteristics then picks strong vs weak path: RouteLLM trains similarity-weighted, matrix-factorization, BERT and causal-LLM classifiers on preference data to route only hard queries to GPT-4, cutting cost 85% on MT-Bench / 45% MMLU / 35% GSM8K at 95% quality [LMSYS RouteLLM, 2024]. Firstmate applies the same idea to formations: cheap SOLO for easy/self-evident, expensive FULL only when complexity + external/unverifiable + mixed tools demand it.

**Input enums (exact):**
- `complexity`: `simple` (<5-line change, single file, no design) | `moderate` (multi-file, known pattern) | `complex` (new design, cross-cutting, migration) | `unknown` (cannot infer from SPEC)
- `verifiability`: `self-evident` (lint/format, deterministic eyeball) | `testable` (unit/PBT/mutation checkable in-repo) | `external` (needs staging, device, human, third-party) | `unverifiable` (no oracle; judgment call)
- `tool-needs`: `read` (search/read-only) | `write` (edit files, no exec) | `execute` (run cmds/tests/build) | `mixed` (write+execute, DB, network)

**Output:** `formation ∈ {SOLO, DUO, PIPELINE, FULL}` + `needs_tester: boolean`. Tester activates when testable OR criteria exist OR DONE claimed OR `src/` touched OR formation is PIPELINE/FULL [Council Context, 2026]; skip for pure read-only research, trivial sub-5-line SOLO, infra outages (defer), diff-free redispatches [routing-integration.md base].

**Decision table (10 rows; first-match wins, top-down):**

| # | complexity | verifiability | tool-needs | → formation | needs_tester | Rationale |
|---|---|---|---|---|---|---|
| 1 | simple | self-evident | read | SOLO | false | trivial read/lint advisory only; SOLO stays lightweight [Council Context, 2026] |
| 2 | simple | self-evident | write | SOLO | false | sub-5-line SOLO skip rule; tester-lite lint advisory only |
| 3 | simple | testable | execute/mixed | DUO | true | executor+verifier; unit+PBT sample, pytest-fail BLOCK [Council Context, 2026] |
| 4 | moderate | testable | write/execute | DUO | true | DUO engineer-then-tester flow SPEC→REQUEST_TESTS→RED→ENGINEER_DONE→verdict |
| 5 | moderate | testable | mixed | PIPELINE | true | sequential specialists researcher-architect-engineer-tester-critic-tester; RED before GREEN, 70% mutation BLOCK |
| 6 | moderate | external | execute/mixed | PIPELINE | true | pre-engineering RED author + final gate; async large suites so gate <10min [SQRBOK, 2025] |
| 7 | complex | testable | mixed | FULL | true | all-agents with mandatory critic + 80% mutation + 90% req-coverage BLOCKs |
| 8 | complex | external/unverifiable | mixed/execute | FULL | true | independent verification separated from implementation rationale [IJECS, 2026]; evidence-bound verdict required [QABattle, 2025] |
| 9 | simple/moderate | unverifiable | read/write | SOLO | false | no oracle → no tester value; route to human-readable summary, log precedent |
| 10 FALLBACK | unknown | *any* | *any* | DUO if testable/criteria/src-touched else SOLO; escalate to PIPELINE on second failure | `testable OR criteria OR done OR src` | unknown never routes direct to FULL; RouteLLM generalization result (same routers transfer Claude-3-Opus/Llama-3-8B without retrain) justifies conservative default + augmentation on miss [LMSYS RouteLLM, 2024]; retune after 5 replays (see §4) |

Fallback rule: `unknown` complexity → default SOLO unless any tester trigger fires → DUO; never FULL on first pass; if DUO verdict=HOLD twice, promote to PIPELINE and log precedent. This caps E2E bloat by pushing verification down to unit/integration [KnowMBA, 2025] and keeps pyramid discipline (most tests small/fast) [SQRBOK, 2025].

### 2. Message ordering (sequence, per-edge timeouts, skip rules, retries)

Canonical order — DUO: `SPEC → REQUEST_TESTS → RED → ENGINEER_DONE → verdict`; PIPELINE/FULL add `architect outputs → suite evidence → critic review → final verdict` [routing-integration.md base]. Handoff pattern uses explicit prompts/agents between phases [Microsoft Agent Framework, 2026]; each handoff is a transit document dead once work lands, not a maintained artifact [AiHero /handoff, 2026], so ordering must be enforced by `message_agent`, not convention.

Why strict ordering: agents assume sequential delivery but networks/queues reorder; financial-trading example shows execution signal arriving before price update causes wrong-price execution without explicit guarantees [Maxim, 2026]. Multi-agent stacks (ChatDev dialogues, MetaGPT pub-sub pool, AutoGen conversations) share artifacts with no causal ordering or stale-read detection — two writers, no version vectors [Meiklejohn, 2026]. Concurrency failures map directly to stale reads / lost updates / inconsistent outcomes amplified by long LLM windows; fix with conflict detection + isolation + structured access [Yang et al., ArXiv 2026]. Handoff note must therefore carry GOAL/DONE/FINDINGS/DECISIONS/OPEN/NEXT/WHERE pointers, because receiver opens cold with no transcript access [Taskade, 2026]; distilled state (contract, current state, decisions+reasons, dead ends, single open question) beats full transcript which transfers noise and burns budget [PaellaDoc, 2026].

**Per-edge timeouts (enforced by orchestrator; `asyncio.wait_for`-style with future cleanup [Mitra, 2024]):**

| Edge | Timeout | Owner | On timeout |
|---|---|---|---|
| SPEC → REQUEST_TESTS (dispatch + tester tag) | 30 min | firstmate | retry ×1, then ESCALATE_HUMAN |
| REQUEST_TESTS → RED (tester authors failing tests) | 15 min | tester | retry ×1 with narrowed scope, then HOLD |
| RED → ENGINEER_DONE (GREEN impl) | 30 min | engineer | retry ≤2, then ESCALATE_HUMAN |
| ENGINEER_DONE → suite (JUnit+coverage+mutation+lint+flake snapshot) | async; gate slice <10 min block | tester/scheduler | small-immediate, medium-queued, large-parallel/nightly [SQRBOK, 2025] |
| suite → critic review | 10 min/file, 30 min/task cap | critic | skip only ifFormation=DUO (no critic); PIPELINE/FULL critic mandatory |
| critic → verdict (PROMOTE/HOLD/ROLLBACK + ledger entry) | 5 min | tester/verifier | evidence-bound verdict (inputs/outputs/traces/policy) [QABattle, 2025] |

Total blocking gate target <10 min SPEC-to-verdict; async large suites (nightly E2E/full mutation) prevent gate timeouts [ArXiv, 2026].

**Skip rules:** skip tester for pure read-only research, trivial sub-5-line SOLO, infra outage (defer, not fail), diff-free redispatch; DUO skips critic; SOLO skips everything except lint advisory. No other skips — `message_agent` rejects out-of-order edges (e.g., ENGINEER_DONE without RED log when needs_tester=true → HOLD).

**Retry/escalation:** retry ≤2 per edge with exponential backoff (60s, 300s, 900s progression per DLQ pattern [Mitra, 2024]); differentiate timeout (retry immediately) vs rate-limit (delay) vs validation error (no retry) [Mitra, 2024]. After 2 failures → `ESCALATE_HUMAN` + move message to dead-letter queue for manual review with `retry_count`, `last_error_time` [Mitra, 2024]; idempotency tokens + deduplication required because timeout-retry ambiguity causes double-execution (payment double-charge example [Maxim, 2026]). Handoff latency baseline 100–500ms per interaction informs timeout budget vs processing time [Maxim, 2026]; coordination overhead must be measured as agent count grows [Maxim, 2026].

Reference implementation pattern: `Event {event_type, payload, application_id, correlation_id, timestamp, producer, version="1.0", retry_count}` with version-compat check + per-type validators + audit store [Mitra, 2024]; ordered delivery via per-application `sequence_numbers` + `asyncio.Queue` hold-back for out-of-order [Mitra, 2024]; broadcast config/health on separate channels with subscription filters [Mitra, 2024].

### 3. Artifact ledger schema (SQLite + per-edge artifacts + retention)

Ledger makes gates auditable via evidence-bound verdicts [QABattle, 2025] and satisfies financial-grade audit (input/output/processing-time/error per action [Mitra, 2024]). Design follows LEDGER: Trace Records (deterministic substrate) → Evidence Nodes (tool-call+result grouped) → Workflow Nodes (phase) → artifact anchors with typed edges `uses/produces/checked_by/supports/frames/informs` [LEDGER, ArXiv 2026]. Artifacts are evidence anchors enabling claim→artifact→action backward traversal [LEDGER, ArXiv 2026].

**SQLite DDL (ledger.db):**

```sql
CREATE TABLE tasks (
  task_id      TEXT PRIMARY KEY,
  spec_path    TEXT NOT NULL,
  complexity   TEXT CHECK(complexity IN ('simple','moderate','complex','unknown')),
  verifiability TEXT CHECK(verifiability IN ('self-evident','testable','external','unverifiable')),
  tool_needs   TEXT CHECK(tool_needs IN ('read','write','execute','mixed')),
  formation    TEXT CHECK(formation IN ('SOLO','DUO','PIPELINE','FULL')),
  needs_tester INTEGER NOT NULL,          -- boolean 0/1
  created_at   TEXT NOT NULL              -- ISO8601
);
CREATE TABLE runs (
  run_id       TEXT PRIMARY KEY,
  task_id      TEXT REFERENCES tasks(task_id),
  edge         TEXT NOT NULL,              -- SPEC|REQUEST_TESTS|RED|ENGINEER_DONE|suite|critic|verdict
  agent        TEXT NOT NULL,              -- firstmate|researcher|architect|engineer|tester|critic
  status       TEXT NOT NULL,              -- OK|HOLD|RETRY|ESCALATED
  started_at   TEXT NOT NULL,
  ended_at     TEXT,
  retry_count  INTEGER DEFAULT 0
);
CREATE TABLE verdicts (
  verdict_id   TEXT PRIMARY KEY,
  task_id      TEXT REFERENCES tasks(task_id),
  decision     TEXT CHECK(decision IN ('PROMOTE','HOLD','ROLLBACK')),
  req_coverage REAL,                      -- 0..1, FULL gate 0.90 BLOCK
  mutation     REAL,                      -- PIPELINE 0.70 / FULL 0.80 BLOCK
  evidence_ref TEXT NOT NULL,             -- path to verdict JSON (inputs/outputs/traces/policy)
  decided_at   TEXT NOT NULL
);
CREATE TABLE flakes (
  flake_id     TEXT PRIMARY KEY,
  task_id      TEXT REFERENCES tasks(task_id),
  test_name    TEXT NOT NULL,
  snapshot     TEXT NOT NULL,              -- flake snapshot path
  runs_pass    INTEGER, runs_fail INTEGER,
  reported_at  TEXT NOT NULL
);
```

**Per-edge artifact list (paths+logs+reports; 100% present required, CI-checked [routing-integration.md base]):**

| Edge | Artifacts (ledger/S3 paths) |
|---|---|
| SPEC | `specs/<task_id>.md` (REQ-IDs), `ledger: tasks` row |
| REQUEST_TESTS | `specs/<task_id>.testplan.md` |
| RED | `tests/<task_id>_red.py`, `logs/<run_id>_red.log` (must fail) |
| ENGINEER_DONE | `src/**` diff, `logs/<run_id>_green.log` (must pass) |
| suite | `reports/<run_id>_junit.xml`, `reports/<run_id>_coverage.json`, `reports/<run_id>_mutation.json`, `reports/<run_id>_lint.json`, `reports/<run_id>_flake.json` |
| critic | `reviews/<run_id>_critic.md` (pass/fail + rationale, independent of impl rationale [IJECS, 2026]) |
| verdict | `verdicts/<task_id>.json` (PROMOTE/HOLD/ROLLBACK + evidence refs), `ledger: verdicts` row |

Shared-memory hygiene: single authoritative store with per-role namespaces + TTLs so stale facts expire rather than linger [Galileo, 2025]; attach role+task_id to every write for audit traceability [Galileo, 2025]. Token/time budgets (step counts, elapsed ceilings, idle guards) act as circuit breakers against 53–86% duplication loops (MetaGPT 72%, CAMEL 86%, AgentVerse 53%) [Galileo, 2025].

**Retention:** hot artifacts (paths+logs+JUnit/coverage/lint) 30 days in ledger/S3; cold reports (mutation, flake snapshots, critic reviews, verdict JSON + full event store) 90 days; audit log rows (`AuditLog{timestamp, application_id, action, agent_id, input_data, output_data, processing_time, error_details}` [Mitra, 2024]) 90 days minimum. Event time-series keys (`event:<correlation_id>:<timestamp>`) 24h hot, then archive [Mitra, 2024].

### 4. Misroute correction (detection → correction → precedent, target misroute <5%)

Base metrics: activation recall 100% PIPE/FULL, precision >80% gated, handoff completeness 100%, gate <10 min block, misroute <5% [routing-integration.md base].

**Detection (ledger-measured, continuous consistency checks [Galileo, 2025]):**
- Activation recall <100% PIPE/FULL → rule gap; fix classifier rules immediately (warning threshold in base table).
- Activation precision <50% (tester runs with no value on verdict audit) → rules too loose; loosen→tighten inversion: restrict needs_tester triggers.
- Handoff completeness <100% (required artifacts missing per CI check) → HOLD; root-cause via distributed tracing causal chains + temporal relationships + context flow + state transitions [Maxim, 2026]; production teams with full tracing report 70% lower MTTR [Maxim, 2026].
- Gate duration >10 min SPEC-to-verdict → move large suites async/nightly [SQRBOK, 2025]; measure coordination overhead (handoff 100–500ms each [Maxim, 2026]) and token multiplier (3× single→5-agent cost documented [Maxim, 2026]).
- Misroute rate >5% (wrong formation on review) → retune.

State-consistency validation runs continuously: cross-agent state compare, causal-consistency verify (formatting observes content edits), temporal freshness thresholds [Maxim, 2026]. Pattern detection flags retry storms, thundering herds, circular dependencies (Agent A→B→C→A deadlock where codegen waits test waits docs waits codegen [Maxim, 2026]) before deadlock.

**Correction loop:**
1. Retune rules: adjust decision-table row thresholds (e.g., promote moderate+mixed→PIPELINE if recall miss; demote unverifiable→SOLO if precision miss). Small augmentation (<2% data) fixes out-of-distribution routing — MMLU golden-label augment lifted causal-LLM router from near-random to 95% quality at 54% strong-calls [LMSYS RouteLLM, 2024]. Analog: replay 5 misrouted tasks as golden labels.
2. Replay 5 tasks: re-run the 5 most recent misroutes through corrected classifier in simulation/adversarial harness (network-partition, timing-perturbation, resource-starvation injection [Maxim, 2026]) before prod.
3. Log precedent: append row to `precedents.md` (task_id, old→new formation, reason, replay result) + checkpoint workflow snapshot (messages+tool calls+memory, Git-commit style with hash) enabling rollback to known-good [Galileo, 2025]; checkpoint before high-impact actions and after dependency boundaries [Galileo, 2025]. Record decisions with reasons at decision time, keep contract outside session, name single open question per handoff [PaellaDoc, 2026]; handoff rules govern who can take over next while mesh preserves context, tool calls filtered from forwarded history [Microsoft Agent Framework, 2026].
4. Re-measure: targets recall 100%, precision >80%, completeness 100%, gate <10 min, misroute <5%; rollback procedure + runbooks + cost monitoring required for prod readiness [Maxim, 2026].

**References for deep dive:**
1. [Council Context, 2026] — Crew v2 formations (DUO executor+verifier, PIPELINE sequential specialists, FULL all-agents) and classification axes; base for §1 table + §4 targets.
2. [routing-integration.md base, via gh api] — 46-line base: tester roles per formation, activation/skip rules, message flows, per-edge artifacts, metrics table with misroute <5% target.
3. [LMSYS RouteLLM, 2024] — https://www.lmsys.org/blog/2024-07-01-routellm/ — router infers query characteristics; 4 router types (SW ranking, matrix factorization, BERT, causal-LLM); 85%/45%/35% cost cuts at 95% GPT-4 quality; 14% GPT-4 calls on MT-Bench augmented; MMLU augment (<2% data) fixes OOD; generalizes Claude-3-Opus/Llama-3-8B untrained.
4. [Meiklejohn, 2026] — https://christophermeiklejohn.com/ai/agents/distributed/zabriskie/2026/03/30/multi-agent-systems-have-a-distributed-systems-problem.html — ChatDev/MetaGPT/AutoGen lack causal ordering + concurrency control; lost-update migration collision; Lamport/vector-clock/CRDT remedies.
5. [Yang et al., ArXiv 2026] — https://arxiv.org/abs/2608.18092 — MAS failures are concurrency anomalies (stale reads, lost updates); need conflict detection + isolation + structured access.
6. [Mitra, 2024] — https://subhadipmitra.com/blog/2024/retail-bank-multi-agent-system/ — Event{version, validators, audit store}, `asyncio.wait_for` timeout pattern, OrderedMessageHandler sequence+queue, DeadLetterQueue max_retries=3 delays [60,300,900], AuditLog schema, retry-per-error-type, 24h event retention.
7. [Maxim, 2026] — https://www.getmaxim.ai/articles/multi-agent-system-reliability-failure-patterns-root-causes-and-production-validation-strategies/ — ordering violations (trading example), timeout-retry double-charge, handoff 100–500ms, N(N-1)/2 races, tracing cuts MTTR 70%, adversarial testing, 3× token multiplier, prod readiness checklist.
8. [Taskade, 2026] — https://www.taskade.com/wiki/ai-agents/agent-handoff — handoff crosses unreopenable boundary; receiver opens cold; artifact fields GOAL/DONE/FINDINGS/DECISIONS/OPEN/NEXT/WHERE; decisions+open-questions do heavy lifting; pointers > pasting.
9. [PaellaDoc, 2026] — https://paelladoc.com/blog/agent-handoffs/ — transcript ≠ handoff; bundle = contract + state + decisions+reasons + dead ends + single open question; record decisions at decision time.
10. [Microsoft Agent Framework, 2026] — https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/handoff — HandoffBuilder add_handoff/with_start_agent, mesh context sync, handoff-tool filtering, autonomous turn limits, approval + checkpointing.
11. [AiHero /handoff, 2026] — https://www.aihero.dev/skills-handoff — handoff is transit document, dead once work lands.
12. [LEDGER, ArXiv 2026] — https://arxiv.org/html/2608.18398v1 — Trace Records → Evidence Nodes → Workflow Nodes + artifact anchors; edges uses/produces/checked_by/supports; claim→evidence backward traversal; sidecar tracer.
13. [Galileo, 2025] — https://galileo.ai/blog/multi-agent-coordination-strategies — shared memory ACL+TTL, token duplication 53–86%, BFT N≥3f+1, checkpoint-as-git-commit rollback, 1600+ MAST traces.
14. [SQRBOK, 2025] — pyramid discipline + small-immediate/medium-queued/large-parallel scheduling; gate <10min (via base).
15. [IJECS, 2026] / [QABattle, 2025] / [KnowMBA, 2025] / [ArXiv, 2026] — independent verification separation; evidence-bound verdicts; E2E caps pushed down; async large suites (via base).
