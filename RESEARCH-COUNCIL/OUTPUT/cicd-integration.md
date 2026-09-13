# CI/CD Integration for AI Agent Testing

## Executive Summary
Every engineer commit triggers unit + targeted mutation with JUnit coverage JSON mutation reports artifacts; tester verdict gates merges large tests async nightly. No native Actions dashboard so upload-artifact + reporters workaround [GitHub Community 2025], CTRF one-command flaky summaries [CTRF 2026], history flips [TestDino 2026], exit-2 mutation gate [Mutagen 2026]. Golden three-layer eval + break drills catch regressions.

In this model, the commit pipeline is blocking and fast (<10 min): `pytest -q` small-first, coverage JSON, targeted `mutmut` on touched lines, oracle/tautology/mock lints, and flake history check. Large, slow, and nondeterministic work — full E2E (capped journeys), full mutation, live contracts, golden eval, break drills — runs async on nightly schedule. Tester verdict (PROMOTE/HOLD/ROLLBACK) gates merges, with quarantine as advisory PR comment and 20-green re-promotion. Artifacts (`junit.xml`, `cov.json`, `mutation-report.json`, `flake-history.json`) provide the audit trail that a native dashboard would otherwise supply.

## Key Findings

1. **No native GitHub Actions test dashboard — use upload-artifact + reporters workaround:** Actions has no first-class test-results UI, so persist `junit.xml` via `actions/upload-artifact@v4` and render on PRs with `dorny/test-reporter@v1`, Allure reports published to GitHub Pages [GitHub Community 2025].
2. **CTRF gives one-command flaky summaries:** Common Test Report Format (CTRF) JSON normalizes JUnit/XUnit across runners and produces single-command flaky-test summaries for Actions annotations and PR comments [CTRF 2026].
3. **Robust flake detection requires history, not single retries:** Track per-test pass/fail history (20-run window, `flake-history.json` + ledger DB) and only quarantine on sustained flip-rate; single-run retry masks real regressions [TestDino 2026].
4. **CI flip detection spans Actions, CircleCI, and Jenkins:** Flip-rate detectors that diff consecutive runs work identically across providers; the pattern is portable — store history outside the runner and compute flip-rate on every commit [Panto 2026].
5. **Same-commit flips signal environment drift, not code bugs:** When the same commit flips between green/red without code change, root-cause is environment (image version, dependency float, time/clock, external API); pin images, lock files, `vcrpy`/`testcontainers`/`freezegun` [Tenki 2026].
6. **Mutagen exit-2 mutation gate with before/after reports:** Targeted mutation on PR-touched lines only; `mutmut run` + `mutation-check --threshold=70` exits 2 on gate failure, emitting before/after `mutation-report.json` for PR annotation [Mutagen 2026].
7. **Tiered scheduling: small / medium / large:** Small (unit, <2 min) blocks every commit; medium (integration + property, <15 min) blocks PR merge; large (E2E, full mutation, contracts) runs async nightly — cost/latency optimal [SQRBOK 2025].
8. **Hermetic test environments are non-negotiable for agents:** Ephemeral containers, synthetic data only, no production secrets, recorded HTTP — otherwise agent-nondeterminism compounds with environment-nondeterminism [KnowMBA 2025].
9. **PROMOTE / HOLD / ROLLBACK verdicts from 38 runs across 20 releases:** Tester-agent verdict object with evidence links gates merge/deploy; field study of 38 pipeline runs over 20 releases shows verdict-gating catches escape-defects that coverage-alone misses [ArXiv 2026].
10. **Probabilistic LLM outputs need schema + embedding + judge, not point equality:** Golden eval is three-layer — JSON-schema validity, latency budget, embedding cosine similarity, plus LLM-judge rubric score — never exact string match [ArizenAI 2025].

## Detailed Analysis

