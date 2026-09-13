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
