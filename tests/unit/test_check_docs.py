#!/usr/bin/env python3
"""Witness tests for the docs gate (`tools/check_docs.py`).

The gate is the project's one automated hot path: `.githooks/pre-commit` and
`.github/workflows/docs-gate.yml` both run it. These tests pin what that run
costs on disk and what it reports, so a refactor cannot quietly re-read a
README or change a verdict.

Run: python3 -m unittest discover -s tests/unit -v
"""

import builtins
import contextlib
import importlib.util
import io
import os
import re
import shutil
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GATE = os.path.join(ROOT, "tools", "check_docs.py")

REAL_OPEN = builtins.open


def load_gate():
    """Import tools/check_docs.py as a module without running main()."""
    spec = importlib.util.spec_from_file_location("check_docs", GATE)
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


def run_gate(module, argv):
    """Run the gate with cwd at the repo root; return (code, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    cwd = os.getcwd()
    os.chdir(ROOT)
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = module.main(argv)
    finally:
        os.chdir(cwd)
    return code, out.getvalue(), err.getvalue()


class GateReadCost(unittest.TestCase):
    """One pass per file: no README may be opened twice in a single run."""

    def test_each_cleaned_readme_is_read_exactly_once(self):
        gate = load_gate()
        counter = ReadCounter()
        builtins.open = counter
        try:
            code, out, err = run_gate(gate, ["check_docs.py"])
        finally:
            builtins.open = REAL_OPEN

        self.assertEqual(code, 0, msg=f"gate failed: {out}{err}")
        for readme in gate.CLEAN_READMES:
            self.assertEqual(
                counter.count(readme),
                1,
                msg=f"{readme} was opened {counter.count(readme)} times in a "
                f"single gate run; the prose and ref rules share one pass",
            )

    def test_no_output_file_is_read_twice(self):
        gate = load_gate()
        counter = ReadCounter()
        builtins.open = counter
        try:
            code, _, err = run_gate(gate, ["check_docs.py"])
        finally:
            builtins.open = REAL_OPEN

        self.assertEqual(code, 0, msg=err)
        repeated = {
            path: counter.count(path)
            for path in set(counter.paths)
            if counter.count(path) > 1
        }
        self.assertEqual(repeated, {}, msg="files read more than once per run")


class GateVerdicts(unittest.TestCase):
    """The gate still reports the same three rules, in the same order."""

    def test_missing_cleaned_readme_fails_the_gate(self):
        gate = load_gate()
        scratch = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, scratch)
        with REAL_OPEN(os.path.join(scratch, "other.md"), "w", encoding="utf-8") as fh:
            fh.write("# Fine\n")
        gate.CLEAN_READMES = (
            os.path.join(scratch, "README.md"),
            os.path.join(scratch, "OUTPUT-README.md"),
        )
        gate.OUTPUT = scratch

        code, _, err = run_gate(gate, ["check_docs.py", scratch])
        self.assertEqual(code, 1)
        self.assertEqual(err.count("missing | the cleaned README is gone"), 2, msg=err)

    def test_empty_tree_exits_two(self):
        gate = load_gate()
        scratch = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, scratch)

        code, _, err = run_gate(gate, ["check_docs.py", scratch])
        self.assertEqual(code, 2)
        self.assertIn(f"no markdown files under {scratch}", err)

    def test_repo_tree_passes_with_the_known_summary(self):
        gate = load_gate()
        code, out, err = run_gate(gate, ["check_docs.py"])
        self.assertEqual(code, 0, msg=err)
        self.assertRegex(
            out,
            r"^docs gate ok: \d+ headings in \d+ files; 2 READMEs clean; "
            r"\d+ refs resolve\n$",
        )

    def test_bad_heading_fails_the_gate(self):
        gate = load_gate()
        scratch = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, scratch)
        with REAL_OPEN(os.path.join(scratch, "chapter.md"), "w", encoding="utf-8") as fh:
            fh.write("# Chapter One Of The Book\n")

        code, out, err = run_gate(gate, ["check_docs.py", scratch])
        self.assertEqual(code, 1)
        self.assertIn("heading case", err)
        self.assertIn("One", err)
        self.assertEqual(out, "")

    def test_readme_prose_and_ref_rules_share_the_pass(self):
        gate = load_gate()
        scratch = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, scratch)
        readme = os.path.join(scratch, "README.md")
        with REAL_OPEN(readme, "w", encoding="utf-8") as fh:
            fh.write(
                "Plain line.\n"
                "A dash — here and **bold** too.\n"
                "Points at `missing.md` and `presents.md`.\n"
            )
        with REAL_OPEN(os.path.join(scratch, "presents.md"), "w", encoding="utf-8") as fh:
            fh.write("# Fine\n")
        with REAL_OPEN(os.path.join(scratch, "other.md"), "w", encoding="utf-8") as fh:
            fh.write("# Fine\n")
        gate.CLEAN_READMES = (readme,)
        gate.OUTPUT = scratch
        counter = ReadCounter()
        builtins.open = counter
        try:
            code, _, err = run_gate(gate, ["check_docs.py", scratch])
        finally:
            builtins.open = REAL_OPEN

        self.assertEqual(code, 1)
        self.assertEqual(counter.count(readme), 1, msg="README opened twice")
        self.assertIn(":2: em dash", err)
        self.assertIn(":2: bold", err)
        self.assertIn(":3: ref | missing.md", err)
        self.assertNotIn("presents.md", err)
        self.assertEqual(
            [line.split(": ", 1)[1].split(" |")[0] for line in err.splitlines()[1:]],
            ["em dash", "bold", "ref"],
            msg=f"rule order drifted:\n{err}",
        )
        self.assertTrue(re.search(r"docs gate: 3 problems", err), msg=err)


if __name__ == "__main__":
    unittest.main()
