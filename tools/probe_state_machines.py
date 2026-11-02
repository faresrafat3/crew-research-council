#!/usr/bin/env python3
"""Reproduce the leaks named in `IMPLICIT-STATE-MACHINES.md`.

Read-only: imports the two tools, builds its own scratch trees, and never
touches the repository. Each row prints the state of one machine as it stands:

    REPRODUCED   the implicit transition still happens (the leak is live)
    FIXED        the tool now refuses the transition (the leak is closed)

So this script is the RED witness for the fix order in that document: run it
before a fix, watch the row flip to FIXED, then replace the row with a real
unit test under `tests/unit/`. Exit status is 0 whenever the probe run itself
completed; a closed leak is not a script failure.

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


def load(relative_path, name):
    spec = importlib.util.spec_from_file_location(
        name, os.path.join(ROOT, relative_path)
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def probe_fence_delimiter():
    """M1: a ``` line inside a ~~~ block closes the fence."""
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
        return (
            "a.md:5: heading case" in err.getvalue(),
            "line 5 sits inside a ~~~ block",
        )
    finally:
        shutil.rmtree(root)


def probe_heading_segment_start():
    """M4: the first word after an em dash is never case-checked."""
    gate = load("tools/check_docs.py", "probe_check_docs_heading")
    bad = gate.violations("A thing \u2014 Two Words")
    return bad == ["Words"], f"violations -> {bad}, 'Two' exempted"


def probe_substring_formation():
    """M6: formation=routed also matches formation=routed-thresholds."""
    tool = load("tools/gen_leaderboard.py", "probe_leaderboard_formation")
    thresholds = (
        "SUMMARY formation=routed-thresholds verify_mode=pre n=46 passed=46 "
        "grave_errors=0 total_cost=250 resolved=23 verifier_calls=8 "
        "verifier_tasks=4 hole_deliveries=0 unverified_deliveries=0"
    )
    routed = (
        "SUMMARY formation=routed verify_mode=pre n=46 passed=46 "
        "grave_errors=0 total_cost=260 resolved=22 verifier_calls=8 "
        "verifier_tasks=4 hole_deliveries=1 unverified_deliveries=0"
    )
    rows = [(None, thresholds), (None, routed)]
    cost = tool.field(tool.pick(rows, "routed", None, 46), "total_cost")
    return cost == 250, f"pick('routed') -> cost {cost} (260 is the routed arm)"


def probe_first_match_wins():
    """M6: in an append-only log the oldest row is the one reported."""
    tool = load("tools/gen_leaderboard.py", "probe_leaderboard_order")
    first = (
        "SUMMARY formation=routed verify_mode=pre n=46 passed=46 grave_errors=0 "
        "total_cost=300 resolved=23 verifier_calls=8 verifier_tasks=4 "
        "hole_deliveries=2 unverified_deliveries=0"
    )
    rerun = (
        "SUMMARY formation=routed verify_mode=pre n=46 passed=41 grave_errors=1 "
        "total_cost=999 resolved=3 verifier_calls=8 verifier_tasks=4 "
        "hole_deliveries=9 unverified_deliveries=0"
    )
    rows = [(None, first), (None, rerun)]
    cost = tool.field(tool.pick(rows, "routed", None, 46), "total_cost")
    return cost == 300, f"two rows, costs 300 then 999 -> reported {cost}"


def probe_indented_rows():
    """M6: a row that does not start at column 0 is invisible."""
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
        return parsed == 2, f"4 rows in the file -> {parsed} parsed"
    finally:
        shutil.rmtree(root)


def probe_missing_field():
    """M6: an absent measurement is interpolated as the string None."""
    tool = load("tools/gen_leaderboard.py", "probe_leaderboard_field")
    row = (
        "SUMMARY formation=routed verify_mode=final n=46 passed=46 grave_errors=0 "
        "total_cost=310 resolved=23 verifier_calls=8 verifier_tasks=4 "
        "unverified_deliveries=0"
    )
    rendered = f"holes {tool.field(row, 'hole_deliveries')} vs 2"
    return rendered == "holes None vs 2", f"renders as '{rendered}'"


def probe_cache_staleness():
    """M5: the digest cache has no transition back to unseen."""
    tool = load("tools/gen_leaderboard.py", "probe_leaderboard_cache")
    root = tempfile.mkdtemp()
    try:
        path = os.path.join(root, "fixture.json")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write('{"tasks": ["t1"]}\n')
        before = tool.sha(path)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write('{"tasks": ["t2"]}\n')
        after = tool.sha(path)
        return before == after, "digest unchanged after the file changed on disk"
    finally:
        shutil.rmtree(root)


def probe_exit_code():
    """M7: no matching row is an exception carrying a message, not a state."""
    tool = load("tools/gen_leaderboard.py", "probe_leaderboard_exit")
    try:
        tool.pick([], "routed", None, 46)
    except SystemExit as failure:
        return isinstance(failure.code, str), (
            f"SystemExit code is {type(failure.code).__name__}: {failure.code}"
        )
    return False, "pick returned instead of exiting"


PROBES = (
    ("M1 fence delimiter identity", probe_fence_delimiter),
    ("M4 heading segment exemption", probe_heading_segment_start),
    ("M6 substring formation identity", probe_substring_formation),
    ("M6 first match wins", probe_first_match_wins),
    ("M6 column-0 row recognition", probe_indented_rows),
    ("M6 absent field renders None", probe_missing_field),
    ("M5 digest cache never clears", probe_cache_staleness),
    ("M7 fail-loud as control flow", probe_exit_code),
)


def main(argv):
    verbose = "--verbose" in argv[1:]
    width = max(len(name) for name, _ in PROBES)
    live = 0
    print(f"{'machine'.ljust(width)}  state")
    print(f"{'-' * width}  -----")
    for name, probe in PROBES:
        reproduced, detail = probe()
        live += 1 if reproduced else 0
        print(f"{name.ljust(width)}  {'REPRODUCED' if reproduced else 'FIXED'}")
        if verbose or not reproduced:
            print(f"{''.ljust(width)}  {detail}")
    print(
        f"\n{live} of {len(PROBES)} implicit transitions still fire; "
        f"{len(PROBES) - live} closed."
    )
    print("See IMPLICIT-STATE-MACHINES.md for the state set behind each row.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
