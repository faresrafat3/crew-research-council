# REPRO-AUDIT — the preprint's rounds R1–R9 (2026-10-12)

> **The one part of this repository whose published numbers reproduce.** The
> nineteen node runs behind `paper/draft:paper.tex` (Table 1) are committed as
> per-node branches under `orx/*`, complete with code, fixture, `variant.json`
> and the fixed `bash run.sh` recipe — so they can be re-executed from a clone,
> offline, in seconds. This file records that reproduction and the exact recipe.
>
> **Read-only w.r.t. the repository.** Every node was extracted with
> `git archive` into `/tmp/nodes/`, then run there. No sandbox was touched, no
> ref was moved, no file here was modified, and no published number is changed:
> the audit's result is that the published numbers are **correct**.
> Owner: Fares. Language: English (artifacts) / Arabic (chat).

## 1. Headline

**18 of 18 rows of the preprint's results table reproduce exactly** — `n`,
`passed`, `cost` and `resolved` all equal the published values — and **19 of 19
tracked node runs are green** (`Ran N tests … OK`, then a `SUMMARY` line). Three
nodes re-run twice produced **byte-identical stdout**.

This is the inverse of the mission rounds: R02–R05 froze their *intent* in the
repository and left their *evidence* in sandboxes (`REPRO-AUDIT-R02-R03-2026-10-12.md`,
`REPRO-PACK-R04-AUDIT-2026-10-12.md`), while the preprint's rounds kept the
runnable revision in git and therefore still run today.

## 2. The reproduction table (published vs re-executed)

Paper: `paper/draft:paper.tex` Table 1. Run: `bash run.sh` inside
`git archive origin/orx/<ref>` in `/tmp`.

| paper's node | ref (`origin/orx/…`) | published n / passed / cost / resolved | re-executed | verdict |
|---|---|---|---|---|
| baseline-solo | `baseline-solo-rule-based-executor-reviewer-on-7` | 7 / 6 / 26 / — | 7 / 6 / 26 (grave 1) | **EXACT** |
| R1 hold-rule | `r1-solo-hold-rule-explicit-briefs-flip-t2` | 7 / 7 / 26 / — | 7 / 7 / 26 | **EXACT** |
| R1 duo | `r1-duo-executor-reviewer-with-verifier-cost` | 7 / 6 / 40 / — | 7 / 6 / 40 (grave 1) | **EXACT** |
| R1 checklist | `r1-solo-checklist-attention-without-decision-rul` | 7 / 6 / 33 / — | 7 / 6 / 33 (grave 1) | **EXACT** |
| R2 contradiction-hold | `r2-contradiction-hold-executor-self-checks-undel` | 8 / 8 / 29 / — | 8 / 8 / 29 | **EXACT** |
| R2 verifier-override | `r2-verifier-override-independent-verifier-flips` | 8 / 8 / 45 / — | 8 / 8 / 45 | **EXACT** |
| R2 routed | `r2-routed-per-task-formation-t7-runs-pipeline` | 8 / 7 / 33 / — | 8 / 7 / 33 (grave 1) | **EXACT** |
| R3 solo-limits | `r3-solo-limits-tool-humility-and-conflict-detect` | 10 / 10 / 35 / 4 | 10 / 10 / 35 / 4 | **EXACT** |
| R3 team-resolve | `r3-team-resolve-researcher-grounds-t10-resolutio` | 10 / 10 / 37 / 5 | 10 / 10 / 37 / 5 | **EXACT** |
| R4 solo-replication | `r4-solo-replication-shuffled-order-unseen-probes` | 13 / 13 / 44 / 4 | 13 / 13 / 44 / 4 | **EXACT** |
| R4 team-replication | `r4-team-replication-shuffled-order-unseen-probes` | 13 / 13 / 48 / 6 | 13 / 13 / 48 / 6 | **EXACT** |
| R5 solo-synthesis | `r5-solo-synthesis-multi-source-probes-tool-humil` | 16 / 16 / 54 / 4 | 16 / 16 / 54 / 4 | **EXACT** |
| R5 team-synthesis | `r5-team-synthesis-researcher-synthesizes-t14-t16` | 16 / 16 / 65 / 8 | 16 / 16 / 65 / 8 | **EXACT** |
| R6 solo-adversarial | `r6-solo-adversarial-poisoned-partial-and-malicio` | 19 / 19 / 64 / 4 | 19 / 19 / 64 / 4 | **EXACT** |
| R6 team-adversarial | `r6-team-adversarial-grounded-synthesis-under-att` | 19 / 19 / 81 / 9 | 19 / 19 / 81 / 9 | **EXACT** |
| R7 red (phantom) | `r7-red-t21-truncation-severs-grounding-coverage` | 20 / 20 / 87 / 10 | 20 / 20 / 87 / 10 | **EXACT** |
| R7 solo-check | `r7-solo-check-t21-under-solo-coverage-audit` | 20 / 20 / 68 / 4 | 20 / 20 / 68 / 4 | **EXACT** |
| R8 repair | `r8-repair-citation-integrity-check-converts-phan` | 20 / 20 / 87 / 9 | 20 / 20 / 87 / 9 | **EXACT** |
| *19th tracked run* (not tabulated) | `r9-consolidation-ledger-backed-laws-written-into` | — | 20 / 20 / 87 / 9 | reproduces the R8 node |

