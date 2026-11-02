#!/usr/bin/env bash
# The one gate. `.githooks/pre-commit` and `.github/workflows/docs-gate.yml`
# both call this file, so the local and CI definitions of "verified" cannot
# drift apart: docs style, the tool witness tests, and the state-machine
# probes, in that order.
set -euo pipefail

cd "$(dirname "$0")/.."

python3 tools/check_docs.py
python3 -m unittest discover -s tests/unit
python3 tools/probe_state_machines.py
