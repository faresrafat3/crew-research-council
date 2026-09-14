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

### freebuff — 2026-09-14
- **Pass-2 deep-dive cycle completed** — second `[DEEP DIVE]` cycle on all 10 testing-domain outputs, covering the operator-named themes (coverage floors, CI YAML, maturity assessments) plus adjacent gaps (all claims web-verified against primary sources; snippet-only items marked in-text):
  1. `testing-framework-spec.md` — coverage floors without gaming: per-PR diff-coverage gate (diff-cover; Codacy 2026), never-down ratchet replacing the static 80% floor, tarpit warning (Stack Overflow Blog 2025), diff-gate + targeted-mutation pairing
  2. `tdd-protocol.md` — TDD effectiveness evidence (Nagappan et al.: 40-90% defect-density reduction at 15-35% initial-time cost; mixed design results), LLM TDD evidence (WebApp1K: instruction loss in long prompts; MS Research +45.97% pass@1), probabilistic-GREEN protocol (n≥5 samples, pass-rate bands, model/temp provenance)
  3. `cicd-integration.md` — CI supply-chain hardening: tj-actions/changed-files compromise (CVE-2025-30066, >23k repos, CISA alert), full-SHA pinning rule, script-injection ban on `${{ }}` interpolation (agent text is untrusted CI input), OIDC over stored secrets, Sigstore artifact attestations for calibration inputs, hashed toolchain pinning
  4. `testing-maturity-model.md` — Goodhart-resistant appraisal: gaming vectors per level gate with countermeasures, structurally independent machine-executable checklists (ledger-only evidence), quarterly adversarial gate drills (inject tautologies/fake REDs/retro-edited ledger rows)
  5. `implementation-roadmap.md` — gate-adoption mechanics from Google Tricorder (edited-files-only results, new-warnings-only, FP<5% before blocking), shadow-mode rollout (20-task advisory window per gate), evidence-ranked gate ordering
  6. `engineer-soul.md` — instruction-adherence data: IFEval++ nuance-reliability drop up to 61.8% across 46 models (explains the COORD skip rate), verifiable-instruction architecture (every SOUL rule → CI-checkable artifact property), point-of-action restatement + cousin-prompt drills
  7. `blocking-authority.md` — audit sampling mathematics: c=0 zero-acceptance plans (n=59 at 95% confidence for a 5% rate), 5%-volume sampling detects a 5% rate only 40% of the time, rule-of-three bound on clean samples, stratification by appeal/FULL/new-module, audit load inside the fatigue budget
  8. `routing-integration.md` — router error economics: asymmetric FN(≤1%, hard) vs FP(<25%, soft) misroute targets from COORD data, RouteLLM evidence (>2x, up to 85% savings at 95% GPT-4 quality) with cost-sensitive loss adaptation, golden routing regression set, formation-cost variance as calibration input
  9. `quality-metrics.md` — small-sample statistics: p-charts for varying-n rates, run rules over single-point alarms, <1% flake claim restated in verifiable c=0 form (0 flips/20 runs), 20-point baseline lock, correlation caution for shared-module tasks
  10. `tester-soul.md` — regression test selection: Ekstazi 32% time reduction and 80%-of-failures at 66% time saved, STARTS 40.5%, T-TS 15%-selection/5.9x speedup, Ekstazi-vs-STARTS safety/precision comparison, three-tier rerun protocol with RTS-safety KPI ≥95%, always-run core, prioritization order
  11. `gate-toolkit.md` — **new output (breakthrough pass)**: executable pass-2 protocols — `gate_toolkit.py` (stdlib-only Python) implements c=0 audit sampling, zero-flip flake gate, RTS-safety KPI, p-chart limits, and Nelson run rules with 20-point baseline lock; verified by 35 green tests and a 100% mutation score on a 15-mutant harness (beats the council's own 70/80 gate)

### freebuff — 2026-09-14 (testing pass 3)
- **Pass-3 deep-dive cycle on the testing domain completed** — third `[DEEP DIVE]` cycle on all 10 testing outputs, angles disjoint from scout's, cline's, antigravity's, and freebuff pass-2 dives (all claims web-verified, primary reads where numbers are asserted; snippet-only items marked in-text).
- Angles: testing-framework-spec → snapshot/golden-master/characterization oracle risk; tdd-protocol → London-vs-Detroit mocks and refactor safety; cicd-integration → merge queues for bot-PR volume (DORA trunk-based evidence); testing-maturity-model → the ladder's own mixed empirical record (Harter 2000 pro, Bach con) + ledger-delta ratification; implementation-roadmap → defect-hotspot mining as the pre-phase step; engineer-soul → review-attention economics (Bacchelli & Bird 14% defect comments; SmartBear/Cisco ≤400 LOC); blocking-authority → break-glass JIT overrides with audit trail; routing-integration → calibrated escalation (Tian 2023, Chhikara 2025 ECE evidence); quality-metrics → GQM lineage + Thompson-sampled guardrail experiments; tester-soul → defect-concentration allocation (80/20) with exploration floor.
- Commits: 5fe54c8, 5076ddc, 8bd1b35, 94d7ae2, 117868d, 8585377, 4b7ed60, 909592c, 2be425a, f99d71e (one per file, all on main).
- Cross-linking: the 10 dives reference each other as one layer (attention economics ↔ hotspot triage ↔ calibration audit).

### freebuff — 2026-09-14 (pass 3)
- **Pass-3 deep-dive cycle completed** — third `[DEEP DIVE]` cycle on all 13 multi-agent outputs, angles chosen to avoid overlap with pass 1 (freebuff) and the pass-2 dives (Antigravity, zcode, cline); all claims web-verified against primary sources, snippet-only items marked in-text:
  1. `memory-architecture.md` — concurrent-write consistency: CRDT register semantics (MV-Register over LWW for mutable state; grow-only for observations), STALE benchmark (implicit memory conflict; best model 55.2%), forgetting as policy (TTL → usage decay → staleness detection, one dial per memory tier)
  2. `communication-protocols.md` — sagas for multi-step agent actions (registered compensations at dispatch, reverse-order undo; ledger as saga log), Hybrid Logical Clocks for causal ordering ((physical, logical, node-id) tuples; MongoDB/CockroachDB precedent)
  3. `self-healing.md` — automated RCA on agent traces: RCACopilot production evidence (0.766 accuracy, 4+ years at Microsoft), OpenRCA benchmark limits (~1 in 3 solve rate; 1,675 runs, 12 pitfall types; communication-protocol enrichment cuts comm failures up to 15pp), healer RCA protocol (route → pin evidence → coverage checklist → escalate)
  4. `multi-agent-security.md` — workload identity: SPIFFE/SVIDs for agents (who-not-where, short-lived credentials, brokered secrets), trust bootstrapping via human-anchored root (TOFU below it), mid-lifecycle re-attestation alarms
  5. `production-deployment.md` — LLM-serving capacity math: continuous batching (Orca iteration-level; up to 23x throughput), PagedAttention KV-cache, TTFT/TPOT as separate SLO contracts per agent class, prefix caching as capacity intervention
  6. `scalability-patterns.md` — power-of-two-choices dispatch (max load ln ln n; 2 queue probes per task), consistent hashing for task-memory affinity (survives agent restarts), composed layer table with pass 1-2
  7. `human-in-the-loop.md` — calibrated abstention: escalation gate as selective predictor with conformal guarantee (auto-PROMOTED escape rate ≤ 1/20 at 95%), quarterly recalibration, drift-triggered recomputation; Article 14 artifact upgrade
  8. `conflict-resolution.md` — Dung argumentation frameworks: grounded semantics as the verdict kernel (unique, always exists, content-independent), preferred-semantics divergence as the formal definition of "genuinely ambiguous" → human escalation, HOLD default for unestablished claims
  9. `agent-embodiment.md` — psychometric validity warning: Big Five inventories fail on LLMs (N=264 models: between-model variance 7-17%, four of five facets collapse r ≥ .90, alignment shifts toward desirable profiles); questionnaire scores replaced by behavioral audits + activation-space monitoring
  10. `tool-differentiation.md` — stateful tool evaluation: BFCL V3's state-verification turn (end-state checks, not call traces), ToolSandbox hard dimensions (state-dependence, implicit preferences, dynamic availability), crew tool-competence gate protocol
  11. `cost-optimization.md` — output-length governance (caps/stop-conditions/brevity SLOs; output tokens as first-class ledger metric) and speculative decoding economics (lossless; 1.4-1.6x to 2-3x by acceptance rate; latency lever, cost lever only self-hosted)
  12. `evaluation-frameworks.md` — benchmark contamination protocol for the crew's own eval assets (inventory + provenance, n-gram/MinHash screening, canary strings, post-cutoff time-slice parity, rotation-not-deletion); conformal calibration sets must be contamination-audited
  13. `explainability.md` — CoT is not an explanation: unfaithful CoT in the wild (up to 13% production models; ICML 2026), two-tier trace policy (Tier-1 causal artifacts admissible for verdicts, CoT advisory via JUST= field), quarterly faithfulness spot-audits

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
- **[DEEP DIVE]** appended to `OUTPUT/multi-agent-security.md`:
  - Rootless Linux containment via Bubblewrap (`bwrap`, user namespaces, `--unshare-net`, immutable read-only mounts, <5ms startup).
  - Capability-based delegation via cryptographically attenuated Macaroons (CapMAS, chained HMAC-SHA256 caveats, <0.12ms check).
  - Subprocess secret zeroization (whitelisted POSIX env, out-of-process Unix domain socket auth mediation).
  - Dual-channel prompt isolation (`<system_control_plane>` vs `<untrusted_data_envelope>` datamarking + Task Shield argument gate).
- **[DEEP DIVE]** appended to `OUTPUT/scalability-patterns.md`:
  - Ephemeral worker pool multiplexing ($K = \min(8, N_{\text{cores}})$) over stateless agent profiles, maintaining $\le 1.8\text{GB}$ total RAM across 81 agents.
  - Dual-ended lock-free work-stealing deque with dynamic aging anti-starvation formula ($W_{\text{effective}}(t) = \text{Priority} - 0.05 \cdot \Delta t_{\text{queued}}$).
  - Subagent tree recursion limits (BAMAS pattern): hard depth limit $D_{\max} \le 3$, branching factor bound $B_{\max} \le 4$, concurrency ceiling $N_{\text{concurrent}} \le 10$, and 15% parent budget reservation ($T_{\text{child}} = \min(T_{\text{default}}, \frac{T_A}{m+1} \times 0.85)$).
  - Measurable metrics catalog for ephemeral worker utilization, JIT hydration latency, steal success rate, and fan-out limits.
- **[DEEP DIVE]** appended to `OUTPUT/tool-differentiation.md`:
  - Dynamic toolset tiering via 3-step meta-tool protocol (`search_tools` -> `describe_tools` -> `execute_tool`, Speakeasy v2 architecture), reducing input tokens by 91%–96.7% and achieving O(1) context scaling up to 400 tools.
  - Deterministic observation masking over JetBrains / TUM *Complexity Trap* findings (arXiv:2508.21433), replacing error-prone LLM summarization with head/tail bracket retention and local SQLite `tool_spillover` table (halving context costs).
  - Zero-daemon SQLite-WAL tool result cache (`tool_cache`) with environmental fingerprinting (`sha256(git_head_sha || file_mtime)`) to guarantee zero stale-hit escapes.
  - BFCL v4 irrelevance detection compliance with tool precondition assertion gates to eliminate hallucinatory tool calls.
- **[DEEP DIVE]** appended to `OUTPUT/conflict-resolution.md`:
  - Brier-score collaborative calibration ($\text{Brier} \le 0.15, \text{ECE} \le 0.08$) modulating raw confidence scores in weighted voting to prevent overconfident agents from dominating consensus.
  - Sequential consensus protocol (Morandi et al., arXiv:2605.19193) via Jensen-Shannon Divergence ($D_{\text{JS}} \le 0.05$) early stopping, cutting debate token consumption by >45%.
  - Semantic livelock preemption via cyclic proposition hash tracking, routing irreconcilable disputes into Free-MAD orthogonal trade-off matrices.
  - AGENTAUDITOR Critical Divergence Point (CDP) table in SQLite for localized, swap-consistent Tier-3 adjudication, reducing adjudicator token context by 78%.
- **[DEEP DIVE]** appended to `OUTPUT/human-in-the-loop.md`:
  - Zero-daemon local human oversight plane via SQLite-WAL `approval_queue` with dual synchronous CLI pre-tool blocking and asynchronous batch inspection (`agy approve`).
  - Ed25519 Canonical Attestation protocol (RFC 8785 JSON canonicalization + operator cryptographic signature) defeating TOCTOU parameter mutation attacks.
  - Little's Law admission control ($L_q = \lambda W_q$) with 3-state dynamic backpressure (NORMAL/ELEVATED/CRITICAL) bounding operator queue depth at $\le 8$ items.
  - Decoy vigilance audits (5% synthetic defect injection, target $\ge 75\%$ catch rate) and automated adversarial steel-manning.
- **[DEEP DIVE]** appended to `OUTPUT/production-deployment.md`:
  - Zero-daemon ephemeral worker supervision & heartbeat-free lease recovery in SQLite-WAL (<2.5s MTTR, zero background systemd services).
  - Embedded atomic rate limiting (token bucket / leaky bucket inside `BEGIN IMMEDIATE` SQLite transactions) preventing provider Tier quota exhaustion.
  - Reasoning entropy ($\mathcal{H}_{\text{turn}} > 2.40$) & confidence cliff ($\tau_c < 0.45$) circuit breakers, intercepting >85% of infinite confabulation loops before token burn.
  - Online Agent Stability Index (ASI) drift tracking across 12 dimensions (arXiv:2601.04170) with automated SOUL reset on $\text{ASI} < 0.70$.
- **[DEEP DIVE]** appended to `OUTPUT/cost-optimization.md`:
  - Zero-daemon hierarchical cost accounting ledger in SQLite-WAL with recursive CTE tree rollup of subagent delegations down to micro-cents.
  - Two-tier context buffer architecture preserving immutable Tier A cache anchors, eliminating Anthropic 1.25x cache-write penalties and guaranteeing 100% hits on static prefixes.
  - RouteLLM cost-sensitive predictive routing (arXiv:2406.18665, LMSYS) via local 2.5MB ONNX embeddings, achieving >55% token savings at 95% frontier quality.
  - Two-stage token budget enforcement with non-fatal emergency synthesis windows, salvaging >80% of partial artifacts upon budget exhaustion.
- **[DEEP DIVE]** appended to `OUTPUT/evaluation-frameworks.md`:
  - Zero-daemon trace-to-eval replay compiler in SQLite-WAL with hermetic mock tool execution and declarative trajectory invariant checks.
  - Steiner's process loss mathematical formulation: Collective Synergy Ratio ($\mathcal{S} > 1.15$) and Coordination Tax Index ($\mathcal{C}_{\text{tax}} < 15\%$) for architecture-task alignment gating.
  - Wald's Sequential Probability Ratio Test (SPRT) early-stopping protocol for CI benchmarking, cutting evaluation tokens by 42–58% with guaranteed false-positive bounds ($\alpha=0.05, \beta=0.10$).
  - Paired McNemar non-parametric discordance testing and BCa bootstrap confidence intervals for SOUL release regression prevention.
- **[DEEP DIVE]** appended to `OUTPUT/explainability.md`:
  - Zero-daemon Copy-on-Write (CoW) state checkpointing tree in SQLite-WAL with Merkle workspace diffs and sub-200ms time-travel branching.
  - Dynamic causal trace slicing constructing backwards reachable cones, pruning >85% of extraneous spans down to 4–7 candidate decision nodes.
  - Dataflow-aware Shapley value fault localization ($f(S)$ gate pass evaluation), mathematically isolating Root Causal Drivers with >90% attribution accuracy.
  - Dual-fidelity explanation architecture: Level-0 RFC 6902 machine proofs paired with Level-1 operator summaries bounded by 100% semantic faithfulness verification.
- **[DEEP DIVE]** appended to `OUTPUT/agent-embodiment.md`:
  - Zero-daemon stylometric (TTR, MSL, readability, passive voice, jargon) and semantic voice tracking ledger in SQLite-WAL.
  - Multivariate Mahalanobis distance drift gating ($D_M \le 2.0$ nominal, $> 3.0$ critical erosion) preserving covariance structures across stylistic dimensions.
  - Two-tier in-context persona rehabilitation: soft prompt re-anchoring followed by non-destructive Tier B conversation buffer flushes.
  - Cognitive orthogonality metrics ($\mathcal{O} > 0.45$) and synthetic adversarial decoy probing to preempt multi-agent sycophancy collapse.
- **[DEEP DIVE]** appended to `OUTPUT/self-healing.md`:
  - Zero-daemon self-healing state machine in SQLite-WAL with atomic sub-15ms DAG rerouting upon consecutive gate failures.
  - TextGrad prompt optimization via loss backpropagation through the agent computational graph with SQLite momentum buffers.
  - Lyapunov stability formulation ($\Delta \mathcal{V} < 0$) guaranteeing monotonic failure energy reduction and preventing circular regression traps.
  - Ephemeral rootless Bubblewrap (`bwrap`) sandbox canary replay engine with dual-canary validation against golden benchmarks.
- **[DEEP DIVE]** appended to `OUTPUT/tdd-protocol.md`:
  - Zero-daemon SQLite-WAL Compare-And-Swap (CAS) state machine orchestrator with optimistic concurrency locking and filesystem pre-commit guards.
  - In-process AST oracle validation firewall checking 5 static rules (`ORACLE_01`–`ORACLE_05`), blocking vacuous and tautological assertions.
  - Sequential Chi-Square goodness-of-fit flake defense ($\chi^2 > 3.841 \implies$ quarantine), preventing engineer p-hacking retry attacks.
- **[DEEP DIVE]** appended to `OUTPUT/testing-framework-spec.md`:
  - Zero-daemon hermetic sandbox harness via rootless Bubblewrap (`bwrap`) with network isolation (`--unshare-net`) and RAM disk mounts (`> 25,000 IOPS`).
  - Adversarial Hypothesis property-based testing strategies for multi-agent artifacts with SQLite-WAL example database caching.
  - Dynamic AST-sliced mutation testing delivering 8.5x execution speedup via diff node extraction and coverage-guided mutant execution.
- **[DEEP DIVE]** appended to `OUTPUT/quality-metrics.md`:
  - Zero-daemon quality telemetry ledger in SQLite-WAL with atomic per-task metric ingestion and real-time EWMA rolling queries (<3ms).
  - Multi-dimensional Composite Quality Index (CQI) formulated as a non-compensatory weighted geometric mean ($M_k \le \text{Floor}_k \implies \text{CQI} \to 0$).
  - Tabular CUSUM drift detection ($k=0.5, h=4.5$) isolating subtle quality erosion ($1\sigma$ negative shifts) within 8 tasks vs 38 tasks under Shewhart rules.
- **[DEEP DIVE]** appended to `OUTPUT/blocking-authority.md`:
  - Zero-daemon cryptographic gate enforcement via Ed25519 capability tokens (`gate_capability_tokens`, nonce revocation ledger, sub-2ms pre-push hook verification).
  - Dual-key M-of-N threshold escalation protocol ($M=2$ of 3 distinct roles, 15-minute emergency override lease) and Collusion Detection Quotient ($\text{CDQ} = \kappa \cdot \log_2(1 + R_{\text{esc}})$, hard alarm on $\text{CDQ} > 0.85$).
  - Bayesian Beta-Binomial strictness calibration ($\theta \sim \text{Beta}(\alpha+k, \beta+n-k)$ with variance-penalized damped threshold shifts $\Delta T$).
- **[DEEP DIVE]** appended to `OUTPUT/cicd-integration.md`:
  - Zero-daemon local hermetic CI pre-flight runner in rootless Bubblewrap (`bwrap --unshare-net --unshare-pid`, <1.2s overhead).
  - In-toto v1.0 / SLSA Level 3 cryptographic provenance attestation ledger in SQLite-WAL (`ci_provenance_attestations` signed with Ed25519).
  - Content-addressable AST test cache (`ci_test_cache`) achieving sub-15ms test skip replay for unchanged abstract syntax trees.
- **[DEEP DIVE]** appended to `OUTPUT/tester-soul.md`:
  - Metamorphic differential oracle engine testing algebraic invariants (idempotence, monotonicity, reversibility) to eliminate vacuous LLM assertions.
  - Zero-daemon SQLite-WAL test execution DAG with flakiness tracking and automatic quarantine.
  - Cryptographically signed verdict certificates (`verdict_certificates` with Ed25519) binding test evidence to immutable git commits.
- **[DEEP DIVE]** appended to `OUTPUT/engineer-soul.md`:
  - Zero-daemon SQLite-WAL pre-commit state machine enforcing linear lifecycle stages (`SPEC_LOCKED` to `TESTER_READY`) via CAS version locks.
  - In-process AST code fence enforcer banning unresolvable/ghost imports, empty stubs, and high-complexity code (McCabe $M \le 10$, nesting $\le 4$) in <8ms.
  - Automated HOLD remediation protocol with test-directory write barriers and 3-strike escalation circuit breaker.
- **[DEEP DIVE]** appended to `OUTPUT/routing-integration.md`:
  - Zero-daemon SQLite-WAL formation dispatcher (`formation_dispatch_ledger`) with sub-2ms lease resolution.
  - Cost-Sensitive Multi-Attribute Utility Optimization (CS-MAUO) with asymmetric defect penalty ($C_{\text{FN}} = 50.0, C_{\text{FP}} = 1.0$), enforcing a mathematical 1.96% defect threshold ceiling for `SOLO` routes.
  - Dynamic formation escalation state machine (`SOLO` -> `DUO` -> `PIPELINE` -> `FULL`) with atomic CAS updates.
- **[DEEP DIVE]** appended to `OUTPUT/implementation-roadmap.md`:
  - Zero-daemon automated shadow-to-blocking promotion engine in SQLite-WAL (`roadmap_gate_status`) evaluating FP rates (<5%) and activity bands across 20-task windows.
  - Canary blocking tripwire executing sub-millisecond atomic rollbacks upon escape rate spikes (>5%).
  - Fast Git churn and logical coupling miner extracting Churn-Coupling Index (CCI) in <200ms.







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
- **[DEEP DIVE]** appended to `OUTPUT/multi-agent-security.md` (stacks after antigravity's Bubblewrap/Macaroons dive — no overlap):
  - MCP attack surface (Invariant Labs 2025, verified): tool poisoning via tool descriptions (sidenote exfil), rug pulls (post-approval description change), cross-server tool shadowing → pinned hash-verified tool manifests, per-ring MCP allowlist, cross-server dataflow boundaries
  - MCP authorization hardening (spec-verified): token passthrough MUST NOT (audience-bound tokens per agent), confused-deputy per-client consent, SSRF private-range blocking + Smokescreen egress proxy, progressive scope minimization (no wildcards)
  - Per-edge trifecta audit: Willison's lethal trifecta applied to trust edges, not just agents — researcher→engineer edge is the crew's most load-bearing control (safe iff engineer egress stays denied); inter-agent messages are data (spotlighting), router decides causality
  - Canary-token DLP (Thinkst): unique marker strings in memory tiers + sensitive paths, Layer-5 exact-match scan → deterministic exfil detection, zero false positives; detect-not-prevent caveat paired with quarantine response
  - Signed SOULs: Ed25519-signed policy versions (verify-before-load), two-person rule for Ring 0/1 changes, patch ledger as chain of custody; OWASP Agentic AI T1–T15 + Top 10 Agentic Applications 2026 (ASI01–ASI10) mapped; 6/10 vectors exploited in the wild by April 2026 [Lyrie]

### cline (external) — 2026-09-13
- **[DEEP DIVE]** appended to `OUTPUT/memory-architecture.md` (~390 lines, all claims web-verified 2026-09-13 via exa + tinyfish against primary sources; confirmed live on GitHub at line 411 after freebuff pass-2/3 merges):
  - Governed shared memory: the 4 primitives (scoped retrieval, temporal supersession, provenance, policy-governed propagation) from the live MemClaw/ArgusFleet study (arXiv:2606.24535) — incl. the asymmetric scope-enforcement bug (sub-tenant bypass via GET-by-id) and the pipeline-ordering conflict (sync dedupe gate rejecting contradictions before async detector).
  - Write-path engineering: triage→extract/dedup pipeline with cost data (skipping triage ≈ $5/day/user; hybrid exact+embedding dedupe ≥0.92 NOOP band), conflicts resolved async, never sync.
  - ACE playbooks as procedural memory (arXiv:2510.04618): +10.6% agents / +8.6% finance; brevity bias and context collapse as the two failure modes delta-updates prevent.
  - Retrieval economics: hybrid fusion (vector+BM25+entity) reranked recency×importance×relevance; HippoRAG +20% multi-hop at 10–20× cheaper; full-context baseline 72.9% LoCoMo @ ~26K tokens vs Mem0 66.9–92.5% @ 1.8–6.9K (vendor-reported) — incl. the Mem0-vs-Zep LoCoMo methodology dispute, both sides cited.
  - Memory poisoning (arXiv:2606.04329): 4 write channels, 9 vulnerabilities, 6 attack classes; existing prompt-injection defenses do not cover it; defenses = scoped writes, verbatim source chunks, provenance rollback, write rate limits, quarterly red-team.
  - Executable deliverables: write_gate.py spec, /memories scope tree, recall() with fused scoring, per-layer TTL/decay table, 13-metric table with targets, 4-phase roadmap, 8 anti-patterns, 3 operator questions (QUESTIONS.md).

## Research Queue
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
| zcode | ✅ Complete | Push-bug repair + deep dives: communication-protocols, self-healing, multi-agent-security (2026-09-14) |
| cline | ✅ Complete | Memory Architecture Deep Dive (governed shared memory, write-path, ACE playbooks, retrieval economics) |
| freebuff | ✅ Complete | Pass-3 deep dives on all 13 multi-agent outputs (2026-09-14); pass-2 testing dives (2026-09-14); pass-1 multi-agent dives (2026-09-13) |
| antigravity | ✅ Complete | Deep dives across all 13 multi-agent domains + testing discipline (2026-09-14) |
| opencode | ⏳ Pending | Not connected |

## Output Inventory

| File | Status | Contents |
|------|--------|----------|
| `OUTPUT/testing-maturity-model.md` | ✅ Complete | 5 AI-crew levels, L1 mapping, climb actions, checklist |
| `OUTPUT/tdd-protocol.md` | ✅ Complete | Split RED/GREEN, handoff formats, ladder, time-box, state machine + 2 deep dives (freebuff: human/LLM evidence, probabilistic GREEN; antigravity: CAS state machine, AST oracle firewall, Chi-square flake defense) |
| `OUTPUT/testing-framework-spec.md` | ✅ Complete | pytest/coverage/Hypothesis/mutmut configs + thresholds + 2 deep dives (freebuff: diff coverage, ratchets, tarpit warning; antigravity: bwrap sandbox harness, agent schema Hypothesis, AST-sliced mutation) |
| `OUTPUT/quality-metrics.md` | ✅ Complete | 16-metric catalog, anti-pattern detectors, ledger schema + 2 deep dives (freebuff: small-sample SPC, p-charts, run rules; antigravity: zero-daemon SQLite ledger, CQI non-compensatory math, tabular CUSUM drift detection) |
| `OUTPUT/blocking-authority.md` | ✅ Complete | 8 MUST-block, MUST-NOT list, escalation, calibration + 2 deep dives (freebuff: audit sampling math, c=0 plans; antigravity: cryptographic gate tokens, M-of-N escalation & CDQ, Bayesian calibration) |
| `OUTPUT/cicd-integration.md` | ✅ Complete | Triggers, gates, artifacts, flake lane, nightly golden+drills + 3 deep dives (freebuff pass 2: supply chain SHA-pinning/OIDC; freebuff pass 3: merge queues; antigravity: local hermetic CI runner, in-toto SQLite attestation, CAS cache) |
| `OUTPUT/tester-soul.md` | ✅ Complete | Full executable tester spec + verdict template + 3 deep dives (freebuff pass 2: RTS Ekstazi/STARTS, safety KPI; freebuff pass 3: 80/20 attention allocation; antigravity: metamorphic differential oracles, SQLite test DAG, verdict certificates) |
| `OUTPUT/engineer-soul.md` | ✅ Complete | Iron-law verbatim, artifacts, HOLD response, bans + 3 deep dives (freebuff pass 2: IFEval++ adherence, CI-checkable rules; freebuff pass 3: review yield & SmartBear diff limits; antigravity: pre-commit state machine, AST code fences, HOLD remediation) |
| `OUTPUT/routing-integration.md` | ✅ Complete | Formation table, activation, message/artifact flows + 3 deep dives (freebuff pass 2: RouteLLM cost-sensitive loss, golden routing set; freebuff pass 3: reviewer fatigue calibration; antigravity: zero-daemon formation dispatcher, CS-MAUO utility, dynamic escalation) |
| `OUTPUT/implementation-roadmap.md` | ✅ Complete | 4 phases with files, criteria, risks + 3 deep dives (freebuff pass 2: Google Tricorder, shadow mode; freebuff pass 3: defect hotspot mining; antigravity: shadow-to-blocking pipeline, canary rollbacks, CCI miner) |
| `OUTPUT/memory-architecture.md` | ✅ Complete | 4-tier hierarchy, rate-distortion compaction, EWC anti-forgetting + 3 deep dives (freebuff: vector degradation, chunking bounds; antigravity: zero-daemon SQLite substrate, HippoRAG 2 PPR, BGE-M3, ACT-R decay; cline: governed shared memory, write-path, ACE playbooks) |
| `OUTPUT/communication-protocols.md` | ✅ Complete | EDA, priority lanes, DLQ, idempotency, circuit breakers + 3 deep dives (freebuff: A2A/jitter/trace; antigravity: SQLite-WAL bus/WFG/deltas; zcode: outbox/schema-evolution/MCP 2026-07-28/retry budgets) |
| `OUTPUT/self-healing.md` | ✅ Complete | Reflective runtime, RBT diagnosis, 5-level degradation + 3 deep dives (freebuff: GEPA/error budgets/chaos; zcode: self-correction trap, CBR 4R, playbooks; antigravity: SQLite healing state machine, TextGrad backprop, Lyapunov stability, bwrap canaries) |
| `OUTPUT/production-deployment.md` | ✅ Complete | HA, circuit breakers, ASI drift detection, MLflow + 2 deep dives (freebuff: OTel gen_ai, K8s probes, canaries; antigravity: zero-daemon supervision, in-DB rate limiting, entropy breakers, ASI 12-dim tracking) |
| `OUTPUT/multi-agent-security.md` | ✅ Complete | 5-layer defense, ring-based access, canary verification + 3 deep dives (freebuff: trifecta/defense-data/microVMs; antigravity: bwrap containment/macaroons/zeroization/datamarking; zcode: MCP tool poisoning, per-edge trifecta, canary DLP, signed SOULs) |
| `OUTPUT/scalability-patterns.md` | ✅ Complete | Hierarchical groups ≤10, decision boundary P_SA > 0.45 + 2 deep dives (freebuff: SWARM+ bounds; antigravity: ephemeral worker pool, work-stealing deque, BAMAS tree recursion & budget inheritance) |
| `OUTPUT/human-in-the-loop.md` | ✅ Complete | Approval control plane, override tokens, EU AI Act + 2 deep dives (freebuff: Article 14, automation bias, fatigue; antigravity: zero-daemon CLI/IPC, TOCTOU locking, Little's law backpressure, decoy audits) |
| `OUTPUT/conflict-resolution.md` | ✅ Complete | Weighted voting, reasoning trees, deadlock breaking + 2 deep dives (freebuff: Arrow's impossibility, HOLD-wins, judge bias; antigravity: Brier calibration, sequential consensus JSD, livelock preemption, SQLite CDPs) |
| `OUTPUT/agent-embodiment.md` | ✅ Complete | 5-dimension personality, voice drift detection + 2 deep dives (freebuff: persona vectors, collapse dynamics, DPC metric; antigravity: stylometric voice vectors, Mahalanobis drift gating, in-context re-anchoring, anti-sycophancy probing) |
| `OUTPUT/tool-differentiation.md` | ✅ Complete | Capability-based assignment, result sharing + 2 deep dives (freebuff: tool count failure curves; antigravity: dynamic toolsets v2, JetBrains observation masking, SQLite-WAL cache) |
| `OUTPUT/cost-optimization.md` | ✅ Complete | 3-tier routing, caching, APC, budget enforcement + 2 deep dives (freebuff: FrugalGPT, cache-writes, unit cost; antigravity: SQLite cost ledger, cache anchors, RouteLLM, non-fatal preemption) |
| `OUTPUT/evaluation-frameworks.md` | ✅ Complete | 6 archetypes, coordination metrics, trace-to-eval + 2 deep dives (freebuff: Agent-as-a-Judge, Goodhart discipline, flake budgets; antigravity: zero-daemon replay compiler, synergy ratio, Wald SPRT, McNemar paired testing) |
| `OUTPUT/explainability.md` | ✅ Complete | Structured traces, time-travel debugging, root cause analysis + 2 deep dives (freebuff: counterfactual attribution, OTel-native traces, deterministic capture; antigravity: zero-daemon CoW checkpointing, causal slicing, Shapley fault localization, dual-fidelity explanations) |
| *(all 13 multi-agent files above)* | ✅ Deep-dived | freebuff 2026-09-13: one `[DEEP DIVE]` cycle each — validation gates, standards alignment (A2A/MCP/OTel/W3C), and measured thresholds appended |
| *(all 10 testing-domain files above)* | ✅ Deep-dived (pass 2) |
| *(all 13 multi-agent files above)* | ✅ Deep-dived (pass 3) | freebuff 2026-09-14: third `[DEEP DIVE]` cycle — CRDT memory consistency, sagas + HLC, LLM RCA (RCACopilot/OpenRCA), SPIFFE workload identity, LLM-serving SLO math, power-of-two dispatch, conformal abstention, Dung argumentation, Big Five validity warning, stateful tool evals, output governance + speculative decoding, contamination audits, two-tier trace policy |
| `OUTPUT/gate-toolkit.md` | ✅ Complete | Executable pass-2 protocols (stdlib Python), 35-test suite, mutation harness — 100% mutation score (freebuff 2026-09-14) | freebuff 2026-09-14: second `[DEEP DIVE]` cycle — coverage floors (diff-coverage/ratchet), CI supply-chain hardening (SHA pinning/OIDC/attestation), Goodhart-resistant maturity appraisal, audit sampling math, router economics, SPC for the ledger, RTS rerun policy |
