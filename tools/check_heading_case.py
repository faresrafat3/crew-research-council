#!/usr/bin/env python3
"""Gate: headings in RESEARCH-COUNCIL/OUTPUT must be sentence case.

Fails (exit 1) when a heading outside a fenced code block carries Title
Case words. Acronyms, tool names, and proper nouns are allowed; the
[DEEP DIVE] marker headings are skipped because STATUS.md greps for that
literal.

Usage: python3 tools/check_heading_case.py [directory]
"""

import glob
import os
import re
import sys

# Multi-token names whose capitalisation is part of the name.
PROTECTED_PHRASES = (
    "Blocking-Authority Charter",
    "GitHub Actions",
    "EU AI Act",
    "Article 14",
    "Little's Law",
    "Redis Streams",
    "Hippocampal-Cortical Consolidation",
    "Test Maturity Model Integration",
    "TMMi Foundation",
    "World Quality Report",
)

# Whole tokens that are names or trademarks.
PROTECTED_TOKENS = {
    "Free-MAD",
    "Self-Verifying",
    "Arabic-English",
}

# Single words that are names, not Title Case.
PROTECTED_WORDS = {
    "Antigravity",
    "Bubblewrap",
    "Braintrust",
    "Brier",
    "Capgemini",
    "Claude",
    "CMMI",
    "Arabic",
    "Cohesion",
    "Crew",
    "Docker",
    "English",
    "Free",
    "Git",
    "Google",
    "Goodhart",
    "Hypothesis",
    "Kafka",
    "Little",
    "Mahalanobis",
    "Meta",
    "MLflow",
    "Morandi",
    "NeurIPS",
    "OpenText",
    "OpenAI",
    "Orpheus",
    "OTel",
    "Redis",
    "Shapley",
    "Sogeti",
    "SOULs",
    "Speakeasy",
    "Span",
    "SQLite",
    "Stanford",
    "Linux",
    "Tricorder",
    "TMMi",
    "Verifying",
    "Weir",
    "Whisper",
}

LABEL = re.compile(
    r"^(?:\d+(?:\.\d+)*\.?|[A-Za-z](?:\.\d+)+|[A-Za-z]\d+\.?|[A-Za-z]\.)\s+"
)
WORD = re.compile(r"[A-Za-z][A-Za-z0-9'’_]*")
FENCE = re.compile(r"^\s*(?:```|~~~)")
HEADING = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
CODE_SPAN = re.compile(r"`[^`]*`")


def is_allowed_capital(part):
    """True when a capitalised word-part is an acronym, code, or number."""
    if re.search(r"\d", part):
        return True
    core = part[:-1] if part.endswith("s") and len(part) > 2 and part[:-1].isupper() else part
    if core.isupper() and len(core) >= 2:
        return True
    if re.search(r"[a-z][A-Z]", part):
        return True
    if len(part) == 1:
        return True
    return False


def violations(body):
    """Capitalised words that should be lowercase in this heading."""
    text = LABEL.sub("", body, count=1)
    text = CODE_SPAN.sub("code", text)
    for phrase in PROTECTED_PHRASES:
        text = text.replace(phrase, "protected")
    bad = []
    for segment in re.split(r"\s+—\s+", text):
        words = WORD.findall(segment)
        for index, word in enumerate(words):
            base = word[:-2] if word.endswith("'s") or word.endswith("’s") else word
            if base in PROTECTED_WORDS or word in PROTECTED_WORDS:
                continue
            if word in PROTECTED_TOKENS or base in PROTECTED_TOKENS:
                continue
            parts = [p for p in re.split(r"[-/]", base) if p]
            start = 1 if index == 0 else 0
            for part in parts[start:]:
                if not part[0].isupper():
                    continue
                if is_allowed_capital(part):
                    continue
                if part in PROTECTED_WORDS:
                    continue
                bad.append(part)
    return bad


def main(argv):
    root = argv[1] if len(argv) > 1 else "RESEARCH-COUNCIL/OUTPUT"
    paths = sorted(glob.glob(os.path.join(root, "*.md")))
    if not paths:
        print(f"no markdown files under {root}", file=sys.stderr)
        return 2
    checked = 0
    failures = []
    for path in paths:
        fenced = False
        with open(path, encoding="utf-8") as handle:
            for lineno, line in enumerate(handle, 1):
                if FENCE.match(line):
                    fenced = not fenced
                    continue
                if fenced:
                    continue
                match = HEADING.match(line.rstrip("\n"))
                if not match:
                    continue
                body = match.group(2)
                checked += 1
                if "[DEEP DIVE" in body:
                    continue
                bad = violations(body)
                if bad:
                    failures.append(f"{path}:{lineno}: {', '.join(bad)} | {body}")
    if failures:
        print(f"Title Case headings in {root} ({len(failures)}):", file=sys.stderr)
        for failure in failures:
            print(f"  {failure}", file=sys.stderr)
        return 1
    print(f"heading case ok: {checked} headings checked in {len(paths)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))