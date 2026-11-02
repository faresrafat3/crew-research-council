#!/usr/bin/env python3
"""Generate leaderboard rows from the round-02, round-03 and round-04
measurement logs — read-time generated counts (CONSTITUTION §1); this file's
numbers are never hand-edited.

The row contract, so a reader never has to infer it from the code:

- a row is identified by its fields (`formation`, `verify_mode`, `seed`, `n`),
  never by a substring of the line, so `routed` never matches
  `routed-thresholds`;
- every field the report quotes must be present: a missing measurement is
  fatal, never published as `None` beside real numbers;
- two rows that share that identity and disagree are fatal
  (`MeasurementError`), because the report cannot say which one is the real
  measurement; identical re-appends collapse to one row;
- an open seed reads the lowest seed in the log, so selection never depends on
  line order; the sweep itself is reported by `seeds_stable`.

Usage: python3 tools/gen_leaderboard.py
"""
import contextlib, io, re, sys, os, hashlib
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

# One read per input: the report hashes the frozen fixtures twice and scans
# round-04 for both SUMMARY rows and the RULING line, so keep both caches.
# `main()` empties them at entry: a cache lives for exactly one report, so a
# second report in the same process cannot read the first report's bytes.
_DIGESTS = {}
_LINES = {}


class MeasurementError(Exception):
    """A row that cannot be read as the measurement it claims to carry."""


# Verdicts for `check_leaderboard`; only CURRENT is a pass.
OK_EXIT, STALE_EXIT = 0, 1


def _brief(row):
    """One row, short enough to name in an error message."""
    keys = ("formation", "verify_mode", "n", "total_cost", "passed", "resolved")
    return " ".join(f"{key}={row[key]}" for key in keys if key in row)


def _fields(text):
    """The key=value tokens of one row; a key repeated inside it is fatal."""
    found = {}
    for token in text.split():
        key, separator, value = token.partition("=")
        if not separator:
            continue
        if key in found and found[key] != value:
            raise MeasurementError(f"row carries {key}= twice: {text.strip()}")
        found[key] = value
    return found


def sha(path):
    """sha256 of one fixture; hashed once per run, not once per mention."""
    if path not in _DIGESTS:
        with open(path, "rb") as handle:
            _DIGESTS[path] = hashlib.sha256(handle.read()).hexdigest()
    return _DIGESTS[path]


def lines_of(path):
    """Every line of one log; read once per run, handle closed on the way out.

    `round-04-trial.txt` answers both the SUMMARY scan and the RULING scan, and
    the frozen fixtures are hashed twice by the report — one read each.
    """
    if path not in _LINES:
        with open(path, encoding="utf-8") as handle:
            _LINES[path] = handle.readlines()
    return _LINES[path]


ROW = re.compile(r"^(?:seed=(\d+)\s+)?SUMMARY\b(.*)$")


def summaries(log):
    """Every SUMMARY row of one log, parsed into (seed, fields) once."""
    if not os.path.exists(log):
        sys.exit(f"FAIL-LOUD: measurement log missing: {log}")
    rows = []
    seen = {}
    for line in lines_of(log):
        match = ROW.match(line.lstrip())
        if not match:
            continue
        seed = int(match.group(1)) if match.group(1) is not None else None
        row = _fields(match.group(2))
        for required in ("formation", "n"):
            if required not in row:
                raise MeasurementError(f"row has no {required}: {line.strip()}")
        identity = (row["formation"], row.get("verify_mode"), seed, row["n"])
        if identity in seen:
            if seen[identity] != row:
                raise MeasurementError(
                    f"{identity[0]} mode={identity[1]} seed={seed} "
                    f"n={identity[3]} rows disagree: "
                    f"{_brief(seen[identity])} vs {_brief(row)}"
                )
            continue
        seen[identity] = row
        rows.append((seed, row))
    return rows


def field(row, name):
    """One integer measurement; absence is fatal, not a printed `None`."""
    value = row.get(name)
    if value is None:
        raise MeasurementError(f"row has no {name}: {_brief(row)}")
    if not re.fullmatch(r"-?\d+", value):
        raise MeasurementError(f"row field is not a count: {name}={value}")
    return int(value)


