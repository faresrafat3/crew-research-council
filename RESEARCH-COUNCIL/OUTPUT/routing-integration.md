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

## [DEEP DIVE Cycle 3]: Critic Timeout Root-Cause Fix — Time-Box, Path-Awareness, and Partial Verdicts

> Extends `routing-integration.md` (gate <10 min, async large suites, evidence-bound verdicts). Does NOT repeat formation table. Root cause per CONTEXT.md: critic dies on complex tasks because (a) no timeout config — hangs look like freezes, never yield a verdict, block PIPELINE/FULL gates; (b) no path awareness — critic does repo-wide search instead of reviewing only touched files, exploding input/runtime caps on large diffs.

### 1. Time-box spec (10 min/file, 30 min/task hard timeout)

**Rule:** No critic invocation may run unbounded. Per-file budget 10 min, per-task hard cap 30 min. On timeout → emit `PARTIAL_VERDICT` + `HOLD`, never silent hang, never PROMOTE on incomplete evidence.

**Why this fixes it:** Copilot Code Review on 1000+ file PRs "hangs indefinitely and never completes" — in practice large diffs exceed input/runtime caps and review aborts behind a server-side timeout while UI looks frozen. Fix is fail-fast with explicit timeout + size gate before review starts (disable auto-review, gate with Actions check on `changed_files`, post "Skipping — too large").

**Exact GitHub Actions YAML snippet (gate + time-box):**

```yaml
name: critic-gate
on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  critic:
    runs-on: ubuntu-latest
    timeout-minutes: 10          # per-file/shard budget; task fan-out caps at 30 min total
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0         # need main for diff --name-only
      - name: Size gate (fail fast before critic)
        id: sizegate
        run: |
          FILES=$(git diff --name-only origin/main...HEAD | wc -l)
          LINES=$(git diff --stat origin/main...HEAD | tail -1)
          echo "files=$FILES" >> "$GITHUB_OUTPUT"
          echo "stat=$LINES" >> "$GITHUB_OUTPUT"
          if [ "$FILES" -gt 50 ]; then
            echo "SKIP_CRITIC_FULL=1 — $FILES files exceeds critic scope; use incremental shards" >> "$GITHUB_STEP_SUMMARY"
          fi
      - name: Run critic (sharded, hard timeout)
        timeout-minutes: 10
        run: |
          chmod +x ./scripts/critic_shard.sh
          ./scripts/critic_shard.sh --budget-sec 600 --task-cap-sec 1800
      - name: Upload partial verdict on timeout/failure
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: critic-partial-verdict
          path: |
            critic_verdict.json
            critic_ledger.jsonl
```

**Exact shell `timeout` wrapper (per-file 600s, per-task 1800s):**

```bash
#!/usr/bin/env bash
# scripts/critic_shard.sh — hard time-box; always emits verdict JSON even on timeout
set -u
BUDGET_SEC=600 TASK_CAP_SEC=1800
while [ $# -gt 0 ]; do case "$1" in
  --budget-sec) BUDGET_SEC="$2"; shift 2;;
  --task-cap-sec) TASK_CAP_SEC="$2"; shift 2;;
  *) shift;;
esac; done

REVIEWED=(); UNREVIEWED=()
> critic_ledger.jsonl
TASK_START=$(date +%s)

review_one() {
  local f="$1"
  local elapsed=$(( $(date +%s) - TASK_START ))
  if [ "$elapsed" -ge "$TASK_CAP_SEC" ]; then
    echo "[critic] TASK CAP ${TASK_CAP_SEC}s hit — marking remaining HOLD"
    return 99
  fi
  # timeout 600 = SIGTERM on overrun; exit 124 signals timeout
  if timeout "$BUDGET_SEC" ./scripts/critic_review_file.sh "$f"; then
    echo "{\"file\":\"$f\",\"status\":\"reviewed\"}" >> critic_ledger.jsonl
    REVIEWED+=("$f")
  else
    local rc=$?
    if [ $rc -eq 124 ]; then
      echo "{\"file\":\"$f\",\"status\":\"timeout_partial\"}" >> critic_ledger.jsonl
      UNREVIEWED+=("$f (timeout@${BUDGET_SEC}s)")
    else
      echo "{\"file\":\"$f\",\"status\":\"error_rc=$rc\"}" >> critic_ledger.jsonl
      UNREVIEWED+=("$f (rc=$rc)")
    fi
  fi
}

while IFS= read -r f; do
  review_one "$f" || { # task-cap hit: drain rest to UNREVIEWED
    UNREVIEWED+=("$f (task-cap)")
    while IFS= read -r rest; do UNREVIEWED+=("$rest (task-cap)"); done
    break
  }
done < <(git diff --name-only origin/main...HEAD -- 'src/**' 'tests/**' ':!*.generated.*' ':!vendor/**')

# Always emit PARTIAL_VERDICT-compatible JSON (see §4)
python3 -c "
import json
reviewed=[l for l in open('critic_ledger.jsonl') if 'reviewed' in l]
print(json.dumps({'verdict':'PARTIAL_VERDICT','reviewed_shards':len(reviewed)}))
" > critic_verdict.json
```

