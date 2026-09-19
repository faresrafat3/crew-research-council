#!/bin/bash
# Fixed run recipe (Round 0 contract): stdlib only, no network, no third-party installs.
# Rebuilds nothing from the session env; the snapshot carries all code.
# Prints unit-test results, then the blind evaluation with its SUMMARY block.
# Variant selection comes from variant.json on the branch (same command string
# on every node; only versioned code/config differs).
set -u
python3 -m unittest discover -s tests -v
python3 -m crew.eval --tasks tasks/real-missions.json $(python3 -c "
import json
try:
    v = json.load(open('variant.json'))
except FileNotFoundError:
    v = {}
parts = ['--formation', v.get('formation', 'solo')]
if v.get('hold_on_vague'): parts.append('--hold-on-vague')
if v.get('checklist'): parts.append('--checklist')
if v.get('verifier_override'): parts.append('--verifier-override')
if 'shuffle_seed' in v: parts += ['--shuffle-seed', str(v['shuffle_seed'])]
print(' '.join(parts))
")
# REPRO stage (present only on branches carrying repro/): isolated venv with
# torch+transformers, then the paired micro-benchmark. Stdlib stages above are
# unaffected.
if [ -d repro ]; then
  if [ ! -d venv ]; then
    python3 -m venv venv
    # --extra-index-url (not --index-url): PyTorch wheels come from the CUDA
    # index while everything else still resolves from PyPI. A single
    # --index-url replaces the index for ALL packages and breaks the install.
    venv/bin/pip install -q torch --extra-index-url https://download.pytorch.org/whl/cu126 transformers 2>&1 | tail -n 1
  fi
  venv/bin/python repro/run_repro.py
fi
