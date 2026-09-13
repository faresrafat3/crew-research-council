# Implementation Roadmap

## Executive Summary
Four phases climb TMMi levels without stalling delivery: Foundation (3-5 days) commits policy and SOUL gates; Mandatory Tests (1-2 weeks) enforces RED/GREEN evidence and fast CI; Quality Gates (2-3 weeks) adds property, mutation, oracle, and ledger gates; Continuous Improvement (ongoing) converts escapes into knowledge and calibration. Each phase names exact files, deltas, metrics, and risks so an operator can execute directly, following the staged TMMi climb [TMMi Foundation, 2016] with Test Certified-style graduation [KnowMBA, 2025].

## Key Findings
- Staged levels each lay foundations for the next; skipping stages fails [TMMi Foundation, 2016].
- Policy plus planning plus environments come before measurement [TMMi Foundation, 2018].
- Shared standards plus lifecycle integration precede meaningful metrics [TMMi Foundation, 2018].
- Measurement of process and product quality precedes optimization [TMMi Foundation, 2018].
- Prevention and process optimization close the loop [TMMi Foundation, 2018].
- Graduated test certification moves teams to full TDD stepwise [KnowMBA, 2025].
- Mutation feedback needs about 4 iterations to converge [ArXiv, 2025].
- Flake quarantine with 14-day SLAs protects velocity during rollout [KnowMBA, 2025].
- PROMOTE/HOLD/ROLLBACK gates prove stable across dozens of releases [ArXiv, 2026].
- Consensus plus human review on disagreement prevents automation capture [IJECS, 2026].

## Detailed Analysis
Phase 1 creates `crew/TEST-POLICY.md`, patches tester SOUL to full spec, adds engineer iron law, patches firstmate activation, scaffolds test dirs, installs pytest plus coverage. Phase 2 enforces message templates, fixes critic timeouts and paths, makes completer reject missing verdicts, and blocks merges on pytest plus coverage artifacts. Phase 3 adds Hypothesis, mutmut with covered-lines and stack limits, oracle/tautology/mock lints, ledger DB, verdict gates, nightly large plus golden eval plus break drills. Phase 4 runs prevention reviews, quarterly FP/FN calibration, safe-class auto-patches with human review, and trend dashboards. Risks per phase: workaround RED logs (audit them), critic timeouts (time-box now), flake storms (quarantine lane), E2E bloat (caps), slow mutation (targeted plus parallel), PBT difficulty (seed from KB), strictness drift (calibrate).

## Practical Recommendations
| Phase | Duration | Files and Deltas | Success Criteria | Risks |
|---|---|---|---|---|
| 1 Foundation | 3-5d | TEST-POLICY.md; tester/engineer/firstmate SOUL patches; test dirs; pytest+coverage | 100% new PIPE/FULL have REQ+RED (10 tasks) | workarounds; timeouts |
| 2 Mandatory | 1-2wk | message templates; critic fix; completer gate; CI pytest+coverage+JUnit | >=80% tests pre-done (20 tasks); <10 min | flakes; E2E bloat |
| 3 Gates | 2-3wk | Hypothesis+mutmut; lints; ledger; verdicts; nightly+golden+drills | mut 70/80%, req-cov 90%, flake<2%, drill 100% | speed; PBT learning |
| 4 Improve | ongoing | KB SLA; calibration; safe auto-fix; dashboards | -25% escapes/qtr; MTTR<14d; KB lag 0 | strict/lenient drift |

## Metrics and Targets
| Metric | Definition | How to Measure | Target | Warning |
|---|---|---|---|---|
| RED-witness | merged with RED | audit | 100% P2+ | <100% |
| Gate pass | PROMOTE share | ledger | rising | falling |
| Coverage/mutation | gates | CI | 80%/70-80% | below HOLD |
| Drill pass | REQ breaks caught | drill | 100% | <100% |
| Escape delta | per quarter | reports | -25% | rising |
| Phase slip | days overdue | plan | 0 | >3d replan |

## References
1. [TMMi Foundation, 2016] Staged model and benefits.
2. [TMMi Foundation, 2018] Level process areas.
3. [KnowMBA, 2025] Test Certified graduation, quarantine, budgets.
4. [ArXiv, 2025] MutGen iteration convergence.
5. [ArXiv, 2026] Self-testing gates at scale.
6. [IJECS, 2026] Consensus, HITL, safe auto-fix.

