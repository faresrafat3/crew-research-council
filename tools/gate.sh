#!/usr/bin/env bash
# The one definition of "verified": the docs gate, the witness tests for both
# tools, and the generated board's freshness. `.githooks/pre-commit` and
# `.github/workflows/docs-gate.yml` both call this script, so a green hook and a
# green CI run mean the same three checks instead of two different ones.
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

python3 tools/check_docs.py
python3 -m unittest discover -s tests/unit
python3 tools/gen_leaderboard.py --check
