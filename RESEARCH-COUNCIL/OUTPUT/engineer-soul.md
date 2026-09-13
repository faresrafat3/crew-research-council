# Engineer Agent SOUL Updates (Test Integration)

## Executive Summary
One iron-law rule ends zero-test shipments: no production code without a witnessed failing test first, and no DONE claim without RED reference plus GREEN log plus clean full suite. The engineer requests RED tests instead of inventing oracles, implements one requirement slice at a time, and answers HOLDs by fixing listed files without weakening assertions. Tests-first answers what code should do while tests-after merely rationalizes what was built [Hermes TDD Skill, 2026].

## Key Findings
- Missing done-gates caused COORD-01, COORD-02, and T09-T12 zero-test repeats [Council Context, 2026].
- Iron law with deletion of pre-written code enforces tests-first [Hermes TDD Skill, 2026].
- Watching tests fail proves they detect the missing feature [Hermes TDD Skill, 2026].
- Tracer bullets (one test to one impl) beat horizontal all-tests-first slices [Hermes TDD Skill, 2026].
- Green means minimal code only, never extra features [Hermes TDD Skill, 2026].
- Other-test failures must be fixed immediately as regressions [Hermes TDD Skill, 2026].
- Fully in-loop self-testing without separation shows no quality gain [Bockeler, 2026].
- Code-derived oracles always pass and prove nothing [Eleks, 2025].
- Survivor feedback loops need genuine fixes, not narrowed generators [ArXiv, 2025].
- Single-appeal discipline with evidence prevents veto wars [Priygop, 2026].

## Detailed Analysis
Insert the iron law at the top of the engineer SOUL before Done, and reorder the procedure to SPEC, await RED (REQUEST_TESTS if absent), minimal impl, targeted GREEN, full `pytest -q`, then ENGINEER_DONE with all five artifacts (paths, sha, RED ref, GREEN log, selfcheck). On HOLD, patch only listed assertions and files, rerun targeted plus full, resubmit within 3 rounds, appeal at most once. Banned: DONE without tests, ignoring or rewriting failures, editing tests to pass, narrowing Hypothesis strategies, weakening asserts, bare sleeps, live externals in unit tests, scope-expanding during GREEN.

## Practical Recommendations
| Recommendation | Implementation | Tools | Threshold |
|---|---|---|---|
| Add iron law verbatim | SOUL top, before Done | patch | exact text below |
| Require 5 artifacts | paths+sha+RED+GREEN+selfcheck | message template | 100% DONE claims |
| Request, don't invent | REQUEST_TESTS when RED missing | message_agent | 0 self-oracles |
| Slice per REQ | tracer bullets only | pytest -v per test | 1 REQ/cycle |
| Answer HOLDs cleanly | fix listed files, rerun all | pytest -q | <=3 rounds |

Verbatim rule:
IRON LAW: NO PRODUCTION CODE WITHOUT A WITNESSED FAILING TEST FIRST. You MUST NOT declare DONE without (a) tester's RED tests for every REQ-ID you touched, (b) your GREEN run log for those tests, (c) full `pytest -q` green with no regressions. Missing RED log means you are NOT done.

## Metrics and Targets
| Metric | Definition | How to Measure | Target | Warning |
|---|---|---|---|---|
| RED-miss rate | DONE claims without RED | log audit | 0% | >0% HOLD |
| Selfcheck honesty | claimed green vs actual | CI rerun | 100% match | mismatch HOLD |
| Regression rate | full-suite breaks | CI | 0 on submit | >0 fix now |
| Rounds per task | fix iterations | ledger | <=3 | >3 escalate |
| Oracle violations | self-derived expectations | lint | 0 | >0 HOLD |

## References
1. [Council Context, 2026] Crew v2 trials COORD-01, COORD-02, T09-T12.
2. [Hermes TDD Skill, 2026] Iron law, RED/GREEN verification, tracer bullets.
3. [Bockeler, 2026] TDD inside the agent loop (separation requirement).
4. [Eleks, 2025] Independent Oracle (code-derived expectations).
5. [ArXiv, 2025] MutGen (survivor feedback done honestly).
6. [Priygop, 2026] Escalation discipline (evidence-based appeals).

