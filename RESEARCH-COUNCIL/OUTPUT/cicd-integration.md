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
