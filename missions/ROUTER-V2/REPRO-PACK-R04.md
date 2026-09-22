# REPRO-PACK — mission ROUTER-V2 Round 04

> Round 03's pack is preserved beside this one (`REPRO-PACK-R03.md`, sandbox
> `2026-09-22-router-round-03`). R04 adds a configuration axis (verification
> mode), prices it, and adopts **nothing**: `pre` stays shipped, `final` stays
> an exercised non-default mode. Everything below reproduces the numbers the
> ruling was computed from.

## Frozen inputs

| item | value |
|---|---|
| frozen fixture (20) | `tasks/real-missions.json` — sha256 `28406677825eeeb5489e7ea6fc60ee7a992e55ea0629f8348436052cfba59a87` |
| expanded fixture (46) | `tasks/expanded-missions.json` — sha256 `26b3b832a2233693875b5b12e1093b4d55d0c019421f63bfbbebab3c417898c0` |
| pre-registration | `missions/PRE-REGISTRATION-R04.md` — sha256 `ad9451cefd805d9567f5852eefb98d7d1683b11cffef94b524009fa740599717` |
| trial log (verbatim arms) | `logs/round-04-trial.txt` — sha256 `64ac515d03f275b7ebab81778f6519fdac9cd3a90aac56f141aef2e35f92d65f` |
| generated analysis | `logs/r04-analysis.md` — sha256 `6ec17759a4d804b147040f65513954ac0a1921f8a87176c69b7e30b011b78588` |
| ablation log (alias path) | `logs/r04-no-verifier-ablation.txt` — sha256 `b6d07e83cecfa1259ddc8315434a1ff9e52fe63c8e1429db88350811523e979e` |
| adversarial self-review | `logs/round-04-adversarial.txt` — sha256 `93f882d87655f77b8630ca29cc65892cf4f8136943f5a62b15336a9bf69b6d3a` |
| sandbox | `~/.hermes/crew/experiment/runs/2026-09-22-router-round-04/` |
| environment | stdlib only, offline, Python 3.12, no API keys, no model calls |
| baseline witness | inherited suite `111 passed` at copy time; RED `11 failed`; GREEN `126 passed` (`logs/GREEN-witness-r04.txt`) |

## Full suite (must print `126 passed`)

```
cd ~/.hermes/crew/experiment/runs/2026-09-22-router-round-04
python3 -m pytest tests/ -q
```

## The trial, end to end (regenerates `logs/round-04-trial.txt` + `r04-analysis.md`)

```
python3 tools/run_trial_r04.py
```

It runs, in order: the three verification modes (`pre`, `final`, `off`) on the
frozen fixture (seed 7), the same three on the expanded fixture, the champion
arm (`solo --hold-on-vague`), the seed sweep (7/11/13/17/19 × three modes on
the expanded fixture), and the determinism double-runs; then it computes the
registered three-way ruling (`CUT` / `REPLACE` / `KEEP`) from the pre-registered
clauses and writes `logs/r04-analysis.md`.

Expected key SUMMARY lines (verbatim from `logs/round-04-trial.txt`):

