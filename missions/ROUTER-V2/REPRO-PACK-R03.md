# REPRO-PACK — mission ROUTER-V2 Round 03

> Round 02's pack is preserved beside this one (`REPRO-PACK.md`, sandbox
> `2026-09-22-router-round-02`). R03 changes one measured arm (the ablation
> now runs the ladder) and cuts one mechanism, so it documents both the
> pre-cut revision it measured and the post-cut revision it ships.

## Frozen inputs

| item | value |
|---|---|
| frozen fixture (20) | `tasks/real-missions.json` — sha256 `28406677825eeeb5489e7ea6fc60ee7a992e55ea0629f8348436052cfba59a87` |
| expanded fixture (46) | `tasks/expanded-missions.json` — sha256 `26b3b832a2233693875b5b12e1093b4d55d0c019421f63bfbbebab3c417898c0` |
| pre-registration | `missions/PRE-REGISTRATION-R03.md` — sha256 `1abb28538bb57f4f694b04851c61fbfd61558f7784a770f04fa4f5e1d384f706` |
| pre-cut revision | `logs/precut-sha256.txt` (router/formations/eval/state/test hashes) |
| sandbox | `~/.hermes/crew/experiment/runs/2026-09-22-router-round-03/` |
| environment | stdlib only, offline, Python 3.12, no API keys, no model calls |
| baseline witness | inherited suite 90 passed at copy time; RED `14 failed, 4 passed`; GREEN `109 passed` |

## Full suite (must print `109 passed`)

```
cd ~/.hermes/crew/experiment/runs/2026-09-22-router-round-03
python3 -m pytest tests/ -q
```

## The trial, end to end (regenerates logs/round-03-trial.txt + r03-analysis.md)

```
python3 tools/run_trial_r03.py
```

This runs, in order: the three arms on the frozen fixture (seed 7), the three
arms on the expanded fixture (authored order), the seed sweep
(7/11/13/17/19 × three arms on the expanded fixture), and the determinism
double-runs; then it computes the H13 ruling from the four pre-registered
clauses and writes `logs/r03-analysis.md`.

Expected key SUMMARY lines (verbatim from `logs/round-03-trial.txt`):

```
SUMMARY n=20 passed=20 rate=1.000 grave_errors=0 total_cost=68 resolved=4 routing_match=11/20 ... formation=solo
SUMMARY n=20 passed=20 rate=1.000 grave_errors=0 total_cost=127 resolved=9 routing_match=19/20 ... formation=routed
SUMMARY n=20 passed=20 rate=1.000 grave_errors=0 total_cost=122 resolved=9 routing_match=11/20 ... formation=routed-thresholds
SUMMARY n=46 passed=46 rate=1.000 grave_errors=0 total_cost=159 resolved=12 routing_match=23/46 ... formation=solo
SUMMARY n=46 passed=46 rate=1.000 grave_errors=0 total_cost=307 resolved=23 routing_match=44/46 ... formation=routed
SUMMARY n=46 passed=46 rate=1.000 grave_errors=0 total_cost=292 resolved=23 routing_match=25/46 ... formation=routed-thresholds
```

Expected ruling line (generated): `--- H13 RULING: KILL ... ---`.

## Single arms by hand

```
python3 -m crew.eval --tasks tasks/expanded-missions.json --formation solo --hold-on-vague --max-tool-calls 2000
python3 -m crew.eval --tasks tasks/expanded-missions.json --formation routed --hold-on-vague --max-tool-calls 2000
python3 -m crew.eval --tasks tasks/expanded-missions.json --formation routed-thresholds --hold-on-vague --max-tool-calls 2000
python3 -m crew.eval --tasks tasks/real-missions.json --formation routed --hold-on-vague --shuffle-seed 7 --max-tool-calls 2000 --summary-json /tmp/s.json
```

`--max-tool-calls` matters: the cap is per RUN, and the expanded fixture
exceeds the historical default of 100.

## Post-cut verification (must print `RESULT: ALL-PASS`)

```
python3 tools/verify_postcut_r03.py
```

Checks: the router exposes no `CLASS_TABLE`; `routed` and `routed-thresholds`
are behaviourally identical on both fixtures; the post-cut arm numbers equal
the trial's ablation arm (122 / 292 calls, 9 / 23 resolved); and it prints the
sha256 of the untouched trial log.

## Honest limits on reproduction

- `wall_s` varies by machine; every other SUMMARY field is deterministic
  (H14 measured sd=0.000 across five seeds).
- The pre-cut numbers require the pre-cut revision
  (`logs/precut-sha256.txt`). The shipped revision no longer contains the
  class table by design; re-running the trial after the cut reproduces the
  `routed-thresholds` column for both arm names, and that is the post-cut
  expectation, not a reproduction failure.
- `logs/_tmp/` holds the per-arm JSON summaries written by the last trial run;
  the generated tables in `logs/r03-analysis.md` read from those files, not
  from prose. They are overwritten on each run.
- Any deviation from the expected lines is a finding: record it on the board
  with the diff.