## [DEEP DIVE]: Day-by-Day Phase 1, Risk Playbooks, Rollback Criteria, and Progress Dashboard

> Extends base `implementation-roadmap.md` (45 lines, 4 phases: Foundation 3–5d → Mandatory 1–2wk → Gates 2–3wk → Improve ongoing). This dive does NOT repeat the phase table — it makes Phase 1 executable day-by-day, adds 6 risk playbooks, per-phase rollback gates, and a ledger-backed progress dashboard.

### 1. Phase 1 day-by-day (Foundation, 5 working days)

Principle: staged levels each lay foundations for the next; skipping stages fails [Base-R1]. Policy + planning + environments come before measurement [Base-R2]. Phased rollouts must start with stability management + staging before production exposure [DD-1]. New tests should soak outside the critical CI path before gating — cf. Google's "Reservoir" loop pattern [DD-2].

#### Day 1: TEST-POLICY.md + test dirs + pytest+coverage install

Goal: policy committed, skeleton dirs green, coverage tooling proven on one dummy test.

Exact commands:

```bash
# 1. scaffold dirs
mkdir -p crew/tests/{unit,integration,e2e} crew/fixtures docs
# 2. install toolchain (pin for reproducibility)
pip install "pytest>=8.0" "pytest-cov>=5.0" "coverage>=7.0"
pip freeze | grep -Ei 'pytest|coverage' | tee crew/tests/toolchain.pins
# 3. minimal config — coverage gate source + JUnit artifact (standard pytest-cov pattern [DD-5])
cat > pytest.ini <<'EOF'
[pytest]
testpaths = crew/tests
addopts = --cov=crew --cov-report=term-missing --cov-report=xml:crew/tests/coverage.xml --cov-report=html:crew/tests/htmlcov --junitxml=crew/tests/junit.xml -q
EOF
# 4. smoke test to prove toolchain
cat > crew/tests/unit/test_smoke.py <<'EOF'
def test_smoke():
    assert True
EOF
pytest crew/tests/unit/test_smoke.py
# 5. create policy doc (Phase 1 deliverable per base)
cat > crew/TEST-POLICY.md <<'EOF'
# TEST-POLICY (v0.1 Foundation)
- Scope: all new PIPE/FULL tasks require REQ link + RED-witness log + GREEN evidence.
- RED-witness: failing-test log committed BEFORE fix; CI independently reruns and asserts retcode != 0.
- Coverage floor (advisory in Phase 1, enforced Phase 2+): 80% line, mutation 70% targeted.
- Flake rule: flake rate >2% → quarantine lane, 14d SLA to fix or delete.
- E2E budget: SOLO 0 / DUO 0 / PIPE ≤3 / FULL ≤10.
EOF
git add crew/TEST-POLICY.md pytest.ini crew/tests && git commit -m "phase1-day1: policy + test dirs + pytest+coverage"
```

Done-criteria: `crew/TEST-POLICY.md` merged; `crew/tests/{unit,integration,e2e}` exist; `pytest` passes on smoke test.
Verification command:

```bash
test -f crew/TEST-POLICY.md && test -d crew/tests/unit && pytest crew/tests/unit/test_smoke.py --cov=crew --cov-report=term | tail -5
ls crew/tests/junit.xml crew/tests/coverage.xml
```

Target: JUnit + coverage XML artifacts present (same artifact pair CI will gate on in Phase 2 [Base, Phase 2]).

#### Day 2: tester SOUL patch (full spec)

Goal: tester agent cannot claim done without REQ+RED evidence. Shared standards + lifecycle integration must precede meaningful metrics [Base-R3].

Patch (append to tester SOUL / system prompt):

```markdown
## TESTER IRON PROTOCOL (Phase 1)
1. Before any fix: write failing test reproducing REQ; commit log to `crew/tests/evidence/<task>-RED.log` (must show non-zero exit).
2. Never mark task done without: REQ id, RED log path, GREEN rerun path.
3. If critic times out: emit PARTIAL verdict + what was checked (see Risk R2).
4. Workaround RED logs are rejected — CI reruns independently (see Risk R1).
```

