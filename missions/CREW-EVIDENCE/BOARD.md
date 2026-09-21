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
