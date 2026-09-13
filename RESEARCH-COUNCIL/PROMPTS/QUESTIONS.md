# Questions for the Operator

If you are unsure about scope, context, or priorities, add your question here. The operator will respond.

## Guidelines

1. Be specific — "What is the coverage threshold?" not "Help"
2. Explain why you need the answer
3. Continue working on other tasks while waiting

## Questions

1. **Verdict schema — add oracle provenance fields?** The tester-soul deep dive recommends extending the TEST VERDICT template with `ORACLE=<req-derived|regression|mixed>` and `TAUT=<n>`, with PROMOTE requiring req-derived oracles for all P0/P1 REQ-IDs. This needs a decision before Phase 1 implements the verdict parser.
2. **Mutation gate scope.** LLM- and human-written oracles both average ~43-45% mutation score (ASE 2025, 13,866 oracles). The roadmap's 60-80% target is only reachable with req-derived oracles plus per-REQ mutation slices. Confirm the gate applies per-REQ slice (not whole-suite average), and at which maturity level it activates.
3. **Flake adjudication policy.** Is 3x rerun with recorded seed + bisect acceptable before quarantine, or should the operator set different retry policy for the tester's own harness?