### 1. Blocking Commit Pipeline (fast-gate, <10 min)
- **Runner:** `pytest -q` small-first: `tests/unit` then `tests/integration`, `-v --tb=short --strict-markers`, parallelized with `pytest-xdist --numprocesses=auto --dist=loadscope`, Hypothesis `ci` profile.
- **Coverage JSON:** `--cov=src --cov-report=json:artifacts/cov.json --cov-branch --cov-fail-under=80` plus `term-missing` for PR annotation.
- **Targeted mutation:** `mutmut run --paths-to-mutate=src --mutate-only-covered-lines=true` scoped to PR-touched lines; threshold 70% on PR gate, 80% on nightly full gate.
- **Oracle / tautology / mock lints:** `crew.testing.lints --check-tautologies --check-oracle-violations --check-mock-ratio` fails builds with tautological asserts (`assert True`, `x == x`), oracle violations, or mock-ratio excess.
- **Flake 20-run history:** `crew.testing.flake-check --history=artifacts/flake-history.json --max-rate=0.02 --db=ledger.db` blocks on flip-rate >2% over trailing 20 runs.

### 2. Nightly Async Pipeline (large, nondeterministic)
- **Large E2E:** `pytest tests/e2e -m e2e --max-journeys=10`, capped to bound time/cost; full journeys replay nightly or on `workflow_dispatch`.
- **Full mutation:** whole-`src` `mutmut run`, threshold 80%, 60-min timeout, 90-day retention for quarterly calibration.
- **Live contracts:** recorded-by-default (`vcrpy`); live-contract subset runs nightly against sandbox with rotated test-only secrets.
- **Golden eval (three-layer):** `crew.testing.golden-eval --golden-set=tests/golden/golden_set.json` checks (a) schema validity, (b) latency budget, (c) embedding cosine + LLM-judge rubric — catches semantic regressions point-equality misses.
- **Break drills:** `crew.testing.break-drills --reqs=requirements/reqs.json` breaks each REQ and asserts the suite reddens; silent green = missing coverage, filed as gap ticket.

### 3. Quarantine and Re-promotion Policy
- Quarantine is **advisory, never silent skip**: flaky test opens PR comment with history link, `quarantine` label, and owner assignment.
- Quarantined tests move to nightly-only shard; commit gate no longer blocks on them.
- **20-green re-promotion:** 20 consecutive nightly greens auto-re-promotes to blocking gate; any red resets the counter.
- Same-commit flip without code diff triggers env-drift investigation (image pin, lockfile diff, clock mock), not code revert [Tenki 2026].

### 4. Artifacts Contract
- `junit.xml` — JUnit for `dorny/test-reporter` PR rendering and CTRF conversion; 30-day retention.
- `cov.json` — machine-readable coverage for trend analysis and `--cov-fail-under` enforcement; 30-day retention.
- `mutation-report.json` — before/after targeted (PR) and full (nightly) reports for exit-2 gate audit; 30/90-day retention.
- `flake-history.json` — 20-run trailing history + `ledger.db` for flip-rate computation and quarantine decisions; 90-day retention.
- Additional: `property-results.xml` (14d), `e2e-results.xml` (14d), `golden-results.json` (90d), `drill-results.json` (90d).

## Practical Implementation

| Concern | Commit (blocking) | Nightly (async) | Tooling |
|---------|-------------------|-----------------|---------|
| Unit + integration | `pytest tests/unit tests/integration -q` small-first, xdist | replay on failure | `pytest`, `pytest-xdist`, `dorny/test-reporter` |
| Coverage | `cov.json`, `--cov-fail-under=80`, PR comment | trend dashboard | `pytest-cov`, `upload-artifact@v4` |
| Mutation | targeted touched-lines, threshold 70, exit 2 | full suite, threshold 80 | `mutmut`, `mutation-check` |
| Flakiness | `flake-check --max-rate=0.02`, history gate | 20-green re-promotion, quarantine shard | CTRF, `flake-history.json`, ledger DB |
| Reporting (no native dashboard) | `upload-artifact` + PR reporter | Allure to Pages, CTRF summary | `upload-artifact@v4`, `dorny/test-reporter`, Allure, CTRF |
| Golden eval | schema check only (fast) | full 3-layer: schema + latency + embedding cosine + judge rubric | `golden-eval`, embedding model, judge LLM |
| Break drills | off | per-REQ break + assert-redden | `break-drills` |
| Secrets / hermetic | no secrets in fast gate | test-only secrets via GitHub Secrets, `vcrpy`/`testcontainers`/`freezegun` | GitHub Secrets, branch protection |
| Verdict | tester HOLD blocks merge | PROMOTE/HOLD/ROLLBACK with evidence links | tester agent |

## Metrics

