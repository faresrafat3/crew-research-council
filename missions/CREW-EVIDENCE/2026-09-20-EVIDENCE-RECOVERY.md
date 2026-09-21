# EVIDENCE RECOVERY — 2026-09-20 · mission CREW-EVIDENCE

> **What this file is:** the record of what survived, where it lives now, and what is still
> missing, after this repo's harness source turned out to be bytecode-only and its decisive
> experiment's verdict turned out to be absent. Written under the Owner's goal (chat: "go").
> **It is a dated record, not law** — supersede it, never rewrite it.

## 0. The two gaps it addresses

- `GOAL.md` records `DECISIVE-01 CLOSED (2026-09-12, see experiment/VERDICT.md)` with numbers
  (A 12/16 · trio 10/16 · system-chosen 8/16; later `REPLICATION` A 15/20 · B 14/20 · C 10/20).
  No `experiment/VERDICT.md` exists anywhere on disk (repo, `~/.hermes/crew/`, `~/crew/` all searched).
- The repo tracks 52 files — all `.md` except `.gitignore`. `crew/`, `harness/`, `repro/`,
  `tests/` held only `__pycache__`. This repo's own `PROTECTED.md` (written today, 11:21–11:22
  by a parallel session) states exactly that: *"Currently untracked working copies (only
  `__pycache__` on disk). Do not treat the empty trees as an implemented test/harness layer."*

## 1. What was found, and where

| find | location | evidence (command-level) |
|---|---|---|
| Full harness **source**: `crew/` 5 modules, `harness/` 2, `repro/` 2, `tests/` 1 | `/tmp/opencode/verify-consol/` — another session's working copy (mtimes 08:05–09:05 today, **volatile /tmp**) | `python3 -m unittest discover -s tests` → `Ran 46 tests … OK` |
| The **task fixture**: 20 tasks, T1..T20 with class/brief/requirements/constraints/correction/multi_step/expected | `/tmp/opencode/verify-consol/tasks/real-missions.json` (11,013 B · sha256 `28406677…59a87`) | parsed: 20 tasks; classes = 17 distinct probe classes; expected PASS 4 / HOLD 8 / FLEX 8 |
| Run recipe, variant record, packaging | `run.sh`, `variant.json`, `pyproject.toml` | `variant.json` = `{"checklist": false, "formation": "team", "hold_on_vague": true, "shuffle_seed": 7}` |
| The **later revision** of three modules (the v5 judge) | repo bytecode only: `crew/__pycache__/abstain.cpython-312.pyc`, `repro/__pycache__/run_repro.cpython-312.pyc`, `tests/__pycache__/test_crew.cpython-312.pyc` | recursive code-fingerprint diff, §2 |

**Rescue (byte-preserving, source untouched):** the whole `/tmp` tree was copied to
`~/.hermes/crew/experiment/rescued/2026-09-20-verify-consol/` with `MANIFEST.sha256` +
`PROVENANCE.md`; `sha256sum -c MANIFEST.sha256 --quiet` → **69 files match**. Nothing at the
source was moved, edited, or deleted.

## 2. Identity map — repo bytecode vs rescued source (recursive fingerprint)

Method: unmarshal each `.pyc`, walk **every** code object, hash `(co_name, argcount,
flags&0xF, sha256(co_code), co_names, co_varnames, repr of every non-code const, recursively
nested code objects)`, then compare the two trees by qualname. Tool:
`~/.hermes/crew/experiment/recovery/pyc_inventory.py` (marshal/dis only — it never executes the
recovered bytecode).

| module | objects repo / source | verdict |
|---|---|---|
| `crew/__init__.py` | 1 / 1 | IDENTICAL |
| `crew/eval.py` | 2 / 2 | IDENTICAL |
| `crew/roles.py` | 7 / 7 | IDENTICAL |
| `crew/router.py` | 4 / 4 | IDENTICAL |
| `harness/__init__.py` | 1 / 1 | IDENTICAL |
| `harness/state.py` | 9 / 9 | IDENTICAL |
| `crew/abstain.py` | 11 / 9 | DIFFERS — repo adds `is_abstain_v5` (+ its genexpr); `<module>` body differs |
| `repro/run_repro.py` | 12 / 11 | DIFFERS — repo adds `judge_transfer_v5`; `check_protocol` (+genexpr) and `<module>` differ |
| `tests/test_crew.py` | 78 / 75 | DIFFERS — repo adds `test_judge_v5_scopes_paraphrases_restores_sens_keeps_transfer` (+lambda/genexpr); `<module>` and `TestReproFixture` differ |

**Conclusion.** For six of nine modules the repo bytecode **is** the compile of the rescued
sources. For the other three, the repo bytecode is a **later revision**, and the only semantic
delta is the v5 judge plus the test that pins it.

**Retraction on the record.** A first pass compared only module-level bytecode plus non-code
constants and reported "7/9 identical". That check was too weak — module-level code is identical
for any two revisions with the same top-level names — and it was superseded by the recursive
fingerprint above the moment the later revision's compiled suite exposed a v5 test the rescued
source did not contain. The weak result is not quoted anywhere as evidence.

