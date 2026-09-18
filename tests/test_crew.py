"""Router + role unit tests (stdlib unittest; pytest migration is a Phase-1 target)."""

import inspect
import json
import unittest

from crew.router import propose_formation
from crew.roles import run_executor, run_reviewer


def load_tasks():
    with open("tasks/real-missions.json") as f:
        return {t["id"]: t for t in json.load(f)}


class TestRouter(unittest.TestCase):
    def test_simple_task_proposes_solo(self):
        tasks = load_tasks()
        formation, _, _ = propose_formation(tasks["T6"])
        self.assertEqual(formation, "SOLO")

    def test_multistep_task_proposes_pipeline(self):
        tasks = load_tasks()
        formation, _, score = propose_formation(tasks["T7"])
        self.assertEqual(formation, "PIPELINE")
        self.assertGreaterEqual(score, 5)


class TestBaselineExecutor(unittest.TestCase):
    def test_explicit_gap_holds(self):
        tasks = load_tasks()
        out = run_executor(tasks["T3"])
        self.assertEqual(out["verdict"], "HOLD")
        self.assertTrue(any("R2" in g for g in out["gaps"]))

    def test_vague_gap_delivered_around_baseline(self):
        # Documents the known baseline weakness (P4 nuance): vague gaps do
        # not trigger HOLD without the hold-rule. The Round-1 child must flip this.
        tasks = load_tasks()
        out = run_executor(tasks["T2"])
        self.assertEqual(out["verdict"], "DELIVER")

    def test_hold_rule_flips_vague_gap(self):
        tasks = load_tasks()
        out = run_executor(tasks["T2"], hold_on_vague=True)
        self.assertEqual(out["verdict"], "HOLD")

    def test_correction_applied(self):
        tasks = load_tasks()
        out = run_executor(tasks["T1"])
        self.assertTrue(out["correction_applied"])
        self.assertIn("2026-10-02", out["text"])

    def test_constraint_respected(self):
        tasks = load_tasks()
        out = run_executor(tasks["T4"])
        self.assertTrue(out["constraints_ok"])
        self.assertLessEqual(len(out["text"].split()), 40)


class TestReviewer(unittest.TestCase):
    def test_reviewer_is_blind_by_construction(self):
        # The grader must not accept a formation label: grading on output only.
        sig = inspect.signature(run_reviewer)
        self.assertNotIn("formation", sig.parameters)

    def test_vague_gap_miss_is_grave(self):
        tasks = load_tasks()
        out = run_executor(tasks["T2"])
        grade = run_reviewer(tasks["T2"], out["text"], out["gaps"])
        self.assertEqual(grade["grade"], "FAIL")
        self.assertTrue(grade["grave_error"])

    def test_correct_hold_passes(self):
        tasks = load_tasks()
        out = run_executor(tasks["T3"])
        grade = run_reviewer(tasks["T3"], out["text"], out["gaps"])
        self.assertEqual(grade["grade"], "PASS")

    def test_hold_withholds_draft_no_breach(self):
        # HOLD delivers nothing — no breach findings on withheld text.
        tasks = load_tasks()
        out = run_executor(tasks["T3"])
        grade = run_reviewer(tasks["T3"], out["text"], out["gaps"])
        self.assertNotIn("CONSTRAINT-BREACH", str(grade["findings"]))


class TestVerifierOverride(unittest.TestCase):
    def test_executor_alone_breaches_t8(self):
        # Documents the gap the override must close: executor DELIVERs T8
        # with a hard-constraint breach (grave error without the verifier).
        tasks = load_tasks()
        out = run_executor(tasks["T8"])
        self.assertEqual(out["verdict"], "DELIVER")
        grade = run_reviewer(tasks["T8"], out["text"], out["gaps"])
        self.assertEqual(grade["grade"], "FAIL")
        self.assertTrue(grade["grave_error"])

    def test_override_flips_breach_to_hold(self):
        from crew.eval import apply_verifier_override
        tasks = load_tasks()
        out = run_executor(tasks["T8"])
        grade = run_reviewer(tasks["T8"], out["text"], out["gaps"])
        out2, grade2 = apply_verifier_override(tasks["T8"], out, grade)
        self.assertEqual(out2["verdict"], "HOLD")
        self.assertTrue(any(g.startswith("OVERRIDE:") for g in out2["gaps"]))
        self.assertEqual(grade2["grade"], "PASS")
        self.assertFalse(grade2["grave_error"])

    def test_override_noop_on_clean_output(self):
        from crew.eval import apply_verifier_override
        tasks = load_tasks()
        out = run_executor(tasks["T6"])
        grade = run_reviewer(tasks["T6"], out["text"], out["gaps"])
        out2, grade2 = apply_verifier_override(tasks["T6"], out, grade)
        self.assertEqual(out2["verdict"], "DELIVER")
        self.assertEqual(grade2["grade"], "PASS")


if __name__ == "__main__":
    unittest.main()
