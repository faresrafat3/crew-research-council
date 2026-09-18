#!/bin/bash
# Fixed run recipe (Round 0 contract): stdlib only, no network, no third-party installs.
# Rebuilds nothing from the session env; the snapshot carries all code.
# Prints unit-test results, then the blind evaluation with its SUMMARY block.
set -u
python3 -m unittest discover -s tests -v
python3 -m crew.eval --tasks tasks/real-missions.json --formation solo