## [DEEP DIVE]: Iron-Law Enforcement Hooks, Message Schemas, HOLD Playbook, and Oracle-Violation Taxonomy
> Base: `engineer-soul.md` (48 lines, fetched 2026-09-13 via `gh api`) defines the iron law, 5-artifact DONE, REQUEST_TESTS, and HOLD discipline [Council Context, 2026; Hermes TDD Skill, 2026]. This deep dive does NOT repeat it — it adds the enforceable machinery beneath it: hook YAML, CI rerun code, wire schemas, timed HOLD playbook, and lintable oracle-violation patterns.

### 1. Iron-law enforcement (3 layers: text → pre-commit → CI)

**Layer 1 — SOUL text (verbatim, normative).** Placed at top of engineer SOUL before Done, exact text from base [Hermes TDD Skill, 2026]:
```
IRON LAW: NO PRODUCTION CODE WITHOUT A WITNESSED FAILING TEST FIRST. You MUST NOT declare DONE without (a) tester's RED tests for every REQ-ID you touched, (b) your GREEN run log for those tests, (c) full `pytest -q` green with no regressions. Missing RED log means you are NOT done.
```
Why verbatim matters: missing done-gates caused COORD-01, COORD-02, T09-T12 zero-test repeats [Council Context, 2026]; fully in-loop self-testing without separation shows no quality gain [Bockeler, 2026].

**Layer 2 — Pre-commit hook that blocks DONE without RED ref.** `pre-commit` manages hook install/execution before every commit and a hook "must exit nonzero on failure" to block the commit [pre-commit.com docs, 2025]. Standard config shape is `repos: [{repo, rev, hooks: [{id, entry, language}]}]` [pre-commit.com docs, 2025]. The pytest-as-hook pattern uses `repo: local`, `language: script`, `entry: venv/bin/pytest`, `pass_filenames: false`, `always_run: true` because a post/commit hook "doesn't know which files were changed" [Switowski, 2023]. The `types: [python]` filter lets unrelated commits pass without running tests [StackOverflow, 2020]. Coverage-gate precedent exists: `coverage-pre-commit` "fails commits that don't meet your specified threshold" and "prevents code with insufficient test coverage from even making it to your repository" [Reddit r/Python, 2024]. Exact hook config for Crew v2 (extends that precedent from coverage% to RED-evidence presence):

```yaml
# .pre-commit-config.yaml — Crew v2 Engineer iron-law gate
repos:
  - repo: local
    hooks:
      - id: engineer-done-gate
        name: engineer DONE requires RED ref + GREEN log + sha
        entry: python3 scripts/check_engineer_done.py
        language: system
        pass_filenames: false
        always_run: true
        verbose: true
      - id: pytest-targeted
        name: pytest targeted (changed REQ slice)
        entry: venv/bin/pytest -q tests/test_red_slice.py
        language: script
        pass_filenames: false
        types: [python]
        always_run: false
```

`scripts/check_engineer_done.py` (exit-nonzero = block, per pre-commit contract [pre-commit.com docs, 2025]):
```python
#!/usr/bin/env python3
"""Block DONE without RED evidence. Fails (exit 1) if ENGINEER_DONE.md lacks any of the 5 artifacts."""
import re, sys, pathlib
p = pathlib.Path("ENGINEER_DONE.md")
if not p.exists():
    sys.exit(0)  # no DONE claim in this commit -> pass
t = p.read_text()
checks = {
    "paths": r"^-\s+paths:\s+\S+",
    "sha": r"\b[0-9a-f]{7,40}\b",
    "RED ref": r"RED\s*:\s*tests/\S+\.py::\S+.*retcode\s*!=\s*0|RED-log:\s*\S+",
    "GREEN log": r"GREEN\s*:\s*pytest.*passed|GREEN-log:\s*\S+",
    "selfcheck": r"selfcheck:\s*(honest|pass)",
}
missing = [k for k, rx in checks.items() if not re.search(rx, t, re.M)]
if missing:
    print(f"BLOCKED: ENGINEER_DONE.md missing: {missing}. No DONE without RED ref + GREEN log + sha.")
    sys.exit(1)
print("engineer-done-gate: 5 artifacts present.")
```
Install: `pre-commit install` sets up `.git/hooks/pre-commit` so it "will run automatically on git commit" [pre-commit.com docs, 2025]. Fast checks belong in pre-commit, slow suites in CI per the "milliseconds in pre-commit, slower in CI" split rule [Switowski, 2023] — hence gate script (ms) blocks locally, full `pytest -q` reruns in CI.

