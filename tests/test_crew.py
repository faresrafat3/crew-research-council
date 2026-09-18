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


class TestContradiction(unittest.TestCase):
    def test_contradictory_brief_holds_with_named_gap(self):
        tasks = load_tasks()
        out = run_executor(tasks["T8"])
        self.assertEqual(out["verdict"], "HOLD")
        self.assertTrue(any(g.startswith("CONTRADICTION:") for g in out["gaps"]))

    def test_hold_withholds_draft_no_breach(self):
        # The T8 draft still contains the banned phrase, but HOLD delivers
        # nothing — the reviewer must not flag a breach on withheld text.
        tasks = load_tasks()
        out = run_executor(tasks["T8"])
        grade = run_reviewer(tasks["T8"], out["text"], out["gaps"])
        self.assertEqual(grade["grade"], "PASS")
        self.assertFalse(grade["grave_error"])

    def test_breach_on_deliver_still_flagged(self):
        tasks = load_tasks()
        grade = run_reviewer(tasks["T8"], "root cause unknown happened",
                             [])
        self.assertIn("CONSTRAINT-BREACH:ban='root cause':PRESENT",
                      grade["findings"])


class TestLimits(unittest.TestCase):
    def test_contested_evidence_holds(self):
        tasks = load_tasks()
        out = run_executor(tasks["T9"])
        self.assertEqual(out["verdict"], "HOLD")
        self.assertTrue(any(g.startswith("CONFLICT:") for g in out["gaps"]))
        grade = run_reviewer(tasks["T9"], out["text"], out["gaps"])
        self.assertEqual(grade["grade"], "PASS")

    def test_unadjudicated_conflict_is_grave(self):
        tasks = load_tasks()
        grade = run_reviewer(tasks["T9"], "[R1] 42min (evidence: log-A)",
                             [])
        self.assertIn("CONFLICT-MISS:R1", grade["findings"])
        self.assertTrue(grade["grave_error"])

    def test_no_fetch_tool_no_citation(self):
        # Solo executor holds with TOOL-GAP rather than inventing a source.
        tasks = load_tasks()
        out = run_executor(tasks["T10"])
        self.assertEqual(out["verdict"], "HOLD")
        self.assertTrue(any(g.startswith("TOOL-GAP:") for g in out["gaps"]))
        grade = run_reviewer(tasks["T10"], out["text"], out["gaps"])
        self.assertEqual(grade["grade"], "PASS")

    def test_fabricated_citation_flagged(self):
        tasks = load_tasks()
        grade = run_reviewer(tasks["T10"],
                             "[R1] 99 minutes (evidence: trust-me-blog)",
                             [])
        self.assertTrue(any(f.startswith("UNGROUNDED:") for f in grade["findings"]))
        self.assertTrue(grade["grave_error"])

    def test_grounded_delivery_passes_flex(self):
        from crew.roles import run_researcher
        tasks = load_tasks()
        fetched, _ = run_researcher(tasks["T10"])
        work = dict(tasks["T10"])
        work["requirements"] = [dict(r, evidence=fetched[r["id"]])
                                for r in work["requirements"]]
        out = run_executor(work)
        self.assertEqual(out["verdict"], "DELIVER")
        grade = run_reviewer(work, out["text"], out["gaps"])
        self.assertEqual(grade["grade"], "PASS")

    def test_team_variant_routes_researcher(self):
        import json
        with open("variant.json") as f:
            v = json.load(f)
        self.assertEqual(v["formation"], "team")
        self.assertTrue(v["hold_on_vague"])


class TestGeneralizationProbes(unittest.TestCase):
    def test_unseen_conflict_probe_holds(self):
        # T11 is a fresh domain for the same rule: no new code was written
        # for it. Generalization, not fitting.
        tasks = load_tasks()
        out = run_executor(tasks["T11"])
        self.assertEqual(out["verdict"], "HOLD")
        grade = run_reviewer(tasks["T11"], out["text"], out["gaps"])
        self.assertEqual(grade["grade"], "PASS")

    def test_unseen_external_probe_withholds_solo(self):
        tasks = load_tasks()
        out = run_executor(tasks["T12"])
        self.assertEqual(out["verdict"], "HOLD")
        grade = run_reviewer(tasks["T12"], out["text"], out["gaps"])
        self.assertEqual(grade["grade"], "PASS")

    def test_unseen_contradiction_probe_holds(self):
        tasks = load_tasks()
        out = run_executor(tasks["T13"])
        self.assertEqual(out["verdict"], "HOLD")
        grade = run_reviewer(tasks["T13"], out["text"], out["gaps"])
        self.assertEqual(grade["grade"], "PASS")

    def test_shuffle_seed_is_deterministic(self):
        import random
        tasks = load_tasks()
        ids = sorted(tasks)
        a = ids[:]
        random.Random(7).shuffle(a)
        b = ids[:]
        random.Random(7).shuffle(b)
        self.assertEqual(a, b)
        self.assertNotEqual(a, ids)


