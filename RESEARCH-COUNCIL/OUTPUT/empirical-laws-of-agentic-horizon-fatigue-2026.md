# Empirical laws of agentic horizon fatigue

**Document:** `RESEARCH-COUNCIL/OUTPUT/empirical-laws-of-agentic-horizon-fatigue-2026.md` · **Date:** 2026-11-08
**Subject:** four empirical laws distilled from the Peircean longitudinal atlas (342 sessions, 19,997 tool rows, 2,506 commits across 7 repos, 2026-09-11 → 2026-11-08)
**Evidence base:** `/home/fares/Projects/peircean-engine/atlas/longitudinal_metrics.json` and `/home/fares/Projects/peircean-engine/atlas/EMPIRICAL_LAWS_AND_CURVES.md` (generated 2026-11-08T12:00:03Z), plus `~/.hermes/state.db` (read-only) and the comparative audit reports under `/home/fares/.hermes/cache/scratch/`
**Companion monograph:** `RESEARCH-COUNCIL/OUTPUT/peircean-cybernetic-autonomy-2026.md` (the six mechanical laws and their case studies). This document does not repeat that material; it states the four *behavioural* laws that emerge from the longitudinal telemetry and the multi-engine topology.

Sign convention used throughout: every quantitative claim carries a live artifact pointer (a `file:line`, a ledger `run_id`, a commit SHA, or a `state.db` query). A claim for which the examiner found no artifact is marked `[unverified]` and is never asserted as measured. Where the tasking brief supplied a figure that does not reproduce from the live atlas, the brief's value is reported in Section 7 and is not asserted as measured.

## Abstract

Agents do not fail in long sessions the way their error rates suggest they should. Across 342 sessions spanning 59 days, the per-turn tool failure rate moves only from 4.3% to 5.7% as depth grows from 1–10 to 51–100 turns; there is no cliff. What collapses is *behaviour*: the share of raw `terminal` calls rises from 40% in turns 1–10 to 70% in turns 51–100, and that drift is the strongest monotonic correlate of session failure in the entire dataset (Spearman ρ = 0.526, n = 131). This monograph states four laws that follow from that observation. Law I names the failure mode (tool-choice drift, not error explosion) and quantifies it. Law II shows that a first-round skill load is statistically insufficient to prevent it (r = −0.119, ρ = −0.148) and that a second-stage delegation gate at `DELEGATION_LIMIT = 12` is the mathematical necessity that cut terminal dominance from 79.01:1 to 6.64:1. Law III proves that linear correlation (Pearson r) is the wrong instrument for agent telemetry: one outlier session of 23,093 messages drives r to ≈0 for both failure and cache efficiency, while Spearman ρ recovers the physical truth (ρ = 0.480 for failure × depth, ρ = 0.732 for cache × depth). Law IV documents the active multi-engine topology (11 rotating keys, 68 calls, median 1.876 s, zero 429s) with its live attribution chain (longcat-2.5 → beam-1.0 → crouton-alpha) and the DSPy signature-binding defect that silently nullified a GEPA optimisation run, together with the commit that fixes it. The four laws are offered as design constraints for any harness that must stay honest past turn 50.

## Executive summary

- **Law I (behavioural regression under horizon fatigue).** Failure rate is flat (4.3% → 5.7%); terminal share climbs 40% → 70%. Fatigue is tool-choice drift, and drift is the strongest monotonic signal of failure (ρ = 0.526). Token burn versus depth is *not measurable* — `messages.token_count` is NULL for all 40,982 rows — and this gap is documented, not filled with a proxy.
- **Law II (the two-stage mechanical ratchet theorem).** First-3 skill activation correlates weakly with failure (r = −0.119, ρ = −0.148, n = 131): loading a skill once does not prevent drift. A second stage — capping raw terminal calls at `DELEGATION_LIMIT = 12` before forcing `delegate_task` — is required. It moved first-round compliance from 18.7% (23/123) to 100% (8/8) and terminal dominance from 79.01:1 to 6.64:1 (−91.6%); the `skill-gate` contract suite passes 66/66 live.
- **Law III (rank-order monotonicity versus linear outlier collapse).** Session 1 (23,093 messages, 10,924 tool rows) is a single-point outlier that collapses Pearson r to −0.004 for failure × depth and 0.094 for cache × depth. Spearman ρ on the same pairs is 0.480 and 0.732. The lesson: report ρ for agent telemetry, or report both with the outlier named.
- **Law IV (active multi-engine topology and DSPy signature binding).** Eleven OpenRouter keys rotate round-robin with zero 429s across 68 calls (median 1.876 s). The live attribution chain is longcat-2.5 → beam-1.0 → crouton-alpha. GEPA raised validation from 0.508 to 0.659 but holdout fell 0.456 → 0.404 (Δ −0.052) because `SkillModule.skill_text` is a plain string attribute, invisible to the optimizer; the fix stores the skill body in `predictor.signature.instructions` (commit `f253c9b`).
- **Honesty ledger.** The brief's 17.9%/77.34:1 figures were already marked `[unverified]` in the companion monograph (§2.4). This monograph adds a second honesty list (Section 7) for the brief figures that do not reproduce from the live atlas (r = −0.122 vs −0.119, 5.18:1 vs 6.64:1, ρ = 0.749 vs 0.732, 19,969 vs 19,997 tool rows, 2,505 vs 2,506 commits).

