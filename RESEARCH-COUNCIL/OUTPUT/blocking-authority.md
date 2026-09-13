# Blocking Authority and Governance

## Executive Summary
Tester holds a hard-bounded veto: 8 machine-checkable HOLD/ROLLBACK conditions only. An explicit out-of-scope (MUST-NOT) list prevents overreach into style, scope, or ambiguity disputes. Appeal is once to critic tie-break, then to human with a full evidence package [Priygop 2026]. Code-layer vetoes (failing tests, gates, oracle violations) are absolute; semantic disagreements escalate rather than block [QABattle 2025]; any tester–critic disagreement triggers human review [IJECS 2026]. Thresholds calibrate quarterly on false-positive and escape rates to hold trust.

## Key Findings
1. **Code-layer vetoes are absolute:** failing pytest, missing RED log, oracle violation, or gate breach = HOLD/ROLLBACK with no discretion [QABattle 2025].
2. **Policy engine verdicts are five-state:** pass / fail / warn / review / inconclusive — only fail blocks; warn/review route to critic, inconclusive reruns [Priygop 2026].
3. **Consensus HITL keeps safe auto-fix:** agreed tester+critic PROMOTE ships; any split requires human; low-risk fixes auto-apply with audit [ArXiv 2026].
4. **PROMOTE/HOLD/ROLLBACK validated at scale:** 38 runs across 20 releases show three-state verdicts cut escapes vs binary pass/fail [ArXiv 2026].
5. **Escalation ladder is fixed:** tester → critic rerun → human with logs/diff/thresholds/options A/B/C; one appeal per task [Priygop 2026].
6. **Gatekeeper bottleneck is the top abuse mode:** unbounded testers blocking 50%+ on preference erode trust and invite bypass [Medium 2025].
7. **Requirement text beats code as oracle:** tester writes from REQ-IDs without reading implementation; independent oracle catches tautologies [Eleks 2025].
8. **Healers must classify before fixing:** environment vs logic vs flake vs oracle failure determines rerun / HOLD / ROLLBACK, not blind retry [IJECS 2026].
9. **False-positive erosion is real:** overturned-block rate >5% destroys developer trust faster than escapes do; tighten FP tracking [ArizenAI 2025].
10. **Healed-test capture is collusion:** engineer-written weak tests rubber-stamped by tester yield 100% coverage with single-digit mutation; mutation gate + critic rerun required [QABattle 2025; ArXiv 2025].

## Detailed Analysis

### MUST-Block: 8 Machine-Checkable Conditions
1. **No RED log** — tester never produced a failing-first run; no proof the test can catch anything.
2. **pytest fail** — any blocking-suite failure on current diff.
3. **Coverage/mutation below threshold** — line/branch coverage or mutation score under TEST-POLICY.md floor (default 80%/70%).
4. **Req-coverage <90% on FULL tasks** — fewer than 90% of mapped REQ-IDs exercised by at least one blocking test.
5. **Oracle violation** — test asserts implementation behavior contradicting REQ text, or oracle separation breached (test derived from code).
6. **Unresolved PBT/mutant survivor** — property-based counterexample open, or non-equivalent mutant survives blocking suite.
7. **Blocking-suite flake** — same commit yields pass+fail across reruns; HOLD until quarantined or fixed (max 3 reruns / 15 min).
8. **E2E cap / live breach** — E2E time budget exceeded, or test touched live/production resource.

Any one = HOLD (fixable in place) or ROLLBACK (implementation must revert). Tester cites condition number + log line.

### MUST-NOT Block (Out of Scope)
- **Style / formatting / naming** — warn only, never block.
- **Out-of-scope performance** — no REQ/SLO cited → warn, not HOLD.
- **Scope disputes** — "should this feature exist" goes to human, not tester veto.
- **Ambiguous requirement** — ask for clarification (review/inconclusive), do not HOLD.
- **Infra outage** — CI provider down, network partition, expired secret → inconclusive + rerun, never fail.

### Appeals: One + Critic Rerun + Human
1. Engineer files **one appeal** per HOLD/ROLLBACK with counter-evidence.
2. Critic performs **independent rerun** (no tester rationale read) and tie-breaks.
3. If critic–tester split, escalate to **human with evidence package**: full logs, diff, threshold table, and options A/B/C (promote / hold-fix / rollback) [Priygop 2026].
4. Human decision is final and recorded as **KB precedent**; tester SOUL patched if precedent changes interpretation.

### Governance Precedent
- Every human ruling enters the KB with REQ-IDs, condition cited, FP/escape context.
- SOUL patch versioned in TEST-POLICY.md; precedent application lag target = 0 (next run applies it).
- Quarterly calibration on FP rate (>5% loosen) and escape rate (>1/10 tighten) [IJECS 2026; ArizenAI 2025].

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

## Practical Recommendations

| Situation | Action | Owner | Evidence to Attach |
|-----------|--------|-------|-------------------|
| Tester wants to HOLD | Cite 1 of 8 MUST-block conditions with log line + threshold | Tester | RED log / pytest output / coverage + mutation report |
| Style / perf nit, no REQ | Emit warn, PROMOTE with note; never HOLD | Tester | REQ-ID search showing no match |
| Ambiguous REQ | Return review/inconclusive + clarification question | Tester | Quoted REQ text + two readings |
| Infra outage / flake suspected | Mark inconclusive, rerun ≤3× / 15 min, then quarantine | Tester | Rerun matrix (pass/fail per run) |
| Engineer disagrees | One appeal → critic independent rerun → human on split | Engineer → Critic → Human | Counter-evidence + diff + threshold table |
| Tester–critic split | Escalate to human with options A/B/C | Critic | Both verdicts + logs + options memo |
| Human ruling | Record KB precedent, patch SOUL / TEST-POLICY.md | Human | Precedent ID + version bump |
| FP >5% or escape >1/20 | Quarterly calibration ±5% thresholds, human approves >10% | Maintainer | FP/escape/appeal ledger |

## Metrics
- **Block rate:** 10–30% early in rollout, falling as quality stabilizes; >50% = too strict, <5% = rubber stamp.
- **Appeal rate:** <5% of HOLD/ROLLBACK verdicts appealed.
- **False-positive rate:** <2% of blocks overturned by human (loosen at >5%).
- **Escape rate:** <1 per 20 FULL tasks PROMOTED (tighten at >1/10).
- **Verdict latency:** <5 min from diff-ready to tester verdict (excluding E2E cap).
- **Precedent lag:** 0 — next run after a human ruling applies the KB precedent.

## References
1. [Priygop 2026] — Escalation frameworks: one-appeal rule, critic tie-break, evidence package (logs/diff/thresholds/options A/B/C).
2. [QABattle 2025] — Layered LLM evaluation: absolute code-layer vetoes, independent oracle, healed-test capture.
3. [IJECS 2026] — Detect-Fix-Learn loop: tester–critic disagreement → human, model diversity, FP/escape calibration.
4. [ArXiv 2026] — Oversight capacity + 38 runs / 20 releases: PROMOTE/HOLD/ROLLBACK validation, fatigue model, safety-optimal escalation below full.
5. [Medium 2025] — Quality assistance: gatekeeper bottleneck, structural tester–engineer conflict.
6. [Eleks 2025] — Independent oracle: requirement text over code, tautology detection, oracle separation.
7. [ArizenAI 2025] — End of determinism: FP erosion of trust, rubber-stamp detection, escape tracking.
