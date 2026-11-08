# Peircean cybernetic autonomy: mechanical laws against collusion and hallucination

**Document:** `RESEARCH-COUNCIL/OUTPUT/peircean-cybernetic-autonomy-2026.md` · **Date:** 2026-11-08
**Subject:** the Peircean Engine (v3.1.0 · pipeline `PEIRCEAN-SCIENTIFIC-RATCHET-V4` · kernel schema 3.0.0)
**Evidence base:** `peircean-engine/docs/SCIENTIFIC_FOUNDATIONS.md` and `peircean-engine/memory/scientific_ledger.jsonl`
(20 JSON lines), plus the comparative audit reports found under `/home/fares/.hermes/cache/scratch/`
(`forensic-report.txt`, `forensic-data.json`).

Sign convention used throughout this monograph: every quantitative claim carries a live artifact
pointer (a `file:line`, a ledger `run_id`, or a SHA-256). A claim for which the examiner found no
artifact is marked `[unverified]` and is never asserted as measured.

## Abstract

Contemporary software-engineering agents fail for method reasons, not capacity reasons: they grade
their own exams (illusory self-evaluation), they are judged by models that share their habits
(LLM-as-a-judge collusion), they optimise the metric instead of the behaviour (Goodhart's law),
and they grow code instead of shrinking it (additive slop). The Peircean Engine is a
zero-dependency instrument that relocates the verdict from the model to the repository itself —
its own gate command plus a cryptographically sealed adversarial cage — and lets a full
falsification-and-repair cycle run end to end without human supervision. The human re-enters only
to review a ledger of oracle-locked boundaries: findings whose only remedy would mutate the test
oracle, which is a teleological decision, not a surgical one. This monograph states the autonomy
thesis, proves it against the live ledger (reductive distillation from 9 to 1 violations, a
mechanical Catch-22 created and dissolved, a bipolar anti-gaming gate enforced at two seal
points), and maps three high-impact conversion paths: conference papers, open-source
contributions to agent frameworks, and independent verification products for companies.

## Executive summary

- **Thesis.** A scientific instrument is defined not by the intelligence of its operator but by
  the impossibility of its own self-deception; the engine buys that impossibility with filesystem
  permissions, cryptographic hashes, and a ratchet that only moves in one direction
  (`docs/SCIENTIFIC_FOUNDATIONS.md:22`).
- **Autonomy shape.** Five specialised agents (xray-prober, illusion-breaker, iron-prosecutor,
  surgeon-03, niche-distiller) run a full red-to-green cycle alone. The only human-visible output
  is the `oracle_locked_boundaries` list and the occasional `SCIENTIFIC_HALT`. That is
  human-out-of-the-loop operation with a boundary ledger, not human-in-the-loop supervision.
- **Proof cluster 1.** On `dsh-rtl-bidi`, reductive distillation moved `total_violations` 9 →
  1 with `total_loc` and `total_functions` unchanged (613, 24), because the single remaining
  violation is `event.data` at `client.js:270` — the DOM `MessageEvent.data` contract, which
  RULE 0 forbids rewriting (ledger record 10, `run_id 22bba231…`).
- **Proof cluster 2.** On `dsh-compaction-plus`, a locus-only arbitration sealed a 6-trap cage
  (SHA-256 `1530165d…`) that the surgeon could not close in 7 attempts — a mechanical Catch-22.
  Remediation-aware arbitration collapsed it to exactly 1 legal trap (`TRAP-01-ENFORCECAP-MODE-0600`,
  cage SHA-256 `1163ef34…`) with `src/spill.ts` patched (+10 LOC), gate exit 0, trap `PASS_CAUGHT`
  (ledger records 7–9).
- **Proof cluster 3.** Law VI (dual-polarity cages, anti-overfitting) was enforced at both seal
  points on the same target repo: a degenerate single-state cage was refused with
  `DEGENERATE_SINGLE_STATE_TRAP`, and a green patch echoing a cage-only literal was refused with
  `OVERFITTED_LITERAL_ECHO_DETECTED`; the one-line honest repair then sealed green, 22/22 tests
  (ledger record 11, field experiment §4.7 of the foundations document).
- **The discipline figure.** Section 2.4 now measures the discipline jump directly from
  `/home/fares/.hermes/state.db`: first-turn skill compliance 15.4% (19/123) before commit
  `e1cff19` rising to 100% (7/7) after, with the terminal-to-skill ratio falling from 79.01:1
  to 5.68:1. The tasking brief's figures (17.9% = 26/145; 77.34:1 → 11.18:1) and its proof file
  were not found and do not reproduce, so they are not asserted; the verifiable proxies for
  "the laws bite" remain those in §§2.1–2.3 and the engine gate 58/58 (94/94 per ledger record 11).

## Section 1: human-out-of-the-loop scientific autonomy and how six mechanical laws break agent collusion and hallucination

### Section 1.1: four failure modes of contemporary agents

The failures below are stated in the foundations document with their detection sites; each is a
method failure with a mechanical countermeasure (§1.3).

**Illusory self-evaluation.** An agent asked to evaluate its own output is a graded student grading
their own exam: the judge inherits the generator's blind spots. The engine names the five
fabricated-certainty signals it scans for (`agents/illusion-breaker/mcp-server/index.js:272-340`):
`TAUTOLOGICAL_ASSERTION` (`assert.ok(true)`), `SWALLOWED_EXIT_CODE` (`|| true`, empty `catch {}`),
`ZERO_ASSERTION_TEST` (cases declared, nothing asserted), `SELF_GRADING_MOCK` (assertions scored
against a local stub sharing the test's own assumptions), and `SYNTHETIC_PERFECT_BENCHMARK`
(a perfect score from a deterministic synthetic loop). The first three were empirically verified
on the e2e testbed (ledger record 1 in Appendix A of the foundations document): the run's summary
lists exactly `SYNTHETIC_PERFECT_BENCHMARK`, `SWALLOWED_EXIT_CODE`, `TAUTOLOGICAL_ASSERTION`.

**LLM-as-a-judge collusion.** When the same model family generates and judges, the score measures
fluency, not truth. The countermeasure is architectural: the judge is not a model at all. It is the
repository's own gate command plus the sealed adversarial cage, whose verdict vocabulary is binary
and mechanical (`TRAP_RESULT:<ID>:FAIL_EXPOSED | PASS_CAUGHT`, `agents/common/peircean-kernel.js:309-325`).
A model cannot flatter a `chmod 0444` file.

**Goodhart's law.** An agent optimising a benchmark will find the shortcut that moves the score
without moving the behaviour. The countermeasure is the Double-Blind Test Oracle lock: the
measurement instrument (tests, `verify/`, the gate definition in `package.json` and
`.github/workflows/`) is removed from the optimisable surface entirely
(`peircean-kernel.js:32-57`). The agent cannot move the score because the score is not editable;
the only remaining way to turn the cage green is to change production behaviour.

**Additive slop.** The path of least resistance for a helpful agent is addition: a new wrapper, a
new helper, a new abstraction. The countermeasures are the Mechanical Git Ratchet and the Occam
gate: a step is accepted only if the violation count falls, or if violations hold flat while LOC
falls and the function count does not grow (`agents/niche-distiller/mcp-server/index.js:493-504`).
A step that adds functions without reducing violations is reverted with
`FUNCTION_INFLATION_REJECTED`; a repair that increases clone clusters or wrapper slops is reverted
with `OCCAM_BLOAT_REJECTED` (`agents/surgeon-03/mcp-server/index.js:808`).

### Section 1.2: why the judge cannot be a model

Peirce's three modes of inference are orthogonal, not sequential stages of one method, and the
engine assigns each mode to a different agent so that no agent can be its own judge:

| Mode | Question it answers | Engine realisation | Agent |
|---|---|---|---|
| Abduction | What hypothesis would explain this surprising fact? | Illusion hunting: a documented claim compared against an empirical execution in the shadow lab | `illusion-breaker` |
| Deduction | What must be true if the hypothesis holds — what trap would it necessarily spring? | Trap locking: a cryptographically sealed cage that must `FAIL_EXPOSED` on the unpatched repo | `iron-prosecutor` |
| Induction | Does the repaired system actually behave as the hypothesis predicts, under constraint? | Green-phase verification: gate exit 0 + every trap `PASS_CAUGHT` + Occam gate | `surgeon-03` |
| Habit (agapasm) | What must the instrument remember next time? | The ledger converts each run into a `distilled_law` appended at `bin/cybernetic-pipeline.mjs:856` | all |

Three further design facts remove the human from the loop without removing honesty:

1. **Isolation.** Every agent works in its own shadow lab (`/tmp/*_shadow_lab`), copied from the
   source with the `.git` pointer sanitised so no git operation can reach the host
   (`surgeon-03/index.js:472-490`, `iron-prosecutor/index.js:40-49`,
   `niche-distiller/index.js:148-157`). The surgeon cannot read the sealed cage before its first
   verification attempt (`BLIND_CAGE_POLICY`, `surgeon-03/index.js:559-563`), and the Hermes plugin
   refuses `handoff_01` reads during surgery at the level of every tool
   (`hermes-plugin/peircean_bridge.py:462-465`, `:484-486`).
2. **Variable isolation.** The H0 baseline is measured before any change; the H1 delta is computed
   after exactly one atomic mutation set (`niche-distiller/index.js:767-869`). One variable moves
   at a time, so the delta is attributable.
3. **Systematic doubt.** The abductive stage must produce at least three distinct illusions before
   it may commit a handoff, each carrying a substantive `abductive_hypothesis`
   (`illusion-breaker/index.js:558-561`). The instrument cannot merely assert; it must hypothesise
   — and it must also state which weak instinct it burned (`discarded_rl_instinct`), Peirce's
   "irritation of doubt" as a required field.

The attention model behind this shape is thalamic, not softmax: the repository is folded into a
skeleton whose bodies are hidden (`agents/xray-prober/mcp-server/index.js:669-686`) and only one
small focal cell is opened while a change is being made, respecting the 4 ± 1 working-memory bound
(Cowan 2001, as reviewed in the foundations document) instead of asking flat attention to hold a
whole repository.

### Section 1.3: the six mechanical laws of the kernel

Laws I–V are implemented twice — in `agents/common/peircean-kernel.js` (the authority for the MCP
servers) and in `hermes-plugin/peircean_rules.py` (a faithful in-process translation, with the JS
kernel remaining authoritative). Law VI is enforced at both seal points through the same kernel.

| Law | Name | One-line content | Enforcement anchor |
|---|---|---|---|
| I | H0 baseline measurement and thalamic skeleton folding | No delta without a sealed H0; the fold is a lossy compression with a correctness contract | `xray-prober/index.js:696-843`, shared extractor `peircean-kernel.js:423-465` |
| II | Reductive distillation, the mechanical git ratchet, and the Occam gate | Accept iff violations fall, or violations hold flat with LOC down and function count not growing | `niche-distiller/index.js:493-504` |
| III | Double-blind isolation across tools | Oracle, cage, secrets, and source repo are unreachable; all work happens in the shadow lab | three layers: filesystem, sandbox, tool hook (`peircean_bridge.py:431-490`) |
| IV | Remediation-aware oracle arbitration | A finding is cage-eligible iff locus AND remedy are both outside the oracle surface | `classifyOracleLock` (`peircean-kernel.js:516-546`); `ILLEGAL_ORACLE_REMEDIATION_CONTRACT` (`iron-prosecutor/index.js:396-432`) |
| V | The right to scientific halt and the RULE 0 contract | A halt is a first-class output; oracle, source, and cage are immutable; no green seal on a stale worktree | `*_scientific_halt` at all four stages; `GREEN_GATE_LOCKED`, `UNVERIFIED_MUTATION_DETECTED` |
| VI | Dual-polarity counterexample and anti-overfitting verification | A cage must carry at least two distinct verification sites and both polarities, and the patch may not echo any cage-only literal | `verifyCounterexamplePolarity` + `verifyAntiOverfitting` in the kernel; hooks at Red (`ip_verify_and_seal_cage`) and Green (`sg_commit_green_handoff`) |

Three of these deserve their formal statements, because they are the parts that do the work:

- **Law II (acceptance).** Let `V(R)` be the total violation count (scattering files, clone
  clusters, wrapper slops, identifier drift). A step `R0 -> R1` is accepted iff
  `tests(R1) = 0` and no category regressed and either `V(R1) < V(R0)`, or `V(R1) = V(R0)` with
  `LOC(R1) < LOC(R0)` and function count non-increasing (`niche-distiller/index.js:489-504`).
  On rejection the shadow repository is reverted with `git reset --hard HEAD` + `git clean -fd`
  and a `negative_result` is appended to `ratchet_ledger.jsonl` (`:808-829`).
- **Law III (permission).** For every tool call `t` during an active cycle,
  `permit(t)` iff the target misses the oracle surface, misses the cage, is contained in the
  shadow lab, and misses the secrets denylist (`peircean-kernel.js:354-365`, `:507-508`).
  The plugin's laws are cycle-scoped by an explicit decision (commit `dfff2b3`): they are inert
  outside an active cycle, so the instrument does not become a hostile tenant.
- **Law IV (eligibility).** A finding `f` is eligible for the cage iff
  `locus(f)` is outside the oracle surface **and** `remedy(f)` is not contained in it. A finding
  is oracle-locked if either its locus or its only remedy falls inside a protected surface. The
  surgeon never sees an unreachable trap; the instrument instead records an
  `oracle_locked_boundary` for human review.

### Section 1.4: what autonomy means here: a sealed instrument with a boundary ledger

"Partial autonomy without human supervision" has a precise shape in this engine. The machine
decides: which illusions are proven, which traps are sealed, whether a repair turns the cage
green, whether a step was ratcheted or reverted, and whether to halt. The human sees exactly two
things: the `oracle_locked_boundaries` list (findings the instrument declined to repair because the
remedy would mutate a protected surface — a disagreement with a codified specification, which only
a human may settle), and the ledger's `distilled_law` per run. Meanwhile the instrument protects
itself against its own operator's temptation: a gate is red but the baseline is still recorded,
because a red baseline is data; the surgeon refuses to initialise when the upstream handoff is
missing rather than manufacturing it (ledger record 6, `run_id 50fb2266…`, `SCIENTIFIC_HALT`).

## Section 2: quantitative proofs from the live lab

All values below are taken from the ledger records cited. Two production targets were measured:
`dsh-rtl-bidi` (baseline `18a375b8…`, 22/22 tests) and `dsh-compaction-plus` (HEAD `574d8cab…`,
18 files, 2000 LOC, 41 functions), plus the `/tmp/peircean_e2e_lab` testbed.

### Section 2.1: reductive distillation from 9 to 1 violations on dsh-rtl-bidi

**Setup.** Isolated `niche-distiller` profile, session
`local-851fb602fd1ed77fe78f4501a0c44da50cd60539bcb097d6fe4df6847e127733`, target
`dsh-rtl-bidi`; evidence extracted into the ledger as record 10 (run_id
`22bba231-6395-4cae-916d-640b4dfc6526`, `DISTILLATION_LAW_SEALED`).

| Metric | H0 | H1 | Δ |
|---|---|---|---|
| total_violations | 9 | **1** | −8 |
| drift_count | 9 | 1 | −8 |
| total_loc | 613 | 613 | 0 |
| total_functions | 24 | 24 | 0 |
| clone_clusters / wrapper_slop | 0 | 0 | 0 |

**What the 9 were.** All nine H0 violations were `vague_identifier` drift on the token `data` in
`onMessage` (`client.js:270-283`). The ratchet committed exactly one step
(`8328958cd7d19c9a5956e52d212768781ec9183f`) renaming the local binding `data` → `message` at the
8 renameable sites (lines 270, 271, 272, 280, 283) — sealed patch
`7dc2c40ce2ab442ace950ddf78f70513f1b24c0f3ea12bada9def6047f7188e0`, handoff
`/tmp/distiller_shadow_lab/handoff_00_distiller.json`.

**What the 1 is.** The single remaining violation is `event.data` at `client.js:270` — the DOM
`MessageEvent.data` property, i.e. the browser/framework message-passing contract. Renaming it
would break the plugin's ability to receive `postMessage` payloads. Under RULE 0 — if a reported
token cannot be renamed without breaking an external/DOM/framework contract, leave it as an
irreducible boundary — the instrument lawfully stopped at 1 violation instead of "achieving 0" by
breaking the product.

**The falsified probe is preserved, not hidden.** A first probe passed a 17-line fragment to a
whole-file tool and collapsed `client.js` to 21 lines; the run went red and was reverted
(`RATCHET_REVERTED` / `TESTS_FAILED`). A corroborating ablation study (session
`local-94259bef…`, patch `1a7637b9…`) sealed 28 → 27 violations over 9 ledger entries and
3 committed steps. The distillation claim is therefore: **9 → 1, with the residual explained by an
external contract, and one recorded counterexample against the instrument's own first instinct.**

### Section 2.2: the mechanical catch-22 on dsh-compaction-plus

**The proof that the catch-22 was real.** The illusion-breaker proved 7 illusions on
`dsh-compaction-plus` (memory `dsh-compaction-plus_peircean_cycle_2026-11-07.md:36-48`):

| ID | Category | Locus | Empirical proof |
|---|---|---|---|
| ILL-01 | `SEMANTIC_LIE` | `src/spill.ts:141-145` | mutation followed the symlink and wrote the secret through it; gate exit 0 |
| ILL-02 | `BLIND_GATEMAN` | `cordis.patch.yml` (shipped bundle) | file shrank 24064 → 63 B of invalid YAML; gate exit 0 |
| ILL-03 | `INERT_WIRING` | `package.json:36` + `tests/` | `tests/` emptied → `tests 0, pass 0`, gate exit 0 |
| ILL-04 | `SEMANTIC_LIE` | `src/engine.ts:323` abort rethrow | guard removed; `grep -ri abort tests/` → no matches; gate exit 0 |
| ILL-05 | `BLIND_GATEMAN` | `package.json:55` vs `package-lock.json` | `npm ci --dry-run` → `Missing: left-pad@1.3.0`, exit 1; local gate exit 0 |
| ILL-06 | `FRAGILE_ASSUMPTION` | `src/spill.ts:241` `try { chmodSync(tmp,0o600) } catch {}` | post-cap file mode 644 (world-readable); gate exit 0 |
| ILL-07 | `BLIND_GATEMAN` | `src/engine.ts:209-271` uncommitted override | gate green with the override present AND with HEAD `engine.ts` — two trees, one verdict |

The prosecutor sealed a 6-trap cage (`SHA-256 1530165d…`, mode `0444`): on the unpatched repo the
red phase exited 1 with all six traps `FAIL_EXPOSED`. The surgeon then made **7 attempts, all
red**: attempts 1–6 failed at the gate (exit 2, then 1, 1, 1, 1, 1), and attempt 7 achieved
*gate green with the traps still exposed* — the exact breaking point. The root cause was not a code
defect but a mechanical Catch-22: the arbitration was locus-based, so all six traps (loci in
`src/`) were cage-eligible, yet every trap was a mutation test whose only remedy was to strengthen
the oracle — which `ORACLE_MUTATION_FORBIDDEN` blocks. The prosecutor's own contract even ordered
the surgeon to edit `package.json`, i.e. it ordered a forbidden act. The distilled law (ledger
record 9, `run_id 754d942d…`):

> A mutation-testing cage whose remediation requires strengthening the test oracle is
> unreachable under a Double-Blind Oracle Lock. Arbitration must be remediation-aware, not
> locus-aware.

**The resolution.** `classifyOracleLock` now locks on locus or remedy (`peircean-kernel.js:516-546`),
and `ip_verify_and_seal_cage` rejects mutation-testing cages and oracle-editing contracts with
`ILLEGAL_ORACLE_REMEDIATION_CONTRACT` (`iron-prosecutor/index.js:396-432`). Re-run result:

| Artifact | Value |
|---|---|
| cage-eligible illusions | 1 (`ILL-06`, the `#enforceCap` defect) |
| oracle-locked boundaries | 6 (with reasons, for human review) |
| sealed cage | `TRAP-01-ENFORCECAP-MODE-0600`, `0444`, SHA-256 `1163ef34…` |
| red phase on unpatched | exit 1, `FAIL_EXPOSED` |
| surgeon patch | `src/spill.ts` only, +10 LOC, 0 functions, 0 clones, 0 wrappers |
| green phase | gate exit 0, trap `PASS_CAUGHT`, `ALL_GATES_AND_TRAPS_GREEN` |
| containment | `head_matches_baseline=true`, `status_matches_baseline=true` |
| ledger | `FALSIFICATION_SEALED` — 7 illusions, 1 trap, 6 oracle-locked boundaries |

**Honest caveat (recorded in the foundations document itself).** The agent sessions for stages 2 and
3 were degraded (the MCP stdio subprocess died, its tools deregistered), so both stages were
executed deterministically through the same MCP instruments the agents use. The artefacts and the
cryptographic seal are the instrument's own, not a simulation — but the per-stage autonomy claim
for that re-run is weaker than for a live session, and this monograph reports it at its true
weight.

### Section 2.3: the bipolar gate against degenerate and overfitted cages

Law VI closes the two escape hatches a purely mechanical cage leaves open: a single-state trap can
be satisfied by a constant return, and a repair that hardcodes the trap's own inputs passes
without restoring the invariant. Both checks are enforced at the Red seal
(`ip_verify_and_seal_cage` → `DEGENERATE_SINGLE_STATE_TRAP`) and at the Green seal
(`sg_commit_green_handoff` → `OVERFITTED_LITERAL_ECHO_DETECTED`).

**Live field experiment (single session, target `dsh-rtl-bidi`).** Ledger record 11
(`run_id f6c1a2b4…`, `FIELD_EXPERIMENT_SINGLE_PROCESS`); the source repository was never touched
(`git status` clean, HEAD unchanged):

| Phase | Evidence |
|---|---|
| Hunt | 3 illusions proven; ILL-02 and ILL-03 oracle-locked; ILL-01 cage-eligible |
| Cage | `TRAP-00-BASELINE` (positive control) + `TRAP-01-LOCALSTORAGE-DOMAIN` (negative edge: per-run `randomBytes` poison must not paint RTL); `0444`; SHA-256 `ae8f2f22…`; red exit 1, `TRAP-01:FAIL_EXPOSED` |
| Law VI.1 | a deliberately degenerate single-state cage was refused: `DEGENERATE_SINGLE_STATE_TRAP` (`distinct_check_sites=2, assertion_calls=0, has_positive_control=false, has_negative_edge=true`) |
| Surgery | one-line fix in `client.js`; gate 22/22; both traps `PASS_CAUGHT`; patch SHA-256 `02f3ee6a…` |
| Law VI.2 | a green patch echoing the cage-only literal `TRAP-01-LOCALSTORAGE-DOMAIN` was refused: `OVERFITTED_LITERAL_ECHO_DETECTED`; echo removed, seal succeeded |
| Negative result | the first degenerate-cage seal was NOT refused (cage SHA-256 `1c329475…`) because the long-lived dispatcher (pid 259506, started 2026-11-07T16:04:04Z) had cached the pre-Law-VI kernel. After a restart the same cage was refused |

The last row is the most instructive number in this section: the instrument's process lifetime,
not its source, decides which laws are live. That class of failure (a stale module deciding the
verdict) is exactly what check_docs-style gates exist to catch in this repository.

**Gate strength.** The law is covered by contract tests: the foundations document reports the
engine gate 58/58 green verified live on 2026-11-08 (20 xray-prober tests + 38 plugin checks,
exit 0), while ledger record 11's change entry reports 94/94 (20 + 13 single-process-topology
tests + 61 plugin checks) after the topology change, pushed as commit `e1cff19`. This monograph
cites 58/58 as the documented gate at the time of writing and 94/94 as the ledger's own evidence;
the two numbers describe two recorded states of the same suite, not a contradiction.

### Section 2.4: the discipline jump measured from the session database

**Measured 2026-11-08 from `/home/fares/.hermes/state.db`.** The tasking brief
supplied for this monograph asserted a discipline jump (145 sessions before the
gate, first-turn skill compliance 17.9% = 26/145, terminal-to-skill ratio
77.34:1 → 11.18:1, −85.5%) and pointed to a proof file
`before-after-cohort-proof.md` under `/home/fares/.hermes/cache/scratch/`. That
file does not exist (scratch entries are pruned after 24h idle) and the brief's
figures do not reproduce from `state.db` under any natural cohort definition,
so they are **not asserted** here. The same effect was measured instead, with a
stated method:

- Source: `state.db` `messages` rows with `role='tool'` (one row per executed
  tool call), ordered by `messages.id`; sessions with `tool_call_count >= 1`.
- Cohort split: `sessions.started_at` before vs at/after commit `e1cff19`
  (2026-11-08T02:02Z), the cycle-scoping change of record 11.
- *First-turn skill compliance*: the session's first executed tool call is
  `skill_view`.
- *Terminal-to-skill ratio*: total `terminal` calls / total `skill_view` calls.

| Cohort | Sessions | First tool is `skill_view` | Terminal : skill_view |
|---|---|---|---|
| Before `e1cff19` | 123 | 19 (15.4%) | 79.01 : 1 (12,168 / 154) |
| At/after `e1cff19` | 7 | 7 (100%) | 5.68 : 1 (125 / 22) |

The after cohort is small (n=7) and `state.db` is live, so the after ratio
drifts slightly on re-run; the before cohort is fixed. The direction the brief
claimed is confirmed: after the gate, sessions open with a specialist skill and
raw terminal dominance falls by an order of magnitude.

The enforcement mechanism behind the measured compliance is the `skill-gate`
plugin (`~/.hermes/plugins/skill-gate/`): phase 2 caps raw terminal calls at
`DELEGATION_LIMIT = 12` before forcing a `delegate_task`, and its contract
suite passes 66/66 live on 2026-11-08. The verifiable proxies for "the laws
bite" remain those in §§2.1–2.3.

## Section 3: converting the architecture into three high-impact paths

Each path below names the artifact that carries the claim, the venue or customer, and what must be
built to make the claim survive review. Costs are stated in examiner time, not money: the engine
already exists, is zero-dependency, and is gated.

### Section 3.1: publishable papers for AI and SE conferences

Three papers fall out of §§1–2 without new science — each is a reframing of a theorem or a measured
result already in the ledger:

1. **Remediation-aware oracle arbitration: a mechanical Catch-22 in agent verification.**
   Claim: locus-only eligibility admits an unclosable cage; remediation-aware eligibility collapses
   6 impossible traps to 1 legal one. Evidence: ledger records 7–9 (7 red surgeon attempts, then
   `ALL_GATES_AND_TRAPS_GREEN`). Target: ICSE/FSE (software engineering venues reward the
   verification framing) or a NeurIPS/ICLR analysis track. Reviewer-grade hardness: the negative
   result (7 red attempts) must be published as the motivating evidence, not hidden. Prep: an
   anonymous code mirror with reproduction scripts (`--repo … --mode falsify`), plus per-claim
   experiment tables.
2. **Dual-polarity cages: anti-gaming verification for LLM-authored repairs.**
   Claim: two mechanical checks (polarity completeness, literal-echo detection) block the two
   dominant reward-hacking channels of LLM repairs — constant cages and hardcoded test inputs.
   Evidence: ledger record 11, both rejections observed live. Target: ICLR/NeurIPS (the
   reward-hacking channel is the community's live problem). The stale-dispatcher negative result
   should ship in the appendix as process-lifetime evidence; it is the kind of honesty that gets
   papers cited.
3. **Thalamic gating of code-agent attention: skeleton folding under the 4 ± 1 bound.**
   Claim: folding the repository into a body-less skeleton with exact coordinates, and opening one
   focal cell at a time, bounds the working-memory load a flat-attention agent must hold — and a
   single shared extractor makes function counts agree across harnesses (without the control-flow
   keyword filter the count was 96 instead of 58, foundations §2.3). Target: COLM/NeurIPS (a
   cognition-meets-systems result). Prep: a controlled comparison of flat-context vs folded input
   on one task family, with the extractor-count agreement as a reported instrument check.

### Section 3.2: flagship contributions to open-source agent frameworks

The engine's transferable surface is the plugin + kernel, not the agents. Three contributions, in
order of leverage:

1. **Cycle-scoped tool-call guarding as a reference pattern.** The native Hermes plugin
   (`pre_tool_call` blocking on every tool, stage inferred from the delegated goal, laws inert
   outside an active cycle) plus the unified in-process dispatcher (no per-tool subprocess, no
   orphaned stdio, hard per-call timeout, process-group kill) is a complete answer to a problem
   every agent framework now faces: how to enforce policy at the tool layer without becoming a
   hostile tenant. Submit upstream as a plugin; document the cycle-scoping law (commit
   `dfff2b3`) as the part that makes it adoptable.
2. **The kernel rules as a standalone policy module.** `peircean-kernel.js` + its faithful Python
   translation (`peircean_rules.py`) are small enough to vendor. The six laws are written as
   re-usable predicates with rejection codes — an MCP tool-guard implementation that works for any
   framework, not only Hermes. Publish as its own package with the 58/58 contract suite as the
   conformance tests.
3. **The ledger format as an evidence-trail standard.** Append-only, corrupt-line-tolerant, with
   `run_id`, `h0_baseline`, `h1_final`, `net_delta`, `distilled_law`, and negative results
   preserved. Agent frameworks report successes; a sealed, append-only run record with the
   breakage is a differentiating standard. Propose the schema (not the philosophy) to SWE-bench-style
   harnesses and MCP registries.

### Section 3.3: independent verification products for companies

The commercial wedge is the cage: a sealed, anti-gaming verification of a repository that a legal
or procurement team can read without trusting a model.

1. **Sealed-cage CI gate for AI-generated code.** A company submits a repository; the engine returns
   a sealed adversarial trap suite + the repair + the ledger, and the CI pipeline re-verifies the
   seal. Sold against the documented failure modes: tautological tests, swallowed exit codes,
   zero-assertion probes — the exact five-signal scan of §1.1.1 as an audit checklist. This is the
   product form of Law III + Law VI.
2. **Oracle-integrity audit.** Most teams' tests are weaker than their gates assume. The illusion
   catalogue (7 categories exercised on real repos, §2.2's table) is a ready-made audit: every
   finding ships with an empirical proof (emptied `tests/`, gate exit 0) and an oracle-locked
   classification so the audit never recommends a change the team cannot legally make.
3. **Anti-bloat merge gate.** The ratchet + Occam gate as a merge rule: a pull request is accepted
   only if violations fall, or LOC falls with no function growth, with reverts recorded. For
   companies whose AI adoption curve is now a code-growth curve, this is a one-line CI policy with
   a measured effect (the 9 → 1 result is the demo).

## Limitations and honest caveats

- **Small evidence base.** Two production targets (1237 and 2000 LOC) plus a synthetic e2e lab.
  The laws are written generally; the proof is not yet at scale. The first external-repo run
  under §3.3 is also the first scaling data point.
- **One re-run was instrument-driven, not agent-driven.** The degraded stages 2–3 of §2.2 were
  executed deterministically through the MCP instruments. The artefacts are real; the autonomy
  credit for that run is partial and is reported as such.
- **Process lifetime governs live laws.** The stale-dispatcher negative result in §2.3 shows a
  law can exist in source and not in force. Any deployment of the kernel needs a startup
  fingerprint check (dispatcher build time vs kernel edit time), which the engine does not yet
  have.
- **The discipline figure is measured with a small after cohort** (§2.4): 7 sessions
  at/after `e1cff19`, so the exact after ratio is indicative, not precise. The brief's
  original figures (17.9% = 26/145; 77.34:1 → 11.18:1) were not reproduced and must not be
  quoted.
- **Reproduction.** `npm test` in `peircean-engine` (58/58 as documented; 94/94 per ledger
  record 11), `node bin/cybernetic-pipeline.mjs --show-history`, and the commands in foundations
  §4.6 regenerate the ledger this monograph is built on.

## Executive summary of actions

| Order | Action | Why, in one line | Evidence that it stands on |
|---|---|---|---|
| 1 | Re-run the session-level tool-call discipline audit as the post-gate cohort grows | The audit is measured (§2.4) but the after cohort is n=7; a larger cohort firms the after ratio | record 11, §2.3; §2.4 |
| 2 | Externalise the kernel + plugin as a standalone package with the 58/58 suite as conformance tests | The adoption-track contribution (§3.2) needs no new science, only packaging | Law III layering, §1.3 |
| 3 | Draft paper 1 (Catch-22 / remediation-aware arbitration) with the 7 red attempts as motivating evidence | Strongest theorem; the negative result is publishable and rare | ledger records 7–9, §2.2 |
| 4 | Pilot the sealed-cage gate on one external repository | First scaling data point and first product validation in the same step | §3.3.1 |
| 5 | Add a startup fingerprint check (kernel edit time vs dispatcher build time) | Closes the stale-dispatcher class before it bites in production | §2.3 negative result |

## References and artifact index

No external URLs are cited: this monograph's claims resolve to artifacts a reader can re-check.

| Claim family | Artifact |
|---|---|
| Six mechanical laws, formal statements, rejection codes | `peircean-engine/docs/SCIENTIFIC_FOUNDATIONS.md` §§1–3, Appendix B |
| Ledger statistics (11 records, Appendix A) | `peircean-engine/docs/SCIENTIFIC_FOUNDATIONS.md` §4 + Appendix A |
| Distillation 9 → 1 | foundations §4.2, ledger record 10 (`run_id 22bba231…`) |
| Catch-22 and its resolution | foundations §§3.4.1, 4.3; ledger records 7–9 |
| Bipolar gate rejections | foundations §§3.6, 4.7; ledger record 11 (`run_id f6c1a2b4…`) |
| Gate strength 58/58 / 94/94 | foundations §4.4; ledger record 11 (commit `e1cff19`) |
| Comparative audit reports consulted | `/home/fares/.hermes/cache/scratch/forensic-report.txt`, `forensic-data.json` |
| Historical grounding (Peirce, Bacon 1620, Ibn al-Haytham, Cowan 2001, Miller 1956, Platt 1964, Feynman 1974) | as reviewed in foundations §§1.2, 2.2 — named, not URL-cited, per the no-invented-citations rule |

*End of monograph. Every number above was read from the live repository, ledger, and `state.db` on 2026-11-08; the tasking brief's original discipline figures were not reproduced and are not asserted (§2.4).*