**Layer 3 — CI check that reruns RED independently with `result.retcode != 0` assert.** CI is the separation layer: "run the fast checks in pre-commit and all the slow and fast checks in the CI" so local and server never diverge [Switowski, 2023]. Minimal GitHub Actions shape (`actions/checkout`, `setup-python`, `pip install pytest`, `run: pytest`) is the documented baseline [Switowski, 2023]. Crew v2 adds independent RED-witness rerun — the engineer-claimed RED test is executed against the pre-fix stash/sha and MUST fail, otherwise the oracle proves nothing [Eleks, 2025; Hermes TDD Skill, 2026]:

```yaml
# .github/workflows/engineer-iron-law.yml
name: engineer-iron-law
on: [push, pull_request]
jobs:
  witness:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: {fetch-depth: 0}
      - uses: actions/setup-python@v5
        with: {python-version: "3.11"}
      - run: pip install pytest hypothesis pyyaml
      - name: Rerun claimed RED independently (must FAIL pre-fix)
        run: python3 scripts/ci_witness_red.py
      - name: Rerun GREEN + full suite (must PASS post-fix)
        run: |
          pytest -q tests/test_red_slice.py
          pytest -q
```

```python
# scripts/ci_witness_red.py — independent RED witness
import subprocess, sys, re, pathlib
done = pathlib.Path("ENGINEER_DONE.md").read_text()
m = re.search(r"RED\s*:\s*(tests/\S+?)(?:\s|$)", done)
assert m, "CI HOLD: no RED ref parseable from ENGINEER_DONE.md"
red_node = m.group(1).strip()
# checkout pre-fix sha claimed in DONE, run RED, expect FAILURE
sha = re.search(r"\b([0-9a-f]{7,40})\b", done).group(1)
subprocess.run(["git", "stash", "-u"], check=False)
subprocess.run(["git", "checkout", "-q", sha], check=False)
result = subprocess.run(["python", "-m", "pytest", "-q", red_node],
                        capture_output=True, text=True)
subprocess.run(["git", "checkout", "-q", "-"], check=False)
subprocess.run(["git", "stash", "pop"], check=False)
print(result.stdout[-2000:])
assert result.returncode != 0, f"CI HOLD: claimed RED {red_node} PASSED pre-fix — oracle proves nothing [Eleks, 2025]"
print(f"RED witnessed: {red_node} failed pre-fix (retcode={result.returncode}).")
```
`result.returncode != 0` is the machine form of "watching tests fail proves they detect the missing feature" [Hermes TDD Skill, 2026]. Selfcheck honesty is then `claimed green vs actual` via CI rerun with target 100% match, mismatch → HOLD [Base Metrics, 2026].

### 2. Message schemas (REQUEST_TESTS + ENGINEER_DONE, each with 1 full example)

Schemas enforce "request, don't invent": 0 self-oracles, 100% DONE claims carry 5 artifacts [Base Recommendations, 2026]. Separation is load-bearing because "the author can't be the verifier" — AI code carries ~1.7x more issues when self-verified [AgentIQA, 2026] — and every agent must report type-check + lint + test suite before reporting back [dev.to validation, 2026].

**REQUEST_TESTS — engineer → tester (when RED missing).** Fields: `task` (1 REQ slice only, tracer-bullet rule [Hermes TDD Skill, 2026]), `req` (REQ-ID + verbatim requirement text), `files` (production paths to be touched, no test paths).

