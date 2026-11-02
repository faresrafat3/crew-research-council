#!/usr/bin/env python3
"""Check each implicit transition named in `IMPLICIT-STATE-MACHINES.md`.

Read-only: imports the two tools, builds its own scratch trees, and never
touches the repository. Every row carries the state it is expected to be in:

    CLOSED       the tool refuses the transition (closed on 2026-11-02)
    OPEN         the transition is kept on purpose and pinned by a unit test

A row whose observed state differs from its expected state is a REGRESSION and
the script exits 1, so it can run beside the gate. `--verbose` prints the
detail line for every row, not only for the failing ones.

Usage: python3 tools/probe_state_machines.py [--verbose]
"""

import contextlib
import importlib.util
import io
import os
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NL = "\n"

CLOSED = "CLOSED"
OPEN = "OPEN"


def load(relative_path, name):
    spec = importlib.util.spec_from_file_location(
        name, os.path.join(ROOT, relative_path)
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def probe_fence_delimiter():
    """M1: a backtick fence inside a tilde block must stay content."""
    gate = load("tools/check_docs.py", "probe_check_docs_fence")
    root = tempfile.mkdtemp()
    try:
        with open(os.path.join(root, "a.md"), "w", encoding="utf-8") as handle:
            handle.write(
                "# Fine\n"
                "\n"
                "~~~text\n"
                "```python\n"
                "# Not A Heading\n"
                "```\n"
                "~~~\n"
                "\n"
                "# Bad Heading Here\n"
            )
        err = io.StringIO()
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
            gate.main(["probe", root])
        inside = "a.md:5: heading case" in err.getvalue()
        after = "a.md:9: heading case" in err.getvalue()
        return not inside and after, f"line 5 graded={inside}, line 9 graded={after}"
    finally:
        shutil.rmtree(root)


def probe_heading_segment():
    """M4: each em-dash segment is its own phrase (declared, not removed)."""
    gate = load("tools/check_docs.py", "probe_check_docs_heading")
    bad = gate.violations("A thing \u2014 Two Words")
    return bad != ["Words"], f"segment-start exemption still passes -> {bad}"


def probe_formation_identity():
    """M6: formation=routed must not answer for formation=routed-thresholds."""
    tool = load("tools/gen_leaderboard.py", "probe_leaderboard_formation")
    thresholds = tool._fields(
        "SUMMARY formation=routed-thresholds verify_mode=pre n=46 passed=46 "
        "grave_errors=0 total_cost=250 resolved=23 verifier_calls=8 "
        "verifier_tasks=4 hole_deliveries=0 unverified_deliveries=0"
    )
    routed = tool._fields(
        "SUMMARY formation=routed verify_mode=pre n=46 passed=46 grave_errors=0 "
        "total_cost=260 resolved=22 verifier_calls=8 verifier_tasks=4 "
        "hole_deliveries=1 unverified_deliveries=0"
    )
    rows = [(None, thresholds), (None, routed)]
    cost = tool.field(tool.pick(rows, "routed", None, 46), "total_cost")
    return cost == 260, f"pick('routed') -> cost {cost}"


def probe_duplicate_rows():
    """M6: two rows for one key that disagree must be refused, not ordered."""
    tool = load("tools/gen_leaderboard.py", "probe_leaderboard_duplicate")
    root = tempfile.mkdtemp()
    try:
        path = os.path.join(root, "log.txt")
        first = (
            "SUMMARY formation=routed verify_mode=pre n=46 passed=46 "
            "grave_errors=0 total_cost=300 resolved=23 verifier_calls=8 "
            "verifier_tasks=4 hole_deliveries=2 unverified_deliveries=0"
        )
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(first + NL + first.replace("total_cost=300", "total_cost=999")
                         + NL)
        try:
            rows = tool.summaries(path)
        except tool.MeasurementError as failure:
            return True, f"refused: {failure}"
        cost = tool.field(tool.pick(rows, "routed", None, 46), "total_cost")
        return False, f"kept one row silently: cost {cost}"
    finally:
        shutil.rmtree(root)


def probe_indented_rows():
    """M6: indentation must not decide whether a row exists."""
    tool = load("tools/gen_leaderboard.py", "probe_leaderboard_indent")
    root = tempfile.mkdtemp()
    try:
        path = os.path.join(root, "log.txt")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(NL.join([
                "SUMMARY formation=a n=46 total_cost=1",
                "  SUMMARY formation=b n=46 total_cost=2",
                "seed=3 SUMMARY formation=c n=46 total_cost=3",
                "  seed=4 SUMMARY formation=d n=46 total_cost=4",
            ]) + NL)
        parsed = len(tool.summaries(path))
        return parsed == 4, f"4 rows in the file -> {parsed} parsed"
    finally:
        shutil.rmtree(root)


def probe_missing_field():
    """M6: a missing measurement must be fatal, not the string None."""
    tool = load("tools/gen_leaderboard.py", "probe_leaderboard_field")
    row = tool._fields(
        "SUMMARY formation=routed verify_mode=final n=46 passed=46 "
        "grave_errors=0 total_cost=310 resolved=23 verifier_calls=8 "
        "verifier_tasks=4 unverified_deliveries=0"
    )
    try:
        value = tool.field(row, "hole_deliveries")
    except tool.MeasurementError as failure:
        return True, f"refused: {failure}"
    return False, f"rendered as holes {value} vs 2"


def _row(seed, formation, mode, n, cost, holes, verifiers, resolved=23):
    head = f"seed={seed} SUMMARY" if seed is not None else "SUMMARY"
    return (f"{head} formation={formation} verify_mode={mode} n={n} passed={n} "
            f"grave_errors=0 total_cost={cost} resolved={resolved} "
            f"verifier_calls={verifiers} verifier_tasks={verifiers // 2} "
            f"hole_deliveries={holes} unverified_deliveries="
            f"{0 if verifiers else n}")


def probe_cache_lifetime():
    """M5: a second report in one process must read the log again."""
    tool = load("tools/gen_leaderboard.py", "probe_leaderboard_cache")
    root = tempfile.mkdtemp()
    try:
        rounds = {}
        for number in (2, 3, 4):
            path = os.path.join(root, f"2026-09-22-router-round-0{number}")
            os.makedirs(os.path.join(path, "logs"))
            os.makedirs(os.path.join(path, "tasks"))
            rounds[number] = path
        r02, r03, r04 = rounds[2], rounds[3], rounds[4]
        files = {
            os.path.join(r02, "logs/round-02-routed.txt"): NL.join([
                _row(7, "solo", "off", 20, 100, 0, 0, 10),
                _row(7, "routed", "pre", 20, 120, 0, 4, 11)]),
            os.path.join(r03, "logs/round-03-trial.txt"): NL.join([
                _row(None, "solo", "off", 46, 200, 0, 0),
                _row(None, "routed", "pre", 46, 260, 1, 8),
                _row(None, "routed-thresholds", "pre", 46, 250, 0, 8)]),
            os.path.join(r03, "logs/round-03-postcut.txt"): "RESULT: ALL-PASS",
            os.path.join(r04, "logs/round-04-trial.txt"): NL.join(
                [_row(seed, "routed", "pre", 46, 300, 2, 8) for seed in range(1, 6)]
                + [_row(seed, "routed", "final", 46, 310, 3, 8)
                   for seed in range(1, 6)]
                + [_row(seed, "routed", "off", 46, 280, 0, 0)
                   for seed in range(1, 6)]
                + [_row(9, "solo", "solo", 46, 159, 0, 0, 12),
                   _row(7, "routed", "pre", 20, 122, 0, 4, 9),
                   "RULING: KEEP"]),
            os.path.join(r04, "logs/r04-no-verifier-ablation.txt"): "ablation",
            os.path.join(r02, "tasks/real-missions.json"): '{"tasks": []}',
            os.path.join(r03, "tasks/expanded-missions.json"): '{"tasks": []}',
            os.path.join(r04, "tasks/expanded-missions.json"): '{"tasks": []}',
            os.path.join(r04, "tasks/real-missions.json"): '{"tasks": []}',
        }
        for path, body in files.items():
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(body + NL)

        tool.RUNS = root
        tool.R02, tool.R03, tool.R04 = r02, r03, r04
        tool.LOG02 = os.path.join(r02, "logs/round-02-routed.txt")
        tool.LOG03 = os.path.join(r03, "logs/round-03-trial.txt")
        tool.LOG04 = os.path.join(r04, "logs/round-04-trial.txt")
        tool.POSTCUT = os.path.join(r03, "logs/round-03-postcut.txt")
        tool.ABL04 = os.path.join(r04, "logs/r04-no-verifier-ablation.txt")
        tool.FIX02 = os.path.join(r02, "tasks/real-missions.json")
        tool.FIX03 = os.path.join(r03, "tasks/expanded-missions.json")
        tool.FIX04 = os.path.join(r04, "tasks/expanded-missions.json")
        tool.FIX04F = os.path.join(r04, "tasks/real-missions.json")

        def report():
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                tool.main()
            return out.getvalue()

        first = report()
        with open(tool.LOG04, "w", encoding="utf-8") as handle:
            handle.write(NL.join(
                [_row(seed, "routed", "pre", 46, 999, 2, 8) for seed in range(1, 6)]
            ) + NL + NL.join(
                [_row(seed, "routed", "final", 46, 310, 3, 8)
                 for seed in range(1, 6)]
                + [_row(seed, "routed", "off", 46, 280, 0, 0)
                   for seed in range(1, 6)]
                + [_row(9, "solo", "solo", 46, 159, 0, 0, 12),
                   _row(7, "routed", "pre", 20, 122, 0, 4, 9),
                   "RULING: KEEP"]) + NL)
        second = report()
        return first != second and "999" in second, (
            "second report identical to the first" if first == second
            else "second report re-read the log"
        )
    finally:
        shutil.rmtree(root)


def probe_named_error():
    """M7: contradictory measurements raise a nameable error, not a silent row."""
    tool = load("tools/gen_leaderboard.py", "probe_leaderboard_error")
    first = tool._fields(
        "SUMMARY formation=routed verify_mode=pre n=46 total_cost=300")
    second = tool._fields(
        "SUMMARY formation=routed verify_mode=pre n=46 total_cost=999")
    try:
        tool.pick([(None, first), (None, second)], "routed", None, 46)
    except tool.MeasurementError as failure:
        return True, f"MeasurementError: {failure}"
    return False, "pick returned one of two contradictory rows"


PROBES = (
    ("M1 fence delimiter identity", probe_fence_delimiter, CLOSED),
    ("M4 heading segment exemption", probe_heading_segment, OPEN),
    ("M5 cache lifetime", probe_cache_lifetime, CLOSED),
    ("M6 formation identity", probe_formation_identity, CLOSED),
    ("M6 duplicate rows disagree", probe_duplicate_rows, CLOSED),
    ("M6 column-0 row recognition", probe_indented_rows, CLOSED),
    ("M6 absent field", probe_missing_field, CLOSED),
    ("M7 contradiction has a name", probe_named_error, CLOSED),
)


def main(argv):
    verbose = "--verbose" in argv[1:]
    width = max(len(name) for name, _, _ in PROBES)
    regressions = 0
    print(f"{'machine'.ljust(width)}  {'observed':9}  expected  verdict")
    print(f"{'-' * width}  {'--------':9}  --------  -------")
    for name, probe, expected in PROBES:
        closed, detail = probe()
        observed = CLOSED if closed else OPEN
        verdict = "ok" if observed == expected else "REGRESSION"
        regressions += 0 if observed == expected else 1
        print(f"{name.ljust(width)}  {observed:9}  {expected:8}  {verdict}")
        if verbose or observed != expected:
            print(f"{''.ljust(width)}  {detail}")
    print(f"\n{len(PROBES)} probes, {regressions} regression(s).")
    if regressions:
        print("See IMPLICIT-STATE-MACHINES.md: a closed transition reopened.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
