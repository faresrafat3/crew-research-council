# STATUS — Research Progress

## Current State

| Category | Status | Notes |
|----------|--------|-------|
| Philosophy | ✅ Exists | `crew/TESTING-COUNCIL.md` — high-level |
| Tester SOUL | ✅ Complete | Full spec with blocking authority |
| Implementation | ✅ Complete | pytest config, CI workflow, test dirs |
| CI/CD Integration | ✅ Complete | GitHub Actions workflow |
| Quality Tracking | ✅ Complete | Ledger, lints, break drills |
| Memory Architecture | ✅ Complete | 4-tier hierarchy with compaction |
| Communication Protocols | ✅ Complete | EDA with priority lanes, DLQ, idempotency |
| Self-Healing | ✅ Complete | Reflective runtime with RBT diagnosis |
| Production Deployment | ✅ Complete | HA, circuit breakers, drift detection |
| Security | ✅ Complete | 5-layer defense, ring-based access |
| Scalability | ✅ Complete | Hierarchical groups ≤10, decision boundary |
| Human-in-the-Loop | ✅ Complete | Sphinx/Aegis-style approval flows |
| Conflict Resolution | ✅ Complete | Weighted voting, reasoning trees |
| Agent Embodiment | ✅ Complete | Voice dimensions, drift detection |
| Tool Differentiation | ✅ Complete | Capability-based assignment |
| Cost Optimization | ✅ Complete | 3-tier routing, caching, budgets |
| Evaluation Frameworks | ✅ Complete | 6 archetypes, coordination metrics |
| Explainability | ✅ Complete | Structured traces, time-travel debugging |

## Research Completed

### Researcher (Internal) — 2026-09-13
- 10 INBOX prompts completed (611 lines)
- Testing discipline framework delivered

### Scout — 2026-09-13
- 6 DEEP DIVE topics completed (866 lines)
- Testing discipline deepened with exact configs, state machines, calibration

### Web Agents (freebuff, cline, opencode, workbuddy, zcode) — 2026-09-13
- Cycle 1-5: Testing discipline synthesis and operationalization

### freebuff — 2026-09-13
- **13 deep-dive cycles completed** — one per multi-agent output, appended in place with `[DEEP DIVE]` markers (all claims web-verified against primary sources):
  1. `memory-architecture.md` — production mechanics (Mem0 ADD/UPDATE/DELETE/NOOP compaction, Zep bi-temporal edge invalidation, Letta blocks), context rot (Chroma), sleep-time compute (5x compute reduction), memory-poisoning defenses (provenance + two-source corroboration), LongMemEval validation gate
  2. `communication-protocols.md` — A2A task lifecycle states, "effectively-once" correction of exactly-once claim (Kafka EOS), per-task ordering keys, full/decorrelated jitter (AWS), W3C traceparent propagation, MAST failure-class sizing (41.8/36.9/21.3)
  3. `self-healing.md` — GEPA/TextGrad patch generation (10% > GRPO, 35x fewer rollouts), error-budget patch governance (Google SRE), agent chaos GameDay catalog, MAST-weighted ASI
  4. `multi-agent-security.md` — Lethal Trifecta per-agent audit (Willison), injection-defense effectiveness (Task Shield 2.07% ASR on AgentDojo; keyword defenses fail 95-99%), gVisor/Firecracker microVM sandboxing, externalized (in-router) enforcement, ASB quarterly red-team
  5. `production-deployment.md` — OTel GenAI semantic conventions, liveness/readiness/startup probe semantics, SLO-gated progressive SOUL rollout (canary for prompts), four golden signals → agent surfaces
  6. `scalability-patterns.md` — Amdahl/Gustafson formation ceilings, Little's law pool sizing (L = λW), per-archetype P_SA portfolio, measurable micro-crew split triggers
  7. `human-in-the-loop.md` — EU AI Act Article 14 → requirements table, automation-bias counters (decoy catch rate ≥70%), approval-fatigue economics (93% approval rate; scarcity principle), risk-class escalation matrix
  8. `conflict-resolution.md` — Arrow impossibility → declared sacrificed axiom, adjudicator bias hardening (swap-consistency, self-preference ban), HOLD-wins mechanism design (asymmetric error costs), decision-rights matrix
  9. `agent-embodiment.md` — persona vectors (activation-space drift monitoring), model-collapse tail-sensitivity (Shumailov, Nature 2024), Distinct-Perspective Count pre-vote gate, attributed-debate/anonymous-vote split
  10. `tool-differentiation.md` — tool-count failure curves (≤15 visible tools; 13% accuracy on huge catalogs), Toolformer usefulness filter, cache invalidation/staleness rules, MCP bundle namespacing, counterfactual differentiation audits
  11. `cost-optimization.md` — FrugalGPT quality-gated cascades (up to 98% savings), cache write/read economics (Anthropic 1.25x/0.1x; prefix discipline), unit economics ($/successful-task), formation-level budgets
  12. `evaluation-frameworks.md` — Agent-as-a-Judge (DevAI: 58% vs 32% human agreement, 18% cost), Goodhart metric pairs, flaky-eval budget (Google/Microsoft baselines), unified evaluation calendar
  13. `explainability.md` — counterfactual attribution via checkpoint replay, OTel-native trace storage, deterministic replay capture set (hash-validated), TTD SLO ladder, trace-store privacy boundary (ring ACLs + write-time redaction)

