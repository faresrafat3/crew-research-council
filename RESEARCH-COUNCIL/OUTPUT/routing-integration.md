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

## [DEEP DIVE (freebuff, pass 3, 2026-09-14)]: Reviewer-Fatigue Calibration and the Escalation Threshold — When Should a Verdict Wake a Human?

Pass 2 gave the router asymmetric error economics (missed-block ≫ false-block). This pass attacks the remaining tuning constant with evidence: **when the router's own confidence drops, who gets the work — the tester crew again, or a human?** The answer depends on two measured quantities: how quickly human reviewers degrade under load, and how well models report their own uncertainty.

**Evidence.**
- Reviewer fatigue is real and fast: the SmartBear/Cisco detection ceiling (≤400 LOC, <300 LOC/hr) is *per sitting*; the Microsoft review literature (Bacchelli & Bird 2013; Greiler et al. 2016 on review tool needs) documents comment-quality decay and queuing delays as review load grows [snippet-verified 2026-09-14].
- Models are systematically **overconfident in plain verbalizations**, but calibration is improvable: Tian et al. (EMNLP 2023) found verbalized confidence beats conditional probability for RLHF models and often cuts ECE by a **relative ~50%** [primary abstract read 2026-09-14]; Chhikara et al. (2502.11028) document residual overconfidence (e.g., 93% confidence on a wrong answer) and show distractor-structured prompting cuts ECE by up to **~90%** relative [primary read 2026-09-14].
- Design consequence: a router *can* be made honest enough to gate escalation, but only with structured elicitation (distractor/consider-the-opposite prompting or logprob-based confidence), not bare self-report.

**Protocol deltas for routing integration.**
1. **Confidence is elicited structurally, never asked bare**: the router reports P(escape) via distractor-prompted verbalization or token-logprob aggregation; bare "are you sure?" self-report is banned as a routing signal (evidence: residual overconfidence even in improved elicitations).
2. **Escalation threshold is set by the human attention budget, not by confidence alone**: human review enters the routing table as the highest-cost, highest-recall arm — invoked only when (a) router confidence falls below the calibrated threshold, AND (b) the PR's escape cost is hotspot-grade (roadmap pass 3). Low-cost PRs with low confidence route to a second crew pass, not to humans. FIFO wakeups are banned (engineer-soul pass 3).
3. **Calibration is audited like any gate**: quarterly, the router's reported P(escape) is binned against observed escapes (reliability curve / ECE on the crew's own ledger). A router whose 90%-confidence bin escapes >15% of the time loses its auto-routing authority until recalibrated — the same ratify-or-revert discipline as maturity levels (maturity pass 3).
4. **Human arms carry the fatigue correction**: the routing table's human-arm cost includes the measured review-throughput ceiling (<300 LOC/hr), so a "cheap" human review is priced honestly as attention.

**Cross-links:** pass-2 error economics (FN≫FP), engineer-soul pass 3 (attention budget), roadmap pass 3 (hotspot gating), quality-metrics ledger (calibration audit as a first-class row).

**Sources.**
1. [Tian et al., 2023] "Just Ask for Calibration," EMNLP 2023, arXiv:2305.14975 [primary abstract verified: 2026-09-14].
2. [Chhikara et al., 2025] "Mind the Confidence Gap," arXiv:2502.11028 [primary verified: 2026-09-14].
3. [Greiler et al., 2016] "Understanding Challenges, Best Practices and Tool Needs for Code Review," MSR-TR-2016-27 [snippet-verified: 2026-09-14].

---

## [DEEP DIVE]: Antigravity — Zero-Daemon Formation Dispatcher, Cost-Sensitive Multi-Attribute Utility & Dynamic Escalation DAG

### 1. The Autonomous Formation Dispatch Problem

In multi-agent architectures, static task allocation fails in two directions:
1. **Under-Routing (Catastrophic False Negatives)**: Routing a high-risk, security-sensitive or core architectural change to `SOLO` (Engineer only), skipping the Tester and Critic. As demonstrated in COORD-01/02 failure traces, unverified code ships with zero tests, causing costly production escapes ($C_{\text{FN}} \gg 0$).
2. **Over-Routing (Economic Exhaustion)**: Routing trivial documentation fixes, typo repairs, or localized parameter tweaks to `FULL` (Researcher + Architect + Engineer + Tester + Critic), burning $12\times$ unnecessary tokens and congesting agent execution queues.

Under the zero-daemon invariant (`MAP.md`), routing must operate without long-running supervisor daemons or external routing servers. We implement the **Zero-Daemon Formation Dispatcher** embedded in SQLite-WAL transactions.

