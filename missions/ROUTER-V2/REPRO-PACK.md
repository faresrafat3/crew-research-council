# REPRO-PACK — mission ROUTER-V2 Round 02

## Frozen inputs

| item | value |
|---|---|
| fixture | `tasks/real-missions.json` — sha256 `28406677825eeeb5489e7ea6fc60ee7a992e55ea0629f8348436052cfba59a87` |
| pre-registration | `missions/PRE-REGISTRATION.md` — sha256 `7e14c9d28120aa2703ac25e6af8d1929f49357bf41e326cb71b70a779524f0ba` |
| sandbox | `~/.hermes/crew/experiment/runs/2026-09-22-router-round-02/` |
| environment | stdlib only, offline, Python 3.12, no API keys, no model calls |
| baseline witness | source suite 46 passed at copy time |

## Full suite (must print `90 passed`)

```
cd ~/.hermes/crew/experiment/runs/2026-09-22-router-round-02
python3 -m pytest tests/ -q
```

## Arms (seed 7)

```
python3 -m crew.eval --tasks tasks/real-missions.json --formation solo --hold-on-vague --shuffle-seed 7
python3 -m crew.eval --tasks tasks/real-missions.json --formation routed --shuffle-seed 7
python3 -m crew.eval --tasks tasks/real-missions.json --formation routed --hold-on-vague --shuffle-seed 7
python3 -m crew.eval --tasks tasks/real-missions.json --formation routed-thresholds --hold-on-vague --shuffle-seed 7
```

Expected SUMMARY lines (verbatim from `logs/round-02-routed.txt`):

```
SUMMARY n=20 passed=20 rate=1.000 grave_errors=0 total_cost=68 resolved=4 routing_match=11/20 wall_s=0.00 escalations=0 guard_flags=0 formation=solo
SUMMARY n=20 passed=19 rate=0.950 grave_errors=1 total_cost=127 resolved=9 routing_match=0/20 wall_s=0.00 escalations=14 guard_flags=2 formation=routed
SUMMARY n=20 passed=20 rate=1.000 grave_errors=0 total_cost=127 resolved=9 routing_match=0/20 wall_s=0.00 escalations=15 guard_flags=2 formation=routed
SUMMARY n=20 passed=20 rate=1.000 grave_errors=0 total_cost=70 resolved=4 routing_match=0/20 wall_s=0.00 escalations=0 guard_flags=0 formation=routed-thresholds
```

## Variance sweep (expected: identical SUMMARY per arm across all seeds)

```
for s in 7 11 13 17 19; do python3 -m crew.eval --tasks tasks/real-missions.json \
  --formation solo --hold-on-vague --shuffle-seed $s | grep SUMMARY; done
for s in 7 11 13 17 19; do python3 -m crew.eval --tasks tasks/real-missions.json \
  --formation routed --hold-on-vague --shuffle-seed $s | grep SUMMARY; done
```

## Determinism check

```
python3 -m crew.eval --tasks tasks/real-missions.json --formation routed \
  --hold-on-vague --shuffle-seed 7 > /tmp/a.txt
python3 -m crew.eval --tasks tasks/real-missions.json --formation routed \
  --hold-on-vague --shuffle-seed 7 > /tmp/b.txt
diff -q /tmp/a.txt /tmp/b.txt && echo DETERMINISM-PASS
```

## Tracker / probes

```
python3 -m crew.eval --tasks tasks/real-missions.json --formation routed \
  --hold-on-vague --shuffle-seed 7 --ledger expertise/ledger-round02.jsonl
python3 -c "from crew.expertise import ExpertiseTracker as T; \
  t=T(path='expertise/ledger-round02.jsonl'); print(t.report())"
```

## Honest limits on reproduction

- `wall_s` varies by machine; every other SUMMARY field is deterministic.
- The raw JSONL ledger line order follows task shuffle order — stable for a
  fixed seed and fixture hash, different if either changes.
- Any deviation from the expected lines is a finding, not a failure of the
  reproduction: record it on the board with the diff.
