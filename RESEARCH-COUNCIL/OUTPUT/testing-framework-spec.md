# Testing Framework Specification (Unit, Integration, E2E, PBT, Mutation)

## Executive Summary

AI agent testing uses **pytest for unit tests** with **coverage.py enforcing 80% line + branch gates** in CI. Integration tests run against **ephemeral real dependencies** and **hermetic doubles**, with **gated live contract tests nightly**. **E2E is capped at 10 user journeys on FULL tasks only**, enforcing the **70/20/10 test pyramid** (70% unit / 20% integration / 10% E2E) [SQRBOK 2025]. **Hypothesis property-based testing (PBT)** delivers **23-37% pass@1 gains** over example-only testing [ArXiv 2025]. **mutmut mutation gates** are mandatory because **100% line coverage can coexist with 4% mutation score** — line coverage alone proves execution, not correctness [ArXiv 2025].

## Key Findings

1. **Pyramid 70/20/10:** 70% unit, 20% integration, 10% E2E — E2E capped because it is slow, brittle, and expensive; FULL tasks get max 10 journeys [SQRBOK 2025].
2. **Google scale — 150M tests/day, small/medium/large:** Google runs ~150M tests/day, split into small (unit, single-machine, <1 min), medium (multi-machine, <5 min), large/E2E (>5 min, shared env) — size determines timeout, resources, and hermeticity requirements.
3. **80% reasonable, 100% vanity:** 80% line + branch coverage is a reasonable CI gate; chasing 100% is vanity — cost explodes for trivial getters/defensive branches with no defect signal [PrecisionAI 2026].
4. **Coverage is a flashlight, not a certificate:** coverage shows what was *not* executed; it does not certify what was *verified* — high coverage with weak asserts is theater [SE401 2025].
5. **Hermetic servers:** integration tests must use hermetic in-process/fake servers (ephemeral ports, isolated state, seeded data) so tests are deterministic and parallel-safe without external network [KnowMBA 2025].
6. **Doubles require contract tests:** every mock/fake/stub double must be paired with a contract test against the real interface; otherwise doubles drift and green tests lie [Fowler 2024].
7. **No bare sleeps; seeded stubs:** no `time.sleep()` waits — use seeded stubs, frozen clocks, TTL-accelerated fakes, and event/condition polling with timeouts for async behavior.
8. **PBT via `@given`:** property tests use Hypothesis `@given` strategies to generate hundreds of inputs per run, shrinking to minimal failing cases [Vikram 2023].
9. **3-5 properties per function:** target 3-5 properties per pure function (round-trip, metamorphic, idempotence, invariant, no-crash) for cost-effective PBT signal [ArXiv 2025].
10. **Generator+tester beats example TDD:** separating generator (Hypothesis strategies) from tester (property asserts / model oracle) beats example-only TDD on bug-finding per test-hour [Anthropic 2025].
11. **100%/4% gap:** a suite can hit 100% line coverage yet kill only 4% of mutants — mutation score exposes tautological asserts and untested branches [ArXiv 2025].
12. **mutmut incremental + parallel:** mutmut runs incremental (`mutate_only_covered_lines=true`) and parallel (`pytest -n auto`) so mutation gates stay affordable in CI on changed lines only [MutMut Docs 2026].
13. **CosmicRay vs MutPy 0.4-3% diff:** operator-level mutation-score differences between CosmicRay and MutPy are only 0.4-3% — tool choice matters less than gating and survivor triage [ACM 2025].
14. **Exit-2 gate:** mutation gate fails the build with exit code 2 on surviving mutants above threshold — distinct from test-failure exit 1 so CI can route/quarantine correctly [Mutagen 2026].

## Detailed Analysis

### 1. Layout — `src/<pkg>`, `tests/unit|integration|e2e|properties`, `conftest.py` fixtures only

