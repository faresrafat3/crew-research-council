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

## [DEEP DIVE]: Activation Evidence, Handoff Precedents, and Judge-Separation Requirements (cline, 2026-09-13)

### 1. Why activation must be default-on for PIPE/FULL: the compliance data

The activation rule (tester on 100% of PIPELINE/FULL) is set against measured non-compliance, not theory. In COORD-01/02 the engineer skipped tests on 100% of tasks even when testing was explicit; post-fix audits must therefore assume a near-100% skip rate without gating [Council Context, 2026]. Industry data concurs: DORA 2025 links higher AI adoption to higher delivery instability [DORA, 2025], and the Stack Overflow 2025 survey shows distrust (46%) exceeding trust (33%) in AI tool accuracy [Stack Overflow, 2025] — downstream consumers already price in unverified agent output. The skip list (pure read-only research, trivial sub-5-line SOLO, infra outages deferred, diff-free redispatches) is deliberately narrow: every item is verifiable from the dispatch record alone (no judgment call), so the router cannot silently widen it. Precision is protected the other way: activation precision >80% gated is audited from verdicts, and <50% triggers loosening — the router is measured on both recall and precision, not just coverage [Council Context, 2026].

### 2. Handoff pattern precedent: structured messages between phases

The SPEC→RED→GREEN→suite→review→verdict message order follows the VS Code Red-Green-Refactor handoff-agents model, where each phase emits a structured message the next phase consumes [Microsoft, 2026]. The crew's per-edge artifact contract (REQ-IDs; test files + RED log; impl + GREEN log; JUnit + coverage + mutation + lints + flake snapshot; critic pass/fail; verdict + ledger entry) is the evidence-bound verdict pattern: gates are auditable because every decision cites its inputs, outputs, traces, and policy version [QABattle, 2025]. The tester-critic separation (different model families; critic reruns without reading tester rationale) addresses measured self-preference bias: LLM judges systematically favor familiar (low-perplexity, often self-generated) outputs over human-preferred ones [Wataoka et al., 2024/2025], so a critic sharing the tester's model family is a correlated judge, not an independent one [IJECS, 2026].

### 3. Scheduling precedent: tiered test sizes keep the gate under 10 minutes

The gate-latency budget (<10 min blocking) is enforced by size-tiered scheduling, following Google's Small/Medium/Large test-size discipline: Small tests take no network, no DB, no filesystem, no threads, no sleeps, with a 60s limit; Medium allows localhost DB/filesystem/threads within 300s; Large allows externals within 900s+ [Stewart, 2010]. The crew mapping: unit + targeted mutation are Small (block every commit); integration + property are Medium (block PR merge); E2E + full mutation + contracts are Large (nightly async only) [SQRBOK, 2025]. Google's flake data justifies the quarantine lane design: ~1.5% of test runs report flaky results while ~16% of tests exhibit some flakiness, and ~84% of pass→fail transitions involve a flaky test [Micco, 2016] — without a quarantine lane, the gate spends its budget re-investigating known flakes instead of real regressions.

### 4. Pyramid precedent: most tests small and fast

The formation table's test mix (DUO: unit + PBT sample; PIPELINE: +70% mutation; FULL: +80% mutation + 90% req-coverage; E2E capped at 10 per FULL) implements the practical test pyramid: the bulk of tests are fast unit tests at the base, fewer integration/contract tests in the middle, and a small cap of E2E at the top, with explicit guidance against test duplication across layers [Vocke, 2018]. System prompts are the enforcement vehicle: they function as the operational blueprint defining an agent's behavior, constraints, and decision frameworks before any interaction, and minor prompt variations can completely change output distribution — so the formation table and activation rules belong in versioned SOUL text, not in per-dispatch prose [Shah, 2025].

### References for deep dive
- [Council Context, 2026] Crew v2 trials and classification axes.
- [DORA, 2025] AI adoption, throughput, instability, trust gap.
- [Stack Overflow, 2025] Developer survey 46% distrust vs 33% trust.
- [Microsoft, 2026] VS Code handoff agents pattern.
- [QABattle, 2025] Evidence-bound verdicts.
- [Wataoka et al., 2024/2025] Self-Preference Bias in LLM-as-a-Judge (arXiv:2410.21819).
- [IJECS, 2026] Independent verification with HITL.
- [Stewart, 2010] Test Sizes (Small/Medium/Large constraints and time limits).
- [Micco, 2016] Flaky Tests at Google (1.5%/16%/84% figures and mitigation).
- [Vocke, 2018] The Practical Test Pyramid.
- [SQRBOK, 2025] Pyramid and tiered scheduling.
- [Shah, 2025] System prompts as operational blueprints.
- [KnowMBA, 2025] E2E caps and budgets.
- [ArXiv, 2026] Self-testing gates at scale.

---

## [DEEP DIVE (freebuff, pass 2, 2026-09-14)]: Router Error Economics — Asymmetric Misrouting Costs, Learned Routing Evidence, and the Recall-First Design