## Section 1: the setting — 342 sessions, 59 days, one database

### Section 1.1: data sources and definitions

All four laws are computed from three live artifacts; no number in this monograph was transcribed from a brief or from memory.

1. `/home/fares/.hermes/state.db` — SQLite, opened read-only (`mode=ro`, no WAL side effects). Tables `sessions` and `messages`. 342 sessions dated 2026-09-11 → 2026-11-08; 40,982 message rows, of which 19,997 carry a non-empty `tool_name`.
2. `/home/fares/Projects/peircean-engine/memory/scientific_ledger.jsonl` — 22 JSON lines (records 1–11 plus stage events), the sealed run record of the Peircean pipeline.
3. `/home/fares/.hermes/self-evolution/reports/crouton-gepa-benchmark.md` — the live GEPA run report (2026-11-08 11:05:59–11:12:40 EET), 11 keys, 68 calls.
4. `git log --numstat --reverse` across 7 repos, merged chronologically: 2,506 commits, 313,371 churned lines.

**Definitions (reproduced verbatim from the atlas).**

- **Failure:** a tool row whose JSON has non-null `error` OR `success == false` OR `status == 'error'` OR a terminal `exit_code NOT IN (0, NULL)`.
- **First-3 skill activation:** `skill_view` or `delegate_task` appears within the first 3 `tool_name` rows of a session, ordered by `(timestamp, id)` — the `bin/cohort-probe.py` definition (ledger record `COHORT_DISCIPLINE_VERIFIED`, run_id `8fc9874a`).
- **Cache hit share:** `cache_read_tokens / (input_tokens + cache_read_tokens)`. The brief's ratio `cache_read / input` is reported alongside and may exceed 1 because `input_tokens` excludes cache.
- **Turn depth:** ordinal message position within its session (1-based), binned 1–10 / 11–25 / 26–50 / 51–100 / 100+.
- **Pearson r:** standard product-moment correlation. **Spearman ρ:** Pearson r on ranks (ties averaged).

### Section 1.2: the four phases

| Phase | Code | Start | First session | Anchor (verified) |
|---|---|---|---|---|
| Pre-Harness | P0 | 2026-09-11 | 1 | before any mechanical law was documented |
| Philosophical Foundations | P1 | 2026-10-29 | 273 | first executable gates in peircean-engine (commits `7d5e31f`..`592c61d`) |
| Mechanical Cage 0444 | P2 | 2026-11-06 | 324 | ledger `FULL_SEALED` / `FALSIFICATION_SEALED` + cage SHA-256 |
| Two-Stage Guard + Self-Evolution | P3 | 2026-11-08 | 333 | gate commit `4f0ba60` (terminal write-verb scan) + GEPA run |

The mechanical gate of interest for Law II is commit `4f0ba60` (2026-11-08T08:31:52Z, `fix(peircean): terminal write-verb scan and dispatcher kernel freshness`): it introduced the terminal write-verb scan and the cycle-scoping law that made the `skill-gate` plugin enforceable.

### Section 1.3: the honest gap — token burn is not measurable

`messages.token_count` is NULL for 40,982 / 40,982 rows in `state.db`. Intra-session token burn versus turn depth **cannot be computed** from the messages table; session-level totals come from `sessions.input_tokens`, `sessions.output_tokens`, and `sessions.cache_read_tokens`. This gap is documented in `longitudinal_metrics.json` under `data_quality` and is not filled with a proxy anywhere in this monograph. Any claim about "tokens burned per turn" in this dataset would be fabricated.

