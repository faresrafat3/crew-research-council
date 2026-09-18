"""Blind evaluation driver. Prints its own evidence (config + per-task + SUMMARY).

Usage:
    python3 -m crew.eval --tasks tasks/real-missions.json --formation solo

Grading is blind by construction: the reviewer receives output text + gaps
only, never the formation label. Grader cost is excluded from formation cost.
Exit code is always 0: this measures, it does not gate (pytest gates).
"""

import argparse
import json
import time

from crew.router import propose_formation
from crew.roles import run_executor, run_reviewer, run_researcher
from harness.state import Budget, RunLedger


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", required=True)
    ap.add_argument("--formation", default="solo",
                    choices=["solo", "solo-checklist", "duo", "team"])
    ap.add_argument("--hold-on-vague", action="store_true",
                    help="Hold on vague gaps too (hold-rule variant).")
    ap.add_argument("--checklist", action="store_true",
                    help="Attention checklist audit pass (+1 cost/task, "
                         "no behavior change by design).")
    ap.add_argument("--max-tool-calls", type=int, default=100)
    args = ap.parse_args()

    with open(args.tasks) as f:
        tasks = json.load(f)

    used = {"solo": "SOLO", "solo-checklist": "SOLO",
            "duo": "DUO"}[args.formation]
    print(f"CONFIG formation_used={used} variant={args.formation} "
          f"hold_on_vague={args.hold_on_vague} checklist={args.checklist} "
          f"tasks={len(tasks)} budget_calls={args.max_tool_calls}")

    ledger = RunLedger()
    budget = Budget(max_tool_calls=args.max_tool_calls)
    t0 = time.time()
    resolved = 0  # DELIVER-PASS: compliant AND useful (R3 value metric)
    for task in tasks:
        proposed, criteria, score = propose_formation(task)
        used = {"solo": "SOLO", "solo-checklist": "SOLO",
                "duo": "DUO", "team": "SOLO"}[args.formation]
        try:
            work = task
            if args.formation == "team" and task.get("external_source"):
                # Researcher stage (fetch tool) grounds the brief first.
                fetched, rcalls = run_researcher(task)
                budget.spend(rcalls)
                cost = rcalls
                work = dict(task)
                work["requirements"] = [
                    dict(r, evidence=fetched[r["id"]])
                    if r["id"] in fetched else r
                    for r in task["requirements"]
                ]
                used = "TEAM"
            else:
                cost = 0
            out = run_executor(work, hold_on_vague=args.hold_on_vague)
            budget.spend(out["tool_calls"])
            cost = cost + out["tool_calls"]
            if used == "DUO":
                cost += 2  # independent verifier pass (different checks)
                budget.spend(2)
            if args.checklist:
                cost += 1  # audit pass only: perfect trail, same decision
                budget.spend(1)
            grade = run_reviewer(work, out["text"], out["gaps"])
            if grade["grade"] == "PASS" and out["verdict"] == "DELIVER":
                resolved += 1
            status = "ok"
        except RuntimeError as e:
            out = {"verdict": "HOLD", "text": "", "gaps": ["budget:" + str(e)],
                   "tool_calls": 0}
            grade = {"grade": "FAIL", "verdict_ok": False,
                     "findings": ["BUDGET-EXHAUSTED"], "grave_error": False}
            cost = 0
            status = "budget-held"
        ledger.add(task=task["id"], klass=task["class"], proposed=proposed,
                   used=used, score=score, verdict=out["verdict"],
                   gaps=out["gaps"], grade=grade["grade"],
                   findings=grade["findings"],
                   grave_error=grade["grave_error"], cost=cost)
        print(f"TASK {task['id']} [{task['class']}] proposed={proposed} "
              f"used={used} verdict={out['verdict']} gaps={out['gaps']} "
              f"grade={grade['grade']} findings={grade['findings']} "
              f"grave={grade['grave_error']} cost={cost} status={status}")
    s = ledger.summary()
    dt = time.time() - t0
    rate = s["passed"] / s["n"] if s["n"] else 0.0
    print(f"SUMMARY n={s['n']} passed={s['passed']} rate={rate:.3f} "
          f"grave_errors={s['grave_errors']} total_cost={s['total_cost']} "
          f"resolved={resolved} "
          f"routing_match={s['routing_match']}/{s['n']} wall_s={dt:.2f} "
          f"formation={used}")


if __name__ == "__main__":
    main()
