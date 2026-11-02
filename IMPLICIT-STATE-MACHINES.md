# IMPLICIT-STATE-MACHINES — every state machine the tree carries without declaring it (2026-11-02)

Verdict first: the tree ran on sixteen state machines and declared none of
them. Eight lived in the two Python tools, one in the test harness, seven in the
process documents. On 2026-11-02 seven of the eight code transitions were
closed in code with witnessed tests, one (M4) was declared and pinned because
the protected corpus depends on it, and the seven document machines are still
prose. `tools/probe_state_machines.py` records the state of every code row and
exits 1 if one reopens; `bash tools/gate.sh` runs it beside the gate.

Two of them were leaking wrong answers: the leaderboard's row selector could
print the wrong arm's numbers, and the docs gate's fence reader dropped out of a
`~~~` block the moment it saw a ```` ``` ```` line. Both are reproduced below
with the command that showed them, and both are closed.

Definition used here: an implicit state machine is any place where distinct
behaviour is selected by a variable's value, a sentinel, a position in a list,
an exception, an exit code, or a documentation convention, and where the legal
transitions exist only in the author's head. Explicit means a named state set
plus a checked transition, or a test that pins the illegal ones.

## Inventory

| ID | Machine | States | Where the state lives | Enforced by |
|----|---------|--------|----------------------|-------------|
| M1 | Fence reader | outside fence, inside fence | `fenced` bool, `tools/check_docs.py:107` | nothing |
| M2 | Read-once document cache | unseen, seen | `lines_by_path` key presence, `tools/check_docs.py:220` | the witness read counter |
| M3 | Gate verdict | ok, problems, no input | return code 0 / 1 / 2, `tools/check_docs.py:215,263,268` | CI non-zero check |
| M4 | Heading-case verdict | allowed capital, sentence case, exempt | whitelists plus word index, `tools/check_docs.py:136-156` | nothing |
| M5 | Input cache | unhashed, hashed / unread, read | `_DIGESTS`, `_LINES`, `tools/gen_leaderboard.py:25-26` | nothing |
| M6 | Row recognition and selection | recognised, ignored, selected, absent | line prefix, field substrings, list order, `None`, `tools/gen_leaderboard.py:49-79` | nothing |
| M7 | Fail-loud path | measured, unmeasured | `sys.exit` from inside loops, `tools/gen_leaderboard.py:51,79,84,88,93,97,106` | exit code only |
| M8 | Seed-stability verdict | stable, varies | return type `float` or `str`, `tools/gen_leaderboard.py:107` | nothing |
| M9 | Test harness patching | real `open`, counting `open` | module global `builtins.open`, `tests/unit/*:69-73,148-153` | `try/finally` only |
| M10 | Mission pipeline | CLAIM, OBJECTION, VETO/SHAPE, VERDICT | prose, `README.md:14` | nothing |
| M11 | Board write protocol | APPEND, FLAG, SNAPSHOT, RESTORE | prose plus per-bot table, `README.md:8-10` | nothing |
| M12 | Mission status | ACTIVE, CLOSED-GREEN, slots empty or filled | `BLACKBOARD.md:3,39-79,82` | nothing |
| M13 | Trial lifecycle | queued, CLOSED, CLOSED-GREEN, SEALED, RE-BROKEN, HELD, PARKED | append-only log, `GOAL.md:15-38` | nothing |
| M14 | Commit verification | verified, unverified, partially verified | hook versus CI, `.githooks/pre-commit:8-9`, `.github/workflows/docs-gate.yml:4-15,26` | opt-in git config |
| M15 | Leaderboard freshness | generated, stale, hand-edited | file header only, `leaderboard.md:1-3` | nothing |
| M16 | Write-path class | protected, safe, undefined | table, `PROTECTED.md:7-29` | nothing |

## Code machines

Each entry records the machine as the audit found it on 2026-11-02, before the
change; "What closed, machine by machine" below says what replaced it and which
witness test holds it. The `Enforced by` column of the inventory is also the
state at audit time, not after.

### M1 — the fence reader is a two-state toggle that ignores delimiter identity

`tools/check_docs.py:100` accepts either fence marker, and `:110-112` flips a
single bool on any of them. There is no depth counter and no memory of which
marker opened the block, so a ```` ``` ```` line inside a `~~~` block closes it.
The reader then treats the block's body as prose and headings.

Reproduced: a file whose body is `~~~text` then a ```` ```python ```` line, a
`# Not A Heading` line, a closing ```` ``` ```` and a closing `~~~` reports a
heading violation on the line that sits inside the fence.

```
docs gate: 2 problems
  a.md:5: heading case | Heading | Not A Heading      <- inside the ~~~ block
  a.md:9: heading case | Heading, Here | Bad Heading Here
```

Illegal transition that is not rejected: opening a second fence without closing
the first. Legal transition that is not recognised: a fence marker that appears
as content inside another fence.

### M2 — the read-once cache is keyed by path presence, not by a lifecycle

`tools/check_docs.py:217-225` populates `lines_by_path` and skips a key that is
already present. The state is "has an entry" and it is never cleared, which is
correct inside one run and indistinguishable from correct across runs. This is
the one machine with a real witness: `tests/unit/test_check_docs.py:66-99`
counts `open` calls, so a refactor that re-reads a README fails.

### M3 — three verdicts on one integer

`tools/check_docs.py` returns 2 when the directory holds no markdown (`:213-215`),
1 when rules failed (`:259-263`), 0 otherwise (`:264-268`). CI only asks whether
the process succeeded (`docs-gate.yml:26`), so "you pointed the gate at the wrong
directory" and "your headings are wrong" are the same event to every caller.

### M4 — the heading rule exempts the first word of every segment

`tools/check_docs.py:139` splits the heading on an em dash and `:148` skips
index 0 of each resulting segment. The intent is the first word of the heading;
the effect is the first word after every dash. Verified:

```
'A thing \u2014 Two Words' -> ['Words']      <- 'Two' is never checked
'Two Words Here'         -> ['Words', 'Here']
```

So `# Something — Here we go` passes although `Here` is capitalised mid-sentence.
The exemption is a position, not a state, and nothing names it.

### M5 — module-level caches with no transition back to unseen

`tools/gen_leaderboard.py:29-46` keeps `_DIGESTS` and `_LINES` for the process
lifetime. The docstring says "once per run" but nothing defines a run. Verified:
generate a report, overwrite the round-04 log with different costs, generate
again in the same process, and the second report is byte-identical to the first.

```
first  : tax=+20 calls of 300 (6.67%) ...
second : tax=+20 calls of 300 (6.67%) ...
reports byte-identical after log changed: True
```

This also hides defects: while probing M6 below, an indented log still parsed
seventeen rows because the cache served the pre-edit lines.

### M6 — row recognition and selection carry four hidden states

`summaries` (`:49-59`) recognises a row only when it starts at column 0, so a
reflowed or indented log loses rows silently: a four-row file parses as two.
`pick` (`:67-79`) then decides which row is "the" row, and every part of that
decision is implicit:

- identity is a substring, not a field. `f"formation=routed" in s` also matches
  `formation=routed-thresholds`. Verified: with the thresholds row placed first,
  `pick(rows, "routed")` returns cost 250 instead of 260. The current round-03
  log happens to order `routed` before `routed-thresholds`, so the report is
  right today by accident of line order.
- the winner is the first match, so in an append-only log the oldest run wins.
  Verified: two rows for the same arm, earliest `cost=300 passed=46`, latest
  `cost=999 passed=41`; `pick` reports 300.
- `seed=None` means "wildcard, do not filter" (`:75`), while the row tuple uses
  `None` to mean "this log carries no seed" (`:58`). One sentinel, two states.
- a field that is absent becomes the string `None` in the published board,
  because `field` (`:62-64`) returns `None` and the caller interpolates it.
  Verified: dropping `hole_deliveries` from one row prints
  `holes None vs 2 under pre`, which reads as a measurement.

### M7 — fail-loud is control flow, not a state

Every guard in `gen_leaderboard.py` is `sys.exit("FAIL-LOUD: ...")` called from
inside a loop or a selector (`:51,79,84,88,93,97,106`). `sys.exit` with a
message raises `SystemExit` whose code is that string, which the interpreter
reports as exit status 1. Verified:

```
SystemExit code = FAIL-LOUD: no SUMMARY for nope seed=None n=46 mode=None
```

So "the fixture is missing", "the log is missing a ruling" and "no row matches
this arm" are one state to any caller, and none of them can be recovered from
inside the process.

### M8 — a verdict whose type is the verdict

`tools/gen_leaderboard.py:107` returns `0.0` when the sweep is flat and the
string `"VARIES"` when it is not. The caller interpolates both, so the union
type works by luck of `str()`; any future branch on `sd` would compare a float
to a string.

## Harness machine

### M9 — patched global `open`, restored by `try/finally` only

Both test modules replace `builtins.open` with a recorder
(`tests/unit/test_check_docs.py:69-73`, `tests/unit/test_gen_leaderboard.py:148-153`)
and restore the `REAL_OPEN` captured at import (`test_check_docs.py:25`). The
state is process-global and two-valued. Nothing asserts it is back to real after
a test, and several tests also rebind module constants in place
(`test_check_docs.py:111-115`, `:168-169` set `CLEAN_READMES` and `OUTPUT`).
Those mutations survive inside the module object; the suite is only safe because
each test loads a fresh module. That invariant is nowhere written down.

## Process machines

### M10 — the mission pipeline exists only as a sentence

`README.md:14` names the states: `CLAIM → OBJECTION → VETO/SHAPE → VERDICT`,
with the stage order before it. No tool reads a board:

```
grep -rn 'BLACKBOARD\|GOAL.md\|bets-ledger' tools/ tests/ .githooks/ .github/
no hits
```

Every transition, including the illegal ones the prose forbids (verdict before
objection, veto with no smaller subset at `README.md:18`), is unenforced. The
state is re-derived by a human reading the file.

### M11 — four message types, seven writers, one cap, zero parsers

`README.md:8` defines APPEND, FLAG, SNAPSHOT, RESTORE; `:9` maps each bot to
allowed sections; `:10` caps active CONSTRAINTS at seven with overflow into OPEN
GAPS. That is a complete protocol — message alphabet, write rights, a bounded
counter — and it exists exclusively as prose.

### M12 — two representations of mission status that disagree

`BLACKBOARD.md:3` says the ACTIVE MISSION is `CREW-EVIDENCE`, while `:82`
records ROUTER-V2 as CLOSED-GREEN and `:243` opens a further append. Meanwhile
all eleven structured slots (`:39-79`: GOAL, CONSTRAINTS, EVIDENCE, OPEN GAPS,
DECISIONS, BET MEMO, ARTIFACT, FLAGS, K-LINES, DISTILLED RULES, INTERVENTION
LOG) still read `_none_`. The board therefore stores status twice: as typed
slots that are empty, and as dated prose that is current. A reader has to know
which representation wins.

### M13 — trial lifecycle in an append-only log, with a duplicate transition

`GOAL.md:15-38` is the transition log: `Trial-NN queued` then `Trial-NN CLOSED`,
one line per trial, with verdicts CLOSED (21 occurrences), queued (17),
RE-BROKEN (16), HELD (7), SEALED (2), PARKED (1), CLOSED-GREEN (1). The current
state is "the last line", and nothing rejects an impossible transition. It has
already accepted a duplicate: `GOAL.md:30` (Trial-17) and `:32` (Trial-19) carry
the same three breaks and the same three fixes, so the log claims two distinct
trials produced one identical result.

### M14 — "this commit is verified" has two definitions

`.githooks/pre-commit:8-9` runs the docs gate and the unit tests. CI
(`.github/workflows/docs-gate.yml:26`) runs the docs gate only, and only when a
push touches `RESEARCH-COUNCIL/OUTPUT/**`, `RESEARCH-COUNCIL/README.md`,
`tools/check_docs.py` or the workflow itself (`:4-15`). Consequences: the
witness tests have never run in CI; a change to `tools/gen_leaderboard.py` or
`tests/**` triggers nothing; and the local half is opt-in because
`core.hooksPath` is not set in a fresh clone (verified: `core.hooksPath NOT set`),
so the default state of a commit is "unverified" while the repository reads as
gated. Commit `cfefa2a`, titled `ci: run the tool witness tests with the gate`,
landed in the hook, not in CI.

### M15 — a generated file with no way to tell it is stale

`leaderboard.md:1` says GENERATED, do not hand-edit, and `:3` says regenerate
with the tool, but no job regenerates it, no diff is compared and no hash of the
output is stored (grep for `gen_leaderboard` outside the tool: no hits). The
"generated" claim is unobservable, so stale and hand-edited are the same state.

### M16 — protected, safe, and everything else

`PROTECTED.md:11-13` lists protected trees; `:27-29` lists the safe write path.
A path in neither list has no defined state, and `tools/` and `tests/` are in
neither although `AGENTS.md:30-31` treats them as owned surfaces. No check
compares a diff against the table, so the classification is advice.

## Leaks found, ranked (state after the 2026-11-02 fixes)

1. ~~M6 substring identity: the leaderboard can print the `routed-thresholds`
   arm as `routed`.~~ Closed: `pick` compares parsed fields for equality.
2. ~~M6 first-match selection: a re-run appended to a log is ignored in favour of
   the older row.~~ Closed: contradictory duplicates are fatal, identical ones
   collapse, and an unpinned seed reads the lowest seed.
3. ~~M6 absent field: a missing measurement is published as `None`.~~ Closed:
   `field()` raises `MeasurementError`, `main()` turns it into `FAIL-LOUD`.
4. M1 delimiter identity: a `~~~` block that shows a ```` ``` ```` example
   produced false heading violations. Closed: the reader tracks its opening
   marker and length.
5. ~~M6 column-0 recognition: an indented log loses rows.~~ Closed: the row is
   recognised by its fields, not by its indentation.
6. M10-M16: the process rules are still unenforced, so a violation is only ever
   found by a reader who happens to check. M14 is the exception and is closed.

## The three decisions, and what they changed

Taken by the operator on 2026-11-02, because each one changes a contract rather
than a line:

1. Duplicate rows: two rows that share `(formation, verify_mode, seed, n)` and
   disagree are a hard error; byte-identical re-appends collapse. A report
   cannot say which of two contradictory measurements is the real one, so it
   refuses instead of choosing.
2. Missing field: fatal. `field()` raises `MeasurementError`; `main()` maps it
   to `FAIL-LOUD`. A printed `None` reads as a measurement, which is worse than
   a stopped report.
3. Fence policy: strict delimiter matching, CommonMark-style. A block closes
   only on a fence of the same character that is at least as long as the one
   that opened it.

One more, taken because the protected corpus forced it: the em-dash heading
exemption (M4) stays. Two `RESEARCH-COUNCIL/OUTPUT` headings depend on it
(`memory-architecture.md:413`, `testing-maturity-model.md:267`) and that corpus
is not editable, so the rule is named in a docstring and pinned by
`tests/unit/test_check_docs.py::HeadingConvention` instead of being removed.

## What closed, machine by machine

| Machine | Before | Now | Witness |
|---------|--------|-----|---------|
| M1 fence | one bool, either marker | opening marker and length tracked | `GateFenceReader` |
| M2 read-once cache | path presence | unchanged, already witnessed | `GateReadCost` |
| M3 verdicts | bare 0/1/2 | `OK`/`PROBLEMS`/`NO_INPUT` names | `GateVerdicts` |
| M4 heading | per-segment exemption, undeclared | same rule, declared and pinned | `HeadingConvention` |
| M5 caches | process lifetime | cleared at each `main()` | `LeaderboardFreshness` |
| M6 rows | substring, first match, `None` | field equality, fatal contradictions | `LeaderboardSelection`, `LeaderboardRefusals` |
| M7 fail-loud | `sys.exit` inside loops | `MeasurementError`, mapped once in `main()` | `LeaderboardRefusals` |
| M8 seed verdict | `0.0` or `"VARIES"` return | `(values, stable: bool)` | `LeaderboardFreshness` |
| M9 harness patch | `try/finally` only | unchanged, one module per test | `load_gate`, `load_tool` |
| M10-M16 process | prose | prose, except M14 (below) | none |
| M14 verified state | hook and CI disagree | both call `tools/gate.sh` | the script itself |

`tools/gate.sh` is the one definition of "verified": docs gate, witness tests,
state-machine probes. `.githooks/pre-commit` and
`.github/workflows/docs-gate.yml` both call it, and the workflow now triggers on
`tools/**`, `tests/**` and `.githooks/**` instead of `tools/check_docs.py`
alone, so the witness tests finally run in CI.

## What is still open

- M15 leaderboard freshness: `leaderboard.md` still carries no proof it matches
  the logs, and it was **not** regenerated on 2026-11-02 because
  `~/.hermes/crew/experiment/runs` is absent. The numbers in it predate these
  fixes and should be regenerated before anyone cites them again.
- M10-M13, M16: the pipeline, the board protocol, mission status and the
  write-path class are still prose. A board linter is the first slice worth
  building; do not start with the pipeline.
- M9: the harness still patches a global `open` and rebinds module constants;
  it is safe only because each test loads a fresh module. A `subTest`-based
  fixture that owns the patch would remove the last of that.

## What is already explicit, and should stay that way

The read-once contract is the model to copy: `tests/unit/test_check_docs.py:66-99`
and `test_gen_leaderboard.py:190-198` count real `open` calls, so M2 and the
read side of M5 are pinned by a witness rather than a convention. Rule ordering
in the gate's output is likewise pinned (`test_check_docs.py:183-187` asserts
the sequence em dash, bold, ref). Anything above that gets a witness test stops
being implicit.

## How this was checked

```
bash tools/gate.sh
  docs gate ok: 776 headings in 25 files; 2 READMEs clean; 32 refs resolve
  Ran 26 tests ... OK
  8 probes, 0 regression(s).
```

M1, M4, M6, M7 and M8 were first reproduced against scratch directories and logs
inside the process, then closed with a failing test written before the change
(`TEST-POLICY.md` §3): 14 new tests, of which 10 failed against the old code.
M5 was reproduced by generating twice around an in-place log edit. M10-M16 were
established by reading the files named in each entry and by the greps quoted
there.

The probes are committed as `tools/probe_state_machines.py` so the evidence
outlives the session: one row per machine, `CLOSED` when the tool refuses the
transition, `OPEN` when it is kept on purpose, and exit 1 if a row disagrees
with the state recorded above.

## Resume here

State: seven code transitions are closed and witnessed, M4 is declared and
pinned, and the gate runs the tests and the probes in one definition. Nothing in
this file is an outstanding decision; what follows is work, not judgement.

Order, if the thread is picked up again:

1. M15: regenerate `leaderboard.md` once a `~/.hermes/crew/experiment/runs`
   tree exists, and add the regeneration diff to CI. Until then its numbers are
   older than these fixes: do not cite them.
2. M9: give the harness one fixture that owns the `builtins.open` patch and the
   module-constant rebinding, so safety stops depending on "each test loads a
   fresh module".
3. M10-M13, M16: a board linter is the smallest enforceable slice. Start with
   the one contradiction that already exists: `BLACKBOARD.md:3` calls
   `CREW-EVIDENCE` the ACTIVE mission while `:82` records ROUTER-V2 as
   CLOSED-GREEN and all eleven slots read `_none_`.
4. Everything else in the "still open" list is prose by choice; leave it until
   a violation actually costs something.

Rules for whoever resumes: a probe row that flips is a regression, so fix the
tool rather than the expectation, and update `tests/unit/` in the same commit as
the tool. Do not hand-edit `leaderboard.md`, do not rewrite anything under
`RESEARCH-COUNCIL/**` (`PROTECTED.md:11`), and keep the §3 order: failing test,
then change.

Where this work sits: branch `cline/t60wwm9y` on origin. `AGENTS.md:39-40` asks
for everything on `main`, so land it with `git checkout main && git merge
--no-ff cline/t60wwm9y && git push origin main` once the Owner has read it.

When a fix makes a probe row print `FIXED`, the witness is gone: add the
replacement unit test under `tests/unit/` in the same commit, otherwise the
next refactor can reintroduce the transition silently.

What not to do while resuming: do not hand-edit `leaderboard.md`, do not rewrite
anything under `RESEARCH-COUNCIL/**` (`PROTECTED.md:11`), and do not regenerate
the board until a `~/.hermes/crew/experiment/runs` tree exists, because
`gen_leaderboard.py` exits rather than inventing numbers.

Where this work sits: branch `cline/t60wwm9y` on origin. `AGENTS.md:39-40` asks
for everything on `main`, so land it with `git checkout main && git merge
--no-ff cline/t60wwm9y && git push origin main` once the Owner has read it.
