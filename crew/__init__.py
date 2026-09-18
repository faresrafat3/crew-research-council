"""Anatomy-lab crew v2 baseline: router + executor + reviewer.

REVIEW-02 compliant: start smallest (executor+reviewer), roster as library,
constitution (crew/) split from harness (harness/).
"""

from .router import propose_formation, FORMATIONS
from .roles import run_executor, run_reviewer, run_researcher

__all__ = ["propose_formation", "FORMATIONS", "run_executor", "run_reviewer",
           "run_researcher"]