`grave_errors` is not a column in the paper's table; the re-runs report it and it
agrees with each node's `passed` deficit (baseline, R1 duo, R1 checklist and R2

## 3. The recipe (copy-paste)

```
# one node, end to end — no network, no install, stdlib only
d=/tmp/nodes/r7-red && mkdir -p $d
git archive origin/orx/r7-red-t21-truncation-severs-grounding-coverage | tar -x -C $d
cd $d && bash run.sh            # unit tests, then the blind evaluation + SUMMARY

# determinism (the paper's "deterministic" claim)
bash run.sh > /tmp/a.txt 2>&1; bash run.sh > /tmp/b.txt 2>&1; diff -q /tmp/a.txt /tmp/b.txt
```

`run.sh` is the fixed recipe quoted in the paper's Method: `python3 -m unittest
discover -s tests -v` followed by `python3 -m crew.eval --tasks
tasks/real-missions.json` with the arm's flags taken from that node's
`variant.json`. Nothing in it installs or fetches anything (the torch path exists
only on the `orx/repro-*` branches, behind `REPRO_MODEL=1`, and was **not**
exercised).

## 4. Fixtures per node (so a reader can pin what ran)

| ref group | fixture sha256 (12) | tasks |
|---|---|---|
| baseline + R1 (4 refs) | `90c6fed1504a` | 7 |
| R2 (3 refs) | `72e56f08de9a` | 8 |
| R3 (2 refs) | `b2ddd73dce48` | 10 |
| R4 (2 refs) | `8850bf47040b` | 13 |
| R5 (2 refs) | `eea367d1e0b3` | 16 |
| R6 (2 refs) | `75cc3191a8b3` | 19 |
| R7 + R8 + R9 (4 refs) | `28406677825e` | 20 |

**A provenance link worth recording:** the R7–R9 fixture hash is the *full*
`28406677825eeeb5489e7ea6fc60ee7a992e55ea0629f8348436052cfba59a87` — the same
frozen-20 that R02, R03 and R04 measured and that `leaderboard.md` L5 cites. The
mission's frozen fixture is therefore the preprint lineage's R7+ fixture,
inherited byte-identical. That is the one artifact the two evidence worlds share.

## 5. Why this reproduces and the mission rounds do not

| | preprint rounds R1–R9 | mission rounds R02–R05 |
|---|---|---|
| code | committed per node (`orx/*`) | sandbox only, on no ref |
| fixture | committed per node | frozen-20 committed (R7+ hash); expanded-46 on no ref |
| recipe | committed (`run.sh` + `variant.json`) | quoted in the repro pack, path absent |
| logs | not committed — but **not needed**: `run.sh` regenerates the SUMMARY | not committed and not regenerable |
| result | **18/18 rows reproduce** | `UNVERIFIABLE` |

The difference is not rigour, it is where the runnable revision was kept: the
preprint rounds kept it in git, the mission rounds kept it in a `.gitignore`d
sandbox and shipped only papers.

## 6. Smallest correction proposed

**NO CHANGE to any artifact.** Nothing is missing, wrong or misleading here: the
published table is correct as written, the recipe is in the repository, and this
file is the record that the check happened. Two optional, non-blocking notes:

1. `paper/draft:paper.tex` Method says "All 19 tracked runs …" while Table 1 has
   18 rows; the 19th is the R9 consolidation run, which reproduces the R8 node
   (20/20/87/9). A one-line footnote in a **future** revision of the paper would
   close that small gap — not worth touching a committed draft.
2. The `orx/*` branches are the only place the preprint's runnable revisions
   exist. If those branches are ever deleted, the paper becomes as unreproducible
   as R02–R05. Worth knowing before any branch cleanup.

## 7. Method and limits

- 19 refs, `git archive` → `/tmp/nodes/<ref>`, `bash run.sh` each; 3 re-run twice
  for the determinism check. Total wall time: seconds; nothing written inside the
  repository or any ref.
- The re-runs use this machine's CPython (3.11.2) while the sandboxes declared
  3.12; `random.Random(seed).shuffle` and the stdlib-only code paths are
  version-stable, and the byte-identical double runs support the paper's
  determinism claim. A 3.12 cross-check remains open (not run).
- This audit reproduces the **preprint** (pre-v2) stack. It says nothing about
  R02–R05, whose revisions are still absent, and it does not re-score any
  mission ruling.

---
**Audit closed 2026-10-12 · base `ecaa656`, `main` at `ecce3e4` · read-only.**

routed carry exactly 1 grave each). Suite results: `Ran 10, 10, 10, 10, 13, 14,
12, 18, 19, 22, 23, 26, 27, 30, 31, 34, 33, 35, 35 tests … OK` in that row order
— all green, matching the paper's "All 19 tracked runs are local, deterministic,
and green".
