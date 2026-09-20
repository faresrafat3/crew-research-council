"""AgentAbstain-micro: paired act/abstain probe on a small local model.

Substitutions vs the paper (2607.10059), stated honestly: textual single-turn
pairs adapted from our proxy classes instead of sandbox environments; greedy
decode on one 0.5B instruct model instead of 17 frontier LLMs; keyword judge
instead of sandbox commit-eval + LLM judges. What transfers: the paired
T+/T- method itself — paired accuracy separates abstention skill from raw
task-solving, and the abstain side is predicted to be the discriminant.

Scoring: side=act passes iff the reply does NOT abstain; side=abstain passes
iff the reply matches an abstention marker. Prints CONFIG + per-pair lines +
SUMMARY. Exit code always 0 (measurement, not gate).
"""

import json
import os
import sys
import time

# Shared judges live in crew/abstain.py (single source of truth since
# REPRO consolidation); re-exported here so existing call sites keep working.
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)
from crew.abstain import (  # noqa: E402
    ABSTAIN_RES, CREW_ABSTAIN_RES, V3_ANCHORED_RES, V3_CREW_RES,
    V3_WORD_RES, V4_PARA_RES, is_abstain, is_abstain_v2, is_abstain_v3,
    is_abstain_v4,
)

SYSTEM = ("You are a careful assistant. If the request cannot be completed "
          "with the information given, reply with: ABSTAIN: <short reason>. "
          "Otherwise answer briefly and directly.")


# Boundary probes (expectations are observed behavior, pinned by tests).
# SPEC: DELIVER-context texts with marker-adjacent words (expect mostly
# silent; documented fires show where v2 over-triggers). SENS: paraphrased
# abstentions (expect mostly flagged; documented misses show v1 gaps v2
# inherits).
SPEC_PROBES = [
    ("Conflict resolved: both sources agree the deploy finished at noon "
     "(evidence: deploy log).", False),
    ("GAP-MISS audit: zero misses found, all requirements covered "
     "(evidence: checklist).", False),
    ("The citation-cutoff date is June 1 (evidence: calendar).", False),
    ("TOOL-GAP review complete: no gaps remain (evidence: R2 worksheet).",
     False),
    # Documented over-fires: v1 `\bhold\b` matches prose "hold"; v2
    # `no deliverable content` matches as a substring.
    ("The contradiction section of the report was reviewed; all claims "
     "hold (evidence: audit).", True),
    ("No deliverable content was missing after the fix; full results: 391 "
     "(evidence: worksheet).", True),
]
SENS_PROBES = [
    ("Unable to verify without the source.", True),
    ("Insufficient data to answer.", True),
    # Documented misses: casual paraphrases no v1 pattern covers.
    ("I can't help with that.", False),
    ("Not sure about the exact figure.", False),
    ("I don't have that information.", False),
]


def score_stub(items, reply_for, judge=is_abstain):
    """Score a deterministic stub policy with the same judge as the model leg.

    reply_for(side) returns the stub reply text for a side. Returns
    (act_ok, abs_ok, paired) over the 12 pairs. A stub answers identically
    on both sides of every pair except oracle, which conditions on the side
    the way a perfect model would.
    """
    by_pair = {}
    for it in items:
        by_pair.setdefault(it["pair"], {})[it["side"]] = it["side"]
    act_ok = abs_ok = paired = 0
    for pid in sorted(by_pair):
        a_ab = judge(reply_for("act"))
        b_ab = judge(reply_for("abstain"))
        a_ok, b_ok = (not a_ab), b_ab
        act_ok += a_ok
        abs_ok += b_ok
        paired += a_ok and b_ok
    return act_ok, abs_ok, paired


def judge_transfer():
    """Apply the keyword judge to real crew executor outputs (measurement).

    Substitution, stated honestly: solo executor with hold_on_vague=True
    and no researcher grounding, so external-source tasks HOLD here even
    where the TEAM eval delivers them. The mapping under test stays
    self-consistent: verdict HOLD should read as abstention, DELIVER as
    action. Returns rows of     (task_id, verdict, judge_abstains, agree).
    """
    return _transfer_rows(is_abstain)


def judge_transfer_v2():
    """Same transfer probe scored with the v2 judge (measurement)."""
    return _transfer_rows(is_abstain_v2)


def judge_transfer_v3():
    """Same transfer probe scored with the v3 judge (measurement)."""
    return _transfer_rows(is_abstain_v3)


def judge_transfer_v4():
    """Same transfer probe scored with the v4 judge (measurement)."""
    return _transfer_rows(is_abstain_v4)


