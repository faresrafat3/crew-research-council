#!/usr/bin/env python3
"""Witness for the CI half of the gate: it is closed or it is recorded.

`.github/workflows/docs-gate.yml` must either already run `tools/gate.sh`, or
the recorded patch `tools/ci-gate.patch` must still apply cleanly, so a token
that holds the `workflows` permission can close the gap in one command. The
third state (neither) is a lie in the file, and this test refuses it.

Run: python3 -m unittest discover -s tests/unit -v
"""

import os
import shutil
import subprocess
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORKFLOW = os.path.join(ROOT, ".github", "workflows", "docs-gate.yml")
PATCH = os.path.join(ROOT, "tools", "ci-gate.patch")


class CiGateState(unittest.TestCase):
    """Two legal states: CI runs the gate, or the patch to make it run applies."""

    def setUp(self):
        with open(WORKFLOW, encoding="utf-8") as handle:
            self.workflow = handle.read()

    def test_ci_runs_the_gate_or_the_recorded_patch_still_applies(self):
        if "tools/gate.sh" in self.workflow:
            return
        git = shutil.which("git")
        if git is None:
            self.skipTest("git is not installed; cannot check the recorded patch")
        result = subprocess.run(
            [git, "apply", "--check", PATCH],
            cwd=ROOT, capture_output=True, text=True,
        )
        self.assertEqual(
            result.returncode, 0,
            msg="CI runs the docs gate alone and the recorded patch no longer "
                f"applies, so the recorded CI state is stale:\n{result.stderr}",
        )

    def test_the_recorded_patch_carries_the_whole_change(self):
        if "tools/gate.sh" in self.workflow:
            self.skipTest("CI already runs the gate; there is no patch to check")
        with open(PATCH, encoding="utf-8") as handle:
            patch = handle.read()
        self.assertIn("+        run: bash tools/gate.sh", patch)
        self.assertIn('+      - "tools/**"', patch)
        self.assertIn('+      - "tests/**"', patch)
        self.assertIn('+      - ".githooks/**"', patch)

    def test_a_closed_ci_half_keeps_no_stale_patch(self):
        if "tools/gate.sh" not in self.workflow:
            return
        self.assertFalse(
            os.path.exists(PATCH),
            msg="CI already runs the gate; delete tools/ci-gate.patch so the "
                "record stops claiming the half is open",
        )


if __name__ == "__main__":
    unittest.main()
