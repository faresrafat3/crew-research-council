# REPRO-PACK-R04 — AUDIT (2026-10-12): availability + revision-pin check

> **What this file is:** a read-only audit of the reproducibility of mission
> ROUTER-V2 round 04, filed *beside* the frozen `REPRO-PACK-R04.md` — the
> mechanism `PROTECTED.md` prescribes ("add a new dated document beside it").
> It amends nothing: no number, claim, ruling or historical record is changed,
> re-scored or superseded by it. Every figure below is quoted from the paper
> that owns it.
>
> **What it did not do:** it did not run the R04 trial, the R04 suite or the R04
> ablation; it did not restore, move or reconstruct any artifact; it did not
> touch `~/.hermes/**`; it makes no claim about whether R04's numbers are true.
> It executed exactly one tracked command, `python3 tools/gen_leaderboard.py`
> (read-only, stdout only), and computed sha256 for tracked files.
>
> **Status:** audit artifact. It proposes one fix (§7) and **applies none**;
> that fix waits for the Owner's ruling. Owner: Fares. Language: English
> (artifacts) / Arabic (chat).

## 1. Checkout under audit

| item | value |
|---|---|
| commit | `ecaa656c8afe2a32913f4f9c86a5b5467433b97a` — "chore: add MIT license" (branch `main`, tree clean) |
| history | **1 commit total** (`git rev-list --count HEAD` = 1): the repository is a squashed publishing snapshot, so `git log` can corroborate **no** R04 claim |
| clone | partial (`promisor = true`, `partialclonefilter = blob:none`) — blobs arrive on demand |
| tracked files | 78 |
| R04 record here | `missions/ROUTER-V2/{PRE-REGISTRATION-R04,FINDINGS-R04,ADR-ROUTER-V2-R04,REPRO-PACK-R04}.md` · `BOARD.md` §ROUND 04 (L211–330) · `DECISIONS-LOG.md` (R04 rows) · `PRINCIPLES.md` P15–P18 · `BLACKBOARD.md` (L182–240) · `leaderboard.md` (L9–23) · `bets-ledger.md` (L9–18) |
| home dir | `$HOME` = `/home/node`; **`/home/node/.hermes` does not exist** — every `~/.hermes/...` path in this mission is local-only, as the brief required me not to assume otherwise |
| other refs | **31 non-`main` refs on `origin`** (30 × `orx/*` + `paper/draft`, all 2026-09-18/19) were fetched **trees-only** (`--filter=blob:none`) and inspected: they are the *pre-history* of this repository, not the ROUTER-V2 revision (§4) |

## 2. Verdict

**R04 is verifiable as a *report* and not reproducible from this checkout** — and
the deep dive says it is not reproducible from any of the repository's 33 refs
either (§4): what produced its numbers exists nowhere in git.

1. **The evidence is split by design.** Every artifact that produced R04's
   numbers — the runnable revision (`crew/**`), the suite (`tests/**`), the
   trial tools, both fixtures (`tasks/*.json`) and every verbatim log
   (`logs/round-04-trial.txt`, `r04-analysis.md`, the ablation, the witnesses,
   the adversarial log) — lives under
   `~/.hermes/crew/experiment/runs/2026-09-22-router-round-04/`, i.e. under the
   `.gitignore` entry `.hermes/`. `main` carries the papers only. §4 records the
   two exceptions that *are* retrievable from git — the frozen-20 fixture
   (byte-verified) and the round-01 ancestor stack — and neither of them is the
   revision R04 measured. `REPRO-PACK-R04.md` is therefore conditional on
   possessing the sandbox, and it does not say so.
2. **R04 pins no revision of the code that ran** (the one substantive
   *regression*, see §3 rows R9–R11). R03 pinned its measured revision
   (`logs/precut-sha256.txt`, `logs/artifacts-sha256.txt` — `BOARD.md` L206–207,
   `PRINCIPLES.md` P14). R04 records fixture, pre-registration and log hashes
   but **no hash of `crew/*.py` / `tests/**` / `tools/*.py`**, so "the exact
   implementation version" behind 292 / 288 / 278 is unpinned — for R04 and, by
   inheritance, for the R05 trial that will decide between `pre`,
   `pre + post-hop guard` and `final` (`ADR-ROUTER-V2-R04.md` ADR-14 Reversal).
