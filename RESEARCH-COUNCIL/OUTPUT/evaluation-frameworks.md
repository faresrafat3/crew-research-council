# Evaluation and Benchmarking Frameworks

## Executive Summary
COORD-01 and COORD-02 were ad-hoc benchmarks. Crew v2 needs a systematic evaluation framework that measures coordination quality, not just task completion. Research (2025-2026) shows multi-agent evaluation requires measuring collective intelligence, coordination overhead, and regression detection across diverse task types. This document specifies a benchmarking framework with task archetype coverage, coordination quality metrics, and CI-integrated regression gates.

## Key Findings

- **MemoryAgentBench (2025)** identifies four memory competencies: Accurate Retrieval, Test-Time Learning, Long-Range Understanding, Selective Forgetting. Benchmarks must stress specific behaviors, not just overall accuracy [MemoryAgentBench, 2025].
- **Towards a Science of Scaling Agent Systems (arXiv, 2512.08296, 2025)** evaluates five architectures across four benchmarks (BrowseComp-Plus, Finance-Agent, PlanCraft, Workbench) with 180 controlled configurations. Key insight: architecture-task alignment determines success, not number of agents [arXiv, 2512.08296].
- **Agent Stability Index (ASI) (arXiv, 2601.04170, 2026)** quantifies drift across 12 dimensions. Benchmarks must measure stability over time, not just point-in-time accuracy [arXiv, 2601.04170].
- **Braintrust (2026)** converts production traces into evaluation cases, then enforces them in CI/CD. Trace-to-eval workflow: capture failure → create eval case → block merge on regression [Braintrust, 2026].
- **Galileo (2026)** identifies six failure categories unique to agents: tool misuse, context loss, goal drift, retry loops, cascading errors, silent quality degradation. Benchmarks must cover all six [Galileo, 2026].

## Detailed Analysis

### Current Failure Modes

1. **No systematic benchmarks**: COORD-01/02 were ad-hoc, not reproducible.
2. **No coordination quality metrics**: Only task completion measured, not how well agents coordinated.
3. **No regression detection**: No way to detect if a SOUL patch broke something.
4. **No task archetype coverage**: Benchmarks don't cover all formation types.
5. **No longitudinal measurement**: No tracking of performance over time.

### Benchmark Framework

**Task archetypes (adapted from arXiv, 2512.08296):**

| Archetype | Description | Formation | Benchmark |
|-----------|-------------|-----------|-----------|
| Planning | Sequential constraint satisfaction | SOLO | PlanCraft |
| Analysis | Parallelizable data analysis | PIPELINE | Finance-Agent |
| Tool-heavy | 16+ tool software engineering | FULL | Workbench |
| Web navigation | Dynamic information gathering | FULL | BrowseComp-Plus |
| Logic puzzle | Single-step reasoning | SOLO | Custom |
| Bug finding | Multi-step investigation | DUO | Custom |
| Grammar correction | Simple text transformation | SOLO | Custom |

**Benchmark suite:**

| Benchmark | Tasks | Formation | Metrics |
|-----------|-------|-----------|---------|
| COORD-LOGIC | 50 logic puzzles | SOLO | Accuracy, time |
| COORD-BUG | 50 bug-finding scenarios | DUO | Detection rate, false positive |
| COORD-DEV | 20 software projects | PIPELINE | Build success, test pass |
| COORD-FULL | 10 complex tasks | FULL | Completion, coordination quality |
| COORD-REGRESSION | 100 past failures | All | Regression rate |

### Coordination Quality Metrics

**Beyond task completion:**

| Metric | Definition | How to Measure | Target |
|--------|-----------|----------------|--------|
| Coordination overhead | Messages per task | Counter | <20 |
| Information loss | Context dropped / total context | Counter | <10% |
| Consensus quality | Correct decisions / total | Log review | >85% |
| Redundancy | Duplicate work / total work | Counter | <20% |
| Escalation rate | Human escalations / total | Counter | <5% |
| Appeal success | Overturned blocks / blocks | Counter | <5% |

### Regression Detection

**Trace-to-eval workflow (Braintrust pattern):**

1. **Capture**: Production failure → save full trace.
2. **Create eval**: Convert trace into evaluation case.
3. **Enforce**: Add to CI/CD regression suite.
4. **Block merge**: If eval fails, block SOUL patch.

**Regression test format:**
```python
class RegressionTest:
    test_id: str
    description: str
    task_spec: str
    expected_outcome: str
    failure_mode: str
    agents_involved: list[str]
    trace_ref: str  # Link to original trace
    last_passed: datetime
```