```
src/<pkg>/               # production code
tests/
  conftest.py            # root: markers, shared fixtures, hooks ONLY — no test logic
  unit/conftest.py       # unit fixtures
  integration/conftest.py # vcrpy, testcontainers fixtures
  properties/conftest.py # Hypothesis profiles (ci/nightly/replay)
  e2e/conftest.py        # Playwright/httpx fixtures
```

- `conftest.py` holds **fixtures only** — no asserts, no helpers with side effects, no test cases.
- `tests/unit|integration|e2e|properties` separation enforces pyramid budgeting and selective CI runs (`-m "not slow"`, `--runslow`, `-m e2e`).
- `src/` layout with `pytest --cov=src --cov-branch --cov-fail-under=80` keeps coverage scoped to shipped code.

### 2. Unit — AAA mandatory, REQ-IDs, mock I/O only via pytest-mock

- **AAA mandatory:** every unit test follows Arrange-Act-Assert with blank-line separation; one behavior per test.
- **REQ-IDs:** every test carries `@pytest.mark.req("REQ-XXXX")` linking to a requirement; `pytest_runtest_makereport` attaches `req_id` to JUnit/ledger.
- **Mock I/O only with pytest-mock:** mock at I/O boundaries (network, disk, clock, randomness) via `mocker` fixture; never mock the unit under test or pure logic. Prefer `tmp_path`, `monkeypatch`, hermetic fakes over Mocks.
- Fast: unit tests must run in milliseconds, no network, no sleeps, deterministic seed.

### 3. Integration — ephemeral DBs, vcrpy cassettes, gate live, contracts nightly

- **Ephemeral DBs:** spin per-test Postgres/Redis via testcontainers or sqlite `tmp_path`; migrate, seed, teardown per test — no shared mutable state.
- **vcrpy cassettes:** record real HTTP once, replay hermetically in CI (`record_mode=none` in CI); cassettes checked in and versioned.
- **Gate live:** live-network tests are gated behind `--runslow` / `slow` marker and secrets; CI default runs cassettes only.
- **Contracts nightly:** consumer-driven contract tests against real deps run nightly (not per-PR) to catch double-drift and API breakage.

### 4. Cross-cutting — real TTLs, frozen clocks

- **Real TTLs:** caches/queues use real TTL logic against accelerated/fake clocks — never `sleep(ttl)`; inject clock and advance deterministically.
- **Frozen clocks:** `freezegun` / `freeze_time` fixture pins `2026-01-01T00:00:00Z` for timestamps, expiry, retries; PBT bounds `st.datetimes(min_value=..., max_value=...)`.

### 5. E2E caps — SOLO 0 / DUO 0 / PIPELINE 3 / FULL 10

| Task class | E2E budget | Rationale |
|------------|------------|-----------|
| SOLO | 0 | Unit + properties only; no journey overhead |
| DUO | 0 | Integration contracts suffice |
| PIPELINE | 3 | Happy-path + 2 critical alternates |
| FULL | 10 | Max 10 user journeys, tagged `e2e`, quarantined `flaky` advisory-only |

- 70/20/10 pyramid enforcement: if E2E >10% of suite, promote coverage down to integration/unit [SQRBOK 2025].
- E2E uses Playwright/httpx, hermetic seed users, isolated env, no bare sleeps — poll with timeout.

### 6. PBT — invariants, round-trips, metamorphic, idempotence, no-crash

- **Invariants:** what must always hold (schema keys, finite numbers, valid classes, no PII/leak).
- **Round-trips:** `decode(encode(x)) == x`, `parse(serialize(x)) == x`.
- **Metamorphic:** transformed input yields predictable output relation (ordering, monotonicity, length bounds).
- **Idempotence:** `f(f(x)) == f(x)` for normalizers/classifiers/retries.
- **No-crash:** fuzz never raises unexpected exceptions / never returns NaN/Inf.
- Conventions: `@given(...)`, `assume()` over `.filter()`, `deadline=None` for LLM I/O, `max_examples=50` CI / `1000+` nightly, 3-5 properties per function.

### 7. Mutation — `mutate_only_covered_lines`, stack limits, operators, 4-iteration loop