3. **A dangling pointer forward.** `bets-ledger.md` L10 carries an R05 row that
   names `runs/2026-09-22-router-round-05/missions/PRE-REGISTRATION-R05.md`
   (sha256 `2f5c4b46…`, outcome `PENDING`). No `*-R05.md` file exists in this
   repository, and the path it names does not exist on disk. Nothing in the
   repository supersedes R04 — no `*-R05` paper, no FLAGS entry
   (`BLACKBOARD.md` §FLAGS = `_none_`; `missions/ROUTER-V2/BOARD.md` has no
   FLAGS section) — but the generated surface cannot represent R05 either:
   `tools/gen_leaderboard.py` reads rounds 02–04 only (L11–13).

**What is verifiable here, and checks out:** the frozen pre-registration hash,
and R04's internal arithmetic. Both are recorded in §3 (rows R12–R13 and R18).


## 3. Evidence table — claim | source | required artifact | status here

`MISSING` = absent from this checkout **and** not tracked by git; `UNVERIFIABLE`
= the claim depends on a `MISSING` artifact; `VERIFIED` = checked here today.

| # | claim (quoted) | source | artifact it requires | status here |
|---|---|---|---|---|
| R1 | tax `14` calls of `292` (4.79%), `14 = 7 tasks × 2` | `FINDINGS-R04.md` L37–43; `BOARD.md` E17–E18 (L248–256) | `logs/round-04-trial.txt` (sha256 `64ac515d…`), `logs/r04-analysis.md` (`6ec17759…`) | MISSING → UNVERIFIABLE |
| R2 | per-task identity `cost(pre) − cost(off) == verifier_calls` on all 46 | `FINDINGS-R04.md` L36–37; `REPRO-PACK-R04.md` L66–70 | the same trial log + the ablation log | MISSING → UNVERIFIABLE |
| R3 | frozen 20: `pre` 122, `+4` (3.28%), `off` 118, T7 + T15 | `FINDINGS-R04.md` L45; `REPRO-PACK-R04.md` L47–49 | `tasks/real-missions.json` (sha256 `28406677…`), trial log | fixture: **retrievable from git and byte-verified** (R18) · arm numbers: UNVERIFIABLE (they need the absent v2 code) |
| R4 | expanded 46 fixture, 17 classes | `REPRO-PACK-R04.md` L14 | `tasks/expanded-missions.json` (sha256 `26b3b832…`) | MISSING → UNVERIFIABLE |
| R5 | ablation reproduced through the literal `--no-verifier` alias; outcomes identical | `REPRO-PACK-R04.md` L59–70; `leaderboard.md` L23 | `tools/ablation_no_verifier_r04.py`, `logs/r04-no-verifier-ablation.txt` (`b6d07e83…`) | MISSING → UNVERIFIABLE |
| R6 | alias identity is one line (`verify_mode = "off" if args.no_verifier else args.verify`) and suite-asserted | `REPRO-PACK-R04.md` L81–83 | `crew/eval.py`, `tests/` | MISSING → UNVERIFIABLE |
| R7 | `final` skips HOLDs and re-verifies after a hop; max hops 2; 0 selection disagreements | `ADR-ROUTER-V2-R04.md` ADR-14/15; `FINDINGS-R04.md` L170–179 | `crew/formations.py`, `tools/adversarial_r04.py`, `logs/round-04-adversarial.txt` (`93f882d8…`) | MISSING → UNVERIFIABLE |
| R8 | RED `11 failed` → GREEN `126 passed` (111 + 13 + 2) | `REPRO-PACK-R04.md` L22; `BOARD.md` E15 (L242–244) | `tests/`, `logs/{RED,GREEN}-witness-r04.txt` | MISSING → UNVERIFIABLE; note the pack says "stdlib only" while the suite needs **pytest** (unpinned, not installed here) |
| R9 | the implementation version that ran | `ADR-ROUTER-V2-R04.md` ADR-14; `PRE-REGISTRATION-R04.md` L26 ("inherited revision \| round-03 sandbox") | a **revision pin**: `logs/artifacts-sha256.txt` / `precut-sha256.txt` over `crew/*.py`, `tests/**`, `tools/*.py` (R03 practice: `BOARD.md` L206–207, `PRINCIPLES.md` P14 L147–159) | **MISSING, and never named by R04** → the reported numbers are attributable to no pinned revision |
| R10 | declared budget `--max-tool-calls 2000` (per run) | `PRE-REGISTRATION-R04.md` L58; `REPRO-PACK-R04.md` L83–84 | `crew/` harness `Budget` | MISSING → UNVERIFIABLE |
| R11 | ruling `KEEP pre (registered fallback: the retarget failed its clause)` | `FINDINGS-R04.md` L100–103; `leaderboard.md` L16 | the generated `RULING:` line in `logs/r04-analysis.md` | MISSING → UNVERIFIABLE |
| R12 | pre-registration frozen **before** code and measurement, sha256 `ad9451ce…` | `FINDINGS-R04.md` L3–5; `BOARD.md` L214; `DECISIONS-LOG.md` L29 | `missions/ROUTER-V2/PRE-REGISTRATION-R04.md` | **VERIFIED** — `sha256sum` = `ad9451cefd805d9567f5852eefb98d7d1683b11cffef94b524009fa740599717` (exact match) |
| R13 | R04's arithmetic is internally consistent | `FINDINGS-R04.md` L39–49, L60–65, L78–82; `REPRO-PACK-R04.md` L47–53 | nothing (arithmetic over the quoted tables) | **VERIFIED** — 292−278=14=7×2 · 122−118=4=2×2 · 288−278=10=5×2 · guarded+hole+unselected = 4+1+18 = 23 = `resolved` under `pre`, 5+0+18=23 under `final`, 0+—+23=23 under `off` · 1+18=19 `unverified` under `pre`, 0+18=18 under `final`. Every quoted table closes |
| R14 | `leaderboard.md` is "GENERATED; do not hand-edit" and re-verifies the fixtures (`True`, `True`) | `leaderboard.md` L1–7 | `tools/gen_leaderboard.py` **plus** all four fixtures and three round logs | MISSING → UNVERIFIABLE (§6) |
| R15 | R05 pre-registration exists, sha256 `2f5c4b46…`, PENDING | `bets-ledger.md` L10, L12–18 | `runs/2026-09-22-router-round-05/missions/PRE-REGISTRATION-R05.md` | MISSING → a dangling reference inside a tracked file |
| R16 | `tests/**`, `crew/**`, `harness/**`, `repro/**` are untracked working copies holding "only `__pycache__`" | `PROTECTED.md` L13 | those trees | on `main` **absent entirely**; the 31 other refs carry a *different, older* revision of them (R17) — neither is R04's revision |
| R17 | the round-01 ancestor stack: `crew/{__init__,eval,roles,router}.py`, `harness/{__init__,state}.py`, `tests/test_crew.py`, `run.sh`, `variant.json`, `pyproject.toml` | `REPRO-PACK.md` L6 ("source suite 46 passed at copy time"); `DECISIONS-LOG.md` L5 | any ref | **RETRIEVABLE** from 30 `orx/*` refs + `paper/draft` (2026-09-18/19). It is an *ancestor*, not R04's revision: its `crew/eval.py` (5 077 B) exposes `--formation {solo,solo-checklist,duo,team}`, `--checklist`, `--shuffle-seed` and has **no `--verify`, no `--no-verifier`, no `--max-tool-calls`, no `--summary-json`**; its `crew/router.py` (1 354 B) holds only `complexity_score` + `propose_formation` — the cosmetic round-01 router R02 diagnosed |
| R18 | frozen fixture sha256 `28406677825eeeb5489e7ea6fc60ee7a992e55ea0629f8348436052cfba59a87` | `REPRO-PACK-R04.md` L13; `leaderboard.md` L5 | `tasks/real-missions.json` | **VERIFIED retrievable**: `git cat-file -p origin/orx/r9-consolidation-ledger-backed-laws-written-into:tasks/real-missions.json \| sha256sum` = `28406677…a87`, byte-identical on **15 of the 31** non-`main` refs. The other 16 carry six *divergent* fixture revisions (`72e56f08…`, `75cc3191…`, `8850bf47…`, `90c6fed1…`, `b2ddd73d…`, `eea367d1…`) — do not substitute one for another |
| R19 | the v2 stack + expanded fixture + tools + logs | `BOARD.md` L317–329; `REPRO-PACK-R04.md` L14, L34, L62 | any ref | **ABSENT from all 33 refs**: no `crew/formations.py`, `escalation.py`, `cognition.py`, `expertise.py`, `handoffs.py`, `router_thresholds.py`; no `tests/test_router*`; no `tasks/expanded-missions.json`; no `tools/run_trial_r04.py`, `tools/ablation_no_verifier_r04.py`, `tools/adversarial_r04.py`; no `logs/**` anywhere |