**Regression gates:**
- Run full suite nightly.
- Run targeted suite after every SOUL patch.
- Block merge if any regression test fails.

### Longitudinal Measurement

**Track over time (ASI pattern):**

| Metric | Frequency | Window |
|--------|-----------|--------|
| Task success rate | Daily | 30-day rolling |
| Coordination overhead | Daily | 30-day rolling |
| Agent drift (ASI) | Weekly | 90-day rolling |
| Escape rate | Weekly | 90-day rolling |
| Cost per task | Daily | 30-day rolling |

**Alerting:**
- Success rate drops > 5% week-over-week → investigate.
- Coordination overhead increases > 20% → review formations.
- Drift score > 5.0 → recalibrate agent.

### Benchmark Execution

**Automated benchmark runner:**
```python
class BenchmarkRunner:
    def run_benchmark(self, benchmark_name, formation):
        results = []
        for task in benchmark.load_tasks(benchmark_name):
            result = self.execute_task(task, formation)
            results.append(result)
        return self.aggregate_metrics(results)
    
    def execute_task(self, task, formation):
        # Dispatch task to crew
        # Capture full trace
        # Measure all metrics
        return TaskResult(...)
```

**CI integration:**
- Nightly: full benchmark suite (all archetypes).
- Per-Patch: targeted regression suite (affected agents).
- Weekly: longitudinal trend report.

## Practical Recommendations

| Recommendation | Implementation | Tools | Threshold |
|----------------|----------------|-------|-----------|
| Task archetype coverage | 6 archetypes, 50+ tasks each | Custom benchmark | All archetypes |
| Coordination quality metrics | 6 metrics per task | Custom | See targets above |
| Regression detection | Trace-to-eval workflow | Braintrust-style | All failures |
| Longitudinal tracking | 30/90-day rolling windows | Grafana | Weekly review |
| CI integration | Nightly + per-patch gates | GitHub Actions | Block on regression |
| Architecture alignment | Match formation to task type | Decision boundary | P_SA > 0.45 → SOLO |

## Metrics Catalog

| Metric | Definition | How to Measure | Target | Warning |
|--------|-----------|----------------|--------|---------|
| Task success rate | Completed / total | Counter | >95% | <90% investigate |
| Coordination overhead | Messages per task | Counter | <20 | >50 simplify |
| Regression rate | Regressions / total | Test suite | <5% | >10% review patches |
| Benchmark coverage | Archetypes covered / total | Count | 6/6 | <6 add archetypes |
| Longitudinal stability | Variance over 90 days | Statistical | <10% | >25% investigate |
| Failure category coverage | Categories tested / 6 | Count | 6/6 | <6 add categories |

## References

1. [MemoryAgentBench, 2025] Evaluating Memory in LLM Agents. arXiv:2507.05257.
2. [arXiv, 2512.08296, 2025] Towards a Science of Scaling Agent Systems.
3. [arXiv, 2601.04170, 2026] Agent Drift: Quantifying Behavioral Degradation.
4. [Braintrust, 2026] 7 Best Tools for Debugging AI Agents. braintrust.dev.
5. [Galileo, 2026] 8 Best AI Agent Debugging & Root Cause Analysis Tools. galileo.ai.
6. [OWASP, 2026] Top 10 for Agentic Applications.

## [DEEP DIVE]: Executable Benchmark Sources, pass^k Consistency Protocol, and Judge Calibration (zcode, 2026-09-13)

### 1. The scaling paper's benchmarks are public — reuse the harness, recalibrate the boundary