| Metric | Target | Source |
|--------|--------|--------|
| Fast-gate p95 latency | <10 min | `fast-gate` job duration, Actions insights |
| Commit-gate flip-rate | <2% over trailing 20 runs | `flake-history.json` + ledger DB |
| PR mutation score (targeted) | ≥70% | `mutation-report.json` (exit 2 if below) |
| Nightly mutation score (full) | ≥80% | `full-mutation-report.json` |
| Coverage (branch) | ≥80%, no drop >1% per PR | `cov.json` |
| E2E journeys nightly | ≤10, 100% recorded | `e2e-results.xml` |
| Golden eval pass | 100% schema, ≥0.85 cosine, judge ≥pass, latency within budget | `golden-results.json` |
| Break-drill redden rate | 100% (every broken REQ must redden) | `drill-results.json` |
| Quarantine re-promotion | 20 consecutive greens | nightly shard history |
| Verdict-gated releases | PROMOTE required; HOLD blocks merge | 38 runs / 20 releases field data [ArXiv 2026] |

## References

1. [GitHub Community 2025] Native Test Results Dashboard — no first-class dashboard; `upload-artifact` + `dorny/test-reporter` / Allure-to-Pages workaround.
2. [CTRF 2026] Common Test Report Format on GitHub Actions — JSON report format, one-command flaky summaries and annotations.
3. [TestDino 2026] Flaky Test Detection — history-based flip tracking vs single-retry masking.
4. [Panto 2026] CI Flip Detection across Actions, CircleCI, Jenkins — portable flip-rate detector pattern.
5. [Tenki 2026] Flaky Test Quarantine — same-commit flips as environment drift signal; pin/lock/record.
6. [Mutagen 2026] Mutation-gated LLM Test Generation — targeted mutation gate, exit-2 on threshold breach, before/after reports.
7. [SQRBOK 2025] Tiered Test Scheduling — small/medium/large split for cost/latency-optimal CI.
8. [KnowMBA 2025] Hermetic Test Environments — ephemeral, synthetic-data-only, no production secrets.
9. [ArXiv 2026] PROMOTE/HOLD/ROLLBACK Verdict Gating — 38 pipeline runs across 20 releases; verdict + evidence links.
10. [ArizenAI 2025] Evaluating Probabilistic LLM Outputs — schema + latency + embedding cosine + LLM-judge rubric, not point equality.

---

## [DEEP DIVE]: Exact GitHub Actions Workflow, Parallelization, Artifact Retention, and Secrets

### 1. Exact GitHub Actions Workflow Configuration

**File: `.github/workflows/test-gate.yml`**

```yaml
name: Test Gate (Commit)

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

# Cancel in-progress runs for the same branch
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

permissions:
  contents: read
  pull-requests: write  # for coverage comment
  actions: read

jobs:
  # ── Job 1: Fast Gate (blocking) ──────────────────────────────────
  fast-gate:
    runs-on: ubuntu-latest
    timeout-minutes: 10  # hard gate timeout
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt

      - name: Run pytest (parallel, coverage, JUnit)
        run: |
          pytest \
            tests/unit \
            tests/integration \
            -v \
            --tb=short \
            --strict-markers \
            --numprocesses=auto \
            --dist=loadscope \
            --cov=src \
            --cov-report=json:artifacts/cov.json \
            --cov-report=term-missing \
            --cov-branch \
            --cov-fail-under=80 \
            --junitxml=artifacts/junit.xml \
            --hypothesis-profile=ci

      - name: Run oracle/tautology/mock lints
        run: |
          python -m crew.testing.lints \
            --check-tautologies \
            --check-oracle-violations \
            --check-mock-ratio \
            --src=src \
            --tests=tests

      - name: Check flake history
        run: |
          python -m crew.testing.flake-check \
            --history=artifacts/flake-history.json \
            --max-rate=0.02 \
            --db=ledger.db

      - name: Upload test artifacts
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: fast-gate-${{ github.run_id }}
          path: |
            artifacts/junit.xml
            artifacts/cov.json
            artifacts/flake-history.json
          retention-days: 30

      - name: Publish test results to PR
        if: always() && github.event_name == 'pull_request'
        uses: dorny/test-reporter@v1
        with:
          name: pytest-results
          path: artifacts/junit.xml
          reporter: java-junit
          fail-on-error: true

  # ── Job 2: Mutation Gate (targeted, per-PR) ────────────────────────
  mutation-gate:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    needs: fast-gate  # only if fast-gate passed
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install dependencies
        run: |
          pip install -r requirements-dev.txt
          pip install mutmut

      - name: Run targeted mutation testing
        run: |
          # Only mutate lines touched by this PR
          mutmut run --paths-to-mutate=src \
            --tests-dir=tests/unit \
            --runner="python -m pytest tests/unit -x -q" \
            --mutate-only-covered-lines=true \
            --max-stack-depth=8
          mutmut results > artifacts/mutation-report.json
          mutmut html  # optional HTML report

      - name: Check mutation threshold
        run: |
          python -m crew.testing.mutation-check \
            --report=artifacts/mutation-report.json \
            --threshold=70

      - name: Upload mutation report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: mutation-${{ github.run_id }}
          path: |
            artifacts/mutation-report.json
            html/
          retention-days: 30

  # ── Job 3: Property Tests ──────────────────────────────────────────
  property-tests:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    needs: fast-gate
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install dependencies
        run: pip install -r requirements-dev.txt

      - name: Run property-based tests
        run: |
          pytest tests/properties \
            -v \
            --hypothesis-profile=ci \
            --junitxml=artifacts/property-results.xml

      - name: Upload property results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: property-${{ github.run_id }}
          path: artifacts/property-results.xml
          retention-days: 14
```