```yaml
# schema: REQUEST_TESTS v2
type: REQUEST_TESTS
task: "T14-slice-02"
req:
  id: REQ-014
  text: "Reject login when password expired (>90d): return 403 with code PASSWORD_EXPIRED."
files:
  - src/auth/login.py
constraints:
  - "one REQ per cycle; no impl until RED received [Hermes TDD Skill, 2026]"
  - "no live externals in unit tests; inject clock [Base banned list, 2026]"
```

Full example:
```
REQUEST_TESTS | task=T14-slice-02 | req=REQ-014 "Reject login when password
expired (>90d): return 403 PASSWORD_EXPIRED" | files=[src/auth/login.py]
Need: failing test with frozen clock (expiry=91d), expected 403 + code field.
Do NOT implement. I will await RED log before touching src/.
```

**ENGINEER_DONE — engineer → council (5 artifacts).** Fields: `paths` (touched prod files), `sha` (commit under test), `RED` (tester test node + witnessed-fail log ref), `GREEN` (targeted pass log), `selfcheck` (targeted + full `pytest -q` results, honest). Procedure order is SPEC → await RED → minimal impl → targeted GREEN → full `pytest -q` → DONE [Base Detailed Analysis, 2026].

```yaml
# schema: ENGINEER_DONE v2 (all 5 required; gate script regexes these keys)
type: ENGINEER_DONE
task: "T14-slice-02"
paths: ["src/auth/login.py"]
sha: "a3f9c1e2"
RED: "tests/test_login_expiry.py::test_expired_password_returns_403 retcode!=0"
RED-log: "logs/red_T14_2026-09-13.txt (1 failed, exit 1)"
GREEN: "pytest -q tests/test_login_expiry.py -> 3 passed in 0.41s"
GREEN-log: "logs/green_T14_2026-09-13.txt"
selfcheck: "targeted 3 passed; full pytest -q: 214 passed, 0 failed"
```

Full example (`ENGINEER_DONE.md` as committed):
```
ENGINEER_DONE | task=T14-slice-02 | REQ-014
- paths: src/auth/login.py
- sha: a3f9c1e2
- RED: tests/test_login_expiry.py::test_expired_password_returns_403 retcode!=0
- RED-log: logs/red_T14_2026-09-13.txt
- GREEN: pytest -q tests/test_login_expiry.py -> 3 passed in 0.41s
- GREEN-log: logs/green_T14_2026-09-13.txt
- selfcheck: honest — targeted 3 passed; full pytest -q 214 passed, 0 failed
- notes: minimal impl only (expiry check + 403 mapping); no extra features per GREEN-minimal rule [Hermes TDD Skill, 2026]
```

### 3. HOLD response playbook (6 steps, time-boxed: 30 min/fix, 90 min total)

Rationale: keep fix iterations `<=3` (ledger) with `>3 → escalate`, and single-appeal discipline with evidence to prevent veto wars [Base Metrics, 2026; Priygop, 2026]. Small PRs + automation cut review cycle time ~50% [dev.to review, 2026]; cognitive-error-aware review improves effectiveness [Huang, 2024]. Two-rule framing (small scope, fast turnaround) keeps reviews an instrument not a hurdle [SerCe, 2025].

