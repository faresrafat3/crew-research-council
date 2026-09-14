# Gate Toolkit — Executable Pass-2 Protocols

## Executive Summary

The pass-2 deep dives specified gates and statistics; this output makes them **runnable**. `gate_toolkit.py` implements five protocols (c=0 audit sampling, zero-flip flake gate, RTS safety KPI, p-chart limits, Nelson run rules with baseline lock) in dependency-free stdlib Python. The accompanying suite (35 tests) achieves a **100% mutation score** against a 15-mutant curated harness — beating the council's own mutation gate (70% PR / 80% nightly, tester-soul.md cycle 4 D6-D7). The gap between "specified" and "executable" is where protocols get skipped; this closes it (the COORD lesson, applied to the council itself).

## Provenance: function → deep dive → external source

| Function | Implements | Deep dive | External standard |
|---|---|---|---|
| `sample_size_c0(p, C)` | Audit plan: n = ln(1−C)/ln(1−p), ceil | blocking-authority.md pass 2 §B1 (n=59 @ 95%/5%) | NIST/SEMATECH e-Handbook §7.2.2; NCSS c=0 plans |
| `detection_probability(n, p)` | 1−(1−p)^n; n=10@5% → 40.13% | blocking-authority.md pass 2 §B2 | same |
| `rule_of_three(n, C)` | Exact bound 1−(1−C)^(1/n); ≈3/n for large n | quality-metrics.md pass 2 §Q1 ("0 flips/20 ⇒ ≤13.91%") | rule of three (classical); exact form from c=0 identity |
| `flake_gate(flips, window)` | Zero-flip blocking gate + certified bound + 14-day SLA | quality-metrics.md pass 2 §Q1 | tester-soul cycle 1 (quarantine SLA) |
| `rts_safety(sel, full)` | Safety ratio, ≥0.95 blocking else shadow | tester-soul.md pass 2 §S2 | Ekstazi/STARTS safety data (Gligorić 2015; Shin 2022) |
| `p_chart_limits(p̄, nᵢ)` | p̄ ± 3√(p̄(1−p̄)/nᵢ), clamped | quality-metrics.md pass 2 §Q1 | Oregon State EM 9110; Montgomery, ISQC ch. 7 |
| `SpcChart` (rules 1,2,3,5,6) | Individuals chart, MR̄/1.128 sigma, 20-point baseline lock, zero-variance guard | quality-metrics.md pass 2 §Q2, §Q4 | Nelson (1984) JQT 16(4); ASTM d₂=1.128 for n=2 |

## Source: `gate_toolkit.py`