**File: `.github/workflows/test-nightly.yml`**

```yaml
name: Test Nightly (Async)

on:
  schedule:
    - cron: "0 3 * * *"  # 3 AM UTC daily
  workflow_dispatch:  # manual trigger

permissions:
  contents: read
  actions: read

jobs:
  # ── Full mutation suite ────────────────────────────────────────────
  full-mutation:
    runs-on: ubuntu-latest
    timeout-minutes: 60
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install dependencies
        run: |
          pip install -r requirements-dev.txt
          pip install mutmut

      - name: Run full mutation suite
        run: |
          mutmut run --paths-to-mutate=src \
            --tests-dir=tests \
            --mutate-only-covered-lines=true \
            --max-stack-depth=8
          mutmut results > artifacts/full-mutation-report.json

      - name: Check FULL threshold (80%)
        run: |
          python -m crew.testing.mutation-check \
            --report=artifacts/full-mutation-report.json \
            --threshold=80

      - name: Upload report
        uses: actions/upload-artifact@v4
        with:
          name: full-mutation-${{ github.run_id }}
          path: artifacts/full-mutation-report.json
          retention-days: 90

  # ── E2E tests (capped at 10) ──────────────────────────────────────
  e2e-tests:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    needs: full-mutation
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install dependencies
        run: pip install -r requirements-dev.txt

      - name: Run E2E tests (max 10 journeys)
        run: |
          pytest tests/e2e \
            -v \
            -m "e2e" \
            --max-journeys=10 \
            --junitxml=artifacts/e2e-results.xml

      - name: Upload E2E results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: e2e-${{ github.run_id }}
          path: artifacts/e2e-results.xml
          retention-days: 14

  # ── Golden evaluation ──────────────────────────────────────────────
  golden-eval:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install dependencies
        run: pip install -r requirements-dev.txt

      - name: Run golden evaluation
        run: |
          python -m crew.testing.golden-eval \
            --golden-set=tests/golden/golden_set.json \
            --output=artifacts/golden-results.json \
            --thresholds=tests/golden/thresholds.json

      - name: Upload golden results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: golden-${{ github.run_id }}
          path: artifacts/golden-results.json
          retention-days: 90

  # ── Break drills ───────────────────────────────────────────────────
  break-drills:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install dependencies
        run: pip install -r requirements-dev.txt

      - name: Run break drills (break each REQ, assert redden)
        run: |
          python -m crew.testing.break-drills \
            --reqs=requirements/reqs.json \
            --tests=tests \
            --output=artifacts/drill-results.json

      - name: Upload drill results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: drills-${{ github.run_id }}
          path: artifacts/drill-results.json
          retention-days: 90
```

### 2. Parallelization Strategy

**Two-level parallelization** [Warpbuild, 2026; Qualflare, 2026]:

| Level | Mechanism | When to Use |
|-------|-----------|-------------|
| **Workers** (pytest-xdist) | `-n auto` or `-n 4` | Single job, divides tests across CPU cores |
| **Shards** (matrix) | `strategy.matrix` | Suite > 20 min, divides across runners |