Commands:

```bash
# apply patch (adjust path to actual SOUL file)
ls .dsh/profiles/*/SOUL.md crew/**/SOUL.md 2>/dev/null || ls crew/ | head
# after editing:
git diff --stat
python3 -c "import pathlib; t=[p for p in pathlib.Path('.').rglob('SOUL.md')]; print(t)"
grep -ri "RED.log" .dsh/profiles crew 2>/dev/null | head -5
git add -A && git commit -m "phase1-day2: tester SOUL RED-witness protocol"
```

Done-criteria: tester SOUL contains `RED.log` + REQ requirement; grep hits ≥1 file.
Verification command:

```bash
grep -rl "RED.log" .dsh/profiles crew | wc -l  # expect >=1
grep -rl "REQ" .dsh/profiles/tester* crew 2>/dev/null | head
```

#### Day 3: engineer iron law

Goal: engineer cannot bypass tester; no direct-to-merge without test evidence.

Patch text:

```markdown
## ENGINEER IRON LAW (Phase 1)
- No code merge without linked failing test (RED) + passing rerun (GREEN).
- No editing tests to make them pass without new RED log.
- Violation → merge blocked; repeated violation → task reassigned.
```

Commands:

```bash
# edit engineer SOUL/profile, then:
grep -ri "IRON LAW" .dsh/profiles crew | head -3
git add -A && git commit -m "phase1-day3: engineer iron law"
# dry-run gate locally:
pytest crew/tests/unit -q 2>&1 | tail -3
```

Done-criteria: engineer profile contains IRON LAW block; local pytest still green.
Verification command:

```bash
grep -rl "IRON LAW" .dsh/profiles crew | wc -l  # expect >=1
pytest crew/tests/unit -q; echo "retcode=$?"
```

#### Day 4: firstmate activation

Goal: firstmate enforces activation checklist (policy read + evidence paths present) before dispatching PIPE/FULL work. Staging discipline: test in production-like setup after QA before rollout [DD-1].

Checklist to add to firstmate prompt:

```markdown
## FIRSTMATE ACTIVATION (Phase 1)
Before dispatching PIPE/FULL task, verify:
[ ] crew/TEST-POLICY.md exists
[ ] task has REQ id
[ ] crew/tests/evidence/ dir writable
Else: refuse dispatch with reason.
```

Commands:

```bash
mkdir -p crew/tests/evidence
# patch firstmate SOUL, then:
git add -A && git commit -m "phase1-day4: firstmate activation checklist"
ls -ld crew/tests/evidence && grep -rl "ACTIVATION" .dsh/profiles crew | head -3
```

Done-criteria: `crew/tests/evidence/` exists; firstmate SOUL contains ACTIVATION checklist.
Verification command:

```bash
test -d crew/tests/evidence && echo EVIDENCE_OK
grep -rl "ACTIVATION" .dsh/profiles crew | wc -l  # expect >=1
```

#### Day 5: 10-task pilot with RED-witness 100% check

Goal: prove 100% new PIPE/FULL have REQ+RED on a 10-task pilot (base Phase 1 success criterion [Base, Phase 1]). Run new tests in advisory mode (not yet blocking), mirroring the Reservoir soak pattern — observe flakiness before gating [DD-2]. Google data: at 1.5% flake rate, ~15 failures per 1000 tests — independent rerun/quarantine is mandatory, not optional [DD-3].

Commands:

```bash
# run 10 pilot tasks (replace with real task runner; log each RED)
ls crew/tests/evidence/  # should accumulate <task>-RED.log per task
# RED-witness audit (100% required):
python3 - <<'EOF'
import pathlib
ev = list(pathlib.Path("crew/tests/evidence").glob("*-RED.log"))
print(f"RED logs: {len(ev)}/10")
for p in sorted(ev): print(" ", p)
assert len(ev) >= 10, "pilot incomplete: need 10 RED logs"
EOF
# independent CI-style rerun check (each RED must fail with retcode != 0):
for f in crew/tests/evidence/*-RED.log; do echo "== $f"; grep -Ei "failed|FAILED|retcode|exit" "$f" | head -2; done
pytest crew/tests -q 2>&1 | tail -3
```