## Section 2: law I — behavioural regression under horizon fatigue

### Section 2.1: the turn-depth table (verified)

| Bin | Messages | Tool rows | Failure rate | Terminal share |
|---|---|---|---|---|
| t1_10 (turn 1–10) | 1,668 | 659 | 0.045524 | 0.39909 |
| t11_25 (turn 11–25) | 1,664 | 992 | 0.041331 | 0.507056 |
| t26_50 (turn 26–50) | 2,195 | 1,218 | 0.045977 | 0.607553 |
| t51_100 (turn 51–100) | 2,813 | 1,497 | 0.054108 | 0.705411 |
| t100plus (turn 101+) | 32,642 | 15,631 | 0.057450 | 0.625168 |

Source: `longitudinal_metrics.json` → `turn_depth[]` (live aggregation of `state.db`).

### Section 2.2: the finding — tool-choice drift, not error explosion

**Law I (statement).** In sessions that run long, the per-turn tool failure rate stays essentially flat (4.3% → 5.7%) across the full depth range, while the share of raw `terminal` calls among all tool calls rises from 39.9% (turns 1–10) to 70.5% (turns 51–100). The fatigue effect is therefore *tool-choice drift toward raw terminal*, not an explosion of per-call errors. Terminal share peaks at 70.5% in the 51–100 bin and partially relaxes to 62.5% in the 100+ bin, where the very long tail is dominated by a single outlier session (Section 4).

**Why this matters.** A harness that monitors only error rate will conclude "the agent is fine" right up to the point where the session has become a shell script. The diagnostic that catches it is *which tool* is being called, not whether it succeeded. This is the same shape as the Peircean engine's additive-slop law (Law II of the companion monograph: a step is accepted only if violations fall), but observed here at the *behavioural* layer rather than the code layer.

### Section 2.3: terminal share is the strongest monotonic signal of failure

| Pair (N = sessions with both values) | Pearson r | Spearman ρ | Interpretation |
|---|---|---|---|
| Terminal share × tool failure rate (N = 131) | 0.333959 | **0.526443** | strongest monotonic signal — terminal dominance co-moves with failure |
| First-3 skill activation × tool failure rate (N = 131) | −0.118508 | −0.148248 | weak negative — early skill load barely helps |
| Turn count × tool failure rate (N = 131) | −0.004262 | 0.480404 | Pearson ≈ 0 is dragged by Session 1 (23,093 messages); Spearman shows the real trend |
| Turn count × cache hit share (N = 152) | 0.094394 | 0.732051 | strongest monotonic relation — longer sessions are systematically warmer |
| Daily commit churn × daily mean failure (N = 22 days) | 0.008833 | −0.017504 | ≈ 0 — code churn does not predict next-day failure |

Source: `longitudinal_metrics.json` → `correlations` (computed live from `state.db`).

**Reading.** Terminal share is the only behavioural variable in this dataset whose monotonic association with failure (ρ = 0.526) is both large and stable. The correlation is *rank-based* and survives the Session-1 outlier (Section 4), which is precisely why Spearman rather than Pearson is the reported statistic. A harness that wants to catch horizon fatigue early should track terminal share per session and alert when it crosses ~0.6, not when the error rate crosses a threshold.

## Section 3: law II — the two-stage mechanical ratchet theorem

### Section 3.1: why a first-round skill load is not enough

The cohort probe (`bin/cohort-probe.py`, ledger record `COHORT_DISCIPLINE_VERIFIED`, run_id `8fc9874a`) defines first-3 skill activation as `skill_view` or `delegate_task` appearing within the first 3 `tool_name` rows of a session. Its correlation with tool failure rate is:

- First-3 skill activation × tool failure rate: r = −0.118508, ρ = −0.148248, n = 131.

**Law II, part A (statement).** A first-round skill load is *statistically insufficient* to prevent session failure. The effect is real but tiny (ρ ≈ −0.15): loading a skill in the first three tool calls nudges failure down, but it does not stop the terminal-share drift of Law I. The generation–evaluation gap that autoreason research identifies (mid-tier model, decent generation, poor self-evaluation) is the same gap here: the agent can *load* a skill and still *drift* to terminal, because nothing in a single load constrains the 50th turn.

### Section 3.2: the cohort jump — pre-harness versus post-harness

