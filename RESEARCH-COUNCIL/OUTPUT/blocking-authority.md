## [DEEP DIVE]: Real-World Tester Blocking Abuse, Calibration, Escalation Time, and Collusion

### 1. Real-World Examples of Tester Blocking Abuse

**Pattern 1: The Overly Strict Gatekeeper** [Medium, 2025]
- Symptom: Tester blocks 50%+ of tasks on style preferences, out-of-scope performance, or ambiguous requirements.
- Consequence: Engineer spends more time appealing than developing. Trust erodes. "Just skip the tester" workarounds appear.
- Root cause: Tester SOUL lacks MUST-NOT list. Tester treats all opinions as block-worthy.
- Fix: Closed block list (8 conditions) + MUST-NOT list (style, scope, ambiguity, outages).

**Pattern 2: The Rubber Stamp** [ArizenAI, 2025]
- Symptom: Tester PROMOTES 100% of tasks. Zero HOLDs. Zero ROLLBACKs.
- Consequence: Bugs reach production. Tester is decorative.
- Root cause: Tester SOUL lacks blocking authority or fear of conflict.
- Fix: Escape rate tracking. If escapes > 1/20, tighten tester SOUL. Add mutation gate.

**Pattern 3: The Veto War** [Priygop, 2026]
- Symptom: Engineer appeals every HOLD. Critic sides with engineer. Tester appeals to human. Deadlock.
- Consequence: Human spends hours resolving testing disputes.
- Root cause: No appeal limit. No evidence requirements.
- Fix: One-appeal rule with evidence package. Critic tie-break. Human only on split.

**Pattern 4: The Capture** [QABattle, 2025]
- Symptom: Tester and engineer collude: engineer writes weak tests, tester approves them. Both optimize for "green" not "correct."
- Consequence: 100% coverage, 4% mutation score, bugs in production.
- Root cause: No independent oracle. No mutation gate. No critic review.
- Fix: Oracle separation (tester writes tests, not engineer). Mutation gate. Critic independent rerun.

**Pattern 5: The Fatigue Model** [arXiv, 2026 — Oversight Has a Capacity]
- Symptom: Human reviewer rubber-stamps escalations because too many arrive.
- Consequence: Escalations become meaningless. Real bugs slip through.
- Root cause: Tester escalates too frequently (low threshold).
- Fix: Calibrate escalation rate. Safety-optimal escalation is below full escalation. Monitor reviewer workload.

### 2. Calibrating Tester Strictness Automatically

**Calibration signals** [IJECS, 2026; KnowMBA, 2025]:

| Signal | What It Measures | How to Adjust |
|--------|------------------|---------------|
| **False-positive rate** | Blocks that human overturned | >5%: loosen thresholds by 5% absolute |
| **Escape rate** | Bugs shipped despite PROMOTE | >1/10: tighten thresholds by 5% absolute |
| **Appeal success** | Engineer appeals that overturned | >5%: loosen; <1%: tighten |
| **Block rate** | HOLD+ROLLBACK / total verdicts | >50%: too strict; <5%: too lenient |
| **Coverage/mutation gap** | False confidence | >20%: tighten mutation gate |
| **Reviewer workload** | Escalations per week | >5/week: raise escalation threshold |

**Automatic calibration algorithm:**
```
quarterly_calibration():
  fp_rate = overturned_blocks / total_blocks
  escape_rate = escapes / FULL_tasks
  appeal_success = overturned_appeals / total_appeals
  
  if fp_rate > 0.05:
    coverage_threshold -= 5  # loosen
    mutation_threshold -= 5
  if escape_rate > 0.1:
    coverage_threshold += 5  # tighten
    mutation_threshold += 5
  if appeal_success > 0.05:
    coverage_threshold -= 5
  if appeal_success < 0.01:
    coverage_threshold += 5
  
  # Clamp to industry benchmarks
  coverage_threshold = clamp(coverage_threshold, 70, 95)
  mutation_threshold = clamp(mutation_threshold, 60, 90)
  
  log_adjustment(fp_rate, escape_rate, appeal_success, new_thresholds)
```

**Calibration governance:**
- Adjustments are logged to ledger with evidence.
- Human approves adjustments > 10% absolute.
- Adjustments are versioned in TEST-POLICY.md.

### 3. Optimal Escalation Time

**Evidence-based escalation timeouts** [Priygop, 2026; arXiv, 2026]:

| Escalation Type | Optimal Timeout | Maximum | Rationale |
|-----------------|-----------------|---------|-----------|
| Tester RED not received | 15 min | 30 min | Tester should write RED in one shot; if stuck, escalate |
| Engineer GREEN not received | 30 min | 60 min | Engineer needs time to implement; but not too long |
| Critic review not received | 10 min/file, 30 min/task | 60 min | Critic is read-only; should be fast |
| Human escalation response | 4 hours | 24 hours | Human attention is finite; 4h is the fatigue threshold [arXiv, 2026] |
| Flake rerun cycle | 5 min per rerun | 15 min total | Flake detection should be fast |
| Appeal response | 2 hours | 8 hours | Appeal is one-shot; should be quick |

**Fatigue model insight** [arXiv, 2026]:
- Human reliability declines as cumulative escalation load grows.
- Safety-optimal escalation rate is below full escalation.
- If human receives > 5 escalations/week, they start rubber-stamping.
- Solution: raise escalation threshold so only truly ambiguous cases reach human.

**Escalation budget:**
- Target: < 5 human escalations per week.
- If exceeded: raise tester confidence threshold by 5%.
- If zero for 4 weeks: lower threshold by 5% (may be too lenient).

### 4. Handling Tester-Critic Collusion

**Collusion scenarios:**

| Scenario | Detection | Prevention |
|----------|-----------|------------|
| Tester and engineer agree on weak tests | Mutation survivors > 10% | Mutation gate catches weak assertions |
| Tester and critic are same model | Model ID check | Use different model families for tester vs critic |
| Tester and critic both miss same bug | Drill pass < 100% | Break drills catch what point tests miss |
| Tester writes test, critic uses same oracle | Oracle separation | Tester writes from REQ only; critic reruns independently |

**Anti-collusion measures:**

1. **Oracle separation** [Eleks, 2025]: Tester writes tests from REQ-IDs only, never reads implementation code. Critic reruns tests without reading tester's rationale.
2. **Model diversity** [IJECS, 2026]: Use different model families for tester and critic (e.g., tester = Claude, critic = GPT). Disagreement triggers human review.
3. **Mutation gate** [ArXiv, 2025]: Independent of both tester and critic. Catches weak assertions regardless of collusion.
4. **Drill pass** [KnowMBA, 2025]: Break each REQ independently. If both tester and critic miss a break, the drill catches it.
5. **Audit sampling**: Human reviews 5% of PROMOTED tasks randomly. If audit finds bug, both tester and critic are recalibrated.

**Collusion detection metrics:**
- If tester-critic agreement rate > 99%: suspicious. Normal is 90-95%.
- If mutation survivors = 0 AND drill pass < 100%: likely collusion.
- If appeal success = 0% AND block rate > 30%: likely over-strictness or collusion.

**References for deep dive:**
- [Medium, 2025] Quality Assistance: gatekeeper bottleneck, structural conflict
- [ArizenAI, 2025] The End of Determinism: rubber-stamp detection, FP erosion
- [Priygop, 2026] Escalation Frameworks: veto wars, evidence requirements
- [QABattle, 2025] Layered LLM Evaluation: capture, independent oracle
- [arXiv, 2026] Oversight Has a Capacity: fatigue model, optimal escalation rate
- [IJECS, 2026] Detect-Fix-Learn Loop: model diversity, calibration
- [KnowMBA, 2025] Test Automation Strategy: drill pass, 14-day SLA
- [Eleks, 2025] Independent Oracle: oracle separation, tautology detection
- [ArXiv, 2025] MutGen: mutation gate catches weak assertions
- [TMMi Foundation, 2018] Level 5: calibration, process optimization

---

## [DEEP DIVE (freebuff, pass 2, 2026-09-14)]: Audit Sampling Mathematics — How Many Verdicts to Review and What the Sample Can Prove

Pass-1 anti-collusion measure #5 says: "Human reviews 5% of PROMOTED tasks randomly." It names no sample size, no confidence level, and no detection claim — and that gap matters, because the human audit is the only layer that can catch collusion *between* the machine gates (§4's other defenses each assume at least one uncorrupted component). An undersized audit delivers false assurance, which is worse than no audit: it is rubber-stamping with an alibi.

### B1. The c=0 zero-acceptance plan: deriving n

For attribute sampling with zero tolerated bad verdicts, the sample size needed to have confidence C of catching at least one bad verdict when the true bad rate is p is:

```
n = ln(1 − C) / ln(1 − p)
```

This is the standard c=0 acceptance-sampling plan (zero-nonconformity plans); LTPD-style plans and OC curves are the classical framing [NIST/SEMATECH Engineering Statistics Handbook; NCSS c=0 procedure; variation.com]. Evaluation is attribute-style: a sampled verdict is either validated or defective — no partial credit.

**Derived sample sizes at 95% confidence:**

