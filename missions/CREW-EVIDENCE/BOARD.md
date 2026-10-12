# BOARD — mission CREW-EVIDENCE (opened 2026-09-20)

Mirror of the live board (`~/crew-research-council/BLACKBOARD.md`). Write rights per `README.md`:
@scout → EVIDENCE + OPEN GAPS · @architect → DECISIONS + CONSTRAINTS · @ship → ARTIFACT + TEST
RESULTS · @razor/@gate → flags only · @edge → BET MEMO (plan stage) · @coach → distilled rules.
Entries below are labelled with the seat they are written from. This mission was opened by an
**operator session** (the Owner's goal in chat), not by @firstmate — recorded as such.

## GOAL (owner: @architect)

Recover the crew's lost evidence, make the surviving revision runnable, and re-run the decisive
experiment — so that the numbers the crew's own records rely on either reproduce or are marked
UNREPRODUCED. Deliverables: the missing `experiment/VERDICT.md`, an evidence-recovery record, and
an independent re-run of the measurement.

## CONSTRAINTS (max 7 active)

1. Do not edit protected paths: `RESEARCH-COUNCIL/**`, `RESEARCH-COUNCIL/STATUS.md`,
   `tests/**`, `crew/**`, `harness/**`, `repro/**` (this repo's `PROTECTED.md`).
2. No reconstruction may be presented as original source; every restored byte must cite the
   evidence it came from.
3. Every claim needs a command that reproduces it; counts are generated, never hand-written.
4. RED before GREEN for any restored code (`TEST-POLICY.md` §3).
5. Nothing is promoted into the protected trees without an Owner ruling.
6. No commit while another session's work is uncommitted in the tree (two-writer rule).
7. The model leg (torch + weights) is out of scope; say so, do not fake it.

## EVIDENCE (owner: @scout — append-only, cite sources)

- E1 · `/tmp/opencode/verify-consol/` held a full working copy of the harness (source + tests +
  `tasks/real-missions.json` + `run.sh` + `variant.json` + `pyproject.toml`); `/tmp` is volatile.
  → `~/.hermes/crew/experiment/rescued/2026-09-20-verify-consol/`, 69 files, `MANIFEST.sha256`
  verified (`sha256sum -c` → 69/69). Source untouched at the original path.
- E2 · Repo bytecode vs rescued source, **recursive** code fingerprint: 6/9 modules identical;
  the other three are a later revision whose only semantic delta is the v5 judge
  (`is_abstain_v5`, `judge_transfer_v5`, and the test that pins them).
- E3 · The v5 bindings and body are recoverable from `dis` output; transcription verified by the
  later revision's own compiled test: RED (`AttributeError … is_abstain_v5`) → GREEN
  (`COMPILED-SUITE ok=True run=47 failures=0 errors=0`), source suite still `Ran 46 … OK`.
- E4 · The surviving fixture has **20** tasks (T1..T20), expected PASS 4 / HOLD 8 / FLEX 8 —
  the recorded per-arm numbers refer to a **16-task** fixture that is not on disk.
- E5 · Five arms re-run offline, seed 7, byte-identical on repeat. Matrix and raw SUMMARY lines:
  `~/.hermes/crew/experiment/VERDICT.md` §2.
- E6 · v5 measured: `TRANSFER-V5 agree=20/20=1.000`, `BOUNDARY-V5 spec_fire=1/6 sens_flagged=2/5`
  (v4: `sens_flagged=5/5`) — scoping costs 3 of 5 paraphrase probes.

## OPEN GAPS (owner: @scout)

- The 16-task fixture behind the recorded DECISIVE-01/REPLICATION numbers: **absent**.
- `experiment/VERDICT.md` (original): **absent**; this mission supplies a dated re-run instead.
- The later revision's `run_repro.py` (321 lines) vs rescued (294): only the v5 block was restored;
  any other difference is unexamined.
- The model leg: unrun (torch + weights).

## DECISIONS (owner: @architect — each cites ≥2 EVIDENCE rows)

- D1 (E1,E2): the rescue is the authoritative working copy for any re-run; the repo bytecode is
  the authority for the v5 delta only.
- D2 (E3,E5): the re-run happens **in a sandbox** (`~/.hermes/crew/experiment/runs/…`), never in
  the protected trees.
- D3 (E4,E5): the re-run is reported as a fresh 20-task measurement, **not** as a reproduction of
  the recorded 16-task numbers.

## BET MEMO (owner: @edge — plan stage only)

Prediction on the record: promoting the rescued harness into `crew/**` (Owner act) and re-running
on a restored 16-task fixture would reproduce the *ordering* (single ≤ team on cost; single ≥ team
on compliance with the hold rule) but not the exact counts. Falsifier: a restored fixture on which
`team` beats `solo --hold-on-vague` on both `passed` and `cost`.

## ARTIFACT + TEST RESULTS (owner: @ship — pointers, not prose)

- `missions/CREW-EVIDENCE/2026-09-20-EVIDENCE-RECOVERY.md` — recovery record (findings E1–E6).
- `~/.hermes/crew/experiment/VERDICT.md` — the re-run verdict (matrix + raw SUMMARY lines + ceilings).
- `~/.hermes/crew/experiment/recovery/` — `pyc_inventory.py`, `api-inventory.json`, `dis/*.dis.txt`.
- `~/.hermes/crew/experiment/runs/2026-09-20-replication/` — sandbox the arms ran in.
- `~/.hermes/crew/experiment/runs/2026-09-20-v5-restore/` — sandbox with the v5 transcription.
- Tests: source suite `Ran 46 tests … OK`; compiled later-revision suite `ok=True run=47`; eval
  arms deterministic (two runs byte-identical).
- `~/.hermes/crew/experiment/runs/2026-09-20-replication/VERIFIER-REPORT.md` — blind verifier
  report: five SUMMARY lines matching `VERDICT.md` §2 **5/5**, `VERDICT: REPRODUCIBLE 5/5`,
  md5-baseline integrity check clean (206 lines, md5 `b5a4b0e9…`).

## FLAGS (@razor/@gate only)

_none_

## K-LINE SNAPSHOTS

- K1 · 2026-09-20 · after rescue + identity map · `MANIFEST.sha256@69 files`,
  digest of `api-inventory.json`.

## DISTILLED RULES (owner: @coach)

_none yet_

---

# APPEND 2026-10-12 — the "later revision" gap is retrievable from git

Written from an operator session (the Owner's order in chat), recorded as such
per this board's opening note. Evidence:
`missions/ROUTER-V2/REFERENCE-INTEGRITY-SWEEP-2026-10-12.md` §5. Nothing above
this line is edited.

## OPEN GAPS — closed / narrowed (owner: @scout)

- **CLOSED.** The OPEN GAPS line at L51 — *"The later revision's `run_repro.py`
  (321 lines) vs rescued (294): only the v5 block was restored; any other
  difference is unexamined"* — is answerable from the repository, because **both
  revisions are in git**:
  - `origin/orx/repro-consolidation-judge-promoted-to-shared-cre:repro/run_repro.py`
    — 294 lines, sha256 `433c4bcfe2be0cfe3a3ebfa2e2c583bee142df403b8dd6dad6e54b9c655f4fa5`;
  - `origin/orx/repro-judge-v5-scoped-paraphrase-vs-transfer:repro/run_repro.py`
    — 321 lines, sha256 `d7441d3680443080ee4e9d13c443f6bc8de5deb0d0670118f72197502d8c3754`.
  `diff -u` between them (**RUN**, 2026-10-12): **3 hunks / 33 changed lines, all
  of them the v5 block** — the `is_abstain_v5` + `V5_*` import,
  `judge_transfer_v5()`, and the `TRANSFER-V5` / `BOUNDARY-V5` / `SCOPED5`
  report lines. **No other difference exists between the two revisions.**
- **NARROWED, not closed.** Whether the repository's 294-line blob *is* the
  artifact this mission calls "rescued" is unproven: the rescued copy lives
  outside the repository, so the identity check still needs it. E1/E2 stand
  unchanged, and no claim above is re-scored by this append.
- **Corroborated on the same ref** (E3, unchanged): the later revision's
  `tests/test_crew.py` carries **47** `def test` methods (E3: "run=47"), and its
  `crew/abstain.py` holds `is_abstain_v5` (E3: "the v5 bindings and body are
  recoverable").
- **Note for the record:** `repro/**` — declared an untracked working copy by
  `PROTECTED.md` L13 — is committed on **10** `orx/repro-*` refs
  (`run_repro.py`, `pairs.json`). For this mission the protected tree is *more*
  available in git than the declaration implies.


---

# APPEND 2026-10-12 (b) — the preprint's rounds reproduce from git, 18/18 exact

Written from an operator session. Evidence:
`missions/CREW-EVIDENCE/REPRO-AUDIT-PAPER-ROUNDS-2026-10-12.md`. Nothing above
this line is edited.

## EVIDENCE (owner: @scout)

- **E7 · The published table reproduces.** All **18 rows** of
  `paper/draft:paper.tex` Table 1 re-execute **exactly** — `n`, `passed`, `cost`
  and `resolved` equal the published values — by extracting each per-node branch
  (`orx/baseline-solo-…`, `orx/r1-…` … `orx/r8-…`) with `git archive` into
  `/tmp` and running the node's own `bash run.sh` (offline, stdlib, seconds).
- **E8 · All 19 tracked runs are green** (`Ran 10 … 35 tests … OK`, then a
  `SUMMARY` line), matching the paper's Method sentence; the 19th is the R9
  consolidation run, which reproduces the R8 node (20/20/87/9) and has no table
  row of its own.
- **E9 · Determinism holds**: three nodes re-run twice produced byte-identical
  stdout.
- **E10 · Provenance link**: the R7/R8/R9 fixture hash is the full
  `28406677825eeeb5489e7ea6fc60ee7a992e55ea0629f8348436052cfba59a87` — the same
  frozen-20 that R02–R04 measured and `leaderboard.md` L5 cites. The mission's
  frozen fixture is the preprint lineage's R7+ fixture, inherited byte-identical.
- **E11 · Fixtures per node group**: R1 `90c6fed1504a` (7 tasks) · R2
  `72e56f08de9a` (8) · R3 `b2ddd73dce48` (10) · R4 `8850bf47040b` (13) · R5
  `eea367d1e0b3` (16) · R6 `75cc3191a8b3` (19) · R7–R9 `28406677825e` (20).

## OPEN GAPS (owner: @scout)

- The `orx/*` branches are the **only** place the preprint's runnable revisions
  exist. Deleting them would make the paper as unreproducible as R02–R05 —
  record this before any branch cleanup.
- The paper's Method says "19 tracked runs" while Table 1 lists 18; the missing
  row is the R9 consolidation run (no new node). A future revision of the paper
  can footnote it; the committed draft is left alone.
- The re-runs used CPython 3.11.2 here, while the sandboxes declared 3.12. The
  code is stdlib-only and the double runs are byte-identical, so the claim stands
  on this machine; a 3.12 cross-check is still owed (not run).

## NOT CLAIMED

- Nothing about R02–R05: their revisions remain absent from every ref, so their
  numbers stay `UNVERIFIABLE` (`REPRO-AUDIT-R02-R03-2026-10-12.md`,
  `REPRO-PACK-R04-AUDIT-2026-10-12.md`).
- No number in the paper was changed, and no mission ruling was re-scored.

