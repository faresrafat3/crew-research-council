"""Budgets, stop conditions, per-run ledger (harness-side enforcement)."""

import time


class Budget:
    """Hard caps. Exhaustion -> HOLD, never a silent partial delivery."""

    def __init__(self, max_tool_calls=100, max_seconds=300):
        self.max_tool_calls = max_tool_calls
        self.max_seconds = max_seconds
        self.tool_calls = 0
        self.t0 = time.time()

    def spend(self, n=1):
        self.tool_calls += n
        if self.tool_calls > self.max_tool_calls:
            raise RuntimeError("budget-exhausted:tool-calls")
        if time.time() - self.t0 > self.max_seconds:
            raise RuntimeError("budget-exhausted:time")


class RunLedger:
    """One row per task: formation used/proposed, verdict, grade, cost."""

    def __init__(self):
        self.rows = []

    def add(self, **row):
        self.rows.append(row)

    def summary(self):
        n = len(self.rows)
        passed = sum(1 for r in self.rows if r.get("grade") == "PASS")
        graves = sum(1 for r in self.rows if r.get("grave_error"))
        cost = sum(r.get("cost", 0) for r in self.rows)
        routed_right = sum(1 for r in self.rows
                           if r.get("proposed") == r.get("used"))
        return {"n": n, "passed": passed, "grave_errors": graves,
                "total_cost": cost, "routing_match": routed_right}