class TestSynthesisProbes(unittest.TestCase):
    def test_multi_source_withholds_both_gaps_solo(self):
        tasks = load_tasks()
        out = run_executor(tasks["T14"])
        self.assertEqual(out["verdict"], "HOLD")
        self.assertEqual(2, sum(1 for g in out["gaps"]
                               if g.startswith("TOOL-GAP:")))
        grade = run_reviewer(tasks["T14"], out["text"], out["gaps"])
        self.assertEqual(grade["grade"], "PASS")

    def test_source_conflict_holds_even_when_grounded(self):
        # Contested dominates grounding: fetching SRC-X must not launder the
        # conflict between the brief evidence and the vendor postmortem.
        from crew.roles import run_researcher
        tasks = load_tasks()
        fetched, _ = run_researcher(tasks["T15"])
        self.assertIn("R1", fetched)
        work = dict(tasks["T15"])
        work["requirements"] = [dict(r, evidence=fetched.get(r["id"],
                                                             r.get("evidence")))
                                for r in work["requirements"]]
        out = run_executor(work)
        self.assertEqual(out["verdict"], "HOLD")
        grade = run_reviewer(work, out["text"], out["gaps"])
        self.assertEqual(grade["grade"], "PASS")

    def test_synthesis_under_constraint_withholds_solo(self):
        tasks = load_tasks()
        out = run_executor(tasks["T16"])
        self.assertEqual(out["verdict"], "HOLD")
        grade = run_reviewer(tasks["T16"], out["text"], out["gaps"])
        self.assertEqual(grade["grade"], "PASS")

    def test_researcher_fetches_source_list(self):
        from crew.roles import run_researcher
        tasks = load_tasks()
        fetched, calls = run_researcher(tasks["T14"])
        self.assertEqual(set(fetched), {"R1", "R2"})
        self.assertEqual(calls, 3)


class TestAdversarialProbes(unittest.TestCase):
    def _ground(self, tid):
        from crew.roles import run_researcher
        tasks = load_tasks()
        fetched, _ = run_researcher(tasks[tid])
        work = dict(tasks[tid])
        work["requirements"] = [dict(r, evidence=fetched.get(r["id"],
                                                             r.get("evidence")))
                                for r in work["requirements"]]
        return work

    def test_poisoned_source_withholds_solo(self):
        tasks = load_tasks()
        out = run_executor(tasks["T17"])
        self.assertEqual(out["verdict"], "HOLD")
        grade = run_reviewer(tasks["T17"], out["text"], out["gaps"])
        self.assertEqual(grade["grade"], "PASS")

    def test_cited_poison_trips_self_check(self):
        # Grounded arm cites the poison — the self-check must still catch it.
        work = self._ground("T17")
        out = run_executor(work)
        self.assertEqual(out["verdict"], "HOLD")
        self.assertTrue(any(g.startswith("CONTRADICTION:") for g in out["gaps"]))
        grade = run_reviewer(work, out["text"], out["gaps"])
        self.assertEqual(grade["grade"], "PASS")

    def test_partial_grounding_stays_hold(self):
        work = self._ground("T18")
        out = run_executor(work)
        self.assertEqual(out["verdict"], "HOLD")
        self.assertTrue(any(g.startswith("TOOL-GAP:R2") for g in out["gaps"]))
        grade = run_reviewer(work, out["text"], out["gaps"])
        self.assertEqual(grade["grade"], "PASS")

    def test_instruction_in_source_is_inert(self):
        # Data is data: the smuggled instruction changes neither verdict
        # (grounded DELIVER stands) nor compliance (no findings).
        work = self._ground("T19")
        out = run_executor(work)
        self.assertEqual(out["verdict"], "DELIVER")
        grade = run_reviewer(work, out["text"], out["gaps"])
        self.assertEqual(grade["grade"], "PASS")
        self.assertFalse(grade["grave_error"])


class TestGraderAudit(unittest.TestCase):
    def test_id_collision_does_not_cover(self):
        # R7 audit: "R1" must not hide inside an "R10:..." gap. Fails on the
        # old substring check, passes on exact-segment matching.
        tiny = {"id": "X", "requirements": [
            {"id": "R1", "text": "u1", "verifiable": False,
             "explicit": True, "evidence": None},
            {"id": "R10", "text": "u10", "verifiable": False,
             "explicit": True, "evidence": None}],
            "expected": "HOLD"}
        grade = run_reviewer(tiny, "text", ["R10:u10"])
        self.assertIn("GAP-MISS:R1", grade["findings"])
        self.assertNotIn("GAP-MISS:R10", grade["findings"])

    def test_exact_segment_still_covers(self):
        tasks = load_tasks()
        out = run_executor(tasks["T3"])
        grade = run_reviewer(tasks["T3"], out["text"], out["gaps"])
        self.assertEqual(grade["grade"], "PASS")

    def test_severed_citation_holds_post_fix(self):
        # R8 repair: the word cap still cuts both citations, but the draft
        # now HOLDs instead of delivering a phantom.
        from crew.roles import run_researcher
        import re
        tasks = load_tasks()
        fetched, _ = run_researcher(tasks["T20"])
        work = dict(tasks["T20"])
        work["requirements"] = [dict(r, evidence=fetched.get(r["id"],
                                                             r.get("evidence")))
                                for r in work["requirements"]]
        out = run_executor(work)
        self.assertEqual(out["verdict"], "HOLD")
        self.assertTrue(any(g.startswith("CITATION-CUT:") for g in out["gaps"]))
        cites = re.findall(r"\(evidence: ([^)]*)\)", out["text"])
        self.assertEqual(cites, [])
        grade = run_reviewer(work, out["text"], out["gaps"])
        self.assertEqual(grade["grade"], "PASS")
        self.assertFalse(grade["grave_error"])

    def test_intact_citations_still_deliver(self):
        # The check fires only on severing: T10's short grounded text is
        # unaffected.
        from crew.roles import run_researcher
        tasks = load_tasks()
        fetched, _ = run_researcher(tasks["T10"])
        work = dict(tasks["T10"])
        work["requirements"] = [dict(r, evidence=fetched[r["id"]])
                                for r in work["requirements"]]
        out = run_executor(work)
        self.assertEqual(out["verdict"], "DELIVER")


if __name__ == "__main__":
    unittest.main()