```python
"""gate_toolkit.py — executable versions of the Research Council pass-2 protocols.

Every function here implements a gate or statistic specified in a pass-2 deep
dive (RESEARCH-COUNCIL/OUTPUT/*.md, freebuff, 2026-09-14). The module is
dependency-free (stdlib only) so it can run inside any agent harness or CI
runner without supply-chain surface (cicd-integration.md pass 2, S5).

Implemented protocols:
  1. c=0 zero-acceptance audit sampling ......... blocking-authority.md pass 2 (B1-B3)
  2. Zero-flip flake gate (c=0 form) ............ quality-metrics.md pass 2 (Q1)
  3. RTS safety KPI ............................ tester-soul.md pass 2 (S2)
  4. p-chart limits for varying-n rates ........ quality-metrics.md pass 2 (Q1)
  5. Nelson run rules / baseline lock .......... quality-metrics.md pass 2 (Q2, Q4)

References for the statistics:
  - NIST/SEMATECH e-Handbook 7.2.2 (LTPD, OC curves): https://www.itl.nist.gov/div898/handbook/pmc/section2/pmc22.htm
  - NCSS c=0 zero-nonconformity plans (n = ln(1-C)/ln(1-p))
  - Nelson, W.C. (1984) "The Shewhart Control Chart—Tests for Special Causes", Journal of Quality Technology 16(4)
  - Oregon State Extension EM 9110 (p-chart limits, 3-sigma)
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Iterable, Sequence


# ---------------------------------------------------------------------------
# 1. c=0 zero-acceptance audit sampling (blocking-authority.md pass 2)
# ---------------------------------------------------------------------------

def sample_size_c0(bad_rate: float, confidence: float = 0.95) -> int:
    """Sample size n needed so P(detect >= 1 bad verdict) = confidence,
    when the true bad-verdict rate is `bad_rate`.

    Derivation: P(miss) = (1-p)^n = 1-C  =>  n = ln(1-C) / ln(1-p).
    Rounded UP to the next whole verdict — you cannot sample 58.4 verdicts.
    """
    if not 0.0 < bad_rate < 1.0:
        raise ValueError(f"bad_rate must be in (0,1), got {bad_rate}")
    if not 0.0 < confidence < 1.0:
        raise ValueError(f"confidence must be in (0,1), got {confidence}")
    n = math.log(1.0 - confidence) / math.log(1.0 - bad_rate)
    return math.ceil(n)


def detection_probability(n: int, bad_rate: float) -> float:
    """P(at least one bad verdict in a sample of n) = 1 - (1-p)^n."""
    if n < 0:
        raise ValueError(f"n must be >= 0, got {n}")
    if not 0.0 <= bad_rate <= 1.0:
        raise ValueError(f"bad_rate must be in [0,1], got {bad_rate}")
    return 1.0 - (1.0 - bad_rate) ** n


def rule_of_three(n: int, confidence: float = 0.95) -> float:
    """Upper bound on the bad rate after observing ZERO defects in n samples.

    Exact (small-n, from the c=0 identity): p_max = 1 - (1-C)^(1/n).
    For C=0.95 this converges to the classical rule-of-three 3/n for large n
    (ln(0.05) = -2.996 ~ -3), but is valid at audit sample sizes where 3/n
    understates the bound (e.g. n=10: exact 0.2589 vs 3/n=0.30).
    """
    if n <= 0:
        raise ValueError(f"n must be positive, got {n}")
    if not 0.0 < confidence < 1.0:
        raise ValueError(f"confidence must be in (0,1), got {confidence}")
    return 1.0 - (1.0 - confidence) ** (1.0 / n)


# ---------------------------------------------------------------------------
# 2. Zero-flip flake gate (quality-metrics.md pass 2: "0 flips / trailing 20")
# ---------------------------------------------------------------------------

def flake_gate(flip_count: int, trailing_runs: int = 20) -> dict:
    """Blocking flake gate in verifiable c=0 form: zero flips in the window.

    Returns pass/fail plus the exact upper bound on the true flip rate that
    a clean window certifies (rule_of_three) — so a green gate states what
    it actually proved instead of implying "<1%".
    """
    if flip_count < 0:
        raise ValueError("flip_count must be >= 0")
    if trailing_runs <= 0:
        raise ValueError("trailing_runs must be positive")
    passed = flip_count == 0
    return {
        "passed": passed,
        "flips": flip_count,
        "window": trailing_runs,
        "verdict": "PROMOTE" if passed else "QUARANTINE (14-day fix/delete SLA)",
        "certified_flip_rate_upper_bound": round(rule_of_three(trailing_runs), 4),
    }


# ---------------------------------------------------------------------------
# 3. RTS safety KPI (tester-soul.md pass 2: >= 0.95 over 20 tasks before RTS
#    may gate PRs; below that, selection runs advisory/shadow only)
# ---------------------------------------------------------------------------

def rts_safety(selected_caught: int, full_run_caught: int,
               window: int = 20, threshold: float = 0.95) -> dict:
    """Regression-test-selection safety ratio and gating decision.

    safety = failures caught by selected set / failures caught by full run.
    """
    if window < 1:
        raise ValueError("window must be >= 1")
    if full_run_caught < 0 or selected_caught < 0:
        raise ValueError("caught counts must be >= 0")
    if selected_caught > full_run_caught:
        raise ValueError("selected set cannot catch more failures than the full run")
    if full_run_caught == 0:
        safety = 1.0  # no failures to catch: vacuously safe, nothing missed
    else:
        safety = selected_caught / full_run_caught
    passed = safety >= threshold
    return {
        "safety": round(safety, 4),
        "threshold": threshold,
        "window": window,
        "mode": "BLOCKING" if passed else "SHADOW (advisory only)",
        "missed_failures": full_run_caught - selected_caught,
    }


# ---------------------------------------------------------------------------
# 4. p-chart limits for varying-n rates (quality-metrics.md pass 2)
# ---------------------------------------------------------------------------

def p_chart_limits(p_bar: float, n_i: float, sigma: float = 3.0) -> tuple[float, float]:
    """Per-point 3-sigma limits for a proportion with subgroup size n_i.

    UCL/LCL = p_bar +/- sigma * sqrt(p_bar*(1-p_bar)/n_i), clamped to [0,1].
    Standard p-chart construction (Oregon State EM 9110; Montgomery, Introduction
    to Statistical Quality Control, ch. 7).
    """
    if not 0.0 <= p_bar <= 1.0:
        raise ValueError(f"p_bar must be in [0,1], got {p_bar}")
    if n_i <= 0:
        raise ValueError(f"n_i must be positive, got {n_i}")
    if sigma <= 0:
        raise ValueError(f"sigma must be positive, got {sigma}")
    half = sigma * math.sqrt(p_bar * (1.0 - p_bar) / n_i)
    return max(0.0, p_bar - half), min(1.0, p_bar + half)


# ---------------------------------------------------------------------------
# 5. Nelson run rules with 20-point baseline lock (quality-metrics.md pass 2)
#    Rule numbers follow Nelson (1984): tests 1-8.
# ---------------------------------------------------------------------------

@dataclass
class SpcChart:
    """Individuals chart over an ordered metric series with run-rule signals.

    The first `baseline` points establish the centerline and sigma; rules do
    not evaluate until the baseline is complete (baseline lock, Q4).
    """
    values: list[float] = field(default_factory=list)
    baseline: int = 20
    _center: float | None = None
    _sigma: float | None = None

    def add(self, x: float) -> list[dict]:
        """Append a point; return any run-rule signals it triggered."""
        self.values.append(float(x))
        if self._center is None:
            if len(self.values) >= self.baseline:
                self._fit_baseline()
            return []
        return self._check_point(len(self.values) - 1)

    def _fit_baseline(self) -> None:
        base = self.values[: self.baseline]
        self._center = sum(base) / len(base)
        # Individuals chart: sigma from the average moving range (MR-bar / 1.128)
        diffs = [abs(b - a) for a, b in zip(base, base[1:])]
        mr_bar = sum(diffs) / len(diffs)
        self._sigma = mr_bar / 1.128

    @property
    def center(self) -> float:
        if self._center is None:
            raise RuntimeError(f"baseline not locked ({len(self.values)}/{self.baseline} points)")
        return self._center

    @property
    def sigma(self) -> float:
        if self._sigma is None:
            raise RuntimeError(f"baseline not locked ({len(self.values)}/{self.baseline} points)")
        return self._sigma

    def _check_point(self, i: int) -> list[dict]:
        c, s = self._center, self._sigma
        v = self.values[i]
        if s == 0:
            # Degenerate baseline (constant series): any deviation is a signal.
            if v != c:
                return [{"rule": 1, "detail": "zero baseline variance; any deviation is a signal"}]
            return []
        last9 = self.values[max(0, i - 8): i + 1]   # this point + 8 prior
        last2 = self.values[max(0, i - 1): i + 1]
        last3 = self.values[max(0, i - 2): i + 1]
        last5 = self.values[max(0, i - 4): i + 1]
        signals: list[dict] = []
        # Rule 1: one point beyond 3 sigma
        if abs(v - c) > 3 * s:
            signals.append({"rule": 1, "detail": f"point {abs(v - c) / s:.2f} sigma from centerline"})
        # Rule 2: 9 consecutive points on the same side of the centerline
        if len(last9) == 9 and all(x > c for x in last9):
            signals.append({"rule": 2, "detail": "9 consecutive points above centerline"})
        if len(last9) == 9 and all(x < c for x in last9):
            signals.append({"rule": 2, "detail": "9 consecutive points below centerline"})
        # Rule 3: 6 consecutive points steadily increasing or decreasing
        if len(last6 := self.values[max(0, i - 5): i + 1]) == 6:
            inc = all(b > a for a, b in zip(last6, last6[1:]))
            dec = all(b < a for a, b in zip(last6, last6[1:]))
            if inc or dec:
                signals.append({"rule": 3, "detail": "6-point monotonic trend"})
        # Rule 5: 2 of 3 consecutive points beyond 2 sigma, same side
        if len(last3) == 3:
            hi = sum(1 for x in last3 if (x - c) / s > 2)
            lo = sum(1 for x in last3 if (x - c) / s < -2)
            if hi >= 2:
                signals.append({"rule": 5, "detail": "2 of 3 points beyond +2 sigma"})
            if lo >= 2:
                signals.append({"rule": 5, "detail": "2 of 3 points beyond -2 sigma"})
        # Rule 6: 4 of 5 consecutive points beyond 1 sigma, same side
        if len(last5) == 5:
            hi = sum(1 for x in last5 if (x - c) / s > 1)
            lo = sum(1 for x in last5 if (x - c) / s < -1)
            if hi >= 4:
                signals.append({"rule": 6, "detail": "4 of 5 points beyond +1 sigma"})
            if lo >= 4:
                signals.append({"rule": 6, "detail": "4 of 5 points beyond -1 sigma"})
        return signals


__all__ = [
    "sample_size_c0", "detection_probability", "rule_of_three",
    "flake_gate", "rts_safety", "p_chart_limits", "SpcChart",
]

```