Done-criteria: 10/10 pilot tasks have `*-RED.log` with non-zero-exit evidence; audit script exits 0.
Verification command:

```bash
ls crew/tests/evidence/*-RED.log | wc -l  # expect 10
pytest crew/tests -q; echo "green_retcode=$?"
```

If RED-witness <80% after 10 tasks → rollback tester SOUL patch (see §3).

### 2. Risk playbooks (6 risks)

Each playbook: trigger metric → action → owner. Base names these 6 risks explicitly (workaround RED, critic timeouts, flake storms, E2E bloat, slow mutation, PBT learning) [Base, Detailed Analysis].

| # | Risk | Trigger metric | Action | Owner |
|---|---|---|---|---|
| R1 | Workaround RED logs (fake/manually-written fail logs) | Audit: RED log present but CI rerun exits 0 | CI independently reruns the exact RED test command and asserts `retcode != 0`; reject merge + flag task. Do not trust log text alone — rerun is the witness. | CI owner / tester |
| R2 | Critic timeouts stall verdicts | Critic run > budget (e.g. >5 min single task) | Time-box now: emit PARTIAL verdict (what passed/checked + what timed out + next step); human reviews disagreement — consensus + HITL prevents automation capture [Base-R10]. Never block pipeline on missing full verdict. | Critic owner |
| R3 | Flake storms erode trust | Flake rate >2% on rolling window | Quarantine lane: move flaky test out of gating path, keep in reliability suite; 14-day SLA to fix or delete [Base-R8]. Google practice: mark flaky, rerun only flaky-marked, keep signal clean [DD-2][DD-3]. | Test infra |
| R4 | E2E bloat slows CI | E2E count exceeds caps or gate >10 min | Enforce caps: SOLO 0 / DUO 0 / PIPE ≤3 / FULL ≤10; convert excess E2E → integration/unit; move slow E2E to nightly. Graduated certification moves teams stepwise instead of big-bang [Base-R6]. | Firstmate / CI owner |
| R5 | Slow mutation feedback | Full mutmut run > nightly budget | Targeted + parallel: mutate only covered lines changed in PR (`--covered-lines`), shard workers (`-j N`), stack depth limit; full-corpus only nightly. Feedback needs ~4 iterations to converge, so keep loop fast [Base-R7]. | Quality-gate owner |
| R6 | PBT learning curve (Hypothesis hard to adopt) | <50% of eligible modules have properties after wk 1 Phase 3 | Seed from KB: copy minimal property templates per type (int-range, string-shape, idempotency, round-trip); pair 1 experienced reviewer per team; keep first properties trivially small. Prevention + optimization close the loop only after measurement is stable [Base-R5]. | Tech lead |

R3 detail — quarantine procedure (executable):

```bash
# detect: flake rate query (see §4 Q-flake); if >2%:
mkdir -p crew/tests/quarantine
git mv crew/tests/e2e/test_flaky_*.py crew/tests/quarantine/ 2>/dev/null || true
# mark in pytest:
pytest crew/tests --deselect crew/tests/quarantine -q
git add -A && git commit -m "quarantine: move flaky tests out of gate (14d SLA)"
```

R1 detail — CI assert snippet (GitHub Actions style):

```yaml
- name: RED-witness independent rerun
  run: |
    pytest crew/tests/evidence/repro_${{ github.sha }}.py -q
    test $? -ne 0 || (echo "RED witness FAILED: repro passed, rejecting" && exit 1)
```

Justification: phased rollouts require real-time stability visibility + early-access testing before widening exposure [DD-1]; flaky-gate disruption causes deployment bottlenecks unless quarantined [DD-4].

### 3. Rollback criteria (per phase, with exact revert commands)

Rule: each phase has a numeric tripwire; tripping it reverts the gating change but keeps evidence/logs. Staged climb means a failed stage is re-laid, not skipped [Base-R1]. PROMOTE/HOLD/ROLLBACK gates are proven stable across dozens of releases — use them literally [Base-R9].

