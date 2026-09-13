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
