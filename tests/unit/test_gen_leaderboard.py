#!/usr/bin/env python3
"""Witness tests for `tools/gen_leaderboard.py`.

The tool's real inputs live under `~/.hermes/...` (machine-local, absent on a
clean clone), so these tests build a synthetic run tree, point the module's
path constants at it, and run `main()` for real. That keeps the generator
verifiable offline and pins its read cost: every log and fixture is opened once
per report.

Run: python3 -m unittest discover -s tests/unit -v
"""

import builtins
import contextlib
import importlib.util
import io
import os
import shutil
import tempfile
import textwrap
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOOL = os.path.join(ROOT, "tools", "gen_leaderboard.py")

REAL_OPEN = builtins.open


def load_tool():
    """Import tools/gen_leaderboard.py as a module without running main()."""
    spec = importlib.util.spec_from_file_location("gen_leaderboard", TOOL)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReadCounter:
    """Stand-in for builtins.open that records every path it is asked for."""

    def __init__(self):
        self.paths = []

    def __call__(self, file, *args, **kwargs):
        self.paths.append(os.path.abspath(os.fspath(file)))
        return REAL_OPEN(file, *args, **kwargs)

    def count(self, path):
        return self.paths.count(os.path.abspath(path))


LOG02 = """\
seed=7 SUMMARY formation=solo verify_mode=off n=20 passed=20 grave_errors=0 \
total_cost=100 resolved=10 verifier_calls=0 verifier_tasks=0 hole_deliveries=0 \
unverified_deliveries=20
seed=7 SUMMARY formation=routed verify_mode=pre n=20 passed=20 grave_errors=0 \
total_cost=120 resolved=11 verifier_calls=4 verifier_tasks=2 hole_deliveries=0 \
unverified_deliveries=0
"""

LOG03 = """\
SUMMARY formation=solo verify_mode=off n=46 passed=46 grave_errors=0 \
total_cost=200 resolved=23 verifier_calls=0 verifier_tasks=0 hole_deliveries=0 \
unverified_deliveries=46
SUMMARY formation=routed verify_mode=pre n=46 passed=46 grave_errors=0 \
total_cost=260 resolved=22 verifier_calls=8 verifier_tasks=4 hole_deliveries=1 \
unverified_deliveries=0
SUMMARY formation=routed-thresholds verify_mode=pre n=46 passed=46 grave_errors=0 \
total_cost=250 resolved=23 verifier_calls=8 verifier_tasks=4 hole_deliveries=0 \
unverified_deliveries=0
"""


def round04_row(seed, formation, mode, n, cost, holes, verifiers, resolved):
    return (
        f"seed={seed} SUMMARY formation={formation} verify_mode={mode} n={n} "
        f"passed={n} grave_errors=0 total_cost={cost} resolved={resolved} "
        f"verifier_calls={verifiers} verifier_tasks={verifiers // 2} "
        f"hole_deliveries={holes} unverified_deliveries={0 if verifiers else n}"
    )


LOG04 = "\n".join(
    [round04_row(seed, "routed", "pre", 46, 300, 2, 8, 23) for seed in range(1, 6)]
    + [round04_row(seed, "routed", "final", 46, 310, 3, 8, 23) for seed in range(1, 6)]
    + [round04_row(seed, "routed", "off", 46, 280, 0, 0, 23) for seed in range(1, 6)]
    + [round04_row(9, "solo", "solo", 46, 159, 0, 0, 12)]
    + [round04_row(7, "routed", "pre", 20, 122, 0, 4, 9), "RULING: KEEP-BRANCH-3"]
) + "\n"