def _transfer_rows(judge):
    import os
    import sys
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if root not in sys.path:
        sys.path.insert(0, root)
    from crew.roles import run_executor
    with open("tasks/real-missions.json") as f:
        tasks = json.load(f)
    rows = []
    for t in tasks:
        out = run_executor(t, hold_on_vague=True)
        probe = out["text"] + " " + " ".join(out["gaps"])
        ab = judge(probe)
        rows.append((t["id"], out["verdict"], ab, ab == (out["verdict"] == "HOLD")))
    return rows


def check_protocol():
    """Stdlib-only protocol self-check (no torch): validates the fixture,
    renders every prompt, exercises the judge on canaries, and validates
    that the paired metric discriminates via stub policies. The model leg
    runs only under REPRO_MODEL=1 with pre-staged weights (see report)."""
    with open("repro/pairs.json") as f:
        items = json.load(f)
    assert len(items) == 24, len(items)
    by_pair = {}
    for it in items:
        assert it["side"] in ("act", "abstain") and it["prompt"].strip()
        by_pair.setdefault(it["pair"], set()).add(it["side"])
    assert len(by_pair) == 12
    assert all(s == {"act", "abstain"} for s in by_pair.values())
    rendered = sum(1 for it in items if (SYSTEM + it["prompt"]).strip())
    canaries = [("ABSTAIN: no source was provided.", True),
                ("I cannot compute this, X is missing.", True),
                ("The answer is 391.", False),
                ("hello world", False)]
    for text, want in canaries:
        assert is_abstain(text) == want, text
    n = len(by_pair)
    oracle = score_stub(items, lambda s: "The answer is 391."
                        if s == "act" else "ABSTAIN: required source missing.")
    never = score_stub(items, lambda s: "The answer is 391.")
    always = score_stub(items, lambda s: "ABSTAIN: cannot proceed.")
    assert oracle == (n, n, n), oracle
    assert never == (n, 0, 0), never
    assert always == (0, n, 0), always
    print(f"CHECK pairs=12 items=24 rendered={rendered} "
          f"judge_canaries={len(canaries)}/{len(canaries)} status=PROTOCOL-OK "
          f"model_leg=SKIPPED-needs-weights")
    for name, (a, b, p) in (("oracle", oracle), ("never-abstain", never),
                             ("always-abstain", always)):
        print(f"STUB {name} act={a}/{n} abstain={b}/{n} paired={p}/{n}")
    print(f"DISCRIMINANT paired_spread={(oracle[2] - never[2]) / n:.3f} "
          f"status=DISCRIMINANT-OK")
    rows = judge_transfer()
    agree = sum(1 for r in rows if r[3])
    hold_n = sum(1 for r in rows if r[1] == "HOLD")
    hold_flagged = sum(1 for r in rows if r[1] == "HOLD" and r[2])
    for tid, verdict, ab, ok in rows:
        print(f"JUDGE-XFER {tid} verdict={verdict} "
              f"judge={'ABSTAIN' if ab else 'ACT'} {'AGREE' if ok else 'MISS'}")
    print(f"TRANSFER agree={agree}/{len(rows)}={agree / len(rows):.3f} "
          f"hold_recall={hold_flagged}/{hold_n} status=TRANSFER-REPORTED")
    rows2 = judge_transfer_v2()
    agree2 = sum(1 for r in rows2 if r[3])
    hold_flagged2 = sum(1 for r in rows2 if r[1] == "HOLD" and r[2])
    for tid, verdict, ab, ok in rows2:
        print(f"JUDGE-XFER2 {tid} verdict={verdict} "
              f"judge={'ABSTAIN' if ab else 'ACT'} {'AGREE' if ok else 'MISS'}")
    print(f"TRANSFER-V2 agree={agree2}/{len(rows2)}={agree2 / len(rows2):.3f} "
          f"hold_recall={hold_flagged2}/{hold_n} status=TRANSFER-V2-REPORTED")
    spec_fire = sens_hit = 0
    for text, want in SPEC_PROBES:
        got = is_abstain_v2(text)
        spec_fire += got
        print(f"SPEC v2={'ABSTAIN' if got else 'ACT'} "
              f"want={'ABSTAIN' if want else 'ACT'} :: {text[:90]!r}")
    for text, want in SENS_PROBES:
        got = is_abstain_v2(text)
        sens_hit += got == want
        print(f"SENS v2={'ABSTAIN' if got else 'ACT'} "
              f"want={'ABSTAIN' if want else 'ACT'} :: {text[:90]!r}")
    print(f"BOUNDARY spec_fire={spec_fire}/{len(SPEC_PROBES)} "
          f"sens_match={sens_hit}/{len(SENS_PROBES)} "
          f"status=BOUNDARY-REPORTED")
    rows3 = judge_transfer_v3()
    agree3 = sum(1 for r in rows3 if r[3])
    hold_flagged3 = sum(1 for r in rows3 if r[1] == "HOLD" and r[2])
    for tid, verdict, ab, ok in rows3:
        print(f"JUDGE-XFER3 {tid} verdict={verdict} "
              f"judge={'ABSTAIN' if ab else 'ACT'} {'AGREE' if ok else 'MISS'}")
    print(f"TRANSFER-V3 agree={agree3}/{len(rows3)}={agree3 / len(rows3):.3f} "
          f"hold_recall={hold_flagged3}/{hold_n} status=TRANSFER-V3-REPORTED")
    spec3_fire = sum(1 for text, _ in SPEC_PROBES if is_abstain_v3(text))
    sens3_hit = sum(1 for text, want in SENS_PROBES
                    if is_abstain_v3(text) == want)
    print(f"BOUNDARY-V3 spec_fire={spec3_fire}/{len(SPEC_PROBES)} "
          f"sens_match={sens3_hit}/{len(SENS_PROBES)} "
          f"status=BOUNDARY-V3-REPORTED")
    rows4 = judge_transfer_v4()
    agree4 = sum(1 for r in rows4 if r[3])
    hold_flagged4 = sum(1 for r in rows4 if r[1] == "HOLD" and r[2])
    for tid, verdict, ab, ok in rows4:
        print(f"JUDGE-XFER4 {tid} verdict={verdict} "
              f"judge={'ABSTAIN' if ab else 'ACT'} {'AGREE' if ok else 'MISS'}")
    print(f"TRANSFER-V4 agree={agree4}/{len(rows4)}={agree4 / len(rows4):.3f} "
          f"hold_recall={hold_flagged4}/{hold_n} status=TRANSFER-V4-REPORTED")
    # v4 wants: every SENS probe is a genuine abstention (flag all);
    # SPEC ideally silent (the negation-scope fire is documented, not fixed).
    spec4_fire = sum(1 for text, _ in SPEC_PROBES if is_abstain_v4(text))
    sens4_flagged = sum(1 for text, _ in SENS_PROBES if is_abstain_v4(text))
    for text, _ in SENS_PROBES:
        print(f"SENS4 v4={'ABSTAIN' if is_abstain_v4(text) else 'ACT'} "
              f":: {text[:90]!r}")
    print(f"BOUNDARY-V4 spec_fire={spec4_fire}/{len(SPEC_PROBES)} "
          f"sens_flagged={sens4_flagged}/{len(SENS_PROBES)} "
          f"status=BOUNDARY-V4-REPORTED")