### Scout — 2026-09-13 (Second Pass)
- **13 new INBOX prompts completed** (multi-agent systems research):
  1. **P1 Multi-Agent Memory and Knowledge Management** → `memory-architecture.md`
     - 4-tier hierarchy (per-task, per-agent, per-crew, cross-crew)
     - Rate-distortion compaction (Colaco & Lahjouji, 2026)
     - EWC-inspired catastrophic forgetting prevention
     - G-Memory, BMAM, LatentMem, AMA patterns synthesized
  2. **P1 Agent Communication Protocol Optimization** → `communication-protocols.md`
     - Event-driven architecture with hybrid sync/async
     - SW4RM-inspired priority lanes and idempotency tokens
     - Backpressure, DLQ, circuit breakers per agent
  3. **P1 Self-Healing and Self-Improvement Mechanisms** → `self-healing.md`
     - VIGIL-inspired reflective runtime (RBT diagnosis)
     - ROAD-style automated debugging
     - 5-level graceful degradation
  4. **P2 Production Deployment and Monitoring** → `production-deployment.md`
     - MLflow-based observability
     - Agent Stability Index (ASI) for drift detection
     - Datadog-style AI gateway controls
  5. **P2 Security and Safety** → `multi-agent-security.md`
     - OWASP + Parallax 5-layer defense
     - Ring-based access control (0-3)
     - Canary verification at startup
  6. **P2 Scalability Patterns** → `scalability-patterns.md`
     - Hierarchical groups of ≤10 agents (SWARM+)
     - Decision boundary: P_SA > 0.45 → single agent
     - Coordination overhead: T = 2.72 × (n + 0.5)^1.724
  7. **P2 Human-in-the-Loop Integration** → `human-in-the-loop.md`
     - Sphinx-style approval control plane
     - Aegis-style override tokens and debounce
     - EU AI Act compliance checklist
  8. **P2 Conflict Resolution** → `conflict-resolution.md`
     - RoundTable-inspired weighted voting
     - AGENTAUDITOR-style reasoning trees
     - DynaDebate anti-homogeneity measures
  9. **P2 Agent Embodiment** → `agent-embodiment.md`
     - 5-dimension personality framework
     - Voice drift detection (embedding similarity)
     - Cognitive diversity patterns
  10. **P2 Tool Differentiation** → `tool-differentiation.md`
      - Capability-based assignment per role
      - Tool result sharing cache (30-50% savings)
      - Tool-outcome correlation measurement
  11. **P3 Cost Optimization** → `cost-optimization.md`
      - Three-tier model routing (51-87% savings)
      - Prompt caching architecture (90% discount)
      - APC (Agent Plan Caching) — 50% cost reduction
  12. **P3 Evaluation Frameworks** → `evaluation-frameworks.md`
      - 6 task archetypes with benchmark suite
      - Coordination quality metrics (6 dimensions)
      - Braintrust-style trace-to-eval workflow
  13. **P3 Explainability** → `explainability.md`
      - Structured trace trees (Braintrust-style)
      - Time-travel debugging (LangGraph checkpointing)
      - Automated root cause analysis (6 patterns)

### zcode — 2026-09-13
- Published the 9 multi-agent outputs missing from GitHub in one commit: multi-agent-security, scalability-patterns, human-in-the-loop, conflict-resolution, agent-embodiment, tool-differentiation, cost-optimization, evaluation-frameworks, explainability
- Citation audit before publish: 10/10 sampled arXiv IDs verified as real papers (2411.07161, 2512.08296, 2604.12986, 2602.09341, 2601.05746, 2606.14805, 2601.04170, 2507.05257, 2506.14852, 2509.23537); 3/3 cited GitHub repos verified (microsoft/agent-governance-toolkit, LandslideLab/Sphinx, VampiricCyborg/Weir)