## 4. What *is* retrievable from git (verified today)

`main` is not the whole repository. `origin` carries **31 further refs** (30 ×
`orx/*` + `paper/draft`, all dated 2026-09-18/19): the repository's *pre-history*
— the 7→20-task formation-experiment preprint and its nine paper rounds R1–R9
that precede mission ROUTER-V2 (2026-09-22). They were fetched **trees-only**
(`--filter=blob:none`; blobs on demand), inspected, and nothing was checked out,
executed or modified. Two consequences for R04:

1. **The frozen-20 fixture is available and byte-verified.** Its sha256 on
   `origin/orx/r9-consolidation-ledger-backed-laws-written-into` and
   `origin/paper/draft` equals the `28406677…a87` that R02/R03/R04 froze — so
   that half of `REPRO-PACK-R04.md`'s "Frozen inputs" table is checkable today,
   without the sandbox. It is byte-identical on **15 of the 31** refs; the other
   16 carry six *divergent* fixture revisions (R18) — never substitute one for
   another.
2. **The round-01 ancestor stack is available** (`crew/{__init__,eval,roles,router}.py`,
   `harness/{__init__,state}.py`, `tests/test_crew.py`, `run.sh`, `variant.json`,
   `pyproject.toml`), but it is an *ancestor*, not R04's revision: no
   `crew/formations.py` (the module ADR-14 amends), no `--verify`/`--no-verifier`
   flag, no `tools/`, no `logs/`, no expanded fixture — those exist on **no ref**
   (R19). Running that stack would reproduce the round-01 experiments, not R04.

