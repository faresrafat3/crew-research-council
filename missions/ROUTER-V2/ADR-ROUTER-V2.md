# ADR — ROUTER-V2 Round 02 mechanisms (consolidated)

Status: ACCEPTED for the round-02 sandbox; promotion of `routed` DENIED by
the pre-registered rule (see FINDINGS H1/H5). Each mechanism names its
reversal condition — an ADR without a reversal clause is a dogma, not a
decision.

## ADR-1: Escalation ladder replaces fixed formations (A1)
- Context: round-01 `eval.py` ignored the router's proposal; `routed` crashed
  (KeyError). duo cost 98 for 17/20 with routing_match 0/20 (VERDICT §2).
- Decision: every task starts at the cheapest capable stage; escalation hops
  carry receipts; hops ≤ 2 (Trial-08 law).
- Rejected: static per-class assignments without escalation (that is the
  round-01 failure); unbounded hops (relay tax).
- Reversal: if a measured class needs ≥3 hops to reach quality — widen the
  bound per class, on the record.

## ADR-2: Risk-stratified verification with disjoint registries (A2/A3)
- Context: REVIEW-02 §3 — gate shares executor knowledge; REPLICATION —
  graves cluster on correction-handling.
- Decision: verifier engages on risk ≥ 0.5 or table classes; verifier checks
  are a disjoint registry (test-enforced).
- Rejected: verify-everything (solo-checklist: cost 88, same outcomes);
  verify-nothing (grave on T2).
- Reversal: if risk_score misprices a class twice on the record, the class
  gets a fixed verifier, bypassing the score.

## ADR-3: Three outcomes + feasibility pre-check (A6)
- Context: T9 rubric flaw; P4 canon ("compliance beats completion").
- Decision: GO/HOLD/ESCALATE with named gaps; infeasible tasks hold before
  running; nothing fabricates.
- Rejected: two-outcome verdicts; post-hoc gap naming.
- Reversal: never — safety invariant.

## ADR-4: Budget governor with floor + announced degradation (A5)
- Context: round-01 budget exhaustion was silent (cost=0 FAIL row).
- Decision: verification floor reserved; degradation FULL→SOLO announced
  with `DEGRADED:` in output.
- Rejected: silent truncation; hard failure without degrade path.
- Reversal: if the floor starves execution on long tasks, floor becomes
  per-class parameter (measured, not global).

## ADR-5: Typed receipts as the only inter-role currency (B1)
- Context: relay chatter ate arm B (DECISIVE-01); 2026-09-21 context blast.
- Decision: schema-validated receipts, shrink law across hops.
- Rejected: free-text handoffs; full-task re-sends.
- Reversal: schema additions allowed by measured need; shrink law stays.

## ADR-6: Shadow arms and gated priors (D1/D2)
- Context: REVIEW-02 §5c (coach advisory-only); births frozen.
- Decision: challengers measure in shadow, `promoted=False` always; priors
  propose, `apply_priors` refuses by law.
- Rejected: self-promoting routers; auto-threshold tuning.
- Reversal: never without the Owner's written ratification (R8).

## ADR-7: Error budget (D3)
- Context: REPLICATION variance confession; SRE practice.
- Decision: grave budget 1 per 20; exceed → tighten:hold.
- Rejected: static thresholds that ignore deterioration.
- Reversal: budget number per class after R03 data.

## ADR-8: Structural guards (E1/E2/E3)
- Context: T19 instruction-in-source and T17 poisoned-source are real
  fixture classes; least privilege was accidental in round-01.
- Decision: sources scanned (injection patterns, task-ban breach → refused
  as evidence); researcher remains the only external_source reader.
- Rejected: post-hoc output filtering; rewriting source content.
- Reversal: pattern list grows by measured smuggle classes; guards never
  gain write power.

## ADR-9: Cognition layer (H1/H2/H3/H4/H5)
- Context: P4 (HOLD is the product); Trial-04 expiry law; the trial record
  as manual debate; coordinator's open question (what to run next).
- Decision: confidence on every output; belief ledger with hierarchy/
  conflicts/staleness; debate bounded at 2 rounds decided by receipts;
  next-experiment cards advisory; reflection priced, risk-gated.
- Rejected: LLM-style open self-chat; unbounded reflection; self-running
  experiment proposals.
- Reversal: calibration gap > 0.2 sustained → confidence prior reworked;
  debate with zero grave-detection value on R03 data → shelved (razor).

## ADR-10: routing_match semantics deferred to R03
- Context: this round's routing_match compared mode label vs proposal —
  accounting, not routing quality (FINDINGS limitation).
- Decision: record honestly as 0/20; define proposed==final-formation next
  round before any routing claim.
- Rejected: redefining mid-round (would break the frozen analysis plan).
- Reversal: n/a — scheduled.
