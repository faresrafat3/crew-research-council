# Questions for the Operator

If you are unsure about scope, context, or priorities, add your question here. The operator will respond.

## Guidelines

1. Be specific — "What is the coverage threshold?" not "Help"
2. Explain why you need the answer
3. Continue working on other tasks while waiting

## Questions

### cline (external) — 2026-09-13 (from memory-architecture deep dive)
1. **Memory storage substrate:** files (Anthropic memory-tool pattern, per-agent `/memories` dirs) or SQLite indexes? We recommend hybrid: files for per-agent private memory (L1), SQLite for the crew-shared indexes (L2: cases, expertise, playbooks). Why needed: drives the write-gate implementation in the first memory PR.
2. **Should tester/critic have read access to agent private memory (L1)?** Full opacity vs filtered read views (Collaborative Memory pattern supports per-reader filtered projections). We recommend: tester gets filtered views only, critic gets nothing. Why needed: determines the read-policy design; this is the crew's main trust boundary.
3. **Who curates playbook deltas (procedural memory)?** We recommend: coach drafts from verdict/escape analysis → tester validates against regression ledger → operator approves merges. Why needed: without a named curator, the playbook layer will accumulate unvalidated deltas and collapse (the ACE failure mode).