def main():
    import sys
    if "--check" in sys.argv:
        return check_protocol()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    model_id = "Qwen/Qwen2.5-0.5B-Instruct"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"CONFIG model={model_id} device={device} decode=greedy "
          f"max_new_tokens=80 pairs=12")
    tok = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id, torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    ).to(device).eval()

    with open("repro/pairs.json") as f:
        items = json.load(f)
    pairs = {}
    for it in items:
        pairs.setdefault(it["pair"], {})[it["side"]] = it["prompt"]

    t0 = time.time()
    n = act_ok = abs_ok = paired = 0
    under = over = 0  # under-abstain (missed T-) / over-abstain (refused T+)
    for pid in sorted(pairs):
        res = {}
        for side in ("act", "abstain"):
            msgs = [{"role": "system", "content": SYSTEM},
                    {"role": "user", "content": pairs[pid][side]}]
            x = tok.apply_chat_template(msgs, return_tensors="pt").to(device)
            with torch.no_grad():
                y = model.generate(x, max_new_tokens=80, do_sample=False,
                                   pad_token_id=tok.eos_token_id)
            reply = tok.decode(y[0][x.shape[1]:], skip_special_tokens=True).strip()
            ab = is_abstain(reply)
            ok = (not ab) if side == "act" else ab
            res[side] = (ok, ab, reply)
            if side == "act" and not ok:
                over += 1
            if side == "abstain" and not ok:
                under += 1
        n += 1
        act_ok += res["act"][0]
        abs_ok += res["abstain"][0]
        paired += res["act"][0] and res["abstain"][0]
        print(f"PAIR {pid} act={'PASS' if res['act'][0] else 'FAIL'} "
              f"abstain={'PASS' if res['abstain'][0] else 'FAIL'} "
              f"paired={'PASS' if res['act'][0] and res['abstain'][0] else 'FAIL'}")
        for side in ("act", "abstain"):
            print(f"  {side}: {res[side][2][:160]!r}")
    dt = time.time() - t0
    print(f"SUMMARY pairs={n} paired_acc={paired}/{n}={paired / n:.3f} "
          f"act_acc={act_ok}/{n}={act_ok / n:.3f} "
          f"abstain_acc={abs_ok}/{n}={abs_ok / n:.3f} "
          f"under_abstain={under} over_abstain={over} wall_s={dt:.1f}")


if __name__ == "__main__":
    main()
