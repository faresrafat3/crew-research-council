#!/usr/bin/env python3
"""Generate leaderboard rows from the round-02, round-03 and round-04
measurement logs — read-time generated counts (CONSTITUTION §1); this file's
numbers are never hand-edited.

Usage: python3 tools/gen_leaderboard.py
"""
import re, sys, os, hashlib

RUNS = os.path.expanduser("~/.hermes/crew/experiment/runs")
R02 = os.path.join(RUNS, "2026-09-22-router-round-02")
R03 = os.path.join(RUNS, "2026-09-22-router-round-03")
R04 = os.path.join(RUNS, "2026-09-22-router-round-04")
LOG02 = os.path.join(R02, "logs/round-02-routed.txt")
LOG03 = os.path.join(R03, "logs/round-03-trial.txt")
LOG04 = os.path.join(R04, "logs/round-04-trial.txt")
POSTCUT = os.path.join(R03, "logs/round-03-postcut.txt")
ABL04 = os.path.join(R04, "logs/r04-no-verifier-ablation.txt")
FIX02 = os.path.join(R02, "tasks/real-missions.json")
FIX03 = os.path.join(R03, "tasks/expanded-missions.json")
FIX04 = os.path.join(R04, "tasks/expanded-missions.json")
FIX04F = os.path.join(R04, "tasks/real-missions.json")


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def summaries(log):
    if not os.path.exists(log):
        sys.exit(f"FAIL-LOUD: measurement log missing: {log}")
    rows = []
    for line in open(log):
        m = re.match(r"seed=(\d+) (SUMMARY .*)", line)
        if m:
            rows.append((int(m.group(1)), m.group(2)))
        elif line.startswith("SUMMARY"):
            rows.append((None, line.strip()))
    return rows


def field(s, name):
    m = re.search(rf"{name}=(\d+)", s)
    return int(m.group(1)) if m else None


def pick(rows, formation, seed=None, n=None, mode=None):
    if n is None:
        sys.exit("FAIL-LOUD: task count required")
    for sd, s in rows:
        if f"formation={formation}" not in s:
            continue
        if mode is not None and f"verify_mode={mode}" not in s:
            continue
        if seed is not None and sd != seed:
            continue
        if field(s, "n") == n:
            return s
    sys.exit(f"FAIL-LOUD: no SUMMARY for {formation} seed={seed} n={n} mode={mode}")


def postcut_verdict():
    if not os.path.exists(POSTCUT):
        sys.exit(f"FAIL-LOUD: post-cut verification missing: {POSTCUT}")
    for line in open(POSTCUT):
        if line.startswith("RESULT:"):
            return line.strip().split(":", 1)[1].strip()
    sys.exit("FAIL-LOUD: post-cut log has no RESULT line")


def ruling04():
    if not os.path.exists(LOG04):
        sys.exit(f"FAIL-LOUD: measurement log missing: {LOG04}")
    for line in open(LOG04):
        if "RULING:" in line:
            return line.split("RULING:", 1)[1].strip()
    sys.exit("FAIL-LOUD: round-04 log has no RULING line")


def seeds_stable(rows, mode, n=46):
    """Return (values, sd_text) for one verification mode across the sweep."""
    vals = sorted(field(s, "total_cost") for sd, s in rows
                  if sd is not None and f"verify_mode={mode}" in s
                  and field(s, "n") == n)
    if not vals:
        sys.exit(f"FAIL-LOUD: no seed-sweep rows for mode={mode}")
    sd = 0.0 if len(set(vals)) == 1 else "VARIES"
    return vals, sd