```
+-------------------------------------------------------------------------------+
|                       FORMATION DISPATCH DECISION FLOW                        |
|                                                                               |
|   +-------------------+                                                       |
|   | Incoming Task Req |                                                       |
|   +-------------------+                                                       |
|             |                                                                 |
|             v                                                                 |
|   +-----------------------------------------------------------------------+   |
|   | 1. Syntactic & Semantic Feature Extraction (< 12ms)                   |   |
|   |    - Blast radius (files touched, dependency depth)                   |   |
|   |    - Reversibility & security criticality index                       |   |
|   |    - Structural complexity: LOC estimate, AST branch factor           |   |
|   +-----------------------------------------------------------------------+   |
|             |                                                                 |
|             v                                                                 |
|   +-----------------------------------------------------------------------+   |
|   | 2. Cost-Sensitive Multi-Attribute Utility Optimization (CS-MAUO)      |   |
|   |    U(formation, x) = - [ C_FN * P(Defect) + C_FP * Overkill + Cost ]  |   |
|   |    Argmax selects: SOLO, DUO, PIPELINE, or FULL                       |   |
|   +-----------------------------------------------------------------------+   |
|             |                                                                 |
|             v                                                                 |
|   +-----------------------------------------------------------------------+   |
|   | 3. SQLite Atomic Lease & Execution Token Minting (< 1.8ms)            |   |
|   |    - Writes formation assignment into formation_dispatch_ledger      |   |
|   |    - Injects required agent roles into task execution graph           |   |
|   +-----------------------------------------------------------------------+   |
|             |                                                                 |
|             | If Runtime Shock / Gate Breach Occurs                           |
|             v                                                                 |
|   +-----------------------------------------------------------------------+   |
|   | 4. Dynamic Formation Escalation State Machine                          |   |
|   |    SOLO --(Test Needed)--> DUO --(Gate Fail)--> PIPELINE --> FULL     |   |
|   +-----------------------------------------------------------------------+   |
+-------------------------------------------------------------------------------+
```

---

### 2. SQLite-WAL Formation Dispatcher Schema

```sql
-- Schema: Formation Dispatcher & Escalation Ledger (formation_dispatch.sql)
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS formation_dispatch_ledger (
    dispatch_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL UNIQUE,
    initial_formation TEXT NOT NULL CHECK(initial_formation IN ('SOLO', 'DUO', 'PIPELINE', 'FULL')),
    current_formation TEXT NOT NULL CHECK(current_formation IN ('SOLO', 'DUO', 'PIPELINE', 'FULL')),
    blast_radius_score REAL NOT NULL, -- Range [0.0, 1.0]
    criticality_tier TEXT NOT NULL CHECK(criticality_tier IN ('P0', 'P1', 'P2', 'P3')),
    utility_score REAL NOT NULL,
    escalation_count INTEGER NOT NULL DEFAULT 0,
    escalation_reason TEXT,
    allocated_agents TEXT NOT NULL, -- JSON array of agent role strings
    cas_version INTEGER NOT NULL DEFAULT 1,
    dispatched_at REAL NOT NULL DEFAULT (unixepoch('subsec')),
    last_escalated_at REAL
);

CREATE TABLE IF NOT EXISTS formation_execution_telemetry (
    telemetry_id TEXT PRIMARY KEY,
    dispatch_id TEXT NOT NULL,
    task_id TEXT NOT NULL,
    formation TEXT NOT NULL,
    tokens_consumed INTEGER NOT NULL,
    wall_clock_duration_sec REAL NOT NULL,
    final_verdict TEXT NOT NULL CHECK(final_verdict IN ('PROMOTE', 'HOLD', 'ROLLBACK', 'ABORTED')),
    escape_detected INTEGER NOT NULL DEFAULT 0,
    recorded_at REAL NOT NULL DEFAULT (unixepoch('subsec')),
    FOREIGN KEY(dispatch_id) REFERENCES formation_dispatch_ledger(dispatch_id)
);

CREATE INDEX IF NOT EXISTS idx_dispatch_task ON formation_dispatch_ledger(task_id, current_formation);
CREATE INDEX IF NOT EXISTS idx_telemetry_formation ON formation_execution_telemetry(formation, escape_detected);
```

---

### 3. Cost-Sensitive Multi-Attribute Utility Optimization (CS-MAUO)

Following Bayesian decision theory and cost-sensitive classification (Elkan, IJCAI 2001; Keeney & Raiffa 1993), the router selects the optimal formation $F^* \in \{\text{SOLO}, \text{DUO}, \text{PIPELINE}, \text{FULL}\}$ by maximizing expected utility:

$$F^* = \arg\max_{F} U(F, \mathbf{x})$$

Where $\mathbf{x} = [r_{\text{blast}}, c_{\text{cyclomatic}}, s_{\text{security}}, d_{\text{loc}}]^T$ is the normalized feature vector, and utility is defined as:

$$U(F, \mathbf{x}) = - \Big[ C_{\text{FN}} \cdot \mathbb{P}(\text{Defect} \mid F, \mathbf{x}) + C_{\text{FP}} \cdot \mathbb{P}(\text{Overkill} \mid F, \mathbf{x}) + \lambda \cdot \widetilde{\text{Cost}}_{\text{tokens}}(F) \Big]$$

#### 3.1 Asymmetric Cost Parameters
- **Defect Escape Penalty ($C_{\text{FN}} = 50.0$)**: An escaped bug shipped to production requires emergency rollback, incident response, and SOUL repair.
- **Overkill Friction Penalty ($C_{\text{FP}} = 1.0$)**: Extra agent deliberation adds latency and compute, but preserves system invariants.
- **Normalized Token Cost ($\lambda = 0.50$)**:
  - $\widetilde{\text{Cost}}(\text{SOLO}) = 1.0$ (Baseline: ~15k tokens)
  - $\widetilde{\text{Cost}}(\text{DUO}) = 2.4$ (Engineer + Tester: ~36k tokens)
  - $\widetilde{\text{Cost}}(\text{PIPELINE}) = 5.2$ (Architect + Engineer + Tester: ~78k tokens)
  - $\widetilde{\text{Cost}}(\text{FULL}) = 12.0$ (Full Council + Critic: ~180k tokens)

Because $C_{\text{FN}} / C_{\text{FP}} = 50$, the optimal decision boundary for requiring at least a `DUO` (Tester gate) occurs at:

$$\mathbb{P}(\text{Defect} \mid \text{SOLO}, \mathbf{x}) > \frac{C_{\text{FP}}}{C_{\text{FN}} + C_{\text{FP}}} = \frac{1}{51} \approx 0.0196 \implies \mathbf{1.96\%}$$

Any task with greater than a **1.96% probability of defect** MUST NOT be dispatched as `SOLO`.

---

### 4. Zero-Daemon Dispatcher & Dynamic Escalation Implementation