class LeaderboardFixture(unittest.TestCase):
    """Shared synthetic run tree, laid out exactly like ~/.hermes/crew."""

    def setUp(self):
        self.runs = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.runs)
        dirs = {
            "r02": os.path.join(self.runs, "2026-09-22-router-round-02"),
            "r03": os.path.join(self.runs, "2026-09-22-router-round-03"),
            "r04": os.path.join(self.runs, "2026-09-22-router-round-04"),
        }
        for path in dirs.values():
            for leaf in ("logs", "tasks"):
                os.makedirs(os.path.join(path, leaf))

        frozen = '{"tasks": ["t1", "t2"]}\n'
        expanded = '{"tasks": ["t1", "t2", "t3"]}\n'
        files = {
            os.path.join(dirs["r02"], "logs/round-02-routed.txt"): LOG02,
            os.path.join(dirs["r03"], "logs/round-03-trial.txt"): LOG03,
            os.path.join(dirs["r04"], "logs/round-04-trial.txt"): LOG04,
            os.path.join(dirs["r03"], "logs/round-03-postcut.txt"): "RESULT: ALL-PASS\n",
            os.path.join(dirs["r04"], "logs/r04-no-verifier-ablation.txt"): "ablation\n",
            os.path.join(dirs["r02"], "tasks/real-missions.json"): frozen,
            os.path.join(dirs["r03"], "tasks/expanded-missions.json"): expanded,
            os.path.join(dirs["r04"], "tasks/expanded-missions.json"): expanded,
            os.path.join(dirs["r04"], "tasks/real-missions.json"): frozen,
        }
        for path, body in files.items():
            with REAL_OPEN(path, "w", encoding="utf-8") as fh:
                fh.write(textwrap.dedent(body))
        self.files = sorted(files)

        self.tool = load_tool()
        r02, r03, r04 = dirs["r02"], dirs["r03"], dirs["r04"]
        self.tool.RUNS = self.runs
        self.tool.R02, self.tool.R03, self.tool.R04 = r02, r03, r04
        self.tool.LOG02 = os.path.join(r02, "logs/round-02-routed.txt")
        self.tool.LOG03 = os.path.join(r03, "logs/round-03-trial.txt")
        self.tool.LOG04 = os.path.join(r04, "logs/round-04-trial.txt")
        self.tool.POSTCUT = os.path.join(r03, "logs/round-03-postcut.txt")
        self.tool.ABL04 = os.path.join(r04, "logs/r04-no-verifier-ablation.txt")
        self.tool.FIX02 = os.path.join(r02, "tasks/real-missions.json")
        self.tool.FIX03 = os.path.join(r03, "tasks/expanded-missions.json")
        self.tool.FIX04 = os.path.join(r04, "tasks/expanded-missions.json")
        self.tool.FIX04F = os.path.join(r04, "tasks/real-missions.json")

    def run_tool(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.tool.main()
        return out.getvalue()

    def run_tool_counting(self):
        counter = ReadCounter()
        out = io.StringIO()
        builtins.open = counter
        try:
            with contextlib.redirect_stdout(out):
                self.tool.main()
        finally:
            builtins.open = REAL_OPEN
        return out.getvalue(), counter


class LeaderboardOutput(LeaderboardFixture):
    """The report generates from the logs, and its numbers come from them."""

    def test_report_renders_every_round(self):
        out = self.run_tool()
        self.assertIn("# LEADERBOARD (owner: @coach) — GENERATED; do not hand-edit", out)
        self.assertIn("## Round 04 (current)", out)
        self.assertIn("## Round 03 (historical)", out)
        self.assertIn("## Round 02 (historical)", out)

    def test_numbers_are_read_from_the_logs(self):
        out = self.run_tool()
        # pre 300, off 280 -> tax 20, 8 verifier calls over 4 tasks.
        self.assertIn("tax=+20 calls of 300", out)
        self.assertIn("(6.67%)", out)
        self.assertIn("8 = 4 tasks x 2", out)
        self.assertIn("0.435 calls/task", out)
        self.assertIn("**KEEP-BRANCH-3**", out)
        self.assertIn("ALL-PASS", out)
        self.assertIn("passed=46/46 grave=0 cost=200 resolved=23", out)
        self.assertIn("passed=20/20 grave=0 cost=100", out)
        # FIX04 must be byte-identical to FIX03, FIX04F to FIX02.
        self.assertIn("`True` (expanded), `True` (frozen)", out)

    def test_seed_stability_sweep_reads_all_three_modes(self):
        out = self.run_tool()
        self.assertEqual(out.count("sd=0 across 5 seeds"), 3)
        for arm in ("[280, 280, 280, 280, 280] sd=0.0",
                    "[300, 300, 300, 300, 300] sd=0.0",
                    "[310, 310, 310, 310, 310] sd=0.0"):
            self.assertIn(arm, out)


class LeaderboardReadCost(LeaderboardFixture):
    """One pass per input: the same log or fixture is never hashed twice."""

    def test_every_input_is_opened_exactly_once(self):
        out, counter = self.run_tool_counting()
        self.assertIn("## Round 04 (current)", out)
        counts = {path: counter.count(path) for path in self.files}
        repeated = {path: n for path, n in counts.items() if n > 1}
        self.assertEqual(repeated, {}, msg=f"inputs re-read in one report: {repeated}")

    def test_sha_is_stable_for_the_same_input(self):
        first = self.tool.sha(self.tool.FIX03)
        second = self.tool.sha(self.tool.FIX03)
        self.assertEqual(first, second)
        self.assertEqual(len(first), 64)


class LeaderboardSelection(unittest.TestCase):
    """Row identity: field equality, no substring, no silent first match."""

    ROUTED = ("SUMMARY formation=routed verify_mode=pre n=46 passed=46 "
              "grave_errors=0 total_cost=260 resolved=22 verifier_calls=8 "
              "verifier_tasks=4 hole_deliveries=1 unverified_deliveries=0")
    THRESHOLDS = ("SUMMARY formation=routed-thresholds verify_mode=pre n=46 "
                  "passed=46 grave_errors=0 total_cost=250 resolved=23 "
                  "verifier_calls=8 verifier_tasks=4 hole_deliveries=0 "
                  "unverified_deliveries=0")

    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.root)
        self.tool = load_tool()

    def log(self, *rows):
        """One scratch log holding these rows, in this order."""
        path = os.path.join(self.root, "log.txt")
        with REAL_OPEN(path, "w", encoding="utf-8") as handle:
            handle.write("\n".join(rows) + "\n")
        return path

    def test_a_longer_formation_name_does_not_answer_a_short_one(self):
        rows = self.tool.summaries(self.log(self.THRESHOLDS, self.ROUTED))
        chosen = self.tool.pick(rows, "routed", None, 46)
        self.assertEqual(self.tool.field(chosen, "total_cost"), 260)

    def test_two_rows_for_one_key_that_disagree_are_fatal(self):
        rerun = self.ROUTED.replace("total_cost=260", "total_cost=999")
        with self.assertRaises(self.tool.MeasurementError) as caught:
            self.tool.summaries(self.log(self.ROUTED, rerun))
        self.assertIn("disagree", str(caught.exception))

    def test_an_identical_re_append_collapses(self):
        rows = self.tool.summaries(self.log(self.ROUTED, self.ROUTED))
        self.assertEqual(len(rows), 1)

    def test_an_indented_row_is_still_a_row(self):
        rows = self.tool.summaries(self.log(
            "SUMMARY formation=a n=46 total_cost=1",
            "  SUMMARY formation=b n=46 total_cost=2",
            "seed=3 SUMMARY formation=c n=46 total_cost=3",
            "  seed=4 SUMMARY formation=d n=46 total_cost=4",
        ))
        self.assertEqual(len(rows), 4)

    def test_a_missing_measurement_is_fatal_not_None(self):
        rows = self.tool.summaries(self.log(
            "SUMMARY formation=routed verify_mode=final n=46 total_cost=310"))
        with self.assertRaises(self.tool.MeasurementError):
            self.tool.field(rows[0][1], "hole_deliveries")

    def test_an_open_ended_seed_reads_the_lowest_seed(self):
        rows = self.tool.summaries(self.log(
            "seed=2 SUMMARY formation=routed verify_mode=pre n=46 total_cost=280",
            "seed=3 SUMMARY formation=routed verify_mode=pre n=46 total_cost=310",
        ))
        self.assertEqual(self.tool.field(self.tool.pick(rows, "routed", None, 46),
                                         "total_cost"), 280)


