# FINDINGS-R03 — NOTE (2026-10-12): the quoted class deltas do not sum to the quoted net

> Dated sibling of `FINDINGS-R03.md`, which is **frozen**: this note adds a
> recomputation. It does not edit, supersede or re-score that round's findings,
> hypotheses or ruling. Filed by an operator-session audit —
> `REPRO-AUDIT-R02-R03-2026-10-12.md` §3 (**F2**). Owner: Fares. Language:
> English (artifacts) / Arabic (chat).

**What does not close.** `FINDINGS-R03.md` L65–70 quotes six per-class cost pairs
and a net:

- wins (the class table is cheaper): external-source `28 vs 32` ·
  instruction-in-source `21 vs 24` · multi-source-synthesis `19 vs 26` → **−14**
- losses: partial-grounding `44 vs 32` · truncation-severs-citation `42 vs 30` ·
  poisoned-source `22 vs 16` → **+30**
- class-level net: **+16**

while the same paragraph's arm totals differ by **+15** (`307 − 292`) and the text
reads "Net: **+15 calls (+5.1%)**".

**What is consistent.** Everything else in that table recomputes exactly:
`resolved/100 calls` = `12/159 = 7.55`, `23/307 = 7.49`, `23/292 = 7.88`;
clause (d) `0.07492 = 23/307` and `0.07877 = 23/292`; the share
`15/292 = 5.14%`.

**Which side is off cannot be settled here.** That needs `logs/r03-analysis.md`
(the generated per-class table), which exists on **no ref** of the 33 on `origin`
(`REFERENCE-INTEGRITY-SWEEP-2026-10-12.md` §4). This note records the discrepancy
and picks no side. The H13 ruling is unaffected either way: its clauses (c) and
(d) fail on the arm totals (23 vs 23 resolved; 0.07492 < 0.07877).

**Reproduce the recomputation:**

```
python3 -c "print(12/159, 23/307, 23/292, 307-292, (28+21+19)-(32+24+26))"
```

---
**Note filed 2026-10-12 · base `ecaa656`, `main` at `f69873f` · no number changed.**
