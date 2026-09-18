"""Executor + reviewer with explicit I/O contracts (REVIEW-02 §2).

Executor contract: in = task dict; out = output dict with
verdict/text/gaps/correction_applied/constraints_ok/tool_calls.
Reviewer contract: in = task + output text/gaps only (NEVER the formation
label — blind by construction); out = grade dict.

Baseline executor behavior (the hypothesis under test): HOLDs on EXPLICIT
gaps only. Vague-qualitative gaps (explicit=false) are delivered around —
the P4 nuance from the GOAL log. The Round 1 `hold-rule` child fixes this
by making briefs explicit; the change must show up as T2 flipping to HOLD.
"""

import re


def _check_constraint(constraint, text):
    """Machine-checkable constraints only. Returns (ok, detail)."""
    m = re.fullmatch(r"MAX_WORDS:(\d+)", constraint.strip())
    if m:
        limit = int(m.group(1))
        n = len(text.split())
        return n <= limit, f"words={n}/{limit}"
    m = re.fullmatch(r"BAN_PHRASE:(.+)", constraint.strip())
    if m:
        phrase = m.group(1).strip().lower()
        ok = phrase not in text.lower()
        return ok, f"ban={phrase!r}:{'absent' if ok else 'PRESENT'}"
    return True, "uncheckable-ignored"


def run_executor(task, hold_on_vague=False):
    """Run the rule-based executor. hold_on_vague=False is the baseline.

    Returns output dict. tool_calls counts simulated steps (parse + per-req
    verify + compose), the cost proxy for ARENA scoring.
    """
    tool_calls = 1  # parse brief
    gaps = []
    for req in task.get("requirements", []):
        tool_calls += 1  # verify step per requirement
        if not req.get("verifiable", True) and not req.get("evidence"):
            if req.get("explicit", True) or hold_on_vague:
                gaps.append(req["id"] + ":" + req["text"])

    correction_applied = False
    text_parts = []
    if task.get("correction"):
        correction_applied = True
        text_parts.append("Applied correction: " + task["correction"])

    for req in task.get("requirements", []):
        if req.get("verifiable", True) and req.get("evidence"):
            text_parts.append(f"[{req['id']}] {req['text']} (evidence: {req['evidence']})")
        elif req.get("verifiable", True):
            text_parts.append(f"[{req['id']}] {req['text']}")
    text = " ".join(text_parts) if text_parts else "No deliverable content."
    tool_calls += 1  # compose

    constraints_ok = True
    constraint_details = []
    for c in task.get("constraints", []):
        ok, detail = _check_constraint(c, text)
        constraint_details.append(detail)
        if not ok:
            constraints_ok = False

    # Enforce word cap by truncation (executor respects constraints; the
    # reviewer still verifies — constraint-respect is inviolable).
    for c in task.get("constraints", []):
        m = re.fullmatch(r"MAX_WORDS:(\d+)", c.strip())
        if m:
            limit = int(m.group(1))
            words = text.split()
            if len(words) > limit:
                text = " ".join(words[:limit])
            constraints_ok, _ = _check_constraint(c, text), None
            constraints_ok = _check_constraint(c, text)[0]

    # Self-check (R2-A): a draft that still breaches hard constraints after
    # repair is undeliverable — HOLD with the contradiction named, never a
    # knowing breach delivered.
    residual = []
    for c in task.get("constraints", []):
        ok, detail = _check_constraint(c, text)
        if not ok:
            residual.append(detail)

    if gaps:
        verdict = "HOLD"
    elif residual:
        verdict = "HOLD"
        gaps.append("CONTRADICTION:" + ";".join(residual))
    else:
        verdict = "DELIVER"
    return {
        "verdict": verdict,
        "text": text,
        "gaps": gaps,
        "correction_applied": correction_applied,
        "constraints_ok": constraints_ok,
        "constraint_details": constraint_details,
        "tool_calls": tool_calls,
    }


def run_reviewer(task, output_text, output_gaps):
    """Blind grade: output text + gaps only. Returns grade dict.

    Flags ANY unverifiable requirement lacking evidence (explicit or vague),
    checks correction application and machine-checkable constraints.
    """
    findings = []
    for req in task.get("requirements", []):
        if not req.get("verifiable", True) and not req.get("evidence"):
            covered = any(req["id"] in g for g in output_gaps)
            if not covered:
                findings.append(f"GAP-MISS:{req['id']}")
    if task.get("correction") and ("Applied correction" not in output_text):
        findings.append("CORRECTION-DROPPED")
    # HOLD withholds the draft: nothing delivered, nothing breached. Constraint
    # findings apply to DELIVERed text only (R2 shared fixture).
    if not output_gaps:
        for c in task.get("constraints", []):
            ok, detail = _check_constraint(c, output_text)
            if not ok:
                findings.append(f"CONSTRAINT-BREACH:{detail}")

    expected = task.get("expected")
    delivered_hold = len(output_gaps) > 0
    if expected == "HOLD":
        verdict_ok = delivered_hold and not any(
            f.startswith("GAP-MISS") for f in findings
        )
    else:
        verdict_ok = not delivered_hold
    grade = "PASS" if (verdict_ok and not findings) else "FAIL"
    grave = (
        (expected == "HOLD" and not delivered_hold)
        or "CORRECTION-DROPPED" in findings
        or any(f.startswith("CONSTRAINT-BREACH") for f in findings)
    )
    return {"grade": grade, "verdict_ok": verdict_ok, "findings": findings,
            "grave_error": grave}