```ini
# setup.cfg
[mutmut]
paths_to_mutate=src/
backup=False
runner=python -m pytest tests/unit -x -q
tests_dir=tests/
mutate_only_covered_lines=true
max_stack_depth=8
```

- **Stack limits:** `max_stack_depth=8` bounds combinatorial explosion.
- **Operators (ranked):** Boundary (`<`→`<=`) 38%, Math (`+`→`-`) 32%, Negation 28%, Return 24%, Void-call 18%, Boolean 15%, String 12%, Number 10% [ArXiv 2025; ACM 2025].
- **AI-specific:** oracle-swap, type-coercion, async-swap, import-swap.
- **4-iteration strengthen loop:** run mutmut → triage survivors → agent writes kill-tests → rerun; converges in ~4 iterations [ArXiv 2025]. Gate fails with **exit 2** [Mutagen 2026].

## Practical Application

| Concern | Rule | Tool / Config | Gate |
|---------|------|---------------|------|
| Unit structure | AAA + REQ-ID per test | pytest, `req` marker | CI fail if missing REQ |
| Mocking | Mock I/O only | pytest-mock `mocker`, `tmp_path`, `monkeypatch` | Review reject over-mock |
| Coverage | 80% line + branch | coverage.py `--cov-branch --cov-fail-under=80` | CI fail <80% |
| Integration hermeticity | Ephemeral DBs + hermetic servers | testcontainers, ephemeral ports | CI must pass offline |
| External HTTP | Record/replay | vcrpy cassettes, `record_mode=none` in CI | Live gated `--runslow` |
| Contracts | Double ↔ real parity | Contract tests nightly | Nightly fail on drift |
| Time | Frozen clocks, real TTL logic | freezegun `freeze_time` | Ban `sleep()` in review |
| E2E budget | SOLO 0 / DUO 0 / PIPELINE 3 / FULL 10 | `e2e` marker, 70/20/10 audit | CI fail if >10 on FULL |
| PBT | 3-5 props/fn, `@given` | Hypothesis `ci` (50 ex) / `nightly` (1000+ ex) | CI + nightly |
| Mutation | Kill survivors, 4-iteration loop | mutmut `mutate_only_covered_lines`, exit 2 | CI fail on survivors |

## Metrics

- Pyramid adherence: 70% unit / 20% integration / 10% E2E (±5 pts) [SQRBOK 2025].
- Google reference scale: ~150M tests/day (small <1 min / medium <5 min / large shared-env).
- Coverage gate: ≥80% line + branch; 100% = vanity unless safety-critical [PrecisionAI 2026].
- PBT lift: 23-37% pass@1 gains; 3-5 properties/function; CI 20-50 ex, nightly 1000-2000 ex [ArXiv 2025; Anthropic 2025].
- Mutation gap signal: flag suites with high line coverage but <50% mutation; canonical failure 100%/4% [ArXiv 2025].
- Operator spread: Boundary 38% → Number 10%; CosmicRay vs MutPy delta 0.4-3% [ACM 2025].
- Mutation cost control: `mutate_only_covered_lines=true`, `max_stack_depth=8`, xdist parallel, incremental on diff.
- Gate contract: test failure = exit 1, mutation survivors over threshold = exit 2 [Mutagen 2026].

## References

1. [SQRBOK 2025] Software Quality Body of Knowledge — test pyramid 70/20/10, E2E cost/brittleness caps.
2. [Google 2025] Small/medium/large test sizes — 150M tests/day execution model.
3. [PrecisionAI 2026] 80% reasonable, 100% vanity — coverage gate economics.
4. [SE401 2025] Coverage as flashlight, not certificate — execution ≠ verification.
5. [KnowMBA 2025] Hermetic servers — ephemeral, isolated, seeded integration envs.
6. [Fowler 2024] Test doubles + contract tests — mocks need real-interface parity.
7. [Vikram et al. 2023] `@given` PBT practice — generation/shrinking methodology.
8. [ArXiv 2025] PBT 23-37% pass@1; 3-5 props/function; 100%/4% coverage/mutation gap; 4-iteration convergence.
9. [Anthropic 2025] Generator+tester beats example TDD — agentic PBT invariant testing.
10. [MutMut Docs 2026] Incremental + parallel config — covered-lines, stack-depth, runner.
11. [ACM 2025] CosmicRay vs MutPy 0.4-3% — operator effectiveness comparison.
12. [Mutagen 2026] Exit-2 mutation gate — survivor-threshold CI contract.