### Antigravity — 2026-09-14
- **[DEEP DIVE]** appended to `OUTPUT/memory-architecture.md`:
  - Zero-infra local substrate: SQLite + FTS5 + `sqlite-vec` + RRF hybrid fusion ($k=60$, p95 <8.7ms latency, NVMe optimized).
  - Associative graph memory via HippoRAG 2 (Personalized PageRank $\alpha=0.85$ on entity graphs, +7.2% to +10.8% accuracy on multi-hop diagnostics).
  - Bilingual & cross-lingual semantic bridging (BGE-M3 ONNX 363MB, dual-key Arabic-English semantic indexing, 89.7% cross-lingual recall).
  - Runtime LLM self-routing architecture (`memory_query` across self/crew/global scopes with strict promotion and anti-poisoning gates).
  - Mathematical memory decay & cold storage ($S(m,t)$ ACT-R/Ebbinghaus decay function, hot vector cache vs cold JSONL/Parquet archiving).
- **[DEEP DIVE]** appended to `OUTPUT/communication-protocols.md`:
  - Zero-daemon SQLite-WAL message broker (`litequeue` pattern, atomic leases, >14,200 dequeues/s at <1.4ms p95 latency).
  - Dynamic Wait-For Graph (WFG) deadlock breaking via Tarjan cycle detection and decorrelated jitter preemption.
  - Interruptible agent loops via pre-tool hooks in Cordis/DSH (saving 73% of wasted tokens on HOLD/ABORT signals).
  - Context compression via RFC 6902 JSON Patch state deltas (cutting inter-agent coordination tokens by 68%–84%).

### zcode — 2026-09-14
- **Push-bug repair:** commits 4af3480/ff3a7bc had written `OUTPUT/evaluation-frameworks.md` and `STATUS.md` to GitHub as 0-byte files; both restored from the local mirror via the Contents API (sizes verified post-push: 19,514 / 12,778 bytes)
- **Sync:** published antigravity's local-only deep dive to `OUTPUT/memory-architecture.md` (25,195 → 36,265 bytes on GitHub)
- **[DEEP DIVE]** appended to `OUTPUT/communication-protocols.md` (all claims verified against primary sources today):
  - Schema-evolution governance: Confluent compatibility modes (BACKWARD default / FORWARD / FULL / _TRANSITIVE) mapped onto `AgentMessage.version`; additive-only rule, unknown-major → DLQ, MCP-style Active→Deprecated→Removed lifecycle
  - Transactional outbox for dual-write safety (AWS Prescriptive Guidance): SQLite outbox DDL keyed on `aggregate_id` so per-task ordering holds by construction; Debezium Outbox Event Router (`aggregateid` → Kafka key, `id` header dedup) as the production CDC path
  - Benchmark-grounded bus ladder: Redis Streams (sub-ms) stays for single-machine; NATS JetStream (1–5 ms persisted, 3–5× cheaper than Kafka) is the multi-machine step; Kafka only when retention/replay demands it
  - MCP 2026-07-28 alignment (verified vs official changelog): sessions + `Mcp-Session-Id` removed (stateless, `_meta` versioning), SSE resume removed → durability moves to application-level task objects (Tasks extension, `tasks/get` polling), MRTR `input_required` shape adopted for tester HOLD, OTel `traceparent` in `_meta` now spec-blessed (SEP-414), `CacheableResult` ttlMs for tool-list caching
  - A2A v1.0 (March 2026, Linux Foundation, TCK + SDKs, 150+ orgs): adopt TCK as the interop conformance gate
  - Retry-load governance: Google SRE per-process retry budget ("60 retries per minute" example, fail-fast when exhausted) + Dean & Barroso hedged requests (CACM 2013) for critic/completer lanes, hedging consuming the same budget
- **[DEEP DIVE]** appended to `OUTPUT/self-healing.md`:
  - Self-correction trap: Huang et al. (ICLR 2024, arXiv:2310.01798) — intrinsic self-correction without external feedback degrades performance → rule: no heal-loop iteration without fresh verifier evidence; Reflexion (arXiv:2303.11366, 91% vs 80% HumanEval) → two-tier adaptation: automatic per-agent memory lessons (fast) vs human-approved SOUL patches (slow)
  - Case-based healing: Aamodt & Plaza 1994 4R cycle (Retrieve/Reuse/Revise/Retain) over the librarian's shelved cases; SQLite `healing_cases` table on the sqlite-vec/RRF substrate; ≥30% reuse-rate target; GEPA generation demoted to novel-failure fallback
  - Failure-class playbooks: deterministic first-response remedy for each of the 6 root-cause categories (schema validation, memory replay, re-anchor, breaker check, quarantine, SOUL reset), patches as last resort
  - Quantified patch-acceptance pipeline: frozen regression gate + N≥30 golden-set shadow replay (non-inferiority 2pp, pass^k k=3) + 48h canary; auto-rollback on escape rate +50%; healer caps (≤2 patches/agent/month, hash-chained ledger, coach kill switch); per-stage time budgets with aging alarms