| Phase | Tripwire (rollback if…) | Rollback action (exact) | Post-rollback mode |
|---|---|---|---|
| 1 Foundation | RED-witness <80% after 10 pilot tasks (i.e. <8/10 RED logs verify) | `git log --oneline -8` → `git revert --no-commit <tester-SOUL-commit>` + `git revert --no-commit <engineer-SOUL-commit>`; `git commit -m "rollback(phase1): revert SOUL gates, keep evidence"` | Advisory only; fix RED template, re-pilot 5 tasks before re-applying |
| 2 Mandatory | Gate p95 >15 min for 3 consecutive days OR flake-blocked merges >20% of PRs | `git revert --no-commit <completer-gate-commit> <ci-gate-commit>`; `git commit -m "rollback(phase2): gate to advisory"`; set CI `gate: advisory` flag | Tests run + reported but non-blocking; re-enforce when p95 <10 min (base target [Base, Phase 2]) |
| 3 Gates | False-positive rate >5% on verdict gates OR mutation nightly fails 3× in a row | `git revert --no-commit <ledger-gate-commit>`; loosen thresholds 5 pts (e.g. mutation 70→65, req-cov 90→85); `git commit -m "rollback(phase3): loosen thresholds 5pts"` | HOLD instead of block; recalibrate quarterly per base [Base, Phase 4] |
| 4 Improve | Escape delta rising 2 quarters OR FP/FN calibration disagreement >30% | `git revert --no-commit <auto-fix-commit>`; restore human-review-required for all safe-class patches; `git commit -m "rollback(phase4): auto-fix back to HITL"` | Human-in-loop on every auto-patch per consensus+HITL rule [Base-R10] |

Generic revert template:

```bash
git log --oneline -15  # identify gating commit(s)
git revert --no-commit <COMMIT_SHA>
git status --short
pytest crew/tests/unit -q  # sanity: still green after revert
git commit -m "rollback(<phase>): <what> -> <advisory/HOLD/HITL> (tripwire: <metric>=<value>)"
git revert --abort  # only if conflicted and you want to abandon the revert
```

Threshold notes: FP >5% → loosen thresholds 5 pts (absolute points, not relative) to restore signal; re-tighten only after 30-task clean window (see §4). Phase slip >3 days → replan per base warning threshold [Base, Metrics].

### 4. Progress dashboard (ledger-backed SQL + targets)

Assumed ledger schema (SQLite; create once in Phase 3 per base [Base, Phase 3]):

```sql
CREATE TABLE IF NOT EXISTS tasks(id TEXT PRIMARY KEY, phase TEXT, req_id TEXT, red_witness INT, created_at TEXT);
CREATE TABLE IF NOT EXISTS gate_runs(id INTEGER PRIMARY KEY, task_id TEXT, verdict TEXT, coverage REAL, mutation REAL, duration_min REAL, created_at TEXT);
CREATE TABLE IF NOT EXISTS drills(id INTEGER PRIMARY KEY, req_id TEXT, caught INT, created_at TEXT);
CREATE TABLE IF NOT EXISTS escapes(id INTEGER PRIMARY KEY, quarter TEXT, count INT);
```

Q1 — RED-witness % (target 100% P2+, warn <100% [Base, Metrics]):

```sql
SELECT COUNT(*) AS n,
  SUM(red_witness)*100.0/COUNT(*) AS red_pct
FROM tasks WHERE phase IN ('P2','PIPE','FULL');
-- target: red_pct = 100; tripwire: < 80 after 10 tasks → rollback Phase 1 (§3)
```

Q2 — Gate pass trend / PROMOTE share (target rising, warn falling [Base, Metrics]):

```sql
SELECT date(created_at) AS d,
  SUM(CASE WHEN verdict='PROMOTE' THEN 1 ELSE 0 END)*100.0/COUNT(*) AS promote_pct,
  COUNT(*) AS n
FROM gate_runs WHERE created_at >= date('now','-14 days')
GROUP BY d ORDER BY d;
-- target: rising week-over-week; warn: 3-day falling streak → investigate R2/R3
```

Q3 — Coverage / mutation 30-task window (targets 80% cov / 70–80% mut, req-cov 90% [Base, Phases 2–3]):

```sql
SELECT task_id, AVG(coverage) AS cov, AVG(mutation) AS mut
FROM gate_runs GROUP BY task_id ORDER BY MAX(created_at) DESC LIMIT 30;
-- target: cov >= 80 AND mut >= 70; HOLD band: cov 70-80 / mut 60-70; warn: below HOLD
```