**Worker configuration:**
```yaml
# In pytest addopts:
--numprocesses=auto  # one worker per physical core
--dist=loadscope     # group by module/class for fixture reuse
```

**Shard configuration (for suites > 20 min):**
```yaml
strategy:
  matrix:
    shard: [1, 2, 3, 4]
steps:
  - run: |
      pytest tests/ \
        --shard-id=${{ matrix.shard }} \
        --num-shards=4
```

**Choosing shard count:**
- `optimal_shards ≈ √(T / o)` where T = total time, o = setup overhead
- For 60 min suite with 4 min overhead: `√(60/4) ≈ 4` shards [Qualflare, 2026]

**GitHub Actions runner specs:**
- Default: 2-core CPU, 7 GB RAM, 14 GB disk
- `-n auto` on 2-core = 2 workers (safe)
- For I/O-bound suites: `-n 4` (hyperthreading helps)
- For CPU-bound suites: `-n 2` (physical cores only)

### 3. Artifact Retention Policy

**Retention schedule** [GitHub Docs, 2025]:

| Artifact Type | Retention | Reason |
|---------------|-----------|--------|
| `junit.xml` | 30 days | PR debugging, flake history |
| `cov.json` | 30 days | Coverage trend analysis |
| `mutation-report.json` | 90 days | Quarterly calibration |
| `flake-history.json` | 90 days | Flake pattern analysis |
| `golden-results.json` | 90 days | Golden set evolution |
| `drill-results.json` | 90 days | Drill trend analysis |
| `property-results.xml` | 14 days | Short-lived, replay via database |
| `e2e-results.xml` | 14 days | Short-lived, rerun daily |

**Configuration:**
```yaml
- uses: actions/upload-artifact@v4
  with:
    name: test-artifacts
    path: artifacts/
    retention-days: 30  # override default 90
```

**Cost optimization:**
- Default artifact storage: free up to 5 GB per repo
- Delete old artifacts: `gh run delete <run_id>` for failed runs
- Compress before upload: `tar -czf artifacts.tar.gz artifacts/`

### 4. Handling Secrets in Test Environments

**Secret categories and handling:**

| Secret Type | Example | Handling |
|-------------|---------|----------|
| **API keys** | `OPENAI_API_KEY`, `ANTHROPIC_API_KEY` | Use GitHub Secrets, never hardcode |
| **Database credentials** | `DB_PASSWORD` | Use `testcontainers` with random passwords |
| **Test data** | PII, financial data | Use synthetic/fake data only, never production |
| **Signing codes** | `GPG_KEY` | Use test-specific keys, never production |

**GitHub Secrets configuration:**
```yaml
env:
  OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}

steps:
  - name: Run tests with secrets
    run: pytest tests/
    env:
      OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

**Test environment isolation:**
1. **Branch protection**: PRs from forks don't have access to secrets (GitHub default)
2. **Environment protection**: Deploy to `test` env only after fast-gate passes
3. **Secret scanning**: GitHub scans for pushed secrets in code
4. **Rotation**: Rotate secrets quarterly or on suspected leak

**Secrets in E2E tests:**
- Use `vcrpy` to record/replay HTTP interactions — no live API calls in CI
- Use `testcontainers` for database — ephemeral, isolated, no persistent secrets
- Use `freezegun` for time-based secrets — deterministic timestamps

**References for deep dive:**
- [GitHub Docs, 2025] Building and testing Python: workflow template, setup-python
- [GitHub Community, 2025] Native Test Results Dashboard: workarounds (upload-artifact)
- [Warpbuild, 2026] Sharding pytest: workers vs shards, --dist loadscope
- [Qualflare, 2026] Test Parallelization: optimal shard count formula
- [Daniel Nouri, 2025] Modern Python CI: coverage + xdist gotchas, sitecustomize.py
- [CTRF, 2026] Flaky Tests on Actions: JSON report format
- [TestDino, 2026] Flaky Test Detection: history tracking
- [Tenki, 2026] Flaky Test Quarantine: same-commit flip detection
- [Mutagen, 2026] Mutation-gated LLM test generation: exit-2 gate
- [FlakyTest, 2026] Detect, quarantine, fix: quarantine patterns