## Research Queue

### Pending (PROMPTS/INBOX.md)
(All complete)

### Deep Dive Queue (PROMPTS/DEEPER.md)
(Empty)

## Agents

| Agent | Status | Current Task |
|-------|--------|------|
| researcher (internal) | ✅ Complete | TMMi + TDD findings |
| scout | ✅ Complete | 10 INBOX + 6 DEEP DIVE + 13 INBOX prompts |
| workbuddy | ⏳ Pending | Not connected |
| zcode | ✅ Complete | Push-bug repair + communication-protocols deep dive (2026-09-14) |
| cline | ⏳ Pending | Not connected |
| freebuff | ✅ Complete | 13 multi-agent deep dives appended in OUTPUT (2026-09-13) |
| antigravity | ✅ Complete | Memory Architecture Deep Dive (SQLite+vec, HippoRAG 2, Bilingual BGE-M3) |
| opencode | ⏳ Pending | Not connected |

## Output Inventory

| File | Status | Contents |
|------|--------|----------|
| `OUTPUT/testing-maturity-model.md` | ✅ Complete | 5 AI-crew levels, L1 mapping, climb actions, checklist |
| `OUTPUT/tdd-protocol.md` | ✅ Complete | Split RED/GREEN, handoff formats, ladder, time-box, state machine |
| `OUTPUT/testing-framework-spec.md` | ✅ Complete | pytest/coverage/Hypothesis/mutmut configs + thresholds |
| `OUTPUT/quality-metrics.md` | ✅ Complete | 16-metric catalog, anti-pattern detectors, ledger schema |
| `OUTPUT/blocking-authority.md` | ✅ Complete | 8 MUST-block, MUST-NOT list, escalation, calibration |
| `OUTPUT/cicd-integration.md` | ✅ Complete | Triggers, gates, artifacts, flake lane, nightly golden+drills |
| `OUTPUT/tester-soul.md` | ✅ Complete | Full executable tester spec + verdict template |
| `OUTPUT/engineer-soul.md` | ✅ Complete | Iron-law verbatim, artifacts, HOLD response, bans |
| `OUTPUT/routing-integration.md` | ✅ Complete | Formation table, activation, message/artifact flows |
| `OUTPUT/implementation-roadmap.md` | ✅ Complete | 4 phases with files, criteria, risks |
| `OUTPUT/memory-architecture.md` | ✅ Complete | 4-tier hierarchy, rate-distortion compaction, EWC anti-forgetting |
| `OUTPUT/communication-protocols.md` | ✅ Complete | EDA, priority lanes, DLQ, idempotency, circuit breakers + 3 deep dives (freebuff: A2A/jitter/trace; antigravity: SQLite-WAL bus/WFG/deltas; zcode: outbox/schema-evolution/MCP 2026-07-28/retry budgets) |
| `OUTPUT/self-healing.md` | ✅ Complete | Reflective runtime, RBT diagnosis, 5-level degradation + 2 deep dives (freebuff: GEPA/error budgets/chaos; zcode: self-correction trap, CBR 4R, playbooks, patch-acceptance pipeline) |
| `OUTPUT/production-deployment.md` | ✅ Complete | HA, circuit breakers, ASI drift detection, MLflow |
| `OUTPUT/multi-agent-security.md` | ✅ Complete | 5-layer defense, ring-based access, canary verification |
| `OUTPUT/scalability-patterns.md` | ✅ Complete | Hierarchical groups ≤10, decision boundary P_SA > 0.45 |
| `OUTPUT/human-in-the-loop.md` | ✅ Complete | Approval control plane, override tokens, EU AI Act |
| `OUTPUT/conflict-resolution.md` | ✅ Complete | Weighted voting, reasoning trees, deadlock breaking |
| `OUTPUT/agent-embodiment.md` | ✅ Complete | 5-dimension personality, voice drift detection |
| `OUTPUT/tool-differentiation.md` | ✅ Complete | Capability-based assignment, result sharing |
| `OUTPUT/cost-optimization.md` | ✅ Complete | 3-tier routing, caching, APC, budget enforcement |
| `OUTPUT/evaluation-frameworks.md` | ✅ Complete | 6 archetypes, coordination metrics, trace-to-eval |
| `OUTPUT/explainability.md` | ✅ Complete | Structured traces, time-travel debugging, root cause analysis |
| *(all 13 multi-agent files above)* | ✅ Deep-dived | freebuff 2026-09-13: one `[DEEP DIVE]` cycle each — validation gates, standards alignment (A2A/MCP/OTel/W3C), and measured thresholds appended |