Commands — **RUN** (read-only; network read of refs/trees, no checkout):

```
git fetch --filter=blob:none --no-tags origin '+refs/heads/*:refs/remotes/origin/*'
git cat-file -p origin/orx/r9-consolidation-ledger-backed-laws-written-into:tasks/real-missions.json | sha256sum
#   28406677825eeeb5489e7ea6fc60ee7a992e55ea0629f8348436052cfba59a87   <- the sha R02/R03/R04 froze
git ls-tree -r --name-only origin/orx/r9-consolidation-ledger-backed-laws-written-into
git cat-file -p origin/orx/r9-consolidation-ledger-backed-laws-written-into:run.sh
#   python3 -m unittest discover -s tests -v   +   python3 -m crew.eval --tasks tasks/real-missions.json ...
git for-each-ref --format='%(refname:short)' refs/remotes/origin   # 33 refs total
```

**Numbering hazard (for the next auditor).** Two round-numbering systems now
coexist here: the preprint's **R1–R9** (on the `orx/*` refs) and the mission's
**R02–R05** (on `main`). `orx/r2-verifier-override-independent-verifier-flips`
is **not** ROUTER-V2 R02 and carries no `verify=final` mode. Read a branch name
as an experiment label, never as a mission round.

**Supersession re-checked against those refs.** `paper/draft` (2026-09-19,
"Compliance Lives in the Actor, Value Lives in the Team": 7→20 tasks, nine
rounds, solo 20/20 at cost 68, routed 87 with 9/20 resolved — not R02's 127)
predates ROUTER-V2 by three days and reports the *pre-v2* stack. It supersedes
nothing in R04; the supersession verdict in §2 stands.

## 5. Reproduction commands found in the record — **NOT RUN**

Quoted verbatim from `REPRO-PACK-R04.md`; all are **NOT RUN** here. Reason, for
every one of them: the working directory they `cd` into does not exist in this
checkout, and neither do the code, fixtures or logs they need.

| command (from `REPRO-PACK-R04.md`) | pack line | why NOT RUN |
|---|---|---|
| `cd ~/.hermes/crew/experiment/runs/2026-09-22-router-round-04` | L27 | path absent (`$HOME/.hermes` does not exist); the tree is `.gitignore`d |
| `python3 -m pytest tests/ -q` (must print `126 passed`) | L28 | `tests/` absent; pytest not installed here (Python here is 3.11.2; the pack declares 3.12) |
| `python3 tools/run_trial_r04.py` (regenerates trial log + `r04-analysis.md`) | L34 | tool absent |
| `python3 tools/ablation_no_verifier_r04.py` (the Owner's ablation) | L62 | tool absent |
| `python3 tools/adversarial_r04.py` (must print `status=ALL-HELD`) | L89 | tool absent |
| `python3 -m crew.eval --tasks tasks/expanded-missions.json --formation routed --hold-on-vague --max-tool-calls 2000 --verify pre` (plus `--verify final`, `--no-verifier`, and the frozen-20 `--shuffle-seed 7 --summary-json /tmp/s.json` variant) | L75–78 | `crew/` and `tasks/` absent |

**Historical passing logs are not treated as proof of a fresh run anywhere in
this audit.** The `126 passed`, `ALL-HELD` and `KEEP pre` lines are *reported*
results; nothing here re-executed them.

## 6. The in-repo command that was RUN, and what it proves

(§4 lists the read-only `git` commands that were also RUN; this section is about
the only tracked *tool* in the ROUTER-V2 evidence chain.)

```
$ python3 tools/gen_leaderboard.py
FAIL-LOUD: measurement log missing: /home/node/.hermes/crew/experiment/runs/2026-09-22-router-round-02/logs/round-02-routed.txt
(exit 1, no stdout)
```

`tools/gen_leaderboard.py` is the **only** runnable tracked artifact in this
repository that belongs to the ROUTER-V2 evidence chain, and it is hard-wired to
the sandbox root (`RUNS = os.path.expanduser("~/.hermes/crew/experiment/runs")`,
L10–22). Consequence: `leaderboard.md` — a surface that declares itself
GENERATED and not to be hand-edited — **cannot be regenerated or validated in
this checkout**; in a clone it is prose that merely looks generated. The tool's
behaviour is correct (fail-loud, never a silent partial board); what is missing
is the evidence root, which the repository deliberately does not carry.

## 7. Smallest correction proposed — one new file, no existing file touched

**Proposal (not applied).** Add a dated addendum beside the frozen pack:
`missions/ROUTER-V2/REPRO-PACK-R04-ADDENDUM-2026-10-12.md`, containing four
things and nothing else:

1. **A reproduction precondition line**, in the pack's own voice: *these
   commands require the sandbox
   `~/.hermes/crew/experiment/runs/2026-09-22-router-round-04/`, which is
   outside version control (`.gitignore`: `.hermes/`); a fresh clone can audit
   the papers, not the run.*
2. **The missing revision-pin row** that R03 had and R04 dropped — declared
   `UNPINNED for R04` rather than back-filled: R04's numbers are not bound to
   any hashed revision, so a future re-run cannot be shown to have used the
   revision that produced 292 / 288 / 278.
3. **The R05 requirement**: before R05 measures, write
   `logs/artifacts-sha256.txt` (code, tests, tools) and
   `logs/fixture-sha256.txt` into the R05 sandbox and cite both in
   `REPRO-PACK-R05.md` — the practice `PRINCIPLES.md` P14 already binds and R03
   already followed.
4. **A retrieval pointer for the half that is available**: the frozen-20 fixture
   (sha `28406677…a87`) is retrievable from `origin/orx/r9-consolidation-ledger-backed-laws-written-into`
   and `origin/paper/draft`, byte-verified; the v2 stack, the expanded fixture,
   the tools and every log are on no ref (§4, R18–R19).

**Why this is the smallest worthwhile change.** It adds no code, dependency,
agent or infrastructure, and no claim; it re-runs, restores and re-derives
nothing; it touches no frozen paper (R02–R04 papers stay byte-identical) and not
`leaderboard.md`. It closes the only gap in the record that is both real and
in-repo-fixable: a reader today cannot tell whether `REPRO-PACK-R04.md` is
runnable from a clone, and the P14 pin for R04 exists nowhere. It is filed as a
*new dated document beside* the pack, exactly as `PROTECTED.md` L38–41 requires
and as `DECISIONS-LOG.md` L37 already did for the R03/R04 papers.

**Affected files:** one added file. If the Owner wants the mission board to
carry it too: an `OPEN GAPS-R04` bullet in `missions/ROUTER-V2/BOARD.md` and a
dated `DECISIONS-LOG.md` row — both *appends* to accumulating surfaces, never
edits to a frozen region (the `logs/prewrite/` pre-append diff practice applies).

**Explicitly out of the proposal (would be scope expansion):** committing
`crew/**`, `tests/**`, `tasks/**` or `logs/**` into the repository; re-running
R04 or R05; changing `tools/gen_leaderboard.py`; editing any frozen paper;
touching the sandbox.

## 8. Acceptance check for the proposed fix

1. `sha256sum missions/ROUTER-V2/PRE-REGISTRATION-R04.md` →
   `ad9451cefd805d9567f5852eefb98d7d1683b11cffef94b524009fa740599717`
   (true today; the addendum must not disturb it).
2. The addendum's status column agrees with the filesystem:
   `for d in crew tests tasks logs harness repro; do [ -e "$d" ] && echo "$d PRESENT" || echo "$d MISSING"; done`
   → all `MISSING` at repo root.
3. The addendum contains `UNPINNED` for R04 and names `artifacts-sha256.txt` as
   the R05 requirement.
4. `git diff --stat <base>..HEAD` lists **only added** files — no modification
   to any R02/R03/R04 paper, `leaderboard.md`, or `tools/gen_leaderboard.py`.
5. Every number in the addendum carries a `file:line` reference; none is newly
   computed.
6. The addendum records the one half that *is* checkable without the sandbox:
   `git cat-file -p origin/orx/r9-consolidation-ledger-backed-laws-written-into:tasks/real-missions.json | sha256sum`
   → `28406677825eeeb5489e7ea6fc60ee7a992e55ea0629f8348436052cfba59a87`
   (true today; §4), together with the caution that 16 other refs carry
   divergent fixtures.

## 9. Handoff task list (for the next agent)

- [ ] Owner ruling on §7. If approved: write
      `REPRO-PACK-R04-ADDENDUM-2026-10-12.md` (the three items above, ≤1 page),
      then optionally the `BOARD.md` / `DECISIONS-LOG.md` appends.
- [ ] Ask the Owner for the R04 sandbox
      (`~/.hermes/crew/experiment/runs/2026-09-22-router-round-04/`) **or** a
      copy of `logs/round-04-trial.txt` + `logs/r04-analysis.md`. Until it
      exists somewhere reachable, R04's numbers stay `UNVERIFIABLE` — do not
      reconstruct them from the papers.
- [ ] If the sandbox is produced: run §5's commands as written, then diff the
      result against `REPRO-PACK-R04.md` L47–53; any deviation is a finding on
      the board with the diff, not a silent re-run.
- [ ] If a reviewer wants the retrievable half instead: `git worktree add /tmp/anc
      origin/orx/r9-consolidation-ledger-backed-laws-written-into` reproduces the
      **round-01** experiments only (its suite is `unittest`, not `pytest`; its
      `eval.py` has no `--verify`). Do not present its numbers as R04's.
      NOT RUN here, by the first-pass boundary.
- [ ] Restore the P14 pin for R04 once the sandbox appears (`sha256sum` over
      `crew/*.py tests/** tools/*.py` → `logs/artifacts-sha256.txt`), and pin
      before R05 measures.
- [ ] Resolve the dangling R05 pointer in `bets-ledger.md` L10: either the R05
      pre-registration lands in `missions/ROUTER-V2/`, or the row is annotated
      as pointing outside the repository.
- [ ] `tools/gen_leaderboard.py` reads rounds 02–04 only (L11–13) while
      `leaderboard.md` calls round 04 "current": extend it when R05 lands, or
      annotate the board — never hand-edit the generated surface.
- [ ] `PROTECTED.md` L13 declares `crew/**` / `tests/**` as present-but-empty;
      today they are absent. Worth a dated note beside `PROTECTED.md` (its own
      L38–41 rule) if the Owner wants the declaration to match the disk.

---
**Audit closed 2026-10-12 · base commit `ecaa656` · read-only · no fix applied.**