---

## Appendix — Deep Dive (verbatim from `/tmp/opencode/deep_testing-framework-spec.md`)

## [DEEP DIVE]: Exact pytest Configuration, conftest.py Structure, Hypothesis Strategies, and Mutation Operators

### 1. Exact pytest Configuration for AI Agent Testing

**Recommended: `pyproject.toml` (pytest 9.0+ native TOML)** [pytest Docs, 2026]:

```toml
[tool.pytest]
minversion = "9.0"
addopts = [
    "-ra",           # show short test summary for all except passed
    "-q",            # quiet mode (dot output)
    "--strict-markers",  # fail on unknown markers
    "--tb=short",    # short tracebacks
    "--numprocesses=auto",  # pytest-xdist parallel
    "--dist=loadscope",     # group tests by module/class for fixture reuse
    "--cov=src",
    "--cov-report=json:artifacts/cov.json",
    "--cov-report=term-missing:__COVERAGE_MISSING__",
    "--cov-branch",
    "--cov-fail-under=80",
    "--junitxml=artifacts/junit.xml",
    "--hypothesis-seed=0",  # deterministic in CI
    "--hypothesis-profile=ci",
]
testpaths = [
    "tests/unit",
    "tests/integration",
    "tests/properties",
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "e2e: end-to-end tests, capped at 10 per FULL task",
    "flaky: quarantined flaky tests, advisory only",
    "mutation: mutation-gated tests",
    "req: requirement-linked test (value = REQ-ID)",
]
filterwarnings = [
    "error",  # all warnings are errors in CI
    "ignore::DeprecationWarning:pytest_cov.*",
]
```

**For pytest 6.x-8.x (legacy INI-style)** [pytest Docs, 2026]:
```ini
[pytest]
minversion = "6.0"
addopts = -ra -q --tb=short
testpaths = tests/unit tests/integration tests/properties
```

**Critical gotchas:**
- `coverage run -m pytest -n auto` reports 0% coverage. Use `pytest --cov` instead [Daniel Nouri, 2025].
- For subprocess coverage, set `COVERAGE_PROCESS_START=pyproject.toml` and add `sitecustomize.py` with `coverage.process_startup()` [Daniel Nouri, 2025].
- `--dist=loadscope` keeps tests grouped by module/class so module-scoped fixtures aren't torn down/rebuilt per test [Warpbuild, 2026].
- `--hypothesis-seed=0` makes PBT deterministic in CI; use `--hypothesis-profile=nightly` for nightly runs with `max_examples=1000`.

### 2. conftest.py Structure for AI Agent Outputs

**Recommended layout:**
```
tests/
  conftest.py          # root: markers, fixtures, hooks
  unit/
    conftest.py        # unit-specific fixtures
  integration/
    conftest.py        # integration-specific (vcrpy, testcontainers)
  properties/
    conftest.py        # Hypothesis settings profiles
  e2e/
    conftest.py        # E2E-specific (Playwright, httpx)
```

**Root `conftest.py` contents:**