> Timeout semantics: `timeout 600` sends SIGTERM at 600s; use `timeout -k 30 600` if critic traps TERM. Job-level `timeout-minutes: 10` is the backstop when the shell itself hangs.

### 2. Path-awareness (review only what the diff touched)

**Rule:** Critic MUST run `git diff --name-only main` first. Review only touched files + linked tests. Never repo-wide `grep`/`glob`/`search`. Repo-wide search is the input-cap explosion that kills large-diff reviews.

**Exact commands (run in this order, paste into critic prompt):**

```bash
git fetch origin main --depth=50
git diff --name-only origin/main...HEAD
git diff --stat origin/main...HEAD | tail -5
git diff --numstat origin/main...HEAD | sort -rn -k1,1 | head -20   # largest files first → shard these
# linked tests only: for each touched src file, resolve counterpart
for f in $(git diff --name-only origin/main...HEAD -- 'src/**'); do
  base=$(basename "$f" | sed 's/\.[^.]*$//')
  git ls-files "tests/**${base}*" "test/**${base}*" "**/test_${base}*"
done
```

**Conftest path map (critic loads ONLY these, no tree-walk):**

```python
# conftest_path_map.py — critic path-awareness: touched file → review scope
PATH_MAP = {
    "src/api/":      {"tests": ["tests/api/"],      "checks": ["contract", "auth", "rate-limit"]},
    "src/core/":     {"tests": ["tests/unit/"],     "checks": ["invariants", "mutation-sample"]},
    "src/db/":       {"tests": ["tests/integration/"], "checks": ["migration-safety", "rollback"]},
    "src/ui/":       {"tests": ["tests/e2e-smoke/"], "checks": ["a11y-spot", "snapshot-cap"]},
    ".github/":      {"tests": [],                  "checks": ["yaml-lint", "timeout-present"]},
}
FALLBACK = {"tests": ["tests/unit/"], "checks": ["lint-only"], "note": "unmapped path → lint-only, HOLD for mapping"}

def scope_for(touched: str):
    for prefix, scope in PATH_MAP.items():
        if touched.startswith(prefix):
            return scope
    return FALLBACK
```

**Anti-patterns (BLOCK-worthy):** `grep -r` over repo, `glob **/*.py`, "review entire codebase for consistency", loading `vendor/`, `*.generated.*`, `dist/`, `node_modules/`. Exclude via `:(exclude)` pathspec: `git diff origin/main...HEAD -- . ':!vendor/**' ':!dist/**' ':!*.min.js'`.

### 3. Incremental review (chunk >500-line diffs into ≤200-line hunks)

**Rule:** If any file's diff >500 lines, do NOT review whole. Chunk into ≤200-line hunks, review hunk-by-hunk, checkpoint ledger after each hunk. Follows 200–400 LOC ceiling (defect-finding drops past 400; target 200, ceiling 400) and incremental-review pattern (re-reviews focus only on new commits, verify critical fixes, suppress re-flagging old code).

**Chunking script:**

```bash
#!/usr/bin/env bash
# scripts/chunk_diff.sh <file> — split diff into ≤200-line hunks with ledger checkpoints
set -euo pipefail
F="${1:?usage: chunk_diff.sh <file>}"
BASE=$(git merge-base origin/main HEAD)
OUTDIR=".critic_hunks/$(echo "$F" | tr '/' '_')"
mkdir -p "$OUTDIR"
git diff -U20 "$BASE" HEAD -- "$F" | split -l 200 - "$OUTDIR/hunk_"
i=0
for h in "$OUTDIR"/hunk_*; do
  i=$((i+1))
  printf '{"file":"%s","hunk":%d,"chunk":"%s","status":"pending"}\n' "$F" "$i" "$h" >> critic_ledger.jsonl
  echo "HUNK $i: $h ($(wc -l < "$h") lines)"
done
echo "Total hunks for $F: $i (review sequentially, append verdict per hunk)"
```