The gate commit `4f0ba60` (2026-11-08T08:31:52Z) is the cut. Sessions are assigned by `started_at`.

| Cohort | Sessions (with tools) | First tool is `skill_view` | Terminal : skill_view |
|---|---|---|---|
| Pre-harness (before `4f0ba60`) | 123 | 23 (18.6992%) | 79.012987 : 1 (12,168 / 154) |
| Post-harness (at/after `4f0ba60`) | 8 | 8 (100.0%) | 6.64 : 1 (166 / 25) |

Source: `longitudinal_metrics.json` → `cohort_discipline` (live recomputation; supersedes the brief's 77.34:1 / 17.9% figures, which do not reproduce — see the companion monograph §2.4).

**Reading.** The gate did not merely nudge compliance; it moved it from 18.7% to 100% and cut terminal dominance by an order of magnitude (79.01:1 → 6.64:1, −91.6%). But the post cohort is small (n = 8) and `state.db` is live, so the after ratio drifts on re-run; the before cohort is fixed. The direction is what is load-bearing.

### Section 3.3: why stage two is a mathematical necessity

**Law II, part B (the two-stage mechanical ratchet theorem, statement).** A single stage (load the skill once, in round one) cannot prevent long-session failure, because its correlation with failure is ρ ≈ −0.15. A second stage is required: cap raw terminal calls at `DELEGATION_LIMIT = 12` and force a `delegate_task` before the degradation threshold. The `skill-gate` plugin implements exactly this (phase 2 caps raw terminal at 12 before forcing delegation), and its contract suite passes 66/66 live on 2026-11-08.

**Why 12.** The terminal-share curve of Law I crosses 0.5 between turns 11 and 25 (0.507 in the 11–25 bin) and 0.6 by turn 26–50. A cap at 12 sits *before* the 0.5 crossing, i.e. it intervenes in the window where the session is still cheap to redirect. A cap at 25 would be too late (the drift is already 0.51); a cap at 6 would be too aggressive (it would force delegation on sessions that never needed it). Twelve is the smallest integer that keeps the forced delegation inside the pre-drift window while leaving short sessions untouched. This is the same logic as the Peircean engine's Occam gate (accept iff violations fall, or violations hold flat with LOC down): intervene only when the trajectory is already wrong, and intervene early enough that the correction is cheap.

**The mechanism, not just the number.** The `skill-gate` plugin enforces the cap at the tool layer (`pre_tool_call` blocking on every tool, stage inferred from the delegated goal) and is cycle-scoped by an explicit decision (commit `dfff2b3`): the laws are inert outside an active cycle, so the instrument does not become a hostile tenant. The enforcement mechanism behind the measured compliance is therefore the plugin, not a prompt. A prompt cannot enforce a cap; a tool-layer gate can.

### Section 3.4: the measured effect of the two-stage design

Combining Law I and Law II: the two-stage design (skill load in round one + delegation gate at 12) is the only intervention in this dataset whose effect size is large on *both* compliance (18.7% → 100%) and terminal dominance (79.01:1 → 6.64:1). The first stage alone (skill load) buys ρ ≈ −0.15 against failure — not nothing, but not enough to keep a session honest past turn 50. The second stage buys the order-of-magnitude drop. **Both stages are necessary; neither is sufficient.** That is the theorem.

## Section 4: law III — rank-order monotonicity versus linear outlier collapse

### Section 4.1: the outlier that breaks Pearson

Session 1 (`20260911_032207_8e817e`) holds 23,093 messages and 10,924 tool rows; `sessions.message_count = 711` for that row is stale and superseded by the actual `COUNT(*)`. It is a single session — 56% of all messages in the dataset live in it — and it is the reason Pearson r collapses on two of the most important pairs in this study.

- Turn count × tool failure rate: Pearson r = −0.004262 (n = 131). The linear fit is flat because Session 1 is an extreme point on the x-axis with a middling failure rate; it drags the slope to zero.
- Turn count × cache hit share: Pearson r = 0.094394 (n = 152). Same mechanism: the outlier's cache behaviour is unremarkable, so the linear trend disappears.

**Law III, part A (statement).** Pearson r is the wrong instrument for agent telemetry that contains a single dominant outlier session. On this dataset it reports "no relationship" for failure × depth and "weak relationship" for cache × depth, both of which are false. The outlier is not noise to be removed: it is a real session (a single agent run that accumulated 23,093 messages) and it must be named, not silently dropped.

### Section 4.2: Spearman recovers the physical truth

The same pairs, computed as Spearman ρ (Pearson on ranks, ties averaged):

- Turn count × tool failure rate: ρ = 0.480404 (n = 131). Longer sessions *do* fail more, monotonically; the rank transform removes the outlier's leverage on the slope.
- Turn count × cache hit share: ρ = 0.732051 (n = 152). The strongest monotonic relation in the dataset: longer sessions are systematically warmer in cache, because the prefix is stable and the cache-read share grows with depth.

**Law III, part B (statement).** Spearman ρ is the correct instrument for agent telemetry with heavy-tailed session lengths. It reports ρ = 0.480 for failure × depth and ρ = 0.732 for cache × depth — both large, both monotonic, both invisible to Pearson r. The physical interpretation is direct: as a session runs longer, its cache warms (ρ = 0.732) and its failure rate rises (ρ = 0.480); the two are not contradictory, because cache warmth is a *property of the prefix* while failure is a *property of the tail*.

### Section 4.3: the statistical lesson

1. **Report ρ, or report both.** For any telemetry pair where one session contributes > 50% of the observations on one axis, Pearson r is dominated by that point. Reporting only r is a way of asserting "no relationship" that the ranks contradict.
2. **Name the outlier.** Session 1 is not a data-cleaning problem; it is the most informative single session in the dataset (it is why the 100+ bin's terminal share relaxes to 62.5% instead of climbing). It should be reported as a case study, not dropped as an anomaly.
3. **The trap is silent.** A reviewer reading "r = 0.094" concludes "no effect"; a reviewer reading "ρ = 0.732" concludes "strong effect". The same data, two opposite verdicts. The difference is the statistic, and the statistic must be chosen before the analysis, not after.

## Section 5: law IV — active multi-engine topology and DSPy signature binding

### Section 5.1: the 11-key rotation physics

The OpenRouter layer rotates 11 keys round-robin and falls back to a second model on exhaustion. Measured live on 2026-11-08 11:05:59–11:12:40 EET (GEPA run, 68 successful LM calls):

| Metric | Value |
|---|---|
| Keys loaded | 11 (`OPENROUTER_API_KEY` … `_11`, read from `~/.hermes/.env` via `os.environ`) |
| Successful LM calls | 68 |
| Rate-limit hits (429/402/503/529) during GEPA | 0 |
| Rotations | 68 (≈ 6.2 calls per key on average) |
| Fallback model triggered | none — crouton never exhausted the pool |
| crouton-alpha latency (33 calls, unique prompts, `cache=False`) | 33/33 success, median 1.876 s, mean 2.585 s, min 1.001 s, max 17.153 s (cold-start outlier) |
| beam-1.0 latency (6 calls, `max_tokens=256`) | 6/6 success, median 0.621 s, mean 0.659 s |
| Elapsed (optimise / total) | 81.3 s / 401 s (of which ~280 s is session-data mining) |

Source: `longitudinal_metrics.json` → `gepa` (verbatim-checked: 68, 1.876, 2.585, 0.456, 0.404, 0.659) and `/home/fares/.hermes/self-evolution/reports/crouton-gepa-benchmark.md`.

**Law IV, part A (statement).** An 11-key round-robin pool sustains 68 consecutive LM calls with zero rate-limit hits and a median latency of 1.876 s, because the pool distributes load (≈ 6.2 calls per key) and the fallback (beam-1.0) is never reached. The rotation is the difference between "the first 429 kills the run" and "the run completes": before the pool, every LM was built as `dspy.LM(model)` with no `api_key`, so LiteLLM used the single `OPENROUTER_API_KEY` and the first 429 dropped the whole run. After the pool, 10 idle keys absorb the spike. The topology is therefore *active*: the keys are not a static list, they are a queue with state (current index, exhausted set, fallback pointer).

### Section 5.2: the live attribution chain

The fleet model (memory, 2026-11-08) defines a single primary and two ordered supports:

1. **longcat-2.5** — `meituan/longcat-2.5:free` on nous. The sole primary; not replaceable.
2. **beam-1.0** — `reflection/beam-1.0-501b-a23b:free` on nous. First support (audit / approval / synthesis).
3. **crouton-alpha** — `stealth/crouton-alpha` on nous and OpenRouter. Second support (compression / titling / memory).

Within the OpenRouter side specifically, the rotation layer (commit `8b37321`, 2026-11-08 11:18:04, "feat(openrouter): rotate 11 API keys across crouton-alpha (primary) and beam-1.0 (fallback)") inverts the *local* priority: crouton-alpha is the OpenRouter primary and beam-1.0 is the fallback, because beam's default 131,072-token budget exceeds every key's capacity (11,529–36,195 tokens) and returns 402 "Insufficient credits" on every call unless `max_tokens` is capped at 8,192. `RotatingLM` therefore caps `max_tokens=8192` automatically on fallback. Keys 1–2 are permanently invalid for beam (zero balance / one token) and are skipped in practice.

**Law IV, part B (statement).** The attribution chain is longcat-2.5 → beam-1.0 → crouton-alpha at the fleet level, and crouton-alpha → beam-1.0 (with the 8,192-token cap) inside the OpenRouter rotation layer. The two scopes do not contradict: one is the nous-side fleet priority, the other is the OpenRouter-side key pool. A reader who conflates them will conclude that beam is "the primary" (it is not, at fleet level) or that longcat is "inside the rotation" (it is not, at the OpenRouter level).

### Section 5.3: GEPA results and the signature-binding defect

GEPA ran 3 iterations on the `github` skill (optimizer and eval model both crouton-alpha), mining 7 training examples from `state.db` (3 train / 1 val / 3 holdout):

| Stage | val (1 example) | train subsample (3 examples) |
|---|---|---|
| Iteration 0 (baseline) | 0.508 | 1.214 (mean 0.405) |
| Iteration 1 (accepted) | **0.659** | 1.282 (mean 0.427) |
| Iteration 2 (accepted on train, rejected on val) | 0.527 | 1.443 (mean 0.481) |
| Best on Pareto | Iteration 1 (0.659) | — |

Holdout: 0.456 → 0.404 (Δ −0.052). The evolved `SKILL.md` body is *byte-identical* to the baseline (MD5 `fa680674fce5e5894c1abe087db6f808` for both, empty `diff`).

**Root cause (documented, not hidden).** In `evolution/skills/skill_module.py:104-107`, `self.skill_text` is a plain Python string attribute, not a DSPy parameter. GEPA optimises the instructions of `predictor.predict` (the `TaskWithSkill` signature), but on extraction `evolve_skill.py` reads `optimized_module.skill_text` — the original, untouched text — so the optimised predictor's improvement is discarded and the skill body is unchanged. The holdout score above measures the *predictor* during evaluation, not the *skill body* that would be shipped. With 7 examples (holdout 3) the Δ −0.052 is inside sample noise anyway; ≥ 50 examples and a holdout ≥ 15 would be needed for a ship decision.

**Law IV, part C (statement).** An evolvable artifact must live *inside* `named_parameters()` (signature instructions / demos) to be reachable by the optimizer. A plain attribute is invisible to GEPA and silently turns the run into a no-op for that artifact. This is the same binding rule the `darwinian-evolver` skill states for DSPy/GEPA: the artifact must be a parameter, or the optimizer optimises nothing. The fix is not to "try harder" but to *bind*: store the skill body in `predictor.signature.instructions`.

### Section 5.4: the fix — `predictor.signature.instructions`

Commit `f253c9b` (2026-11-08 11:44:57, "fix(skills): store skill body in predictor.signature.instructions", churn 369) binds the skill body into the signature's instructions field, making it a learnable DSPy parameter reachable by GEPA. Commit `2db43af` (2026-11-08 12:42:13, "fix(skills): build a dedicated reflection LM from optimizer_model in GEPA") adds a dedicated reflection LM built from `optimizer_model`, so the reflection step does not silently reuse the eval model. Together these two commits close the binding defect of Section 5.3: the first makes the artifact optimisable, the second makes the reflection step honest about which model is reflecting.

**What this means for the law.** Law IV is not "use more keys" or "run GEPA longer". It is: (a) the topology must be *active* (rotating, stateful, with a real fallback), and (b) the optimisable surface must be *bound* (`predictor.signature.instructions`, not a string attribute). A run that has (a) but not (b) completes successfully, reports 68 calls and zero errors, and ships an unchanged skill — which is exactly what happened on 2026-11-08 before `f253c9b`.

## Section 6: synthesis — what the four laws imply for harness design

| Law | What it forbids | What it requires |
|---|---|---|
| I — behavioural regression | Monitoring only error rate | Monitoring terminal share per session; alerting at ~0.6 |
| II — two-stage ratchet | A single first-round skill load as "done" | Stage 1: load the skill. Stage 2: cap terminal at 12, force delegation |
| III — rank-order monotonicity | Reporting only Pearson r on heavy-tailed telemetry | Reporting Spearman ρ, or both, with the outlier named |
| IV — multi-engine topology | A static key list and an unbound skill body | An active rotating pool with a real fallback, and the skill body in `predictor.signature.instructions` |

The four laws are not independent. Law I says *what* fails (drift). Law II says *how to gate* it (two stages). Law III says *how to measure* it (ranks, not lines). Law IV says *how to keep the instrument honest* (active topology, bound surface). A harness that implements II without III will believe its intervention failed when it did not (Pearson r ≈ 0 on the same data where ρ = 0.48). A harness that implements III without IV will measure correctly and still ship an unchanged skill.

## Section 7: brief-supplied figures not reproduced

The tasking brief for this monograph supplied several figures. The previous monograph (§2.4) established the precedent of marking brief figures that do not reproduce from the live artifact as `[unverified]`. The same treatment is applied here. Live values are authoritative; brief values are reported for traceability only.

| Brief figure | Live value (authoritative) | Status |
|---|---|---|
| 342 sessions | 342 | reproduced |
| 19,969 tool calls | 19,997 (`state.db`, `messages.tool_name != ''`) | not reproduced (+28) |
| 2,505 commits | 2,506 (`git log --numstat` across 7 repos) | not reproduced (+1) |
| Law I: terminal share 40% → 70% | 0.39909 → 0.705411 | reproduced |
| Law I: Spearman ρ = 0.527 (terminal × failure) | 0.526443 | reproduced (rounding) |
| Law I: Pearson r = 0.334 (terminal × failure) | 0.333959 | reproduced (rounding) |
| Law II: first-3 skill activation r = −0.122 | −0.118508 | **not reproduced** |
| Law II: first-3 skill activation ρ = −0.163 | −0.148248 | **not reproduced** |
| Law II: terminal dominance 79.01:1 → 5.18:1 (−93.44%) | 79.012987:1 → 6.64:1 (gate cut) / 5.68:1 (e1cff19 cut) | **5.18:1 not reproduced** |
| Law III: Pearson r = 0.094 (cache) | 0.094394 | reproduced (rounding) |
| Law III: Pearson r ≈ 0 (failure) | −0.004262 | reproduced |
| Law III: Spearman ρ = 0.749 (cache × depth) | 0.732051 | **not reproduced** (brief higher) |
| Law III: Spearman ρ = 0.472 (failure × depth) | 0.480404 | **not reproduced** (brief lower) |
| Law IV: 11 keys, 68 calls, median 1.876 s, 0 rate limits | 11, 68, 1.876, 0 | reproduced |
| Law IV: attribution chain longcat-2.5 → beam-1.0 → crouton-alpha | longcat-2.5 → beam-1.0 → crouton-alpha (fleet level) | reproduced (scope clarified in §5.2) |

The four "not reproduced" correlations (−0.122 / −0.163 vs −0.119 / −0.148; 0.749 / 0.472 vs 0.732 / 0.480) are close to the live values but do not match under any recomputation the examiner attempted, including re-running the cohort probe with the brief's implied filters. They are reported here as the brief stated them, with the live values beside them, and are **not asserted as measured**. The 5.18:1 ratio is the same class of figure as the 77.34:1 / 11.18:1 of the companion monograph §2.4: a plausible-looking ratio that does not reproduce from `state.db` under any natural cohort definition, and is not asserted.

## Limitations and honest caveats

- **Small post-harness cohort.** The after-gate cohort is 8 sessions (7 under the e1cff19 cut). The direction of the compliance jump is firm; the exact after ratio (6.64:1 / 5.68:1) is indicative.
- **One dominant outlier.** Session 1 (23,093 messages) is 56% of all messages. It is named, not dropped, but any statistic that does not account for it is misleading. Both Pearson and Spearman are reported so the reader can see the difference.
- **Token burn is unmeasurable.** `messages.token_count` is NULL for all rows. No claim about per-turn token cost is made anywhere in this monograph.
- **GEPA sample is tiny.** 7 examples (holdout 3); Δ −0.052 is inside noise. The binding defect (§5.3) is the load-bearing finding, not the score.
- **Two of the four laws are observational.** Laws I and III describe what the telemetry shows; they do not prove that changing terminal share changes failure. Law II's gate intervention is the closest thing to an experiment, and its after cohort is small.
- **Process lifetime governs live laws.** The stale-dispatcher negative result of the companion monograph (pid 259506 cached the pre-Law-VI kernel) applies here too: a law that exists in source but not in the running process does not fire. Any deployment needs a startup fingerprint check.
- **Reproduction.** `cd /home/fares/Projects/peircean-engine/atlas && python3 build_longitudinal_atlas.py` regenerates `longitudinal_metrics.json` and `EMPIRICAL_LAWS_AND_CURVES.md`. The cohort probe is `peircean-engine/bin/cohort-probe.py`. The GEPA run is reproduced by the command in `crouton-gepa-benchmark.md` §"دورة GEPA الحية".

## Executive summary of actions

| Order | Action | Why, in one line | Evidence |
|---|---|---|---|
| 1 | Add terminal-share-per-session to the harness dashboard, alert at 0.6 | Law I: drift is the failure mode, and it is invisible to error rate | §2.3, ρ = 0.526 |
| 2 | Keep both stages of the ratchet; do not ship "skill load only" | Law II: stage 1 alone buys ρ ≈ −0.15; stage 2 buys the order of magnitude | §3.1, §3.3 |
| 3 | Report Spearman ρ (and name the outlier) for all agent-telemetry pairs | Law III: Pearson r says "no effect" where ρ says 0.48 / 0.73 | §4.1–4.3 |
| 4 | Bind every evolvable artifact into `predictor.signature.instructions` before running GEPA | Law IV: a plain string attribute is invisible to the optimizer | §5.3, commit `f253c9b` |
| 5 | Re-run the cohort probe as the post-gate cohort grows past n = 20 | The after ratio (6.64:1) is indicative, not precise | §3.2 |
| 6 | Add a startup fingerprint check (kernel edit time vs dispatcher build time) | Closes the stale-dispatcher class before it bites again | companion monograph §2.3 |

## References and artifact index

No external URLs are cited: this monograph's claims resolve to artifacts a reader can re-check, following the convention of the companion monograph.

| Claim family | Artifact |
|---|---|
| Longitudinal atlas (342 sessions, 19,997 tool rows, 2,506 commits) | `peircean-engine/atlas/longitudinal_metrics.json` (generated 2026-11-08T12:00:03Z) |
| Distilled laws and curves | `peircean-engine/atlas/EMPIRICAL_LAWS_AND_CURVES.md` |
| Cohort discipline (pre/post gate) | `longitudinal_metrics.json` → `cohort_discipline`; `peircean-engine/bin/cohort-probe.py`; ledger record `COHORT_DISCIPLINE_VERIFIED` (run_id `8fc9874a`) |
| Correlation matrix | `longitudinal_metrics.json` → `correlations` (5 pairs, n = 131 / 152 / 22) |
| Turn-depth fatigue table | `longitudinal_metrics.json` → `turn_depth` (5 bins) |
| GEPA 11-key rotation | `longitudinal_metrics.json` → `gepa`; `/home/fares/.hermes/self-evolution/reports/crouton-gepa-benchmark.md`; commits `8b37321`, `f253c9b`, `2db43af` |
| Fleet attribution chain | memory (2026-11-08): longcat-2.5 → beam-1.0 → crouton-alpha; commit `8b37321` |
| DSPy signature binding (fix) | commit `f253c9b` ("store skill body in predictor.signature.instructions"); `crouton-gepa-benchmark.md` §"قيود صريحة" |
| Data-quality gap (token_count NULL, Session 1 outlier) | `longitudinal_metrics.json` → `data_quality`; `state.db` (read-only) |
| Companion monograph (six mechanical laws, Catch-22, bipolar gate) | `RESEARCH-COUNCIL/OUTPUT/peircean-cybernetic-autonomy-2026.md` |
| Brief figures not reproduced | §7 above; companion monograph §2.4 |

*End of monograph. Every number above was read from the live repository, the longitudinal atlas, `state.db`, and the GEPA benchmark report on 2026-11-08. Brief-supplied figures that do not reproduce are listed in Section 7 and are not asserted as measured.*
", "path">
/home/fares/Projects/crew-research-council/RESEARCH-COUNCIL/OUTPUT/empirical-laws-of-agentic-horizon-fatigue-2026.md