"""Shared abstention judges (single source of truth).

Promoted from repro/run_repro.py at REPRO consolidation: the v1 keyword
judge plus its v2 (crew HOLD idioms), v3 (anchoring repair), and v4
(paraphrase) refinements. Frozen semantics: v1 is the model-leg judge;
v2-v4 are transfer candidates scored side-by-side. Nothing here may
change the v1 patterns without a new experiment node.
"""

import re

ABSTAIN_RES = [
    r"\babstain\b", r"\bcan ?not\b", r"\bcannot\b", r"\bunable\b",
    r"don'?t know", r"\bunknown\b", r"\bmissing\b", r"\bnot provided\b",
    r"\bnot stated\b", r"\bneed more\b", r"\binsufficient\b",
    r"\bno .* (given|provided|attached)\b", r"\bhold\b",
]


def is_abstain(text):
    t = text.lower()
    return any(re.search(p, t) for p in ABSTAIN_RES)


CREW_ABSTAIN_RES = [
    r"tool-gap:", r"conflict:", r"contradiction:", r"citation-cut:",
    r"gap-miss:", r"no deliverable content",
]


def is_abstain_v2(text):
    """v1 keyword judge OR crew HOLD idioms (R8/R3 gap markers)."""
    t = text.lower()
    return is_abstain(text) or any(re.search(p, t) for p in CREW_ABSTAIN_RES)


# v3: anchoring repair. Bare `\bhold\b` matched prose ("claims hold");
# NDC-substring matched mid-sentence use. v3 drops bare hold
# (sentence-initial only) and requires NDC to end the sentence.
# The remaining over-fire ("...content was missing...") comes via
# "missing" — a negation-scope limit load-bearing for T3, kept.
V3_WORD_RES = [p for p in ABSTAIN_RES if p != r"\bhold\b"]
V3_ANCHORED_RES = [r"(?:^|[.!?]\s+)hold\b", r"no deliverable content\s*[.!?]"]
V3_CREW_RES = [p for p in CREW_ABSTAIN_RES if p != r"no deliverable content"]


def is_abstain_v3(text):
    t = text.lower()
    return (any(re.search(p, t) for p in V3_WORD_RES)
            or any(re.search(p, t) for p in V3_ANCHORED_RES)
            or any(re.search(p, t) for p in V3_CREW_RES))


# v4: paraphrase patterns for the stress-documented sensitivity misses
# (can't / not-sure / don't-have). v1-v3 untouched.
V4_PARA_RES = [r"can['\u2019]t\b", r"not sure\b", r"don['\u2019]t have\b"]


def is_abstain_v4(text):
    return is_abstain_v3(text) or any(
        re.search(p, text.lower()) for p in V4_PARA_RES)


# v5 (experiment): scoped paraphrases. v4's bare patterns flag all three
# SENS ACT-context probes ("can't help with that", "not sure about the
# exact figure", "don't have that information"), contradicting the fixture
# want=False semantics. v5 requires a paraphrase to co-occur with an
# evidence-gap noun, so bare refusals stay ACT while grounded paraphrases
# ("can't verify without the source") still flag. v1-v4 untouched.
V5_PARA_RES = list(V4_PARA_RES)
V5_EVIDENCE_RES = [
    r"\bsource\b", r"\bdata\b", r"\bevidence\b", r"\bverif\w*\b",
    r"\banswer\b", r"\bmissing\b", r"\binsufficient\b", r"\bunknown\b",
]


def is_abstain_v5(text):
    t = text.lower()
    if is_abstain_v3(text):
        return True
    has_para = any(re.search(p, t) for p in V5_PARA_RES)
    has_ev = any(re.search(p, t) for p in V5_EVIDENCE_RES)
    return bool(has_para and has_ev)
