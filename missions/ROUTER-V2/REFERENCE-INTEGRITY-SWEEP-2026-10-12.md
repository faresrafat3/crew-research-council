# REFERENCE-INTEGRITY SWEEP — 2026-10-12 (repo-wide; extends the R04 audit)

> **What this is:** a read-only check of every reference the tracked record
> makes — commit hashes, sha256 digests, external `~/...` paths, and each
> round's required-artifact list — against what the repository actually holds
> (all **33** refs fetched). It amends nothing: no number, claim or ruling is
> changed, and it supersedes nothing. It extends
> `REPRO-PACK-R04-AUDIT-2026-10-12.md` (which covered R04) to the rest of the
> record, and it **closes one recorded OPEN GAP** of the CREW-EVIDENCE mission
> with a diff computed from git (§5).
>
> **What it did not do:** no suite, trial, ablation or model call was run; no
> sandbox was touched; no artifact was reconstructed. The only executed
> operations are read-only `git cat-file` / `ls-tree` / `sha256sum` / `diff`
> over blobs written to `/tmp`. Owner: Fares. Language: English (artifacts) /
> Arabic (chat).

## 1. Commit citations in the tracked record

| cited | where | resolves today? |
|---|---|---|
| `ecaa656` | R04 audit §1, addendum, `BOARD.md` append | **yes** — the single squashed commit of `main` |
| `b7cd26e` | `PROTECTED-RECOVERY-20260921.md` L33 ("HEAD (`b7cd26e`, 2026-09-13) held the pre-mission empty board") | **yes** — 2026-09-13 09:52:41 "Update BLACKBOARD.md", reachable from all 31 non-`main` refs |
| `9304650` | `PROTECTED-RECOVERY-20260921.md` L24 ("interim reconstruction — **superseded**, kept in git history") | **NO — absent from the clone with all 33 refs fetched**, and so is the blob it names (`f17a238d8c84…`) |

**F1.** That row's promise — that the superseded `PROTECTED.md` bytes stay
reachable through git history — does not hold in the published repository:
`main` is one squashed commit, so pre-squash history survives only where a
branch happens to carry it (`b7cd26e` does; `9304650` does not). The recovery
record's *evidence* is therefore partly outside the repository, exactly like
R04's logs.

## 2. sha256 claims (11 distinct 64-hex digests appear in tracked files)

Byte-checkable in-repo **today** (4 of 11):

| claimed digest | referent | status |
|---|---|---|
| `7e14c9d28120…` | `missions/ROUTER-V2/PRE-REGISTRATION.md` (R02) | **MATCH** |
| `1abb28538bb5…` | `missions/ROUTER-V2/PRE-REGISTRATION-R03.md` | **MATCH** |
| `ad9451cefd80…` | `missions/ROUTER-V2/PRE-REGISTRATION-R04.md` | **MATCH** |
| `a12092df1709…` | `PROTECTED.md` (cited by `PROTECTED-RECOVERY-20260921.md` L23) | **MATCH** |

No in-repo referent (7 of 11):

| claimed digest | what it names | status |
|---|---|---|
| `28406677825e…` | frozen-20 fixture `tasks/real-missions.json` | **recoverable from refs** — byte-identical on 15 of the 31 non-`main` refs (R04 audit R18) |
| `26b3b832a223…` | expanded-46 fixture | **on no ref** — and it is not one of the seven fixture revisions the refs do carry |
| `64ac515d03f2…` | `logs/round-04-trial.txt` | on no ref |
| `6ec17759a4d8…` | `logs/r04-analysis.md` | on no ref |
| `93f882d87655…` | `logs/round-04-adversarial.txt` | on no ref |
| `b6d07e83cecf…` | `logs/r04-no-verifier-ablation.txt` | on no ref |
| `f17a238d8c84…` | the superseded `PROTECTED.md` reconstruction blob | on no ref (F1) |

## 3. External `~/...` references

Every `~/.hermes/...`, `~/local/...` and `~/dspy-lab/...` path cited by a
tracked file is **absent** in this checkout (`$HOME` = `/home/node`; it holds
only `.cline/`). Two classes: (a) the mission sandboxes (R02–R05 and
CREW-EVIDENCE); (b) the design source of the one in-repo experiment —
`experiments/adaptive-fleet-discovery/METHOD.md` L7 points at
`dspy-lab/programs/adaptive_fleet.py`, which is outside this repository, so even
the experiment whose *inputs* are committed (hashes recorded in §6) cannot be
re-run offline from the repo alone.


## 4. Per-round availability matrix (R02–R05)

| round | in-repo today (hash-verified where cited) | retrievable from a ref | on **no** ref |
|---|---|---|---|
| **R02** | `PRE-REGISTRATION.md` (`7e14c9d2…` ✓), `REPRO-PACK.md`, `FINDINGS.md`, `BOARD.md` §R02 | `tasks/real-missions.json` (`28406677…`), the round-01 ancestor stack (`crew/{eval,roles,router}.py`, `harness/state.py`, `tests/test_crew.py`, `run.sh`, `variant.json`) | `crew/expertise.py` (the `--ledger` tracker its pack uses), `logs/round-02-routed.txt` |
| **R03** | `PRE-REGISTRATION-R03.md` (`1abb2853…` ✓), `REPRO-PACK-R03.md`, `FINDINGS-R03.md`, `ADR-ROUTER-V2-R03.md` | ancestor stack only | `tasks/expanded-missions.json` (`26b3b832…`), `logs/precut-sha256.txt`, `logs/fixture-sha256.txt`, `logs/artifacts-sha256.txt`, `logs/round-03-trial.txt`, `logs/round-03-postcut.txt`, `tools/run_trial_r03.py`, `tools/verify_postcut_r03.py`, the v2 modules |
| **R04** | `PRE-REGISTRATION-R04.md` (`ad9451ce…` ✓), `REPRO-PACK-R04.md`, `FINDINGS-R04.md`, `ADR-ROUTER-V2-R04.md`, plus this audit + addendum | frozen fixture | everything else (R04 audit R19) |
| **R05** | — nothing (no paper exists here) | — | the pre-registration `2f5c4b46…` that `bets-ledger.md` L10 names |

