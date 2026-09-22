# ADR-ROUTER-V2 — Round 03 (2026-09-22)

Round 03 continues the numbering of `ADR-ROUTER-V2.md` (ADR-1…ADR-10). It
closes ADR-10, which R02 explicitly deferred to this round.

## ADR-11: routing_match measures execution fidelity, per task (closes ADR-10)

- **Context:** R02 defined `routing_match` as agreement between a static mode
  label (`used=ROUTED`) and the router's proposal, so it measured nothing —
  it reported 0/20 for every ladder arm (FINDINGS R02 §Limitations, ADR-10).
- **Decision:** `routing_match` = count of tasks where `proposed` equals the
  **final formation actually executed**, with `final` derived structurally from
  the stages that ran (`meta`→FULL, else `researcher`→PIPELINE, else
  `verifier`→DUO, else SOLO). A ladder grounding hop appends a `researcher`
  stage, so an under-proposing router is visible in the metric. Mismatches are
  printed per task with a reason (`escalated:research-hop`, `risk-verifier`)
  and counted per class in the ledger.
- **Evidence:** R03 trial log, frozen block (`routing_match` 11/20 solo,
  19/20 table arm, 11/20 ablation) and expanded block (23/46, 44/46, 25/46);
  H10 confirmed the fix reproduced R02's published solo value (11/20).
- **Consequence measured the same round:** the metric's winner is the deleted
  class table (44/46 vs 25/46) while buying zero additional resolved
  deliveries. The metric is therefore **diagnostic** — it reports how well the
  proposal predicted the task's final shape, and it may not be used as a
  promotion bar (new P11).
- **Rejected:** keeping `used` as the mode label and reporting the mismatch in
  prose (unmeasurable); comparing proposal to a hand-written expectation map
  (the R02 proxy test — replaced).
- **Reversal:** if a future round shows mismatch count predicting cost or
  graves at a useful effect size, it may be promoted from diagnostic to a
  secondary endpoint — with a pre-registered bar, on new data.

## ADR-12: the class table is cut (H13 KILL)

- **Context:** R02 refuted H5, but its counter-arm ran no ladder (hops=0), so
  the refutation could not stand. R03 pre-registered a re-trial on a 46-task
  fixture with a real ablation and a four-clause keep rule.
- **Decision:** **delete `CLASS_TABLE`** from `crew/router.py`. The frozen
  threshold scorer becomes the only proposal source; `route()` loses the
  `use_table` switch (a dead switch would be the same unused mechanism the
  razor just removed). The escalation ladder, the risk-stratified verifier and
  `risk_score` stay. `routed` and `routed-thresholds` remain as arm names and
  are now aliases, so R02/R03 logs stay reproducible by name.
- **Evidence (all generated in `logs/r03-analysis.md`):** passed 46 vs 46;
  grave 0 vs 0; resolved 23 vs 23 (clause c FAIL); resolved/call 0.07492 vs
  0.07877 (clause d FAIL); cost 307 vs 292. Per-class: the table wins three
  fetch classes and loses three ungroundable classes, netting +15 calls for no
  resolved gain. On the frozen fixture it also paid more (127 vs 122) for the
  same 9 resolved.
- **Applied, not just declared:** `logs/round-03-postcut.txt` (ALL-PASS)
  verifies the router exposes no `CLASS_TABLE`, that the two ladder arms are
  behaviourally identical, and that the post-cut numbers equal the ablation
  arm's (122 frozen / 292 expanded). The measured pre-cut revision is pinned
  by sha256 in `logs/precut-sha256.txt`.
- **Rejected:** keeping the table behind a flag "in case it is needed"
  (unused mechanism debt, P7); promoting the table on its 44/46 diagnostic
  win (that metric measures agreement, not value — ADR-11); editing the keep
  rule after seeing the data (the rule was frozen; the ruling was mechanical).
- **Reversal:** a future round may re-introduce a *class-conditioned* prior
  only if it is proposed by the belief ledger from measured mismatch evidence
  and survives its own pre-registered trial on new fixtures. The R02/R03
  evidence does not license the old table's return.

## ADR-13: arm fairness — one budget, symmetric accounting

- **Context:** R02's cost comparison was between arms that were not equally
  governed: the ladder arms received `budget=None` and never touched the
  harness governor.
- **Decision:** every arm spends through the same `Budget`; the declared cap
  for R03 is 2000 calls (per run, not per task — the champion alone needs 159
  on the expanded fixture). The ladder's own spending is counted for the first
  time this round.
- **Evidence:** test `test_arms_are_governed_by_one_budget` inspects the eval
  source for the removed bypass; the expanded arms' costs (159/307/292) are
  the first symmetric numbers the project has.
- **Consequence for prior records:** R02's `routed-thresholds` cost of 70 was
  produced by an arm that ran no ladder; its replacement costs 122 on the same
  fixture. R02's H5 refutation is therefore superseded by R03's re-trial, not
  merely re-confirmed.
- **Rejected:** keeping R02's default cap of 100 for the 46-task fixture (it
  fires mid-run and converts measurement into budget-held noise).
- **Reversal:** if a task class legitimately needs more than the declared cap,
  raise the cap per class on the record (P6), not silently.