1. **Read FIX_REQUIRED (≤5 min).** Open HOLD notice, list every flagged REQ-ID, file:line, and violated rule. Do not touch code yet. Confirm you reproduce the cited failure command verbatim. [Huang, 2024]
2. **Patch only listed files (≤15 min).** Edit exactly the flagged `paths`. No scope-expanding during GREEN, no drive-by refactors [Hermes TDD Skill, 2026]. If a second file must change, note it in resubmit or stop and ask — unlisted edits reset the round counter.
3. **Never weaken asserts (0 tolerance).** Do not edit tests to pass, narrow Hypothesis strategies, lower thresholds, or convert `==` to `in`. See §4 taxonomy for the 6 banned rewrites and their lint regexes [Eleks, 2025; ArXiv MutGen, 2025].
4. **Rerun targeted + full `pytest -q` (≤10 min).** First `pytest -q <red-node>` (must flip fail→pass), then full `pytest -q` (other-test failures fixed immediately as regressions [Hermes TDD Skill, 2026]). Save both logs; selfcheck must match CI rerun 100% [Base Metrics, 2026].
5. **Resubmit ≤3 rounds (ledger-enforced).** Each resubmit repeats the 5-artifact DONE with new sha + fresh logs. Round 3 miss → auto-escalate to lead, no silent round 4 [Base Metrics, 2026]. Budget: 30 min/fix × 3 = 90 min total per HOLD; exceeding 90 min escalates even if rounds remain.
6. **Appeal ≤1 with evidence package (≤30 min to assemble, async).** Only after 1 clean fix attempt. Package: (a) verbatim requirement text, (b) RED log showing fail-then-pass, (c) full-suite log, (d) diff of prod files only, (e) why the flag misreads the requirement. Evidence-based appeals only [Priygop, 2026]. Appeal denied → fix stands, no second appeal.

### 4. Oracle-violation taxonomy (6 types — detection regex/lint + bad/good)

Background: code-derived oracles "always pass and prove nothing" [Eleks, 2025]; tautological AI tests "pass without catching bugs" and need mutation score to expose them [Autonoma, 2026]; survivor feedback must be genuine fixes not narrowed generators [ArXiv MutGen, 2025]; agents must not "remove or rewrite tests that don't verify actual behavior" — instead add assertions that check results [AgentMelt, 2026].

**V1 — Code-derived constant (expected copied from implementation).**
- Lint: `ruff` custom / `grep -Pz`: `expected\s*=\s*\w+\(.*\)|assert\s+\w+\(\)\s*==\s*\w+\(\)` + flag when expected var assigned from same module under test.
- Detection regex: `/(EXPECTED|expected)\s*=\s*(login|calc|parse|format)\w*\(/`
- Bad: `expected = login(u, p); assert login(u, p) == expected`
- Good: `assert login(expired_user).status == 403  # from REQ-014 text, not from code`

**V2 — Self-read assertion (test reads back what code just wrote, no independent check).**
- Lint: semgrep `pattern: $X.write(...); assert $X.read() == ...` without fixture-defined `$X` content.
- Detection regex: `/assert\s+\w+\.read\(\)\s*==\s*\w+[\._]written|assert\s+db\.get\(\w+\)\s*==\s*payload/`
- Bad: `repo.save(u); assert repo.get(u.id) == u  # proves store round-trips, not REQ`
- Good: `repo.save(u); got = repo.get(u.id); assert got.pw_expired is True and got.code == "PASSWORD_EXPIRED"`

**V3 — Snapshot without req check (`.snap` approved once, never compared to requirement).**
- Lint: fail if `snapshot`/`inline-snapshot` added without `REQ-` comment on same test; `grep -P`: `snapshot\(\)` AND NOT `REQ-\d+` within 5 lines above.
- Detection regex: `/def test_\w+\(.*snapshot.*\):(?:(?!REQ-).)*assert/m`
- Bad: `assert snapshot(login_resp)  # approved blindly, expiry code change invisible`
- Good: `assert login_resp.status == 403 and login_resp.code == "PASSWORD_EXPIRED"  # REQ-014; snapshot only for body shape`

**V4 — Healed URL/limit/role/message (agent edits oracle fixture to match broken behavior).**
- Lint: `git diff` on `tests/` must not change literals matching `http[s]?://|status.?code|role=|limit=\d+|PASSWORD_|FORBIDDEN` without `REQ-` justification line; block `tests/**` literal flips in same commit as `src/**` fix unless REQUEST_TESTS references it.
- Detection regex: `/^[-+].*(https?:\/\/|status_code\s*=\s*\d+|role\s*=\s*"|PASSWORD_EXPIRED|limit\s*=\s*\d+)/m` on test diffs.
- Bad: `- assert resp.code == "PASSWORD_EXPIRED"` / `+ assert resp.code == "FORBIDDEN"  # healed to match bug`
- Good: keep `PASSWORD_EXPIRED`; fix `src/auth/login.py` to return it; never edit the expected string.