```
SUMMARY n=20 passed=20 rate=1.000 grave_errors=0 total_cost=122 resolved=9  ... verify_mode=pre   verifier_calls=4  verifier_tasks=2 unverified_deliveries=8  hole_deliveries=0 unselected_deliveries=8  formation=routed
SUMMARY n=20 passed=20 rate=1.000 grave_errors=0 total_cost=120 resolved=9  ... verify_mode=final verifier_calls=2  verifier_tasks=1 unverified_deliveries=8  hole_deliveries=0 unselected_deliveries=8  formation=routed
SUMMARY n=20 passed=20 rate=1.000 grave_errors=0 total_cost=118 resolved=9  ... verify_mode=off   verifier_calls=0  verifier_tasks=0 unverified_deliveries=9  hole_deliveries=1 unselected_deliveries=8  formation=routed
SUMMARY n=46 passed=46 rate=1.000 grave_errors=0 total_cost=292 resolved=23 ... verify_mode=pre   verifier_calls=14 verifier_tasks=7 unverified_deliveries=19 hole_deliveries=1 unselected_deliveries=18 formation=routed
SUMMARY n=46 passed=46 rate=1.000 grave_errors=0 total_cost=288 resolved=23 ... verify_mode=final verifier_calls=10 verifier_tasks=5 unverified_deliveries=18 hole_deliveries=0 unselected_deliveries=18 formation=routed
SUMMARY n=46 passed=46 rate=1.000 grave_errors=0 total_cost=278 resolved=23 ... verify_mode=off   verifier_calls=0  verifier_tasks=0 unverified_deliveries=23 hole_deliveries=5 unselected_deliveries=18 formation=routed
SUMMARY n=46 passed=46 rate=1.000 grave_errors=0 total_cost=159 resolved=12 ... formation=solo   (champion: runs no verification at all)
```

Expected ruling line (generated): `KEEP pre (registered fallback: the retarget
failed its clause)`.

## The ablation the Owner asked for (regenerates `logs/r04-no-verifier-ablation.txt`)

```
python3 tools/ablation_no_verifier_r04.py
```

Runs the literal `--no-verifier` alias against `--verify pre` on both fixtures,
reads each arm's own `--summary-json`, and asserts the per-task identity
`cost(pre) − cost(off) == verifier_calls`. Expected: tax **14 calls of 292**
(4.79%, 0.304 calls/task, 7 selected tasks) on the 46-task fixture and **4 of
122** (3.28%, 0.200/task, 2 tasks) on the frozen one; identity HOLDS on every
task; outcomes IDENTICAL (grade+verdict) in both arms.

## Single arms by hand

```
python3 -m crew.eval --tasks tasks/expanded-missions.json --formation routed --hold-on-vague --max-tool-calls 2000 --verify pre
python3 -m crew.eval --tasks tasks/expanded-missions.json --formation routed --hold-on-vague --max-tool-calls 2000 --verify final
python3 -m crew.eval --tasks tasks/expanded-missions.json --formation routed --hold-on-vague --max-tool-calls 2000 --no-verifier
python3 -m crew.eval --tasks tasks/real-missions.json --formation routed --hold-on-vague --shuffle-seed 7 --max-tool-calls 2000 --summary-json /tmp/s.json
```

`--no-verifier` and `--verify off` must select the same path (implemented in
one line: `verify_mode = "off" if args.no_verifier else args.verify`), and the
suite asserts the two are behaviourally identical. `--max-tool-calls` matters:
the cap is per RUN, and the expanded fixture needs 292 calls on the shipped arm.

## Adversarial self-review (must print `status=ALL-HELD`)

```
python3 tools/adversarial_r04.py
```

10 attacks; the six limited verdicts are the threats listed in
`FINDINGS-R04.md` §Threats to validity (instrument blindness, the post-hoc
metric split, the price's scope, the champion's missing verifier, n=1 hole, the
tautological seed sweep).

## Honest limits on reproduction

- `wall_s` varies by machine; every other SUMMARY field is deterministic
  (sd=0.000 across five seeds for all three modes, and byte-identical
  double-runs per mode).
- The price is a *pass* price. If a verifier ever rejects a delivery and the
  ladder spends a repair hop because of it, the true price includes that hop;
  with `verifier_flips=0` in every mode here, no such hop exists in this round.
- `hole_deliveries` / `unselected_deliveries` were introduced **after** the
  registered clause was refuted and are marked exploratory; they are reported
  alongside `unverified_deliveries` (the pre-registered metric) and are not used
  in the ruling. Reproducing the ruling requires the pre-registered aggregate.
- Under `verify=off` the trigger still fires (`verifier_calls=0`) and the
  deliveries it would have guarded count as holes — `off` is a measurement arm,
  forbidden by the registered no-CUT clause from ever being shipped.
- Any deviation from the expected lines is a finding: record it on the board
  with the diff.