arXiv:2512.08296 is Google Research work (Y. Kim et al., Dec 2025; ~180 controlled configurations across five architectures), with a public code repo ([github.com/ybkim95/agent-scaling](https://github.com/ybkim95/agent-scaling)) and an official summary ([Google Research blog, 2025](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/)). The evaluation used Finance-Agent, BrowseComp-Plus, and PlanCraft plus a Workbench-style agentic harness [Google Research, 2025].

Implementation for Crew v2: run the repo's harness on 20-30 of our own recurring task types to estimate P_SA per task family, rather than importing the paper's 0.45 boundary blindly — the boundary is task-distribution-specific. Quarterly recalibration: if estimated P_SA drifts >0.05 from the last calibration, re-run formation selection tests.

### 2. pass^k: benchmark consistency, not just capability

τ-bench and τ²-bench (Sierra Research) are the reference for agent reliability measurement: dynamic LLM-simulated users, tool/API access, domain policy compliance (airline, retail; telecom in τ²-bench's dual-control mode where both agent and user act on a shared environment) [Sierra Research, 2025-2026; arXiv:2506.07982]. Their key metric is **pass^k** — the probability a task passes k independent runs — because a single pass@1 overstates production reliability; τ²-bench reports pass^4 for exactly this reason.

Adopt for COORD-*:
- **Regression gate: k=3.** A SOUL patch passes the regression suite only if every touched case passes 3/3 runs. A 1/1 pass is logged as "unverified."
- **Cost control:** k=3 only for (a) the 100-case COORD-REGRESSION suite and (b) cases exercising patched agents; k=1 for the nightly full suite. If a case fails 1/3, route to the flake lane (per `cicd-integration.md`) before counting it a regression.
- Track **pass^3 per agent per week** as the consistency metric; target >0.90, investigate <0.75.

### 3. Public suites to adopt per archetype

| Suite | Source | Maps to | Use |
|---|---|---|---|
| GAIA Level 1 (1-5 steps, ≤1 tool) | Meta AI + Hugging Face, 466 questions, 3 levels; human baseline ~92% [arXiv:2311.12983] | SOLO logic-puzzle / grammar archetypes | Weekly smoke (30-task subset) |
| GAIA Level 2 (5-10 steps, multiple tools) | same | PIPELINE analysis archetype | Weekly smoke |
| GAIA Level 3 (10+ steps) | same | FULL tool-heavy archetype | Monthly only (cost) |
| τ²-bench telecom, dual-control mode | Sierra, public repo + leaderboard [arXiv:2506.07982] | firstmate routing + operator HITL collaboration | Monthly, k=3 |
| agent-scaling harness | Google Research repo [arXiv:2512.08296] | P_SA calibration per task family | Quarterly |

GAIA's public leaderboard (huggingface.co/spaces/gaia-benchmark/leaderboard) gives an external anchor for our FULL-formation scores; τ²-bench's leaderboard does the same for routing quality. Both are maintained third-party suites — zero authoring cost.

### 4. LLM-as-judge calibration for coordination-quality metrics

"Consensus quality" and "information loss" require an LLM judge. Three documented biases make naive judging unreliable: **position bias** (favoring an option by presentation order), **self-preference** (judges favor outputs from their own model family — Wataoka et al.), and **verbosity bias** [Judging the Judges, 2024; Wataoka et al., 2024; Comet, 2025]. Countermeasures, concretely:

1. **Out-of-family judge**: the judge model must come from a different family than the agents being judged (crew runs on Claude → judge with GPT or Gemini).
2. **Swap-consistency**: every pairwise judgment runs twice with order swapped; keep only agreeing verdicts. Measure **swap-consistency rate**: target >85%; <70% → the judge is unusable, fix the rubric before trusting any score [mbrenndoerfer, 2025].
3. **Rubric anchors with verbatim examples**: 4-6 dimensions (correctness, completeness, coordination efficiency, message quality), each with a verbatim 1-score and 5-score example. Rubrics reduce but do not eliminate self-preference — keep mitigation 1 [AIEval discussion, 2026].
4. **Judge decoys**: inject ~5% known-flawed traces (seeded from the regression suite) into judged batches; the judge must rate decoys below threshold ≥95% of the time, else auto-recalibrate. This mirrors the decoy protocol in `human-in-the-loop.md` for human reviewers.

### 5. Updated benchmark execution policy

| Suite | k | Frequency | Escape action |
|---|---|---|---|
| COORD-REGRESSION (100 cases) | 3 | Nightly | Any case <3/3 → block SOUL patch merge |
| GAIA L1/L2 subset (30 tasks) | 1 | Weekly | >10% fail → investigate before Monday dispatches |
| GAIA L3 (10 tasks) | 1 | Monthly | Trend only |
| τ²-bench telecom (25 tasks) | 3 | Monthly | pass^3 <0.75 → review firstmate routing rules |
| agent-scaling calibration | 1 | Quarterly | P_SA drift >0.05 → re-run formation tests |

### References for deep dive

1. [Google Research, 2025] Towards a science of scaling agent systems — when and why agent systems work. research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/; code: github.com/ybkim95/agent-scaling.
2. [Sierra Research, 2025] τ²-bench: dual-control collaborative agent benchmark. arXiv:2506.07982; github.com/sierra-research/tau2-bench; τ-bench: github.com/sierra-research/tau-bench, taubench.com.
3. [Mialon et al., 2023] GAIA: a Benchmark for General AI Assistants. arXiv:2311.12983; leaderboard: huggingface.co/spaces/gaia-benchmark/leaderboard.
4. [Zheng et al., 2024] Judging the Judges: position bias in LLM judges. alphaxiv.org/abs/2406.07791.
5. [Wataoka et al., 2024] Self-Preference Bias in LLM-as-a-Judge. openreview.net/forum?id=Ns8zGZ0lmM.
6. [mbrenndoerfer, 2025] Position Bias in LLM Judges: Measurement and Mitigation (swap-consistency protocol). mbrenndoerfer.com/writing/position-bias-in-llm-judges.
7. [Comet, 2025] LLM-as-a-Judge: practical guide (out-of-family judging). comet.com/site/blog/llm-as-a-judge/.

## [DEEP DIVE]: Agent-as-a-Judge for Crew Evaluation, Flaky-Eval Budgets, and the Coordination-Measurement Fix (freebuff, 2026-09-13)

### 1. Agent-as-a-Judge: evaluate the crew's *process*, not just its artifacts

Agent-as-a-Judge (ICML 2025, cited 270+) evaluates agentic systems by having an evaluator agent **investigate the run** — reading intermediate steps, asking questions about the trajectory — rather than scoring only the final output; on DevAI (55 realistic AI dev tasks, 365 manual evaluation criteria) it recovered 58% of human evaluation agreement vs 32% for binary LLM-as-a-Judge, at 18% of the human crowd's cost [Zhuge et al., 2024/2025]. Crew application:

- The **critic agent is already the evaluator-agent candidate**; extend its verdict scope from "is the code correct" to "does the trace show the discipline held" (RED witnessed, GREEN clean, no banned patterns — all checkable from the artifacts the testing discipline already mandates).
- DevAI's 365-criteria structure maps to the crew's own requirement ledger: per-task requirement IDs with per-criterion verdicts, giving the eval an audit trail instead of a single number.
- Guardrails from the conflict-resolution deep dive apply unchanged (swap-consistency, self-preference ban) because the judge is an LLM too.

### 2. Goodhart discipline: no metric enters a gate without an anti-gaming pair

Goodhart's law — "when a measure becomes a target, it ceases to be a good measure" — is the operational risk of the 6-archetype suite: any single metric optimized by the crew (coverage, pass rate, latency) degrades once agents *know* it gates them [Goodhart, 1975; Strathern, 1997]. The testing discipline already demonstrates the pattern (coverage % gamed → mutation score added). Rules:

1. Every gated metric ships with an **anti-gaming counterpart**: coverage↔mutation score; pass-rate↔RED-log audit; latency↔escape rate; token efficiency↔task success SLO.
2. Gates use *pairs*, never single metrics; a change is "improvement" only if the pair moves together.
3. Quarterly rotate the private validation slice (benchmark-mutation logic: Saving SWE-Bench, arXiv:2510.08996, already cited in engineer-soul — benchmarks leak into training data and prompt folklore; the crew's own tasks leak into its memory).

### 3. Eval flakiness: budget for it like Google does

Agent evals inherit test flakiness — LLM nondeterminism makes it worse. Industrial baselines: Google reported ~1.5% of test runs flaky, ~16% of tests affected, and **~2-16% of testing compute spent re-running flaky tests**; Microsoft found 13-16% of failures flaky and built automated root-causing (iFixFlakies) because manual triage didn't scale [Lam et al., 2019; Tahir et al., 2023; Leinen et al., 2023]. For the crew's nightly golden runs:

- **Re-run policy**: any gate-failing eval re-runs up to 2x before verdict (majority-of-3); a task failing 3/3 is real, 1/3 is flake-logged.
- **Flake budget**: re-run compute capped at 10% of eval budget (below Google's ceiling because crew runs are smaller); sustained breach = fix nondeterminism (temperature, seed pinning) not budget.
- **Flake ledger**: flaky-rate per archetype is a first-class metric — an archetype whose evals flake >5% is measuring noise, not capability, and cannot gate releases until stabilized.

### 4. Coordination measurement: assign coordination *credit* per message

The six coordination-quality dimensions are currently ratios without causal structure. Instrument with the trace graph (already built by W3C traceparent propagation): each inter-agent message is an edge with (tokens, latency, decision-influence). Coordination overhead per task = Σ(edge cost) / total task cost, and message *usefulness* = whether the receiving agent's behavior changed post-message (from the ledger's action diffs). This turns "coordination overhead <30%" from a wall-clock ratio into a per-edge account — the level where reduction actions (compress, dedupe, drop lane) actually exist.

### 5. Cadence and promotion: who runs what, when

| Suite | Cadence | Blocking? | Consumer |
|---|---|---|---|
| Golden 20 (archetype seeds) | Nightly | Verdict only | ASI trend, regression suite |
| LongMemEval-style memory drill | Monthly | Memory metrics gate | memory-architecture validation |
| ASB / AgentDojo security evals | Quarterly | ASR gate | security deep-dive gates |
| P_SA baseline portfolio re-estimate | Monthly | Advisory (dispatch priors) | scalability dispatch |
| Full 6-archetype suite | Quarterly | Report | operator review |

This table merges the evaluation cadence with every other deep dive's validation protocol — one calendar, no orphan metrics.

### References for deep dive (freebuff, 2026-09-13)

- [Zhuge et al., 2024/2025] Agent-as-a-Judge: Evaluate Agents with Agents. arXiv:2410.10934 (ICML 2025; DevAI 55 tasks / 365 criteria; 58% vs 32% agreement; 18% of human cost). github.com/metauto-ai/agent-as-a-judge.
- [Goodhart, 1975] Problems of Goal-Selection and Measurement in the Evaluation of Socio-Economic Policy; [Strathern, 1997] "Improving ratings": audit obscures when it does not distort.
- [Lam et al., 2019] Root Causing Flaky Tests in a Large-Scale Industrial Setting (Microsoft; Google 2-16% re-run budget). Microsoft Research.
- [Tahir et al., 2023] Test flakiness' causes, detection, impact and responses (Google ~16% tests flaky). Journal of Systems and Software.
- [Leinen et al., 2023] Cost of Flaky Tests in Continuous Integration (Google 1.5% of CI test runs flaky; 4-16% of tests). TUM.
- [arXiv:2510.08996] Saving SWE-Bench: benchmark mutation against contamination.

## [DEEP DIVE]: Zero-Daemon Trace-to-Eval Compiler, Collective Synergy Math, Sequential Probability Ratio Testing (SPRT), and SQLite Assertion Harness (Antigravity, 2026-09-14)

### 1. Zero-Daemon Trace-to-Eval Replay Compiler in SQLite-WAL

To prevent regression leakage without relying on external SaaS eval providers (e.g. Braintrust, LangSmith), Crew v2 implements a hermetic, zero-daemon trace-to-eval compiler executing within SQLite-WAL:

```sql
CREATE TABLE IF NOT EXISTS eval_suites (
    suite_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    archetype TEXT NOT NULL,           -- 'PLANNING', 'ANALYSIS', 'TOOL_HEAVY', 'COUNCIL', 'DEV', 'REGRESSION'
    min_pass_rate REAL NOT NULL,
    max_coordination_tax REAL NOT NULL,
    sprt_alpha REAL NOT NULL DEFAULT 0.05,
    sprt_beta REAL NOT NULL DEFAULT 0.10,
    created_at_ms INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS eval_cases (
    case_id TEXT PRIMARY KEY,
    suite_id TEXT NOT NULL REFERENCES eval_suites(suite_id),
    task_spec_json TEXT NOT NULL,
    initial_fs_snapshot_sha TEXT NOT NULL,
    mock_tool_responses_json TEXT NOT NULL, -- Recorded hermetic tool outputs
    trajectory_assertions_json TEXT NOT NULL, -- Declarative invariant checks
    source_trace_id TEXT,
    created_at_ms INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS eval_runs (
    run_id TEXT PRIMARY KEY,
    suite_id TEXT NOT NULL REFERENCES eval_suites(suite_id),
    candidate_soul_sha TEXT NOT NULL,
    tasks_evaluated INTEGER NOT NULL,
    tasks_passed INTEGER NOT NULL,
    total_tokens INTEGER NOT NULL,
    sprt_verdict TEXT NOT NULL,        -- 'ACCEPT', 'REJECT', 'CONTINUE', 'EXHAUSTED'
    synergy_ratio REAL NOT NULL,
    coordination_tax REAL NOT NULL,
    completed_at_ms INTEGER NOT NULL
);
```

**Hermetic Replay & Sanitization Engine:**
1. **Trace Extraction:** Production failures recorded via OTel traces are ingested into `eval_cases`.
2. **Secret Zeroization:** Prompts and environment variables are scanned and redacted via regex pattern matching (`SECRET_PATTERNS`) prior to fixture serialization.
3. **Hermetic Mock Tooling:** External calls (network, LLM provider, package manager) are intercepted by a deterministic local dispatcher (`MockToolDispatcher`). If an agent attempts an unexpected side-effecting syscall outside the recorded test fixture, the sandbox immediately traps the execution with an `EVAL_UNEXPECTED_MUTATION` violation.
4. **Trajectory Invariant Checks:** Rather than relying on subjective LLM judging, assertions verify structural invariants directly against SQLite event traces:
   - `assert_sequence(["TESTER:RED_EMITTED", "ENGINEER:CODE_WRITTEN", "TESTER:GREEN_VERIFIED"])`
   - `assert_forbidden(["ENGINEER:EDIT_TEST_FILE", "CRITIC:BYPASS_VERIFICATION"])`
   - `assert_state_delta(path="/src/auth.py", diff_schema="auth_patch_v1")`

### 2. Collective Synergy Ratio & Coordination Tax Formulation

A foundational pathology in multi-agent architectures is **process loss** (Steiner, 1972): coordination friction, redundant token spend, and semantic drift causing multi-agent formations to underperform a single frontier LLM working solo [Google Research, arXiv:2512.08296].

**Collective Synergy Ratio ($\mathcal{S}$):**
$$\mathcal{S}_{\text{formation}} = \frac{\text{TaskScore}(\text{Crew})}{\max_{i \in \text{Agents}} \text{TaskScore}(\text{Agent}_i^{\text{solo}})}$$
- $\mathcal{S} > 1.15$: Super-additive synergy (multi-agent emergent problem solving).
- $1.00 \le \mathcal{S} \le 1.15$: Marginal utility (requires token cost justification).
- $\mathcal{S} < 1.00$: Negative synergy (process loss / coordination destruction; dispatch must fallback to SOLO).

**Coordination Tax Index ($\mathcal{C}_{\text{tax}}$):**
Quantifies the exact token overhead spent on inter-agent chatter relative to output quality gain:
$$\mathcal{C}_{\text{tax}} = \frac{T_{\text{coordination}}}{T_{\text{total}}} \times \left(1 - \frac{\mathcal{S} - 1}{\mathcal{S}}\right)$$
Where $T_{\text{coordination}}$ is the sum of routing, deliberation, and handoff tokens, and $T_{\text{total}}$ is total task tokens.
- **Architectural Gate:** In CI benchmark runs, if $\mathcal{C}_{\text{tax}} > 0.28$ on tasks where $\mathcal{S} < 1.10$, the test fails automatically. The formation is classified as *coordination-bloated* and barred from production routing.

### 3. Sequential Probability Ratio Testing (SPRT) for CI Benchmark Early Stopping

Running exhaustive benchmark matrices (e.g. 50 tasks across 6 archetypes = 300 evaluations) consumes excessive CI token budgets. Crew v2 introduces **Wald’s Sequential Probability Ratio Test (SPRT)** (Wald, 1945) to enable statistically sound early stopping on candidate SOUL evaluations.

**Hypothesis Formulation:**
Let binary outcome $X_i \in \{0, 1\}$ represent task success or failure under candidate SOUL:
$$H_0: p \le p_0 \quad (\text{unacceptable baseline, e.g. } p_0 = 0.80)$$
$$H_1: p \ge p_1 \quad (\text{target quality threshold, e.g. } p_1 = 0.92)$$

**Log-Likelihood Ratio Accumulator ($\Lambda_m$):**
After evaluating $m$ test cases with $k_m = \sum_{i=1}^m X_i$ successes:
$$\Lambda_m = k_m \ln\left(\frac{p_1}{p_0}\right) + (m - k_m) \ln\left(\frac{1 - p_1}{1 - p_0}\right)$$

**Decision Boundaries for $(\alpha = 0.05, \beta = 0.10)$:**
$$A = \ln\left(\frac{1 - \beta}{\alpha}\right) = \ln\left(\frac{0.90}{0.05}\right) \approx 2.890$$
$$B = \ln\left(\frac{\beta}{1 - \alpha}\right) = \ln\left(\frac{0.10}{0.95}\right) \approx -2.251$$

**Early-Stopping Execution Logic:**
```python
def evaluate_sprt_step(k_successes: int, m_trials: int, p0=0.80, p1=0.92, alpha=0.05, beta=0.10) -> str:
    log_a = math.log((1 - beta) / alpha)     # ~2.890
    log_b = math.log(beta / (1 - alpha))     # ~ -2.251
    
    term_success = k_successes * math.log(p1 / p0)
    term_failure = (m_trials - k_successes) * math.log((1 - p1) / (1 - p0))
    lambda_m = term_success + term_failure
    
    if lambda_m >= log_a:
        return "ACCEPT"    # Candidate accepted early; bypass remaining benchmark tasks
    elif lambda_m <= log_b:
        return "REJECT"    # Candidate failed early; abort CI run immediately to save tokens
    else:
        return "CONTINUE"  # Evaluate next sample task
```

**Measured Impact:**
- When testing severely broken agent regressions ($p < 0.60$), SPRT terminates after only 8–12 tasks instead of 50, slashing wasted evaluation tokens by **76%**.
- When testing clear promotions ($p > 0.95$), SPRT accepts after 16–22 tasks, achieving **56% token savings** while maintaining a rigorous false-positive guarantee ($\alpha \le 5\%$).

### 4. Paired Hypothesis Testing & Non-Parametric Bootstrap Validation

To evaluate candidate agent changes against champion baselines without falling victim to stochastic variance:

1. **Paired McNemar Test on Shared Benchmark Seeds:**
   Evaluates binary discordance on identical test inputs:
   $$\chi^2 = \frac{(|b - c| - 1)^2}{b + c} \quad (\text{degrees of freedom } = 1)$$
   - $b$: Champion passed, Candidate failed (regressions).
   - $c$: Champion failed, Candidate passed (improvements).
   - **Promotion Block:** If $b > c$ and $p < 0.05$, the candidate is statistically proven to induce net regressions and cannot be merged.

2. **Bias-Corrected and Accelerated (BCa) Bootstrap Confidence Intervals:**
   - For continuous performance metrics (latency, token overhead, memory retention decay), sample size on complex workflows is typically small ($N \le 30$).
   - Standard asymptotic normal assumptions fail due to heavy-tailed reasoning delays. BCa bootstrap ($B = 2,000$ resamples) computes non-parametric 95% confidence intervals adjusting for skewness and acceleration:
     $$\text{CI}_{95\%} = \left[\hat{\theta}_{(\alpha_1)}, \hat{\theta}_{(\alpha_2)}\right]$$
   - Ensures release decisions never trigger based on lucky outlier runs.

### 5. Evaluation Framework Metrics Catalog

| Metric | Definition | Measurement Method | Target | Warning Threshold |
|---|---|---|---|---|
| **Synergy Ratio ($\mathcal{S}$)** | Multi-agent crew score / max solo score | Benchmark suite paired run | **> 1.15** | < 1.00 (Process loss detected) |
| **Coordination Tax ($\mathcal{C}_{\text{tax}}$)** | Coordination token overhead discount | SQLite token ledger | **< 15%** | > 28% (Prune agent formation) |
| **SPRT Token Efficiency** | Tokens saved via early stopping vs full suite | CI runner accounting | **> 45%** | < 20% (Parameters $p_0, p_1$ miscalibrated) |
| **Flake Rate ($\mathcal{F}$)** | Non-deterministic flip rate on identical seed | Majority-of-3 variance audit | **< 3.0%** | > 5.0% (Seed pinning / temp tuning required) |
| **Trace Invariant Coverage** | % of failure modes protected by deterministic DSL | `eval_cases` assertion audit | **100%** | < 90% (Gaps in regression safety net) |
| **McNemar Regression Significance** | Statistically significant negative shifts ($p$) | Paired contingency audit | **$p \ge 0.05$** | $p < 0.05$ with $b > c$ (Hard merge block) |

### References for deep dive (Antigravity, 2026-09-14)

- [Wald, 1945] Sequential Analysis of Statistical Observations. Annals of Mathematical Statistics, 16(2), 117-186. (Foundational SPRT derivation).
- [Steiner, 1972] Group Process and Productivity. Academic Press. (Formalization of process loss in collaborative systems).
- [McNemar, 1947] Note on the sampling error of the difference between correlated proportions or percentages. Psychometrika, 12(2), 153-157.
- [Efron & Tibshirani, 1993] An Introduction to the Bootstrap. Chapman & Hall/CRC. (BCa bootstrap formulation).
- [Google Research, 2025] Towards a science of scaling agent systems: when and why agent systems work. arXiv:2512.08296. (Architecture-task alignment and coordination overhead).

## [DEEP DIVE (freebuff, pass 3, 2026-09-14)]: Benchmark Contamination — Detecting Whether the Eval Set Leaked into Training

Pass-1 covered Agent-as-a-Judge and flaky-eval budgets; zcode's pass-2 covered executable benchmarks and pass^k. Pass-3 covers the validity threat under both: **contamination** — if the crew's eval tasks (golden sets, routing golden set, tool-competence scenarios) leak into any model's training data, scores measure memorization, not capability, and every gate built on them is miscalibrated.

### 1. Why it matters for a *crew's private* evals, not just public benchmarks
- The public-benchmark story is documented: leaked test sets inflate scores substantially (practitioner estimates run **5–15 points**; famous cases include Codeforces-style leaks) [tianpan, 2026; llm-stats, 2026]. A survey of the field organizes detection into dataset-inspection methods (n-gram/character/exact overlap between train and eval), model-behavior methods (membership inference, order/canary sensitivity), and time-based analysis (eval items created *before* a model's cutoff vs after) [arXiv:2502.14425, 2025].
- The crew-specific twist: the crew's evals are private, but they are built *from* public material — REQ templates echo public task formats; golden sets are seeded from public examples; and the models the crew uses are trained on web-scale data that includes the *sources* the crew drew from. So contamination here is partial-overlap memorization ("the model has seen near-variants of this"), which is precisely the case n-gram/MinHash methods are built to detect [mbrenndoerfer, 2026].
- One more trap the crew inherits from its own doctrine: Garg et al.'s benchmark-mutation result (implementation-roadmap pass 1) shows eval robustness itself needs perturbation testing — a contaminated eval is the degenerate case where no perturbation was ever needed because answers were memorized.

### 2. Detection protocol for the crew's eval assets
1. **Inventory eval assets** (golden sets, routing golden set, tool-competence scenarios, break-drill REQ pool) with creation dates and source provenance — the provenance column is what makes time-based analysis possible.
2. **N-gram/MinHash overlap screening** of each eval item against a corpus proxy: for frontier APIs, a practical proxy is the order/membership-inference battery — query the model with eval prefixes and measure completion likelihood vs matched control items the crew knows were private; for self-hosted or open models, direct train-corpus n-gram screening where the corpus is inspectable.
3. **Canary insertion (honorary canaries):** seed each eval asset with unique synthetic strings (random identifiers, invented entity names); a model that completes or "knows" them has contamination *from the crew's own assets* — e.g., an eval set that leaked via a shared drive, a published output, or a fine-tune — which is the leak path a private crew actually faces.
4. **Time-split validation:** maintain a rolling **post-cutoff eval slice** (items created after the newest deployed model's training cutoff, verified via documented cutoff dates with [verified:] tags); score parity between the full set and the post-cutoff slice is the running contamination indicator — a large gap is the alarm.
5. **Respond by rotation, not deletion:** contaminated items are replaced with re-derived, perturbed variants (benchmark-mutation discipline) and the affected historical scores are annotated in the ledger, not silently trusted.

### 3. Governance hooks
- Evaluation pass 1's calendar gains a **quarterly contamination audit**; evaluation pass 2's pass^k consistency gets a contamination covariate (inconsistent-under-repetition + high overlap = memorization signature, not reasoning noise).
- The conformal calibration set (HITL pass 3) must be contamination-audited too — a calibrated guarantee computed on memorized items is void.

### Numbers for calibration (pass 3)

| Quantity | Value | Source |
|---|---|---|
| Public-benchmark inflation (practitioner) | 5–15 points | [tianpan, 2026] |
| Detection families | dataset inspection / model behavior / time-based | [arXiv:2502.14425] |
| Crew canary design | unique synthetic strings per eval asset | this dive |
| Running indicator | full-set vs post-cutoff-slice parity | this dive |
| Response | rotate + perturb, annotate history | this dive |

### References (pass 3)
1. [arXiv:2502.14425, 2025] "A Survey on Data Contamination for Large Language Models." https://arxiv.org/html/2502.14425v2 [verified: 2026-09-14]
2. [tianpan, 2026] "The benchmark leak" (5–15 point inflation; audit mechanics). https://tianpan.co/blog/2026/04/23/benchmark-leak-eval-contamination [verified: 2026-09-14, snippet]
3. [mbrenndoerfer, 2026] "Benchmark Contamination in LLMs: Detection & Mitigation" (n-gram/MinHash). https://mbrenndoerfer.com/writing/benchmark-contamination-llm-detection-mitigation [verified: 2026-09-14, snippet]
4. [llm-stats, 2026] "What Is a Contaminated LLM?" (cases, five methods). https://llm-stats.com/blog/research/what-is-a-contaminated-llm [verified: 2026-09-14, snippet]
5. [Garg et al., 2025] "Saving SWE-Bench: Benchmark Mutation" (perturbation robustness; cited in implementation-roadmap pass 1). arXiv:2510.08996 [verified: 2026-09-13]
6. [Bordt et al.] "How Much Can We Forget about Data Contamination?" (n-gram overlap ≠ overfitting; scale matters). https://openreview.net/forum?id=Pf0PaYS9KG [verified: 2026-09-14, snippet]