Q4 — Flake rate + gate duration (targets flake <2%, gate <10 min [Base, Phases 2–3]):

```sql
SELECT SUM(CASE WHEN verdict='FLAKE' THEN 1 ELSE 0 END)*100.0/COUNT(*) AS flake_pct,
  AVG(duration_min) AS p_mean, MAX(duration_min) AS p_max
FROM gate_runs WHERE created_at >= date('now','-7 days');
-- target: flake_pct < 2 AND p_mean < 10; tripwire: p95 > 15 min → rollback Phase 2 (§3)
```

Q5 — Drill pass (target 100% [Base, Metrics]) + escape delta (target −25%/qtr [Base, Metrics]; starters typically 30–50%, improve 5–10 pts/qtr is reasonable [DD-6]):

```sql
SELECT SUM(caught)*100.0/COUNT(*) AS drill_pct FROM drills;
-- target: 100; warn: < 100
SELECT quarter, count,
  LAG(count) OVER (ORDER BY quarter) AS prev,
  (LAG(count) OVER (ORDER BY quarter) - count)*100.0/LAG(count) OVER (ORDER BY quarter) AS qoq_drop_pct
FROM escapes ORDER BY quarter;
-- target: qoq_drop_pct >= 25; warn: rising (negative drop)
```

Q6 — Phase slip days (target 0, warn >3 replan [Base, Metrics]):

```sql
SELECT phase, julianday(actual_done)-julianday(planned_done) AS slip_days FROM plan_tracker;
-- target: 0; warn: > 3 → replan
```

Dashboard cadence: Q1–Q4 daily during rollout (phased rollouts need real-time stability visibility [DD-1]); Q5–Q6 weekly/quarterly. Defect escape rate = prod-found / total defects; track per-gate escapes separately so a clean release-failure rate does not hide gate leaks [DD-7][DD-8].

**References for deep dive:**
- [Base-R1]–[Base-R10] Base `implementation-roadmap.md` (45 lines, 4 phases): staged TMMi climb [TMMi Foundation, 2016]; policy/planning/envs before measurement, standards before metrics, measurement before optimization, prevention closes loop [TMMi Foundation, 2018]; Test Certified graduation + quarantine 14d SLA [KnowMBA, 2025]; MutGen ~4 iterations [ArXiv, 2025]; PROMOTE/HOLD/ROLLBACK at scale [ArXiv, 2026]; consensus+HITL [IJECS, 2026].
- [DD-1] DevOps.com, "Do's and Don'ts of Phased Rollouts" (2021-09-09) — stability management, A/B+QA + early access, staging before production. Fetched 2026-09-13.
- [DD-2] Google Testing Blog, "Flaky Tests at Google and How We Mitigate Them" (2016-05-27) — rerun only flaky-marked, Reservoir soak loop, flake-as-signal discussion. Search + fetch 2026-09-13.
- [DD-3] TinyFish search "CI test gate rollout risks mitigation flaky 2025" — Google 1.5%-flake → ~15 failures/1000 tests; 2025 ArXiv flake-repair cost 1.28% dev time. Searched 2026-09-13.
- [DD-4] TinyFish search "CI test gate rollout risks mitigation flaky 2025" (dev.to playbook, semaphore, mill-build) — flaky gates cause deployment bottlenecks; quarantine/detect-diagnose-mitigate. Searched 2026-09-13.
- [DD-5] TinyFish search "pytest coverage gate CI JUnit HTML report setup" — pytest-cov `--cov`, `--cov-report`, `--junitxml` artifact pattern. Searched 2026-09-13.
- [DD-6] TinyFish search "engineering metrics dashboard coverage mutation escape rate 2024" — shift-left starters 30–50% escape, 5–10 pts/qtr improvement target. Searched 2026-09-13.
- [DD-7] TinyFish search "engineering metrics dashboard coverage mutation escape rate 2024" (Opsera DER guide) — DER = prod defects / total defects. Searched 2026-09-13.
- [DD-8] TinyFish search "engineering metrics dashboard coverage mutation escape rate 2024" (getautonoma, gitmore, ardura) — per-stage escape tracking, dashboard KPIs (coverage, MTTR, escape). Searched 2026-09-13.