## Verification transcript

```
$ python3 -m unittest test_gate_toolkit -v
Ran 35 tests in 0.001s
OK

$ python3 mutation_harness.py
mutations applied: 15
killed:   15
survived: 0
mutation score: 100%
```

Mutation harness design (per tester-soul cycle 4: mutants as findings, one operator per site, curated operator classes): 15 mutants spanning boundary (`ceil→floor`, `>=→>`, clamp removal), math (`**→*`, `*→+`, inverted ratio), boolean (condition inversion), number (constants 1.128, 9, 2), negation (numerator swap), string (SLA text), and void-call (guard disabling). Every mutant killed; none is an equivalent mutant (each changes observable behavior asserted by at least one test).

Test-suite quality notes (the council's own anti-tautology bar, tester-soul cycle 1 D2):
- assertions on exact documented constants (n=59, n=299, n=29; 0.4013; 0.1391; UCL 0.1962) — not self-computed from the same formula;
- cross-protocol consistency tests (flake-gate bound ≡ rule-of-three; audit plan round-trip) — the strongest anti-tautology pattern, testing functions against each other;
- boundary-inclusive assertions (RTS ≥ threshold accepts equality; rule 3 rejects flat series);
- input-validation tests on every public function (ValueError paths are asserted, not just happy paths).

## Adoption

1. Drop `gate_toolkit.py` into the crew's testing package; it imports nothing outside stdlib (supply-chain-clean per cicd-integration.md pass 2 §W5).
2. Wire `flake_gate` into the commit gate where `flake-check` runs today; wire `rts_safety` into the nightly report; feed `SpcChart` from the 16-metric ledger (baseline lock enforces the 20-point minimum automatically).
3. Recompute the quarterly audit plan with `sample_size_c0` instead of the fixed table; the function reproduces the pass-2 table exactly (asserted in tests).
4. Keep `mutation_harness.py` in CI as the gate-drill harness (testing-maturity.md pass 2 §M3): it is itself a passing adversarial drill on the toolkit.

## Limits

- `SpcChart` implements Nelson rules 1, 2, 3, 5, 6 — the subset quality-metrics.md pass 2 §Q2 specifies; rules 4, 7, 8 (oscillation, stratification) are not implemented.
- `rule_of_three` is exact for the c=0 identity, not the large-n approximation; tests pin both regimes.
- The harness mutates source text, not ASTs — equivalent-mutant risk is handled by curation, not by the undecidable general check (Meta's ACH lesson, tester-soul cycle 4 D8).

## References

1. [NIST/SEMATECH] e-Handbook of Statistical Methods §7.2.2, Lot Acceptance Sampling Plans. https://www.itl.nist.gov/div898/handbook/pmc/section2/pmc22.htm [verified: 2026-09-14]
2. [Nelson, 1984] "The Shewhart Control Chart—Tests for Special Causes," Journal of Quality Technology 16(4). [run rules 1-8]
3. [ASTM] d₂ = 1.128 for moving range of n=2 (individuals chart sigma). [standard constant]
4. [Oregon State Extension, 2023] EM 9110, Attributes Control Charts (p-chart limits). https://extension.oregonstate.edu/catalog/em-9110-statistical-process-control-part-8-attributes-control-charts [verified: 2026-09-14]
5. [Gligorić et al., 2015] Ekstazi: Lightweight Test Selection, ICSE 2015. https://users.ece.utexas.edu/~gligoric/papers/GligoricETAL15EkstaziTool.pdf [verified: 2026-09-14]
6. [Shin et al., 2022] Empirical comparison of four Java-based RTS techniques, JSS. https://www.sciencedirect.com/science/article/am/pii/S0164121221002582 [verified: 2026-09-14]
7. Council cross-refs: blocking-authority.md pass 2 (§B1-B3), quality-metrics.md pass 2 (§Q1-Q4), tester-soul.md pass 2 (§S2) and cycle 4 (D6-D8), testing-maturity-model.md pass 2 (§M3), cicd-integration.md pass 2 (§W5).