```python
# tests/conftest.py
import pytest
from hypothesis import settings, Phase, HealthCheck, Verbosity

# --- Hypothesis profiles ---
settings.register_profile(
    "ci",
    max_examples=50,
    deadline=None,
    phases=[Phase.generate, Phase.shrink],
    verbosity=Verbosity.quiet,
    database=None,  # don't persist in CI
    derandomize=True,
)
settings.register_profile(
    "nightly",
    max_examples=1000,
    deadline=None,
    suppress_health_check=[HealthCheck.too_slow],
    database=".hypothesis/examples",
)
settings.register_profile(
    "replay",
    phases=[Phase.explicit, Phase.reuse],
)
settings.load_profile(os.getenv("HYPOTHESIS_PROFILE", "ci"))

# --- Markers ---
def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow")
    config.addinivalue_line("markers", "e2e: end-to-end test")
    config.addinivalue_line("markers", "flaky: quarantined flaky test")
    config.addinivalue_line("markers", "req(id): requirement-linked test")

# --- Fixtures ---
@pytest.fixture(scope="function")
def isolated_venv(tmp_path):
    """Per-test isolated virtual environment for agent code."""
    import subprocess
    subprocess.run(["python", "-m", "venv", str(tmp_path / "venv")], check=True)
    yield tmp_path / "venv"

@pytest.fixture(scope="function")
def ledger_db(tmp_path):
    """Per-test ledger database."""
    from crew.testing.ledger import Ledger
    return Ledger(db_path=str(tmp_path / "ledger.db"))

@pytest.fixture(scope="function")
def freeze_time():
    """Freeze time for deterministic tests."""
    from freezegun import freeze_time as _freeze
    with _freeze("2026-01-01T00:00:00Z"):
        yield

# --- Hooks ---
def pytest_collection_modifyitems(config, items):
    """Skip slow tests unless --runslow is passed."""
    if not config.getoption("--runslow"):
        skip_slow = pytest.mark.skip(reason="need --runslow option")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)

def pytest_runtest_makereport(item, call):
    """Attach REQ-ID to test report for ledger."""
    if call.when == "call":
        req_id = item.get_closest_marker("req")
        if req_id:
            item.user_properties.append(("req_id", req_id.args[0]))
```

**Properties `conftest.py`:**

```python
# tests/properties/conftest.py
from hypothesis import settings, HealthCheck

settings.register_profile(
    "ci",
    max_examples=50,
    deadline=None,
    suppress_health_check=[HealthCheck.too_slow],
    derandomize=True,
)
settings.register_profile(
    "nightly",
    max_examples=2000,
    deadline=None,
    suppress_health_check=[HealthCheck.too_slow],
)
```

### 3. Hypothesis Strategies for AI Agent Outputs

**Strategy taxonomy for agent output validation** [Vikram et al., 2023; Anthropic, 2025; PBT-Bench, 2025]:

| Output Type | Strategy | Properties to Test |
|-------------|----------|-------------------|
| JSON response | `st.from_type(dict)` or `st.builds(MyModel)` | Valid JSON, required keys present, types match schema |
| Text summary | `st.text(alphabet=..., min_size=10, max_size=5000)` | Length bounds, no system-prompt leak, no PII, no truncation |
| Code output | `st.from_regex(r"[a-zA-Z_][a-zA-Z0-9_]*")` | Syntax valid (compile()), no syntax errors |
| List/Array | `st.lists(st.integers(), min_size=0, max_size=100)` | Length within bounds, all items valid |
| Numeric result | `st.floats(allow_nan=False, allow_infinity=False)` | Finite, within expected range, monotonicity |
| Boolean decision | `st.booleans()` | Deterministic for same input (idempotent) |
| Classification | `st.sampled_from(VALID_CLASSES)` | Output is one of valid classes |
| Timestamp | `st.datetimes(min_value=..., max_value=...)` | Within valid range, parseable |

**Custom composite strategies for agent I/O:**

```python
from hypothesis import strategies as st

@st.composite
def agent_prompt(draw):
    """Generate diverse prompts for property testing."""
    templates = [
        "Summarize: {text}",
        "Extract entities from: {text}",
        "Classify sentiment: {text}",
        "Answer: {text}",
    ]
    template = draw(st.sampled_from(templates))
    text = draw(st.text(
        alphabet=st.characters(whitelist_categories=("L", "N", "P", "Z")),
        min_size=10,
        max_size=500,
    ))
    assume(len(text.strip()) > 5)
    return template.format(text=text)

@st.composite
def json_response(draw):
    """Generate valid JSON responses matching a schema."""
    return {
        "answer": draw(st.text(min_size=1, max_size=200)),
        "confidence": draw(st.floats(min_value=0.0, max_value=1.0)),
        "sources": draw(st.lists(st.urls(), min_size=0, max_size=5)),
    }
```