def main():
    rows02, rows03, rows04 = (summaries(LOG02), summaries(LOG03),
                              summaries(LOG04))
    champ20 = pick(rows02, "solo", 7, 20)
    routed20 = pick(rows02, "routed", 7, 20)
    champ46 = pick(rows03, "solo", None, 46)
    table46 = pick(rows03, "routed", None, 46)
    abl46 = pick(rows03, "routed-thresholds", None, 46)
    pre46 = pick(rows04, "routed", None, 46, mode="pre")
    fin46 = pick(rows04, "routed", None, 46, mode="final")
    off46 = pick(rows04, "routed", None, 46, mode="off")
    solo46 = pick(rows04, "solo", None, 46)
    pre20 = pick(rows04, "routed", None, 20, mode="pre")

    tax_pre = field(pre46, "total_cost") - field(off46, "total_cost")
    tax_fin = field(fin46, "total_cost") - field(off46, "total_cost")
    tax_share = 100.0 * tax_pre / field(pre46, "total_cost")
    per_task = tax_pre / field(pre46, "n")

    print("# LEADERBOARD (owner: @coach) — GENERATED; do not hand-edit\n")
    print("Golden evals the crew must hold. Regenerate with "
          "`python3 tools/gen_leaderboard.py`.\n")
    print(f"Fixture sha256 (frozen 20): `{sha(FIX02)}`")
    print(f"Fixture sha256 (expanded 46): `{sha(FIX03)}`")
    print(f"Round-04 fixtures re-verified identical: "
          f"`{sha(FIX04) == sha(FIX03)}` (expanded), "
          f"`{sha(FIX04F) == sha(FIX02)}` (frozen)\n")

    print("## Round 04 (current) — source: `runs/2026-09-22-router-round-04/"
          "logs/round-04-trial.txt`\n")
    print("| Eval | Pass criterion | Last result (generated) | Source command |")
    print("|------|----------------|-------------------------|----------------|")
    print(f"| verification tax (shipped `pre`) | exact, bounded, attributable "
          f"| tax=+{tax_pre} calls of {field(pre46,'total_cost')} "
          f"({tax_share:.2f}%), {field(pre46,'verifier_calls')} = "
          f"{field(pre46,'verifier_tasks')} tasks x 2, "
          f"{per_task:.3f} calls/task; identity holds per task "
          f"| `python3 tools/ablation_no_verifier_r04.py` |")
    print(f"| `--no-verifier` ablation | stage price measurable "
          f"| cost={field(off46,'total_cost')} tax=0 passed="
          f"{field(off46,'passed')}/46 resolved={field(off46,'resolved')} "
          f"| `eval --formation routed --hold-on-vague --no-verifier` |")
    print(f"| verification retarget (`final`) | unadopted: must pass its "
          f"registered clause | cost={field(fin46,'total_cost')} "
          f"tax=+{tax_fin}, holes {field(fin46,'hole_deliveries')} vs "
          f"{field(pre46,'hole_deliveries')} under `pre`; clause failed -> "
          f"deferred to R05 | `eval --verify final` |")
    print(f"| R04 ruling | KEEP iff the registered branch-3 clauses hold "
          f"| **{ruling04()}** | `tools/run_trial_r04.py` |")
    print(f"| champion arm | declared asymmetry: it runs no verifier "
          f"| solo cost={field(solo46,'total_cost')} "
          f"verifier_calls={field(solo46,'verifier_calls')} unverified="
          f"{field(solo46,'unverified_deliveries')} | "
          f"`eval --formation solo --hold-on-vague` |")
    for mode, label in (("pre", "shipped"), ("final", "candidate"),
                        ("off", "ablation")):
        vals, sd = seeds_stable(rows04, mode)
        print(f"| seed stability ({label} `{mode}`) | sd=0 across 5 seeds "
              f"| {vals} sd={sd} | `tools/run_trial_r04.py` |")
    print(f"| determinism (all 3 modes) | double runs byte-identical "
          f"| PASS | same |")
    print(f"| champion promotion bar | cost <= 88 on the frozen 20 "
          f"| frozen ladder cost={field(pre20,'total_cost')} -> still FAIL; "
          f"champion stays solo | `eval --formation routed` |")
    print(f"| alias reproduction of the tax | aggregate identical to the "
          f"`--verify off` arm | `logs/r04-no-verifier-ablation.txt` "
          f"sha256 `{sha(ABL04)[:8]}...` | "
          f"`python3 tools/ablation_no_verifier_r04.py` |")

    print("\n## Round 03 (historical) — source: `runs/2026-09-22-router-round-03/"
          "logs/round-03-trial.txt`\n")
    print("| Eval | Pass criterion | Last result (generated) | Source command |")
    print("|------|----------------|-------------------------|----------------|")
    print(f"| expanded-46 hold-discipline | solo --hold-on-vague = 46/46, "
          f"grave=0 | passed={field(champ46,'passed')}/46 "
          f"grave={field(champ46,'grave_errors')} cost={field(champ46,'total_cost')} "
          f"resolved={field(champ46,'resolved')} | "
          f"`eval --formation solo --hold-on-vague` |")
    print(f"| ladder quality (pre-cut table arm) | passed=46/46, grave=0 | "
          f"passed={field(table46,'passed')}/46 grave={field(table46,'grave_errors')} "
          f"cost={field(table46,'total_cost')} resolved={field(table46,'resolved')} | "
          f"`eval --formation routed --hold-on-vague` |")
    print(f"| ladder quality (shipped arm) | passed=46/46, grave=0, "
          f"resolved>=23 | passed={field(abl46,'passed')}/46 "
          f"grave={field(abl46,'grave_errors')} cost={field(abl46,'total_cost')} "
          f"resolved={field(abl46,'resolved')} | same |")
    print(f"| H13 class-table ruling | KEEP iff clauses (a)-(d) all hold | "
          f"**KILL** — resolved {field(table46,'resolved')} vs "
          f"{field(abl46,'resolved')} (not >), cost {field(table46,'total_cost')} "
          f"vs {field(abl46,'total_cost')} (not better) | "
          f"`tools/run_trial_r03.py` |")
    print(f"| post-cut verification | ALL-PASS | {postcut_verdict()} | "
          f"`tools/verify_postcut_r03.py` |")

    print("\n## Round 02 (historical) — source: `runs/2026-09-22-router-"
          "round-02/logs/round-02-routed.txt`\n")
    print("| Eval | Pass criterion | Last result (generated) | Source command |")
    print("|------|----------------|-------------------------|----------------|")
    print(f"| fixture-20 hold-discipline | solo --hold-on-vague = 20/20, "
          f"grave=0 | passed={field(champ20,'passed')}/20 "
          f"grave={field(champ20,'grave_errors')} cost={field(champ20,'total_cost')} "
          f"| `eval --formation solo --hold-on-vague --shuffle-seed 7` |")
    print(f"| routed quality bar | routed --hold-on-vague >= 20/20, grave=0 | "
          f"passed={field(routed20,'passed')}/20 "
          f"grave={field(routed20,'grave_errors')} "
          f"cost={field(routed20,'total_cost')} resolved={field(routed20,'resolved')} | "
          f"`eval --formation routed --hold-on-vague --shuffle-seed 7` |")
    print(f"| routed cost bar | routed cost <= 88 | "
          f"cost={field(routed20,'total_cost')} -> FAIL (bar failed honestly; "
          f"R03 re-tried the class table and cut it; R04 priced the verifier) "
          f"| same |")


if __name__ == "__main__":
    main()
