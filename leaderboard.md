# LEADERBOARD (owner: @coach) — GENERATED; do not hand-edit

Golden evals the crew must hold. Regenerate with `python3 tools/gen_leaderboard.py`.

Fixture sha256 (frozen 20): `28406677825eeeb5489e7ea6fc60ee7a992e55ea0629f8348436052cfba59a87`
Fixture sha256 (expanded 46): `26b3b832a2233693875b5b12e1093b4d55d0c019421f63bfbbebab3c417898c0`
Round-04 fixtures re-verified identical: `True` (expanded), `True` (frozen)

## Round 04 (current) — source: `runs/2026-09-22-router-round-04/logs/round-04-trial.txt`

| Eval | Pass criterion | Last result (generated) | Source command |
|------|----------------|-------------------------|----------------|
| verification tax (shipped `pre`) | exact, bounded, attributable | tax=+14 calls of 292 (4.79%), 14 = 7 tasks x 2, 0.304 calls/task; identity holds per task | `python3 tools/ablation_no_verifier_r04.py` |
| `--no-verifier` ablation | stage price measurable | cost=278 tax=0 passed=46/46 resolved=23 | `eval --formation routed --hold-on-vague --no-verifier` |
| verification retarget (`final`) | unadopted: must pass its registered clause | cost=288 tax=+10, holes 0 vs 1 under `pre`; clause failed -> deferred to R05 | `eval --verify final` |
| R04 ruling | KEEP iff the registered branch-3 clauses hold | **KEEP pre (registered fallback: the retarget failed its clause)** | `tools/run_trial_r04.py` |
| champion arm | declared asymmetry: it runs no verifier | solo cost=159 verifier_calls=0 unverified=12 | `eval --formation solo --hold-on-vague` |
| seed stability (shipped `pre`) | sd=0 across 5 seeds | [292, 292, 292, 292, 292] sd=0.0 | `tools/run_trial_r04.py` |
| seed stability (candidate `final`) | sd=0 across 5 seeds | [288, 288, 288, 288, 288] sd=0.0 | `tools/run_trial_r04.py` |
| seed stability (ablation `off`) | sd=0 across 5 seeds | [278, 278, 278, 278, 278] sd=0.0 | `tools/run_trial_r04.py` |
| determinism (all 3 modes) | double runs byte-identical | PASS | same |
| champion promotion bar | cost <= 88 on the frozen 20 | frozen ladder cost=122 -> still FAIL; champion stays solo | `eval --formation routed` |
| alias reproduction of the tax | aggregate identical to the `--verify off` arm | `logs/r04-no-verifier-ablation.txt` sha256 `b6d07e83...` | `python3 tools/ablation_no_verifier_r04.py` |

## Round 03 (historical) — source: `runs/2026-09-22-router-round-03/logs/round-03-trial.txt`

| Eval | Pass criterion | Last result (generated) | Source command |
|------|----------------|-------------------------|----------------|
| expanded-46 hold-discipline | solo --hold-on-vague = 46/46, grave=0 | passed=46/46 grave=0 cost=159 resolved=12 | `eval --formation solo --hold-on-vague` |
| ladder quality (pre-cut table arm) | passed=46/46, grave=0 | passed=46/46 grave=0 cost=307 resolved=23 | `eval --formation routed --hold-on-vague` |
| ladder quality (shipped arm) | passed=46/46, grave=0, resolved>=23 | passed=46/46 grave=0 cost=292 resolved=23 | same |
| H13 class-table ruling | KEEP iff clauses (a)-(d) all hold | **KILL** — resolved 23 vs 23 (not >), cost 307 vs 292 (not better) | `tools/run_trial_r03.py` |
| post-cut verification | ALL-PASS | ALL-PASS | `tools/verify_postcut_r03.py` |

## Round 02 (historical) — source: `runs/2026-09-22-router-round-02/logs/round-02-routed.txt`

| Eval | Pass criterion | Last result (generated) | Source command |
|------|----------------|-------------------------|----------------|
| fixture-20 hold-discipline | solo --hold-on-vague = 20/20, grave=0 | passed=20/20 grave=0 cost=68 | `eval --formation solo --hold-on-vague --shuffle-seed 7` |
| routed quality bar | routed --hold-on-vague >= 20/20, grave=0 | passed=20/20 grave=0 cost=127 resolved=9 | `eval --formation routed --hold-on-vague --shuffle-seed 7` |
| routed cost bar | routed cost <= 88 | cost=127 -> FAIL (bar failed honestly; R03 re-tried the class table and cut it; R04 priced the verifier) | same |