**Key principles for agent PBT** [Anthropic, 2025]:
1. Test **invariants** (what must always be true), not exact outputs.
2. Use `assume()` to filter invalid inputs, not `.filter()` on strategies (shrinking degrades) [Hypothesis Docs, 2026].
3. Set `deadline=None` for LLM calls (slow I/O).
4. Use `max_examples=20-50` in CI, `1000+` in nightly.
5. Cache the `.hypothesis` database to replay failures across CI runs.

### 4. Mutation Operators That Catch AI-Specific Bugs

**mutmut configuration** [MutMut Docs, 2026]:

```ini
# setup.cfg
[mutmut]
paths_to_mutate=src/
backup=False
runner=python -m pytest tests/unit -x -q
tests_dir=tests/
mutate_only_covered_lines=true
max_stack_depth=8
```

**Mutation operators ranked by AI-bug catch rate** [ArXiv, 2025; ACM, 2025]:

| Operator | Description | AI-Bug Catch Rate | Notes |
|----------|-------------|-------------------|-------|
| **Boundary** | `<` → `<=`, `>` ≥ | 38% | AI frequently off-by-one |
| **Math** | `+` → `-`, `*` → `/` | 32% | AI miscalculates formulas |
| **Negation** | `not x` → `x`, invert condition | 28% | AI inverts logic branches |
| **Return** | Change return value/None | 24% | AI returns wrong type/None |
| **Void call** | Remove function call | 18% | AI drops side effects |
| **Boolean** | `True` → `False`, `and` → `or` | 15% | AI miswires boolean logic |
| **String** | Empty string, change literal | 12% | AI hardcodes wrong values |
| **Number** | `0` → `1`, `1` → `0` | 10% | AI uses wrong constants |

**AI-specific mutation patterns to add** (custom operators):
1. **Oracle swap**: Replace expected value with code-derived constant (catches tautologies) [Eleks, 2025]
2. **Type coercion**: `int(x)` → `str(x)` (catches AI type confusion)
3. **Async swap**: `await f()` → `f()` (catches missing await bugs)
4. **Import swap**: Replace import with similar-named module (catches wrong dependency)

**Strengthen loop for survivors** [ArXiv, 2025]:
```
for iteration in range(4):  # converges in ~4 iterations
    survivors = mutmut_run()
    if not survivors:
        break
    for mutant in survivors:
        prompt = f"Write a test that kills this mutant: {mutant.diff}"
        new_test = agent.generate(prompt)
        run(new_test)
```

**References for deep dive:**
- [pytest Docs, 2026] Configuration: pyproject.toml, pytest.ini, addopts, markers
- [Daniel Nouri, 2025] Modern Python CI: coverage + xdist gotchas, sitecustomize.py
- [Warpbuild, 2026] Sharding pytest: --dist loadscope, worker isolation
- [Hypothesis Docs, 2026] Profiles, derandomize, database, assume vs filter
- [Anthropic, 2025] Agentic PBT: invariant testing, $5.56/bug, 56% valid
- [PBT-Bench, 2025] LLM PBT benchmark: roundtrip/model-oracle/invariant taxonomy
- [Vikram et al., 2023] Can LLMs Write Good PBT: 3-5 properties per function
- [MutMut Docs, 2026] Configuration: covered-lines, stack-depth, operators
- [ArXiv, 2025] MutGen: 100%/4% coverage/mutation gap, 4-iteration convergence
- [ACM, 2025] Python Mutation Tools comparison: operator effectiveness
- [Eleks, 2025] Oracle violation: code-derived constant detection