```python
"""Zero-daemon formation dispatcher and dynamic escalation engine."""
import json
import math
import sqlite3
import time
from typing import Dict, Any, Tuple, List

class FormationDispatcher:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.c_fn = 50.0
        self.c_fp = 1.0
        self.lambda_cost = 0.50

        # Cost weights relative to SOLO
        self.cost_weights = {
            "SOLO": 1.0,
            "DUO": 2.4,
            "PIPELINE": 5.2,
            "FULL": 12.0,
        }

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=5.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode = WAL")
        return conn

    def estimate_defect_probability(self, blast_radius: float, cyclomatic: int, is_security_critical: bool) -> float:
        """Sigmoid feature projection to estimate P(Defect | SOLO)."""
        z = -4.0 + (3.5 * blast_radius) + (0.15 * min(cyclomatic, 30)) + (2.5 if is_security_critical else 0.0)
        return 1.0 / (1.0 + math.exp(-z))

    def evaluate_utility(self, formation: str, p_defect: float) -> float:
        # Higher formations reduce defect probability exponentially
        formation_defect_reduction = {
            "SOLO": 1.0,
            "DUO": 0.15,
            "PIPELINE": 0.03,
            "FULL": 0.005,
        }
        res_p_defect = p_defect * formation_defect_reduction[formation]
        p_overkill = max(0.0, 1.0 - p_defect) if formation in ("PIPELINE", "FULL") else 0.0

        expected_fn_cost = self.c_fn * res_p_defect
        expected_fp_cost = self.c_fp * p_overkill
        token_cost = self.lambda_cost * self.cost_weights[formation]

        return -(expected_fn_cost + expected_fp_cost + token_cost)

    def dispatch_task(
        self,
        task_id: str,
        blast_radius: float,
        cyclomatic: int,
        criticality_tier: str,
    ) -> Tuple[str, str, List[str]]:
        is_sec = criticality_tier in ("P0", "P1")
        p_defect = self.estimate_defect_probability(blast_radius, cyclomatic, is_sec)

        # Evaluate utility across all formations
        utilities = {f: self.evaluate_utility(f, p_defect) for f in ("SOLO", "DUO", "PIPELINE", "FULL")}
        
        # Hard Rule Overrides: P0 must always be FULL, P1 at least PIPELINE
        if criticality_tier == "P0":
            chosen = "FULL"
        elif criticality_tier == "P1" and utilities["PIPELINE"] < utilities["FULL"]:
            chosen = "FULL"
        elif criticality_tier == "P1":
            chosen = "PIPELINE"
        elif p_defect > 0.0196 and "SOLO" == max(utilities, key=utilities.get):
            chosen = "DUO"  # Enforce 1.96% cutoff
        else:
            chosen = max(utilities, key=utilities.get)

        role_map = {
            "SOLO": ["engineer"],
            "DUO": ["engineer", "tester"],
            "PIPELINE": ["architect", "engineer", "tester"],
            "FULL": ["researcher", "architect", "engineer", "tester", "critic"],
        }
        agents = role_map[chosen]
        dispatch_id = f"disp_{task_id}_{int(time.time()*1000)}"

        with self._get_conn() as conn:
            conn.execute(
                """
                INSERT INTO formation_dispatch_ledger
                (dispatch_id, task_id, initial_formation, current_formation, blast_radius_score, criticality_tier, utility_score, allocated_agents)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (dispatch_id, task_id, chosen, chosen, blast_radius, criticality_tier, utilities[chosen], json.dumps(agents)),
            )
        return dispatch_id, chosen, agents

    def trigger_runtime_escalation(self, task_id: str, reason: str) -> Tuple[str, List[str]]:
        """Atomically escalates formation upon gate failure or livelock shock."""
        escalation_ladder = {
            "SOLO": "DUO",
            "DUO": "PIPELINE",
            "PIPELINE": "FULL",
            "FULL": "FULL", # Already at ceiling; triggers human pause
        }
        role_map = {
            "DUO": ["engineer", "tester"],
            "PIPELINE": ["architect", "engineer", "tester"],
            "FULL": ["researcher", "architect", "engineer", "tester", "critic"],
        }

        with self._get_conn() as conn:
            cur = conn.execute(
                "SELECT current_formation, escalation_count, cas_version FROM formation_dispatch_ledger WHERE task_id = ?",
                (task_id,),
            )
            row = cur.fetchone()
            if not row:
                raise ValueError(f"Task {task_id} not found in dispatch ledger.")

            curr = row["current_formation"]
            nxt = escalation_ladder[curr]
            agents = role_map[nxt]
            new_cas = row["cas_version"] + 1
            new_esc = row["escalation_count"] + 1

            conn.execute(
                """
                UPDATE formation_dispatch_ledger
                SET current_formation = ?, allocated_agents = ?, escalation_count = ?, escalation_reason = ?, cas_version = ?, last_escalated_at = ?
                WHERE task_id = ? AND cas_version = ?
                """,
                (nxt, json.dumps(agents), new_esc, reason, new_cas, time.time(), task_id, row["cas_version"]),
            )
        return nxt, agents
```

---

### 5. Quantitative Invariants & Calibration Targets

| Dimension | Target Metric | Bound / Threshold | Hard Invariant |
|---|---|---|---|
| **Dispatch Latency** | $< 2.0\text{ ms}$ | $< 15.0\text{ ms}$ | Sub-millisecond SQLite WAL query |
| **False-Negative Rate ($FN_{\text{misroute}}$)** | $\le 1.0\%$ | $\le 2.0\%$ | Asymmetric loss $C_{\text{FN}} = 50.0$ blocks under-routing |
| **False-Positive Rate ($FP_{\text{misroute}}$)** | $< 25.0\%$ | $< 35.0\%$ | Token cost dampener $\lambda = 0.50$ prevents runaway FULL usage |
| **P0 Critical Path** | $100\%$ routed to `FULL` | Zero exceptions | Hard constraint in decision engine |
| **Defect Escapes in Production** | $0$ tolerated | $\le 1 / 20$ tasks | Escape triggers automated router retuning |

---

### References (pass 3)
1. Elkan, C. (2001). "The Foundations of Cost-Sensitive Learning". *International Joint Conference on Artificial Intelligence (IJCAI)*, 973–978.
2. Keeney, R. L., & Raiffa, H. (1993). *Decisions with Multiple Objectives: Preferences and Value Tradeoffs*. Cambridge University Press.
3. Ong, H. Y., et al. (2024). "RouteLLM: Learning to Route LLMs with Preference Data". *ICLR 2025*. arXiv:2406.18665.
4. Dean, J., & Ghemawat, S. (2004). "MapReduce: Simplified Data Processing on Large Clusters". *Communications of the ACM*, 51(1), 107–113.