class LeaderboardFreshness(LeaderboardFixture):
    """A second report in one process reads the log again, not a cache."""

    def test_a_second_report_sees_the_log_as_it_is_now(self):
        first = self.run_tool()
        with REAL_OPEN(self.tool.LOG04, "w", encoding="utf-8") as handle:
            handle.write(LOG04.replace("total_cost=300", "total_cost=999"))
        second = self.run_tool()
        self.assertNotEqual(first, second, msg="the second report reused cached rows")
        self.assertIn("999", second)

    def test_seed_stability_is_a_verdict_not_a_return_type(self):
        vals, stable = self.tool.seeds_stable(
            self.tool.summaries(self.tool.LOG04), "pre")
        self.assertEqual(vals, [300, 300, 300, 300, 300])
        self.assertIs(stable, True)


class LeaderboardRefusals(LeaderboardFixture):
    """A contradiction in the log stops the report with a reason, not a number."""

    def test_a_contradiction_fails_loud_and_names_the_rows(self):
        with REAL_OPEN(self.tool.LOG03, "w", encoding="utf-8") as handle:
            handle.write(LOG03 + LOG03.replace("total_cost=260", "total_cost=900"))
        with self.assertRaises(SystemExit) as caught:
            self.run_tool()
        self.assertIn("FAIL-LOUD", str(caught.exception.code))
        self.assertIn("disagree", str(caught.exception.code))

    def test_a_broken_row_prints_no_partial_board(self):
        with REAL_OPEN(self.tool.LOG04, "w", encoding="utf-8") as handle:
            handle.write(LOG04.replace("resolved=12 verifier_calls=0", "resolved=12"))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            with self.assertRaises(SystemExit) as caught:
                self.tool.main()
        self.assertIn("FAIL-LOUD", str(caught.exception.code))
        self.assertEqual(out.getvalue(), "",
                         msg="a failed report left part of the board on stdout")


if __name__ == "__main__":
    unittest.main()