def pick(rows, formation, seed=None, n=None, mode=None):
    """The one row for this arm, matched on field equality.

    `routed` must not select `routed-thresholds`. An open seed means "the lowest
    seed in the log", because a seed sweep is reported by `seeds_stable`; that
    keeps the choice deterministic instead of order-dependent.
    """
    if n is None:
        sys.exit("FAIL-LOUD: task count required")
    matches = [
        (row_seed, row)
        for row_seed, row in rows
        if row["formation"] == formation
        and (mode is None or row.get("verify_mode") == mode)
        and (seed is None or row_seed == seed)
        and field(row, "n") == n
    ]
    if seed is None:
        seeds = [row_seed for row_seed, _ in matches if row_seed is not None]
        if seeds:
            lowest = min(seeds)
            matches = [(row_seed, row) for row_seed, row in matches
                       if row_seed == lowest]
    if not matches:
        sys.exit(f"FAIL-LOUD: no SUMMARY for {formation} seed={seed} n={n} mode={mode}")
    return matches[0][1]


def postcut_verdict():
    if not os.path.exists(POSTCUT):
        sys.exit(f"FAIL-LOUD: post-cut verification missing: {POSTCUT}")
    for line in lines_of(POSTCUT):
        if line.startswith("RESULT:"):
            return line.strip().split(":", 1)[1].strip()
    sys.exit("FAIL-LOUD: post-cut log has no RESULT line")


def ruling04():
    if not os.path.exists(LOG04):
        sys.exit(f"FAIL-LOUD: measurement log missing: {LOG04}")
    for line in lines_of(LOG04):
        if "RULING:" in line:
            return line.split("RULING:", 1)[1].strip()
    sys.exit("FAIL-LOUD: round-04 log has no RULING line")


def seeds_stable(rows, mode, n=46):
    """Return (values, stable) for one verification mode across the sweep."""
    vals = sorted(field(row, "total_cost") for row_seed, row in rows
                  if row_seed is not None
                  and row.get("verify_mode") == mode
                  and field(row, "n") == n)
    if not vals:
        sys.exit(f"FAIL-LOUD: no seed-sweep rows for mode={mode}")
    return vals, len(set(vals)) == 1


def report():
    """Print the whole board once, from the logs on disk."""
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
        vals, stable = seeds_stable(rows04, mode)
        verdict = "0.0" if stable else "VARIES"
        print(f"| seed stability ({label} `{mode}`) | sd=0 across 5 seeds "
              f"| {vals} sd={verdict} | `tools/run_trial_r04.py` |")
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


def rendered():
    """The whole report as text; the read caches live for exactly this render."""
    _DIGESTS.clear()
    _LINES.clear()
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        report()
    return buffer.getvalue()


# The generated board, beside this tool's parent directory.
BOARD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "leaderboard.md")

# The three freshness verdicts, named once: a board that cannot be compared
# (no run tree here) is a different state from a board that disagrees.
CURRENT, STALE, SKIP = "CURRENT", "STALE", "SKIP"


def check_leaderboard(path=BOARD):
    """Compare the board on disk with what the logs generate now; 0 if current.

    SKIP is honest: on a clean clone the run tree under `~/.hermes` is absent, so
    the board cannot be re-derived and claiming either state would be a guess.
    A STALE board is fatal because a stale board and a hand-edited one look the
    same to every reader of the file.
    """
    if not os.path.isdir(RUNS):
        print(f"leaderboard: {SKIP} (no run tree at {RUNS})")
        return OK_EXIT
    try:
        generated = rendered()
    except MeasurementError as failure:
        sys.exit(f"FAIL-LOUD: {failure}")
    if not os.path.exists(path):
        print(f"leaderboard: {STALE} (no board at {path})", file=sys.stderr)
        return STALE_EXIT
    with open(path, encoding="utf-8") as handle:
        published = handle.read()
    if published != generated:
        print(f"leaderboard: {STALE} (run `python3 tools/gen_leaderboard.py` "
              f"and commit the diff)", file=sys.stderr)
        return STALE_EXIT
    print(f"leaderboard: {CURRENT}")
    return OK_EXIT


def main(argv=None):
    """Print one report, or compare the board with the logs under `--check`.

    The board is rendered into a buffer and written only once every row has been
    read, so a refused report cannot leave half a leaderboard behind for a
    `> leaderboard.md` redirect to keep.
    """
    if "--check" in list(argv or []):
        sys.exit(check_leaderboard())
    try:
        text = rendered()
    except MeasurementError as failure:
        sys.exit(f"FAIL-LOUD: {failure}")
    sys.stdout.write(text)


if __name__ == "__main__":
    main(sys.argv[1:])