**V5 — Narrowed Hypothesis strategy (survivor feedback shrinks generator instead of fixing code).**
- Lint: forbid shrinking `st.*(` bounds in fix commits: `grep -P`: `st\.integers\(.*max_value\s*=\s*\d+` delta < previous, or `max_examples` reduced; require `hypothesis` profile unchanged between RED and GREEN.
- Detection regex: `/st\.(integers|text|datetimes)\([^)]*max_value\s*=\s*\d+[^)]*\)\s*#.*narrow|given\(.*max_examples\s*=\s*\d{1,2}\)/`
- Bad: `st.integers(min_value=0, max_value=90)  # was 0..365; expiry>90 never generated`
- Good: `st.integers(min_value=0, max_value=400)  # keeps 91d+ survivor region; fix code, not generator [ArXiv MutGen, 2025]`

**V6 — Weakened assert (`==` → `in`, exact → regex, `assert` → `assert len>0`).**
- Lint: semgrep diff rule: flag `==`→`in`, `assert x ==`→`assert x is not None`, added `pytest.mark.xfail`/`skip` on RED node, `time.sleep` insertions (bare sleeps banned [Base, 2026]).
- Detection regex: `/^[-+]\s*assert\s+.*(==|!=).*\n^[+]\s*assert\s+.*(in\s|is not None|>=?\s*0\s*$)/m`
- Bad: `- assert resp.status == 403` / `+ assert resp.status in (200, 403, 500)`
- Good: `assert resp.status == 403; assert resp.code == "PASSWORD_EXPIRED"  # exact, from REQ-014`

**References for deep dive:**
1. [Council Context, 2026] Crew v2 trials COORD-01, COORD-02, T09-T12 zero-test repeats — via base engineer-soul.md.
2. [Hermes TDD Skill, 2026] Iron law, RED/GREEN verification, tracer bullets, GREEN-minimal — via base.
3. [Bockeler, 2026] TDD inside agent loop requires separation — via base.
4. [Eleks, 2025] Independent Oracle; code-derived expectations always pass — via base.
5. [ArXiv MutGen, 2025] Survivor feedback must be genuine fixes, not narrowed generators — via base.
6. [Priygop, 2026] Escalation/appeal discipline with evidence — via base.
7. [pre-commit.com docs, 2025] Hook config shape; `pre-commit install` runs on every commit; hook must exit nonzero to block — fetched 2026-09-13.
8. [Switowski, 2023] Pre-commit vs CI; pytest local pattern `repo: local, language: script, entry: venv/bin/pytest, pass_filenames: false, always_run: true`; ms-vs-slow split; GitHub Actions pytest baseline — fetched 2026-09-13.
9. [StackOverflow, 2020] `types: [python]` lets commits pass when no Python files ran — search result 2026-09-13.
10. [Reddit r/Python, 2024] coverage-pre-commit fails commits below threshold — fetched 2026-09-13.
11. [dev.to validation, 2026] Agents must pass type-check + lint + test suite before reporting back — search result 2026-09-13.
12. [Autonoma, 2026] Tautological AI tests pass without catching bugs — search result 2026-09-13.
13. [AgentIQA, 2026] Author can't be verifier; AI code 1.7x more issues when self-verified — search result 2026-09-13.
14. [AgentMelt, 2026] Remove/rewrite tests that don't verify behavior; add assertions that check results — search result 2026-09-13.
15. [SerCe, 2025] Two simple rules make reviews an instrument not a hurdle — search result 2026-09-13.
16. [Huang, 2024] Cognitive-error-aware review improves effectiveness — search result 2026-09-13.
17. [dev.to review, 2026] PR sizing + automation cut review cycle time ~50% — search result 2026-09-13.