**The asymmetry that matters:** **three of the four** pre-registrations are
in-repo and byte-verified, while **no** round's *code* and **no** round's
*logs* are on any ref. The record is auditable where it froze intent, and
unreachable where it recorded outcome.


## 5. One recorded OPEN GAP closed from git (CREW-EVIDENCE)

`missions/CREW-EVIDENCE/BOARD.md` L51 records: *"The later revision's
`run_repro.py` (321 lines) vs rescued (294): only the v5 block was restored;
any other difference is unexamined."* **Both sides are retrievable from refs:**

```
A=origin/orx/repro-consolidation-judge-promoted-to-shared-cre   # repro/run_repro.py 294 lines  sha256 433c4bcf…4fa5
B=origin/orx/repro-judge-v5-scoped-paraphrase-vs-transfer       # repro/run_repro.py 321 lines  sha256 d7441d36…3754
git cat-file -p $A:repro/run_repro.py > /tmp/rr294.py
git cat-file -p $B:repro/run_repro.py > /tmp/rr321.py
diff -u /tmp/rr294.py /tmp/rr321.py
```

**RUN — result:** `3` hunks / `33` changed lines, and **every one of them is
the v5 block**: the `is_abstain_v5` + `V5_*` import, `judge_transfer_v5()`, and
the `TRANSFER-V5` / `BOUNDARY-V5` / `SCOPED5` report lines. **There is no other
difference between the two revisions.**

Honest scope of that result: the clause "any other difference is unexamined"
closes as *no other difference exists between these two retrievable
revisions*. Whether the repo's 294-line blob **is** the artifact the record
calls "rescued" is **not** proven — the rescued copy lives outside the
repository, so that identity check is still owed.

Corroboration of the same mission's E3 on the same ref: the later revision's
`tests/test_crew.py` carries **47** `def test` methods (E3: *"run=47"*), and its
`crew/abstain.py` holds `is_abstain_v5` (E3: *"the v5 bindings and body are
recoverable"*). The `repro/**` tree that `PROTECTED.md` L13 declares an
untracked working copy is committed on **10** `orx/repro-*` refs
(`run_repro.py`, `pairs.json`) — for that mission the protected tree is *more*
available in git than the declaration implies.

## 6. In-repo artifact hashes recorded for future checks

The one experiment whose inputs are tracked —
`experiments/adaptive-fleet-discovery/` — hashed today so drift is detectable
later:

| file | sha256 |
|---|---|
| `METHOD.md` | `a5e7403d3bf61c2fe0a1ea251e9420b50c5502b23550670b9db22302311107bc` |
| `adaptive_cache_2026-09-22.json` | `3c367051a259aaded3c118d9b4b0b12d3362c233add17d4fd0f584610cd75d00` |
| `run_2026-09-22.txt` | `ab4f2a988ede4b8f99155dc0c2b9275e3e2eb5e49f7729695d71f316e5f305e9` |

Its `METHOD.md` claims a closed loop ("bind → ask 17*23 → 391 correct") that
needs a live provider, so the committed evidence is a *log of a run*, not a
reproduction recipe — the same class of limit as R04's, with the difference
that here the inputs are at least in the repository.

## 7. Actions taken in this pass (append-only, zero deletions)

- `bets-ledger.md` — a dated note beneath the R05 row's own disclosure
  paragraph: the pre-registration it names is not in this repository; the row
  and its sha are left exactly as written.
- `missions/CREW-EVIDENCE/BOARD.md` — a dated append recording §5, addressed to
  the mission that owns the gap (the ACTIVE mission on `BLACKBOARD.md`).
- `missions/ROUTER-V2/DECISIONS-LOG.md` — one dated row.

## 8. Proposals awaiting the Owner's ruling — nothing applied

1. **F1** (`PROTECTED-RECOVERY-20260921.md` L24 promises history that is not in
   the published repo): a dated note beside that file, per its own L38–41 rule.
2. `tools/gen_leaderboard.py` could name this audit in its `FAIL-LOUD` message
   (behaviour-preserving string change). Not done — it is a code change, and
   the R04 audit's minimal-fix scope excluded it.
3. `leaderboard.md` still says "Round 04 (current)" while R05 is
   pre-registered, and the generator reads rounds 02–04 only: extend the
   generator when R05 lands; never hand-edit the generated surface.
4. `PROTECTED.md` L13 describes `crew/**`/`tests/**` as present-but-empty; on
   `main` they are absent, and 31 refs carry an older revision of them.
5. R04 audit §9 items 2–4 (run the pack, restore the P14 pin) remain **blocked**
   on the sandbox.

## 9. Method and limits

- Refs: all 33 (`git for-each-ref refs/remotes/origin`), fetched trees-only
  (`--filter=blob:none`); blobs read via `git cat-file -p` into `/tmp`; no
  checkout, no ref written, no suite executed.
- This sweep verifies **reachability and byte-identity**, not correctness: a
  matching hash proves a file is the one cited, never that a run succeeded.
- Every number quoted from the record is quoted with its source; the numbers
  computed here are line counts, digests and the §5 diff only.

---
**Sweep closed 2026-10-12 · base `ecaa656`, `main` at `6086096` · read-only.**