## 3. The v5 delta — recovered from bytecode, then verified by the repo's own test

The bytecode is executable evidence even when the source is gone. Bindings and bodies were
transcribed from the disassembly (`~/.hermes/crew/experiment/recovery/dis/*.dis.txt`,
produced by `dis.dis(code, depth=4)`; read-only):

- `abstain.py:70` — `V5_PARA_RES = list(V4_PARA_RES)`
  (`PUSH_NULL; LOAD_NAME list; LOAD_NAME V4_PARA_RES; CALL 1; STORE_NAME V5_PARA_RES` — a copy,
  not an alias).
- `abstain.py:71` — `V5_EVIDENCE_RES = [r"\bsource\b", r"\bdata\b", r"\bevidence\b",
  r"\bverif\w*\b", r"\banswer\b", r"\bmissing\b", r"\binsufficient\b", r"\bunknown\b"]`
  (`BUILD_LIST 0; LIST_EXTEND`).
- `abstain.py:77-83` — `is_abstain_v5(text)`: `t = text.lower()`; early `return True` when
  `is_abstain_v3(text)`; then `has_para = any(re.search(p, t) for p in V5_PARA_RES)`,
  `has_ev = any(re.search(p, t) for p in V5_EVIDENCE_RES)`, `return bool(has_para and has_ev)`.
- `run_repro.py` — `from crew.abstain import … V5_PARA_RES, V5_EVIDENCE_RES, … is_abstain_v5`
  re-export (forced by the repo's own test: it asserts `run_repro.V5_PARA_RES`), plus
  `judge_transfer_v5()` = `_transfer_rows(is_abstain_v5)`, docstring recovered verbatim:
  *"Same transfer probe scored with the v5 scoped judge (measurement)."*
- `check_protocol` v5 block — structural facts recovered **by absence**: the later revision's
  constants contain ` status=TRANSFER-V5-REPORTED`, `BOUNDARY-V5 spec_fire=` and
  ` status=BOUNDARY-V5-REPORTED`, but no `JUDGE-XFER5 …` and no `SENS5 v5=…` fragments (their
  v4 twins are present). So the v5 block prints summary lines only — no per-row, no per-probe.

**Iron Law loop — witnessed, not asserted** (RED before GREEN, as `TEST-POLICY.md` §3 demands):

| step | command (sandbox `runs/2026-09-20-v5-restore/`) | result |
|---|---|---|
| RED | repo's **compiled** v5 test loaded sourcelessly and run against the rescued (v4) revision | `AttributeError: module 'run_repro' has no attribute 'is_abstain_v5'` (test_crew.py:424) → `errors=1` |
| GREEN (1) | same compiled test after the transcription | `GREEN-LOG exit_ok=True failures=0 errors=0` |
| GREEN (2) | the **whole** compiled suite of the later revision | `COMPILED-SUITE ok=True run=47 failures=0 errors=0` |
| no regression | rescued source suite | `Ran 46 tests … OK` |
| determinism | same eval arm run twice, outputs diffed | byte-identical |

That the *later revision's own compiled tests* pass against a source reconstructed from its
bytecode is the strongest verification available here: the oracle is not my own writing.

**Measured v5 behaviour** (`repro/run_repro.py --check`, sandbox):

```
TRANSFER-V5 agree=20/20=1.000 hold_recall=16/16 status=TRANSFER-V5-REPORTED
BOUNDARY-V5 spec_fire=1/6 sens_flagged=2/5 status=BOUNDARY-V5-REPORTED
TRANSFER-V4 agree=20/20=1.000 hold_recall=16/16 status=TRANSFER-V4-REPORTED
BOUNDARY-V4 spec_fire=1/6 sens_flagged=5/5 status=BOUNDARY-V4-REPORTED
```

So the scoping keeps transfer perfect but **loses 3 of 5 paraphrase probes** (5/5 → 2/5). That
is the honest reading of "scopes paraphrases": a real cost, paid where the paraphrase carries no
evidence word.

## 4. What this record does NOT claim

- **The recorded per-arm numbers are not reproduced** (A 15/20 · B 14/20 · C 10/20 came from a
  **16-task** fixture; the surviving fixture has **20**). What reproduces is the *shape*: single
  beats team on grave errors and cost once the hold rule is on, the single grave error is the
  vague-qualitative case, and DUO pays a mechanism tax in exhausted budget. See the measured
  matrix in `~/.hermes/crew/experiment/VERDICT.md`.
- **The model leg was not run.** `repro/run_repro.py` needs torch + ~1 GB of weights for
  `Qwen/Qwen2.5-0.5B-Instruct`; the stdlib protocol path prints
  `model_leg=SKIPPED-needs-weights` by design. No claim is made about model behaviour.
- **Nothing was promoted into the protected trees.** `crew/**`, `harness/**`, `repro/**`,
  `tests/**` are untouched in this repo; the restoration lives in the sandbox. Promoting it is
  an Owner act (and would supersede this repo's `PROTECTED.md` row, which this record does not edit).
- **No commit was cut.** The working tree already carried another session's uncommitted work
  (`README.md` modified, `PROTECTED.md` untracked); committing would have mixed two writers.

