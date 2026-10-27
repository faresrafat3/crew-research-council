#!/usr/bin/env python3
"""Gate: docs style for the research tree.

Three rules, one command — the pre-commit hook and CI both run this:

1. Headings in RESEARCH-COUNCIL/OUTPUT/*.md are sentence case. Acronyms,
   tool names and proper nouns are allowed; [DEEP DIVE] marker headings are
   skipped because STATUS.md greps for that literal.
2. The two READMEs (RESEARCH-COUNCIL/README.md and its OUTPUT/README.md)
   carry no prose em dash, no bold and no emoji — outside fenced blocks and
   code spans.
3. Backticked .md references in those READMEs resolve, relative to the file
   or under RESEARCH-COUNCIL/OUTPUT/.

Usage: python3 tools/check_docs.py [output-directory]
"""

import glob
import os
import re
import sys

# Rule 1: heading case. ------------------------------------------------------

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


def unfenced_lines(path):
    """Yield (lineno, line) for lines outside fenced code blocks."""
    fenced = False
    with open(path, encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, 1):
            if FENCE.match(line):
                fenced = not fenced
                continue
            if fenced:
                continue
            yield lineno, line


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


# Rules 2 and 3: the cleaned READMEs. ----------------------------------------

RC = "RESEARCH-COUNCIL"
OUTPUT = os.path.join(RC, "OUTPUT")
CLEAN_READMES = (os.path.join(RC, "README.md"), os.path.join(OUTPUT, "README.md"))

EMOJI = re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF]")
REF = re.compile(r"`([^`\n]+\.md)`")


def prose_issues(path):
    """Em dash, bold and emoji found outside fenced blocks and code spans."""
    issues = []
    for lineno, line in unfenced_lines(path):
        stripped = CODE_SPAN.sub("code", line)
        excerpt = line.strip()[:70]
        if "—" in stripped:
            issues.append((lineno, "em dash", excerpt))
        if "**" in stripped:
            issues.append((lineno, "bold", excerpt))
        if EMOJI.search(stripped):
            issues.append((lineno, "emoji", excerpt))
    return issues


def ref_check(path):
    """(resolved count, issues): backticked .md references with no target file."""
    issues = []
    resolved = 0
    base = os.path.dirname(path)
    for lineno, line in unfenced_lines(path):
        for ref in REF.findall(line):
            if any(ch in ref for ch in "<>* "):
                continue
            candidates = (
                os.path.normpath(os.path.join(base, ref)),
                os.path.normpath(os.path.join(OUTPUT, ref)),
            )
            if any(os.path.exists(candidate) for candidate in candidates):
                resolved += 1
            else:
                issues.append((lineno, "ref", ref))
    return resolved, issues


def main(argv):
    root = argv[1] if len(argv) > 1 else OUTPUT
    paths = sorted(glob.glob(os.path.join(root, "*.md")))
    if not paths:
        print(f"no markdown files under {root}", file=sys.stderr)
        return 2

    headings = 0
    failures = []
    for path in paths:
        for lineno, line in unfenced_lines(path):
            match = HEADING.match(line.rstrip("\n"))
            if not match:
                continue
            body = match.group(2)
            headings += 1
            if "[DEEP DIVE" in body:
                continue
            bad = violations(body)
            if bad:
                failures.append(
                    f"{path}:{lineno}: heading case | {', '.join(bad)} | {body}"
                )

    readmes = 0
    refs = 0
    for path in CLEAN_READMES:
        if not os.path.exists(path):
            failures.append(f"{path}: missing | the cleaned README is gone")
            continue
        readmes += 1
        for lineno, rule, detail in prose_issues(path):
            failures.append(f"{path}:{lineno}: {rule} | {detail}")
        resolved, issues = ref_check(path)
        refs += resolved
        for lineno, rule, detail in issues:
            failures.append(f"{path}:{lineno}: {rule} | {detail}")

    if failures:
        print(f"docs gate: {len(failures)} problems", file=sys.stderr)
        for failure in failures:
            print(f"  {failure}", file=sys.stderr)
        return 1
    print(
        f"docs gate ok: {headings} headings in {len(paths)} files; "
        f"{readmes} READMEs clean; {refs} refs resolve"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
