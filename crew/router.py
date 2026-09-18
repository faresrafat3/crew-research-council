"""Router (firstmate): task classification + formation selection.

v2-ARCHITECTURE §1: analyzes task type, complexity, constraints; picks from
SOLO -> DUO -> PIPELINE -> FULL; sets explicit success criteria.
Baseline heuristic is deliberately simple and documented so Round 1 can beat it.
"""

FORMATIONS = ("SOLO", "DUO", "PIPELINE", "FULL")


def complexity_score(task):
    """Deterministic score from task shape. Counts what the router can see."""
    reqs = task.get("requirements", [])
    score = len(reqs)
    if task.get("correction"):
        score += 1
    score += len(task.get("constraints", []))
    if task.get("multi_step"):
        score += 2
    if any(not r.get("verifiable", True) for r in reqs):
        score += 1
    return score


def propose_formation(task):
    """Return (formation, success_criteria, score). Thresholds are the hypothesis."""
    score = complexity_score(task)
    if score <= 3:
        formation = "SOLO"
    elif score <= 5:
        formation = "DUO"
    elif score <= 8:
        formation = "PIPELINE"
    else:
        formation = "FULL"
    criteria = [
        f"verdict matches expected ({task.get('expected')})",
        "zero grave errors (no non-compliant delivery, no dropped correction, no constraint breach)",
        "gaps named explicitly on HOLD",
    ]
    return formation, criteria, score