Pass-1 measures the router symmetrically ("misroute rate <5%, retune >5%"). The two error directions are not symmetric, and the evidence on learned routing changes how the router should be built and audited.

### V1. Misrouting is asymmetric: recall-first, precision-floored

- **False negative** (complex task routed SOLO, tester skipped): the COORD-01/02 failure class — code ships with zero tests. The cost is an escape, the crew's terminal metric; pass-1's own compliance data says assume ~100% skip without gating.
- **False positive** (trivial task gets tester/PIPELINE): costs latency and compute only. The gate still runs, the verdict is PROMOTE, nothing escapes.

With costs ordered FN ≫ FP, the needs_tester classifier must be **recall-first**: tuned so the FN rate approaches 0 (target ≤1%), accepting FP inflation up to the precision floor pass-1 already sets (>80% gated). The symmetric <5% misroute metric should be split into FN-misroute (target <1%, hard) and FP-misroute (target <25%, soft) — a single blended rate hides the dangerous direction. This is the standard cost-sensitive-threshold argument from detection theory applied to the router.

### V2. Learned routing is proven technology — with one crucial adaptation

RouteLLM (Ong et al., 2024; ICLR 2025) trains routers on human preference data to choose between a strong and weak model per query: **>2× cost reduction without quality loss** on public benchmarks; up to **85% cost reduction on MT Bench** at **95% of GPT-4 quality** (45% on MMLU, 35% on GSM8K) [Ong et al., arXiv:2406.18665; LMSYS blog, 2024; lm-sys/routellm]. Formation choice (SOLO/DUO/PIPELINE/FULL) is the same problem one level up: route each task to the cheapest pipeline that clears its quality bar, with the ledger's verdict history as the preference signal (which formations produced PROMOTEs without rework, at what token cost).

The adaptation: RouteLLM's objective is quality-symmetric — it trades marginal quality against cost. Formation routing must weight FN asymmetrically (V1), so the router's loss function is cost-sensitive: `loss = C_FN × miss(test-needed) + C_FP × overshoot(test-not-needed) + λ × cost(formation)`, with C_FN set high enough that the calibrated router never trades a needed-tester miss for savings. The pass-1 skip list (narrow, verifiable) is the hand-written prior this learned layer must never override.

### V3. The router needs its own regression suite

Misroute rate is measured by review (pass-1: <5% retune). Add the software-engineering move the crew applies everywhere else: a **golden routing set** of 50–100 labeled tasks spanning the classification axes (complexity × verifiability × tool needs [Council Context, 2026]), rerun against every router threshold change, SOUL patch, or formation-table edit. A routing change that flips golden-set labels is a regression — blocked before deployment, exactly like a code change that reddens the suite (tdd-protocol state machine). Edge-case labels double as the adversarial drills testing-maturity pass-2 §M3 injects at the maturity gates.

### V4. Log expected-vs-actual cost per route

RouteLLM's headline numbers (85% savings) hold only while routing decisions are *correct*; wrong routing burns the expensive formation on cheap tasks (FULL for a trivial task) or the reverse. The ledger already records per-task metrics (quality-metrics 16 metrics); add **formation-cost variance** (expected tokens/wall-time for the chosen formation vs actual) as a standing router-calibration input. Systematically positive variance on SOLO→escalation paths is the FN signature; systematic overshoot on trivial FULL routes is the FP signature — both are actionable threshold moves at the quarterly calibration (blocking-authority §2).

### Numbers for calibration (pass 2)

| Quantity | Value | Source |
|---|---|---|
| RouteLLM cost reduction | >2× (up to 85% MT Bench / 45% MMLU / 35% GSM8K) | [Ong et al., 2024; LMSYS] |
| Quality retained at max savings | 95% of GPT-4 (MT Bench) | same |
| FN-misroute target | ≤1% (hard) | this dive, from COORD data |
| FP-misroute target | <25% (soft; precision floor >80% gated) | pass-1 metrics reinterpreted |
| Golden routing set | 50–100 labeled tasks, rerun on router changes | this dive |
| Standing calibration input | formation-cost variance per route | this dive |

### References (pass 2)
1. [Ong et al., 2024] "RouteLLM: Learning to Route LLMs with Preference Data," arXiv:2406.18665 (ICLR 2025). https://arxiv.org/html/2406.18665v4 [verified: 2026-09-14]
2. [LMSYS, 2024] "RouteLLM: An Open-Source Framework for Cost-Effective LLM Routing," 2024-07-01. https://www.lmsys.org/blog/2024-07-01-routellm/ [verified: 2026-09-14]
3. [lm-sys/routellm] Framework README — "reduce costs by up to 85% while maintaining 95% GPT-4 performance." https://github.com/lm-sys/routellm [verified: 2026-09-14, snippet]
4. Cross-refs: Council Context (classification axes); routing-integration pass 1 (activation rules, precision/recall metrics); blocking-authority pass 1 §2 (calibration); testing-maturity pass 2 (adversarial drills); tdd-protocol pass 1 (state machine).