| True bad-verdict rate p | Required n = ln(0.05)/ln(1−p) |
|---|---|
| 10% | 29 |
| 5% | 59 |
| 2% | 149 |
| 1% | 299 |

### B2. What a 5% sample actually detects

The pass-1 "5% of PROMOTEs" rule scales n with volume: 200 quarterly PROMOTEs → n=10 sampled verdicts. Detection probability for a true bad rate p is 1−(1−p)^n:

| True rate p | Detection probability (n=10) |
|---|---|
| 10% | 65% |
| 5% | 40% |
| 2% | 18% |

A 5% sample leaves a 5%-rate collusion undetected **60% of the time**. The fix is not sampling *more of everything* (B4) but sampling to a *stated claim*: the operator should pick the worst tolerable collusive/defective verdict rate and review the c=0-derived n. Recommendation: "95% confidence of detecting collusion affecting ≥5% of verdicts" → **n=59 per quarter**, volume-independent.

### B3. Rule of three: reading a clean sample

When the audit finds zero defects in n sampled verdicts, the 95% upper bound on the bad rate is ≈ 3/n (rule of three). A clean 59-verdict audit certifies a bad rate below ~5.1% — no better. This bounds what calibration can conclude from audit data: pass-1's §2 calibration algorithm moves thresholds on FP signals, but a *clean sample* is absence of evidence, not evidence of absence; threshold moves justified only by audit cleanliness should be conservative (the ±5% clamp already encodes this).

### B4. Stratify before you randomize

Uniform random sampling spends n on high-volume trivial verdicts. Stratify the quarterly plan by information value:
1. **Appeal-overturned blocks** — oversample 3×; an overturned block is already half a collusion signal (§1 Pattern 3).
2. **FULL formation verdicts** — highest blast radius; every FULL PROMOTE in the quarter should be *eligible* with elevated selection weight.
3. **New-module or new-agent verdicts** — fresh failure surfaces.
4. **Maintenance verdicts** — lowest weight.

Stratified attribute sampling is standard audit practice; the AQL/OC-curve machinery applies per stratum [SixSigma.us attribute sampling; NIST/SEMATECH].

### B5. Audit cadence and the fatigue budget

Pass-1's fatigue model (Pattern 5: >5 escalations/week degrades human review) applies to the audit itself: 59 verdicts/quarter ≈ 5/week of *audit* review on top of escalations. Two mitigations keep the audit inside the attention budget: batch the audit into one weekly 60-minute session (5 verdicts × ~10 min evidence review, verdict evidence is machine-fetched by the auditor agent), and rotate auditors if more than one human operator exists. If the audit backlog grows, reduce scope by *tightening p* honestly (declare a 10% detection target → n=29) rather than silently skimming the sample — a silently skimmed audit is Pattern 2 (the rubber stamp) wearing an auditor's badge.

### Numbers for calibration (pass 2)

| Quantity | Value | Source |
|---|---|---|
| n for 95% confidence @ p=5% | 59 | c=0 plan, derived [NIST/SEMATECH] |
| n for 95% confidence @ p=1% | 299 | same |
| 5%-sample (n=10) detection of 5% rate | 40% (1−0.95¹⁰) | derived |
| Clean-sample upper bound (rule of three) | ≈3/n | [NCSS; standard] |
| Pass-1 audit rule, revised | fixed-n c=0 stratified plan, not 5% volume share | this dive |
| Audit load at n=59 | ~5 verdicts/week | derivation |

### References (pass 2)
1. [NIST/SEMATECH] Engineering Statistics Handbook, §7.2.2 "Lot Acceptance Sampling Plans" — LTPD, OC curves. https://www.itl.nist.gov/div898/handbook/pmc/section2/pmc22.htm [verified: 2026-09-14]
2. [NCSS] "Acceptance Sampling for Attributes with Zero Nonconformities" (c=0 plans). https://www.ncss.com/wp-content/themes/ncss/pdf/Procedures/PASS/Acceptance_Sampling_for_Attributes_with_Zero_Nonconformities.pdf [verified: 2026-09-14, doc page]
3. [variation.com] "Selecting Statistically Valid Sampling Plans" — AQL, 95% acceptance mechanics. https://variation.com/selecting-statistically-valid-sampling-plans/ [verified: 2026-09-14, snippet]
4. [SixSigma.us] "How Attribute Sampling Works" — AQL, OC curves, plan selection. https://www.6sigma.us/six-sigma-in-focus/attribute-sampling/ [verified: 2026-09-14, snippet]
5. Cross-refs: blocking-authority.md pass 1 §2 (calibration algorithm), §4 (anti-collusion), Pattern 5 (fatigue); tester-soul.md cycle 4 (escape-classification).