**Hunk review loop (ledger checkpointing):**

```bash
for h in .critic_hunks/<file>_slashed/hunk_*; do
  timeout 600 ./scripts/critic_review_hunk.sh --file "$F" --hunk "$h" \
    && echo "{\"hunk\":\"$h\",\"status\":\"done\"}" >> critic_ledger.jsonl \
    || echo "{\"hunk\":\"$h\",\"status\":\"partial_timeout\"}" >> critic_ledger.jsonl
done
```

**Re-review scope enforcement (from incremental-review skill):** on `synchronize`, diff only new commits (`git diff HEAD~1...HEAD` per push), verify prior critical findings fixed, auto-close style/tech-debt nits, never open new issues in untouched hunks.

### 4. Partial-verdict protocol (timeout → HOLD, never PROMOTE)

**Fields (required):** `reviewed_files`, `unreviewed_files`, `findings_so_far`, `confidence`, `recommendation` ∈ {HOLD, ESCALATE}. Tester treats partial as HOLD, never PROMOTE. ESCALATE only when findings_so_far contains a suspected BLOCK (security/data-loss) needing human.

**Template (`critic_verdict.json`):**

```json
{
  "verdict": "PARTIAL_VERDICT",
  "task": "critic review <PR# / commit>",
  "budget": {"per_file_sec": 600, "task_cap_sec": 1800},
  "reviewed_files": ["src/api/auth.py (hunks 1-3/5)", "tests/api/test_auth.py"],
  "unreviewed_files": ["src/api/auth.py (hunks 4-5, timeout@600s)", "src/db/migrate_042.py (task-cap)"],
  "findings_so_far": [
    {"severity": "major", "file": "src/api/auth.py:112", "note": "token refresh path lacks expiry check"},
    {"severity": "nit", "file": "tests/api/test_auth.py:8", "note": "deferred — style only"}
  ],
  "confidence": 0.45,
  "recommendation": "HOLD",
  "next_action": "re-run critic on unreviewed_files only (incremental), then tester re-gates"
}
```

**Tester handling rule (paste into tester prompt):**

```
IF critic_verdict.verdict == "PARTIAL_VERDICT" → verdict=HOLD (never PROMOTE).
IF recommendation == "ESCULATE" → page human with findings_so_far.
ELSE → schedule incremental critic on unreviewed_files, keep gate <10 min via async.
```

**References Cycle 3:**
1. GitHub Community Discussion #176835 (2025) — Copilot Code Review hangs/times out on 1000+ file PRs; no documented hard limit; large diffs exceed input/runtime caps; workaround = gate with Actions `changed_files` check + per-file Ask Copilot. [verified: 2026-09-13, fetch_content]
2. Augment Code, "Code Review Best Practices That Actually Scale" (2026-01-15) — 200 LOC target / 400 LOC ceiling (SmartBear/Cisco: defect-finding drops past 400); first-response SLA 1 business day; CI check blocking oversize PRs cheaper than reviewer send-back; layered automation (pre-commit → CI build → CI test → pre-deploy). [verified: 2026-09-13, fetch_content]
3. Incremental Code Review skill, MCP Market (Claude Code skill) — re-reviews focus only on new commits, verify critical/important fixes, anti-noise filtering for tech-debt/style, scope enforcement preventing new issues in untouched code. [verified: 2026-09-13, fetch_content]
4. `routing-integration.md` (crew-research-council, OUTPUT/) — gate <10 min block, async large suites, evidence-bound verdicts (SPEC→RED→GREEN→suite→review→verdict); this deep-dive extends it with critic time-box + path-awareness + partial verdicts. [verified: 2026-09-13, gh api]
5. BSSw "Pull Request Size Matters" — >400 lines changed considered too large for single review (cited via search snippet Cycle 3).
6. P4/Helix Swarm Files config docs — files >100 KB paginated in review UI (precedent: size-based review degradation is standard). [search Cycle 3]
