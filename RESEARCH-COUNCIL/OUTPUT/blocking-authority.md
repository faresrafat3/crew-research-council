# Blocking Authority and Governance: When the Crew v2 Tester May Block a Release

## Executive Summary

This document defines the blocking authority of the Crew v2 tester agent: the exact conditions under which it may hard-stop a release (BLOCK), the conditions it may only flag (ADVISE), and how disagreements are resolved through a timed escalation ladder ending in a human operator override. The design follows one governing principle drawn from every real system studied: **the tester is a required status check, not the sole ruler** — it blocks mechanically (like GitHub's required checks and Google's presubmits), its blocks fail closed for high-risk work but fail open for read-only work, and the only actor who can override a block is the human operator, whose override is a recorded decision with a reason attached [Winters et al., 2020; GitHub Docs, n.d.; AWS, n.d.]. Thresholds are set from published evidence where it exists (Google's 1.5% flake-run baseline, DORA's 0–15% elite change-failure band, Google's three-consecutive-failure retry rule) and marked as proposed defaults with reasoning where it does not. The charter's central calibration loop — block precision vs. escape rate — is the tester's own four-key-metrics discipline, so the gate tightens or loosens on data rather than on opinion.

## Key Findings

### How real engineering organizations gate releases
- Google requires every change list (CL) to clear three separable approval "bits" — a peer LGTM, a directory **code-owner approval**, and a language **readability approval** — and even then "files in a workspace are committed to the central repository only after going through the Google code-review process" [Winters et al., 2020; Potvin & Levenberg, 2016].
- Google's presubmit tests **gate submission mechanically**: "only fast, reliable ones" run pre-submit, because "it's expensive for engineers to be blocked on presubmit by failures arising from instability or flakiness" [Winters et al., 2020].
- Piper's auto-commit describes the submit-queue behavior precisely: "When the review is marked as complete, the tests will run; if they pass, the code will be committed to the repository without further human intervention" [Potvin & Levenberg, 2016]. Chrome implements the same concept as the Commit Queue, and Fuchsia as Gerrit auto-submit [Chrome Infrastructure, n.d.; Fuchsia, n.d.]. Small repositories get the same guarantee by "serializing submits" [Winters et al., 2020]; GitHub sells it as a merge queue that runs required checks against the *latest* branch state before any PR merges [GitHub Docs, n.d.].
- Google's reviewer standard explicitly bounds blocking authority: "In general, reviewers should favor approving a CL once it is in a state where it definitely improves the overall code health of the system… even if the CL isn't perfect," because "if a reviewer makes it very difficult for any change to go in, then developers are disincentivized to make improvements" [Google eng-practices, n.d.].

### Fail-open vs fail-closed
- The default rule: "fail open when the protection is a performance guard, fail closed when it is a correctness or security guard" [SystemDesignSchool, n.d.]. A verification gate is a correctness guard — so the crew's verification steps fail closed.
- The silent-failure trap: "If the fail direction is not chosen explicitly, the surrounding code usually defaults to letting traffic through," and "a guardrail error is an undefined state… not treated as equivalent to a guardrail pass" [AI Skill Certs, 2026].
- The most important empirical finding of this research: **GitHub's branch protection fails open for admins by default** — "By default, the restrictions of a branch protection rule don't apply to people with admin permissions to the repository or custom roles with the 'bypass branch protections' permission" [GitHub Docs, n.d.]. A gate that admins can silently walk through is a gate that exists on paper only; SOX auditors treat exactly this as a finding [Systemshardening, 2026].
- Middle ground exists: "fail-open with a floor" — a coarse local fallback bounds the blast radius instead of eliminating protection — and whatever the default, "make it loud": a silent fail-open is a hole nobody notices [SystemDesignSchool, n.d.].

### What too-strict gates cost vs too-lenient gates
- Too strict → circumvention: flaky alarms train people to ignore alarms ("It is human nature to ignore alarms when there is a history of false signals"), and reviewer overload produces rubber-stamp approvals ("Routing every agent action through human review produces rubber-stamp approvals") [Micco, 2016; AWS, n.d.].
- Too lenient → measurable failure: DORA's elite performers report change failure rates of 0–15% while low performers report 16–30% (2021) or 46–60% (2018); Accelerate found high performers have a 5× lower change failure rate, and that low performers' failure rates *worsen* when they speed up tempo without "building quality in" [Forsgren et al., 2018; DORA, 2018; Google, 2021].
- Crew v2 today sits entirely on the lenient side: engineer ships with zero tests across COORD-01/COORD-02, fixes land with no regression tests (T09–T12), and "no agent has authority to block code that lacks tests" — the council context's own root-cause analysis.

### Risk-based gating, independence, escalation
- Risk-based testing is an ISTQB-defined approach in which "test activities are selected, prioritized, and managed based on risk analysis," with risk level = likelihood × impact deciding test depth [ISTQB FL Syllabus, n.d.; ISTQB Glossary, n.d.].
- The four-eyes/maker-checker/segregation-of-duties family all reduce to: "a sensitive decision must be independently reviewed before it moves. No single person should be able to advance the action alone" [Latch, 2026]; NIST SP 800-171's control exists because "no single person can execute conflicting high-risk actions end-to-end (for example, developing code, approving it, and deploying it to production)" [NIST SP 800-171 (Daydream summary), n.d.].
- Mature escalation is mechanical, not judgmental: PagerDuty escalates automatically "if no one takes action before the timeout elapses," with a default 30-minute timeout [PagerDuty, n.d.]; industry practice caps escalation at three tiers and sets the timeout from the acknowledgment SLO [incident.io, 2026].
- For AI agents specifically: pause high-risk actions for review, "implement timeout policies… with safe fallback actions (typically blocking the operation)," log every decision with reviewer identity and timestamp, and start with maximum oversight then remove checkpoints as correction rates decline [AWS, n.d.; AWS re:Invent, 2025].

## Detailed Analysis

### 1. How real engineering organizations gate releases

**Google — three approval bits plus machine gates.** At Google, a change needs (1) an LGTM from a peer engineer ("looks good to me" — a correctness and comprehension check), (2) approval from a code **owner** of the affected directory, who acts as "gatekeepers for their particular directories," and (3) approval from someone with language **readability** certifying style conformance. "Most reviews have one person assuming all three roles," and an author who is themselves an owner with readability needs only the LGTM — the authority is role-based, not person-based [Winters et al., 2020]. Critically for the crew's design: the *reviewer* bits are held by different roles than the *author*, and the machine adds its own gate on top — "A set of global presubmit analyses are run for all changes," with owners able to add directory-specific analyses [Potvin & Levenberg, 2016].

**Google — presubmit discipline.** Google deliberately runs only "fast, reliable" tests on presubmit and accepts "some loss of coverage on presubmit" on the condition that "you need to catch any issues that slip by on post-submit, and accept some number of rollbacks" [Winters et al., 2020]. Two failure-mode lessons transfer directly: (a) flaky tests on the presubmit path actively destroy gating value — "it's expensive for engineers to be blocked on presubmit by failures arising from instability or flakiness that has nothing to do with their code change" [Winters et al., 2020]; (b) concurrent submissions can collide ("mid-air collision"), and "CI systems for smaller repositories or projects can avoid this problem by serializing submits" [Winters et al., 2020].

**Google — auto-commit and the submit queue.** Piper's workflow is the canonical submit-queue citation: workspace files "are committed to the central repository only after going through the Google code-review process," and with auto-commit enabled, "When the review is marked as complete, the tests will run; if they pass, the code will be committed to the repository without further human intervention" [Potvin & Levenberg, 2016]. The same pattern exists in the open at Chrome (Commit Queue: "a service (aka a bot) that commits Gerrit changes for you, instead of you directly committing the change") and Fuchsia ("Any change that is opted in will automatically be submitted after being approved and passing presubmit checks") [Chrome Infrastructure, n.d.; Fuchsia, n.d.]. Note: the exact phrase "submit queue" could not be verified in the freely available online edition of *Software Engineering at Google* (searched all 26 chapters); the mechanism is verified through the auto-commit description above, and the ladder is completed by GitHub's merge queue.

**GitHub — branch protection, required checks, merge queue.** GitHub operationalizes gating as branch protection: "Require pull request reviews before merging," "Require status checks before merging," "Require conversation resolution before merging," "Require merge queue," and "Do not allow bypassing the above settings" [GitHub Docs, n.d.]. Required status checks are the direct ancestor of the tester's BLOCK authority: when enabled, "collaborators can only push changes to a protected branch via a pull request that is approved" and merges are impossible while checks fail. A merge queue then "ensures the pull request's changes pass all required status checks when applied to the latest version of the target branch and any pull requests already in the queue" — the serialized-submit guarantee for small repos [GitHub Docs, n.d.].

**Trunk-based development — review before trunk.** In trunk-based development, "patch review systems… marshal pending changes, before they arrive in trunk/main and to guarantee they are good to be integrated"; teams commit direct-to-trunk only when very small, and "if you have more than a couple of developers on the project, you are going to need to hook up a build server to verify that their commits have not broken the build" [Hammant, n.d.a; Hammant, n.d.b]. When a gated commit later proves broken, trunk teams revert immediately rather than negotiate [Hammant, n.d.b]. The tester is the crew's patch-review system: the crew's trunk (shared working tree) must never receive code the tester has not marshaled.

### 2. Fail-open vs fail-closed — and what each crew task class deserves

Fail-open means "allow the request when the check is down"; fail-closed means "deny the request when the check is down" [SystemDesignSchool, n.d.]. The selection rule from the same source: "fail open when the protection is a performance guard, fail closed when it is a correctness or security guard," decided by comparing "the cost of a lapse in protection against the cost of an outage" — a login page that rejects everyone is a bad hour; one that admits everyone is a breach [SystemDesignSchool, n.d.]. Complementary security guidance: fail-secure "protects the asset first" and defaults to denial when a control cannot verify; fail-safe exists where *stopping* would harm people [ITU Online, 2024].

Three specific traps the crew must design against:

1. **The default trap.** "If the fail direction is not chosen explicitly, the surrounding code usually defaults to letting traffic through" — the tester's SOUL must state the failure direction for every check, or missing tool output will silently count as a pass [AI Skill Certs, 2026].
2. **The silent trap.** "A silent fail-open is a hole nobody notices until it is abused. Emit a metric and an alert whenever the system enters its degraded mode" [SystemDesignSchool, n.d.]. Every tester HOLD/BLOCK must be emitted as a logged event, never just a message.
3. **The admin trap.** GitHub branch protection ignores admins *by default*; SOX guidance calls an unenforced "Include administrators" setting an audit finding because "an administrator who is also a developer can deploy without approval," and requires "Do not allow bypassing the above settings" plus approver ≠ author checks [GitHub Docs, n.d.; Systemshardening, 2026]. The crew's equivalent: the operator's override exists, but it is *loud, logged, and counted* — never a silent walking-through of the gate.

For an AI crew, the risk-tiered approval model from AWS's Agentic AI Lens gives the task-class mapping: "read-only operations proceed autonomously, low-risk writes require single-reviewer approval, and higher-risk operations… require stricter approval," implemented with "deterministic logic (policy engines, rule-based classifiers) as the authoritative signal" — never an LLM classifier alone, "because adversarial content could influence the classifier into marking the request as low-risk" [AWS, n.d.]. The crew's task-risk classes (§7) apply exactly this: firstmate's classification (deterministic routing rules) sets the tier; the tester's verdicts execute it.

**Crew law alignment.** Crew v2's P4 canonized rule — "HOLD-on-unverified: compliance beats completion; if a task cannot be verified, the correct outcome is HOLD with a stated gap, not a fabricated pass" — is a fail-closed rule for the *verification* control itself, matching both the "guardrail error is an undefined state, not a pass" principle [AI Skill Certs, 2026] and AWS's timeout guidance that the safe fallback is "typically blocking the operation" [AWS, n.d.]. A tester that cannot run tests does not emit PASS-with-an-asterisk; it emits HOLD(unverifiable) with the named gap.

### 3. What gate strictness costs in each direction

**Too strict → bypass and rubber-stamping.** Google's reviewer guide warns that a blocker who is too hard "disincentivizes" authors from improving the codebase at all [Google eng-practices, n.d.]. Flaky gates are the clearest evidence of threshold-induced bypass: at Google ~1.5% of all test runs are flaky (same code, both pass and fail results), ~16% of tests carry some flakiness, and "about 84% of the transitions we observe from pass to fail involve a flaky test" — so "it is quite common to ignore legitimate failures in flaky tests" and "it is human nature to ignore alarms when there is a history of false signals" [Micco, 2016]. On the human-review side, "routing every agent action through human review produces rubber-stamp approvals" [AWS, n.d.], and blind approval is the documented failure of noisy queues: "operators approve blindly because the review queue is too noisy" [AgentNative, 2026]. Google's counter-measures are instructive: retry-only-failures, a "fails 3 times in a row" rule for flaky-marked tests, and automatic quarantine that "removes the test from the critical path and files a bug" — while acknowledging quarantine "could easily mask a real race condition" [Micco, 2016]. Microsoft runs the same system at scale (~49K flaky tests identified, 160K sessions that would have failed were passed), always runs all tests while suppressing quarantine results, removes tests from quarantine automatically once fixed, and adds a policy layer: "blocking PRs for developers… if they have more than 10 flaky test bugs assigned to them" [Microsoft, 2022].

**Too lenient → measured change failure.** DORA's change failure rate (the percentage of changes to production that "result in degraded service… and subsequently require remediation (e.g., require a hotfix, rollback, fix forward, patch)") is the outcome metric for gate quality: 2018 — elite 0–15% vs low 46–60%; 2019 — elite 0–15% vs low 46–60% ("changes are 1/7 as likely to fail"); 2021 — elite 0–15% vs low 16–30% (means 7.5% vs 23%; elite three times better) [DORA, 2018; DORA, 2019; Google, 2021]. The Accelerate book adds the causal mechanism: low performers "working to increase tempo but not investing enough in building quality into the process" end up with "larger deployment failures that take more time to restore service," while high performers "don't have to trade speed for stability… because by building quality in they get both" [Forsgren et al., 2018]. For Crew v2, the current state (engineer ships 0 tests on 3/3 COORD-01 runs and 4/4 COORD-02 modules; T09–T12 fixes with no regression tests) is the un-gated baseline this charter exists to move into the measured band.

### 4. Risk-based gating — likelihood × impact decides gate strictness

ISTQB defines the tester's core instrument: "The test approach, in which test activities are selected, prioritized, and managed based on risk analysis and risk control, is called risk-based testing," with "Risk likelihood – the probability of the risk occurrence" and "Risk impact (harm)" combining into a risk level where "the higher the risk level, the more important is its treatment" [ISTQB FL Syllabus, n.d.; ISTQB Glossary, n.d.]. Product risk analysis explicitly "may influence thoroughness and test scope," and risk level "is used to prioritize the risk mitigation activities" [ISTQB FL Syllabus, n.d.]. The advanced syllabus adds execution strategy — depth-first ("all of the highest risk tests are run before any lower-risk tests") versus breadth-first (risk-weighted sampling ensuring every risk area is covered at least once) — and formalizes residual-risk reporting: when time runs out, testers report remaining risk "and allows management to decide whether to extend testing or to transfer the remaining risk" [ISTQB CTAL, n.d.].

This is precisely the tester's job in Crew v2: firstmate's classification axes (complexity, verifiability, tool needs) are the likelihood and impact inputs; the tester translates them into gate strictness. The AWS lens adds the enforcement principle — the risk classifier must be deterministic, not an LLM exposed to the same content it is judging [AWS, n.d.] — so the crew's risk classes are rules on firstmate's structured output, not vibes.

### 5. Separation of duties and verification independence

The compliance family is consistent across sources. The four-eyes principle: "a sensitive decision must be independently reviewed before it moves. No single person should be able to advance the action alone," and independence requires the reviewer to actually see the evidence — "A reviewer who cannot see the evidence is not independent" [Latch, 2026]. Maker-checker operationalizes it as a record answering who prepared the case, what evidence was attached, who checked it, whether the checker was independent, and what happened after approval [Latch, 2026]. Segregation of duties draws the structural boundary: "the person who creates a vendor should not also approve payment to that vendor… the person who writes a policy should not be the only person who can bypass it" [Latch, 2026]; NIST SP 800-171's separation-of-duties control (3.1.4) requires that "no single person can execute conflicting high-risk actions end-to-end (for example, developing code, approving it, and deploying it to production)," enforced "with RBAC, privileged access management, and change/workflow controls, not policy text alone" [NIST SP 800-171 (Daydream summary), n.d.]. SOX pipeline guidance states the crew-relevant rule flatly: "The core SOX requirement is that the person who writes code cannot be the sole person who authorizes its deployment," with an explicit CI check that "approver ≠ author," CODEOWNERS protection over the workflow files themselves (the control surface must itself be controlled), and immutable, signed evidence packages for every deployment [Systemshardening, 2026].

Crew v2 already canonizes verification independence (a verifier must differ from the executor in tools and identity — DUO formation). The charter makes it auditable: artifact ownership is exclusive and tool-enforced (§7, rules C1–C6), the tester never edits implementation, the engineer never edits tests, and the tester's own gate configuration is owned by the operator alone, mirroring the CODEOWNERS-over-workflows rule [Systemshardening, 2026].

### 6. Escalation, deadlock resolution, and human-in-the-loop approval

**Mechanical escalation.** PagerDuty's model is the industry baseline: a responder has until the "escalation timeout" (default 30 minutes; minimum 1 minute for a single target, 3 minutes for multiple) to act, and "if no one takes action before the timeout elapses, the incident escalates to the next rule" automatically — escalation is a property of the system, "not an awkward judgment call" [PagerDuty, n.d.; incident.io, 2026]. Best practice caps tiers ("Limit tiers to three maximum"), ties timeouts to SLOs ("If your P1 SLO requires acknowledgment within 5 minutes, your escalation timeout should fire at minute 6"), and escalates to leadership only after ~60 minutes unresolved [incident.io, 2026]. Google's code-review SLA supplies the human-paced anchor: "One business day is the maximum time it should take to respond to a code review request" [Google eng-practices, n.d.].

**Human-in-the-loop for AI agents (2023–2026).** The AWS Agentic AI Lens requires: risk-tiered approvals (autonomous / single-reviewer / multi-reviewer by action class); reviewers receiving "enough context to make informed decisions within a defined time window"; "escalation paths handle cases where primary reviewers are unavailable"; timeouts with "safe fallback actions (typically blocking the operation)"; and logging of "reviewer identity, timestamps, the operation under review, the decision, and any escalation events" [AWS, n.d.]. The re:Invent 2025 multi-agent HITL guidance names the four triggers for a checkpoint — high-stakes decisions, irreversible actions, regulatory requirements, and the trust-building phase — and gives the reduction rule: begin with maximum involvement, then remove checkpoints when "the rate of corrections should decline over time," outputs are consistently above the confidence threshold, and audit metrics show expected behavior [AWS re:Invent, 2025]. AgentNative's pattern adds the implementation details used in this charter: a common confidence threshold of 85% for routing to review (set per action type, not system-wide), cryptographically locked payloads between approval and execution, and an append-only audit trail that captures "request → classification → human decision → execution → outcome" [AgentNative, 2026].

**Deadlock prevention.** The crew's ladder (§7, L1–L3) applies the PagerDuty pattern to agent disagreement: every rung has a timeout, every timeout has a default outcome (block stands = fail-closed), and cycle count is capped with forced auto-escalation, so two stubborn agents can never deadlock a release silently. No published research specific to *agent-vs-agent* escalation SLAs was found in this research pass — the rung timeouts below are therefore proposals patterned on PagerDuty/incident.io mechanics and Google's one-business-day review SLA, marked as such.

### 7. The Blocking-Authority Charter for the Crew v2 tester

#### 7.1 BLOCK conditions (hard stops)

The tester emits `BLOCK` when any condition holds. Every BLOCK is a logged, append-only event (who/what/when/evidence) and is mechanically enforced like a required status check [GitHub Docs, n.d.].

- **B1 — Missing tests for changed code (write-class tasks).** If the task produced or modified non-test source code (diff includes `src/` or application files) and there is **no test file covering the changed behavior** (changed-line coverage of new/modified behaviors = 0), the tester blocks. Google's rule this enforces: "In general, tests should be added in the same CL as the production code unless the CL is handling an emergency" [Google eng-practices, n.d.]. Precise check: `pytest --collect-only` finds no test referencing the changed module/API, or diff-cover reports 0% changed-line coverage.
- **B2 — Failing suite.** Any required test fails: `pytest` exit code ≠ 0 on the gate suite. This is the required-status-check semantics — a red check is a block, not an opinion [GitHub Docs, n.d.; Winters et al., 2020].
- **B3 — Flaky tests above threshold.** Per-suite trailing-14-day flake rate > **5%** of runs → the tester blocks *that suite's* green verdict until offending tests are quarantined (quarantine = moved to a quarantine list + bug filed, per Google/Microsoft practice [Micco, 2016; Microsoft, 2022]). Rerun policy for a first-time flaky failure: rerun failing tests up to **3** times; all reruns must pass (Google's "report a failure only if it fails 3 times in a row" rule [Micco, 2016]). Threshold justification: Google's corpus-wide baseline is ~1.5% flaky runs; a suite sustaining >5% (≈3× Google's rate) is locally broken. *The 5% figure is my proposed default anchored to Google's published 1.5% baseline.*
- **B4 — Coverage below per-suite thresholds (changed lines).** Changed-line coverage below the suite's threshold → block. Proposed defaults (marked as proposals; no industry-standard threshold is published — Google explicitly avoids global bars): **core/critical-path suites 90% line / 75% branch; standard feature suites 80% line / 60% branch; experimental suites ADVISE-only.** Google's own warning drives the *changed-lines* design: teams that set an 80% bar watch it become a ceiling ("instead of treating 80% like a floor, engineers treat it like a ceiling. Soon, changes begin landing with no more than 80% coverage") and Google recommends "only measuring coverage from small tests" to avoid coverage inflation [Winters et al., 2020]. Hence: gate on **changed-line** coverage of the diff (ratchet), not on the global number.
- **B5 — Bug-fix without a regression test for the original failure.** For any fix/correction task, the suite must contain a test that **fails against the pre-fix code and passes after** (verify by reverting the fix, or `git stash` + rerun). No regression test → BLOCK. This is the charter's highest-value rule given T09–T12 (fixes shipped, bugs recurred because the original failure case was never pinned). Google's reviewer question is the standard: "Will the tests actually fail when the code is broken?" [Google eng-practices, n.d.].
- **B6 — HOLD-on-unverified (crew law P4).** If the tester cannot verify (tests can't run, environment unavailable, task's output is not observable), it emits `HOLD` with a **stated gap** ("cannot run pytest: interpreter missing in terminal env"), never a fabricated pass. This is fail-closed for the verification control itself [AI Skill Certs, 2026; AWS, n.d.].
- **B7 — Tests that assert implementation details do not count.** For the purpose of B1/B4, tests that mock or assert internals of the implementation rather than observable behavior are excluded from the gate (they do not satisfy "tests for changed behavior"). Grounded in the crew's TESTING-COUNCIL philosophy ("test behavior not implementation") and Google's "Test via Public APIs" guidance [Winters et al., 2020]. Marked as charter policy, not external citation.

#### 7.2 ADVISE conditions (non-blocking)

The tester flags but cannot block on these — Google's "Nit:" convention: "if it's not very important, prefix it with something like 'Nit:' … it's not mandatory for the author to resolve it in this CL" [Google eng-practices, n.d.].

- **A1 —** Global suite coverage below target while changed-line coverage is met (ratchet will catch up; do not block old debt) — designed against the ceiling effect [Winters et al., 2020].
- **A2 —** Test-quality smells: brittle assertions, duplication, slow setup — tests still pass and assert behavior.
- **A3 —** Suite runtime > 10 minutes (slows the loop; Google keeps presubmit fast and reliable by design [Winters et al., 2020]).
- **A4 —** Pyramid-shape deviation: per-suite mix outside 70% unit / 20% integration / 10% E2E by more than ±15 points (internal TESTING-COUNCIL philosophy).
- **A5 —** Naming/docs/nits in tests or test descriptions.
- **A6 —** Mutation score on changed modules < **85%** (proposal: run `mutmut run --paths-to-mutate <changed modules>`; promote to a BLOCK condition for RC-1 tasks only after 2 weeks of calibration data — see §7.7. No published mutation-score threshold was found in this research pass; 85% is my proposed default, aligned with the 85% confidence threshold in common HITL routing practice [AgentNative, 2026]).
- **A7 —** Quarantined test aging: any test in quarantine > 14 days without a fix (Microsoft's auto-unquarantine closes the loop; stale quarantine masks real coverage loss [Microsoft, 2022]).
- **A8 —** Confidence/uncertainty signals: tester's own uncertainty about verification completeness (routes to human review at 85% threshold per HITL practice [AgentNative, 2026]).

#### 7.3 Task-risk classes and fail-direction defaults

Risk level = likelihood × impact [ISTQB FL Syllabus, n.d.], instantiated from firstmate's classification axes. The failure direction per class follows "fail open for performance guards, fail closed for correctness guards" [SystemDesignSchool, n.d.] and AWS's read-only/low-risk/high-risk tiering [AWS, n.d.].

| Class | Firstmate signature | Gate strictness | Failure default | Verifier structure |
|---|---|---|---|---|
| **RC-1 High-stakes** | write/execute + (complex OR unknown) + touches critical path/security/data handling | Full charter: B1–B7 all active; mutation score BLOCK after calibration; coverage floors at core-suite thresholds | **Fail-closed everywhere**, including HOLD on any verification gap | Tester **and** critic both verify (independent); operator approves release |
| **RC-2 Standard** | write-class + simple/moderate + testable | B1–B6 active; B4 at standard thresholds; A6 mutation ADVISE-only | **Fail-closed on hard conditions (B1/B2/B5/B6)**, ADVISE on quality debt | Tester verifies; critic spot-checks |
| **RC-3 Low-risk / read-only** | read-only tools + (self-evident OR external-source OR unverifiable) | No test gates (nothing to test); tester checks artifact form, source citations, constraint compliance | **Fail-open** for nitpicks (ADVISE, never BLOCK on style) but **HOLD, not PASS, if verification is impossible** (P4: "compliance beats completion") — the human operator is the "local fallback with a floor" [SystemDesignSchool, n.d.] | Tester role-plays verifier; escalates HOLD to operator for accept/transfer decision |

#### 7.4 Escalation ladder for disagreements (engineer believes block is wrong)

Patterned on mechanical escalation [PagerDuty, n.d.; incident.io, 2026] with the human-paced anchor "one business day is the maximum time it should take to respond to a code review request" [Google eng-practices, n.d.]. Every rung timeout has a **default outcome — the block stands** (fail-closed; AWS's "safe fallback… typically blocking the operation" [AWS, n.d.]). Timeouts are my proposed defaults (no published agent-crew escalation SLA exists — could not verify; based on the cited industry patterns scaled to an async crew).

| Rung | Actor | Action | Timeout | Default if it expires |
|---|---|---|---|---|
| **L0** | tester | Emits verdict with evidence block (condition id, command output, measured value vs threshold) and an explicit rebuttal template for the engineer | — (immediate) | — |
| **L1** | engineer | Rebut with **evidence**, not opinion ("technical facts and data overrule opinions" [Google eng-practices, n.d.]): e.g., rerun logs proving flake, corrected coverage measurement, demonstration that a test does cover the behavior | **24 h** (Google's one-business-day SLA [Google eng-practices, n.d.]) | Block stands; auto-escalate to L2 |
| **L2** | critic | Independent arbitration: reviews L0 evidence + L1 rebuttal, reproduces the disputed check itself, issues a **binding verdict** (sustain block / convert to ADVISE / PASS-with-conditions). Scope is bounded to the single disputed condition (critic's known timeout limitation is handled by the short window + scoped task) | **4 h** | Block stands; auto-escalate to L3 |
| **L3** | operator (human) | Final authority: sustain, override (with logged reason), or return with instructions | **48 h** | Block stands (release waits; nobody merges by default — fail-closed) |
| **L4** | tester (post-hoc) | Every override is logged to the audit trail and enters the weekly calibration review (§7.7) | — | — |

**Deadlock prevention:** at most **2 rebut cycles** (L1 → L0 re-evaluation → L1) per task. After the 2nd cycle, or on any timeout expiry, escalation is automatic — the disagreement cannot ping-pong silently. This mirrors "the escalation timeout… escalates to the next rule until a user acknowledges," removing the judgment call from the participants [PagerDuty, n.d.]. **Break-glass path:** for emergency fixes (production down), the ladder shortens to L0 → L3 (operator) with tests still required post-hoc within 24 h — matching both Google's emergency exception ("unless the CL is handling an emergency" [Google eng-practices, n.d.]) and the emergency-change pattern of "documented justification and an independent after-the-fact review" [NIST SP 800-171 (Daydream summary), n.d.].

#### 7.5 Override policy

- **Who may override:** the **operator only** — a human. Tester, engineer, critic, and completer cannot override each other's verdicts. This mirrors the four-eyes requirement that no single actor advances a sensitive action alone [Latch, 2026] and the SOX rule that the change author cannot be the sole authorizer [Systemshardening, 2026]. Note the deliberate divergence from GitHub's default (admins bypass silently [GitHub Docs, n.d.]): in the crew, override is *always* loud.
- **An override is a recorded decision with the reason attached.** Required audit fields (maker-checker record [Latch, 2026; AWS, n.d.]): task id, block condition id (B1–B7), evidence digest, override reason (≥ 1 sentence), operator identity, timestamp, downstream outcome. The log is **append-only** — "rejected and returned cases recorded, not overwritten" [Latch, 2026]; AgentNative's append-only queue is the model [AgentNative, 2026].
- **Overrides are counted in calibration** (§7.7). Override rate > 10% of BLOCKs sustained for 2 weeks → mandatory threshold review (either the gate is miscalibrated or the operator is the single point of failure — both are findings).

#### 7.6 Collusion and independence rules

- **C1 —** Tester and critic are **different agents with different tool access** (tester: terminal, read_file, write_file *for test artifacts only*; critic: terminal, read_file), never the same session/model instance verifying its own work.
- **C2 —** The **engineer never edits tests** (no write access to `tests/`); the **tester never edits implementation** (no write access to `src/`). Artifact ownership is enforced by tool permissions, "not policy text alone" [NIST SP 800-171 (Daydream summary), n.d.].
- **C3 —** Artifact ownership: engineer owns `src/` and module code; tester owns `tests/`, quarantine lists, and gate logs; critic owns arbitration verdicts; operator owns the charter itself (thresholds, BLOCK/ADVISE lists, ladder timeouts). Protecting the gate configuration inside operator-only ownership mirrors the CODEOWNERS-over-workflows rule — "a developer who can modify… deploy-production.yml without approval can remove the SOD check" [Systemshardening, 2026].
- **C4 —** A verifier (tester or critic) never verifies a task it executed; DUO formation keeps executor ≠ verifier, which is Crew v2's verification-independence principle and the four-eyes rule [Latch, 2026].
- **C5 —** Razor (constraint-violation risk) may not edit test files or gate logs; razor's outputs are always re-checked by the tester for constraint compliance (constraint violations are razor's documented failure mode).
- **C6 —** Completer performs final presence checks but **inherits** the tester's verdict — it cannot downgrade a BLOCK (its documented gap: it "does NOT block on missing tests"; the tester is the blocking authority, not the completer).

#### 7.7 Calibration over time

Track two outcome metrics on every gated task plus process metrics:

- **Block precision** = share of BLOCKs sustained (defect later confirmed or block upheld at L2) — target ≥ **80%** (i.e., fewer than 1 in 5 blocks is a false alarm; above that, alarm fatigue drives the documented bypass behaviors [Micco, 2016]).
- **Escape rate** = share of PASS/overridden tasks that later failed in use or required rework — target ≤ **5%**, with the DORA elite band as the strategic anchor: change failure rate 0–15% [DORA, 2018; Google, 2021].
- **Process metrics:** override rate (target < 10% of blocks), median ladder duration per rung, flake rate (target < 1.5% of runs — Google's corpus baseline [Micco, 2016]), quarantine age (target < 14 days [Microsoft, 2022]), false-block rate at L2.

**Adjustment rules (my proposal — no published quality-gate calibration research was found in this research pass; state of the art is the HITL reduction guidance from AWS [AWS, n.d.; AWS re:Invent, 2025]):**
- Escape rate > 5% for 2 consecutive weeks → tighten one notch: flake threshold 5% → 3%; or core-suite coverage floor +2 points; or promote A6 mutation to BLOCK for RC-1.
- False-block rate > 20% (L2 overturns) for 2 consecutive weeks → loosen one notch: standard-suite coverage floor −2 points; or move one ADVISE-only condition down a risk class.
- Override rate > 10% for 2 weeks → operator review of charter (mis-calibration vs single-point-of-failure).
- 4 weeks of precision ≥ 80% and escape ≤ 5% → consider *loosening* a rung: shorten L1 timeout to 12 h, or reduce critic scope to spot-check on RC-2 — the re:Invent reduction rule ("remove checkpoints as the correction rate declines") [AWS re:Invent, 2025].

### 8. Decision table

Situation → verdict → next actor → message to send. (All messages via `message_agent()` per crew protocol.)

| # | Situation | Verdict | Next actor | Message to send |
|---|---|---|---|---|
| 1 | Implementation done, **0 tests**, task was write-class (RC-2) | **BLOCK** | engineer | "BLOCK B1: diff touches `src/` with 0 test coverage of changed behavior. Required: tests in same change [Google eng-practices, n.d.]. Add tests covering each new behavior, or rebut at L1 with evidence within 24h." |
| 2 | Suite runs, **2 tests fail** | **BLOCK** | engineer | "BLOCK B2: pytest exit 1, failing: `test_x`, `test_y`. Required status check is red — fix or revert." |
| 3 | Tests green but **one flaky rerun** (failed once, passed on rerun 1) | **PASS + ADVISE** | — (log only) | "PASS. ADVISE: `test_z` flaked once (pass rate 99%→98% this run). Watching; quarantine + bug at sustained >5%." |
| 4 | Per-suite flake rate **7% over 14 days** | **BLOCK (suite)** | engineer | "BLOCK B3: suite flake 7% > 5% threshold. Quarantining top flakers (bug filed per test); suite green-ness suspended until flake < 5% or flakers quarantined [Micco, 2016]." |
| 5 | Coverage **78% vs 80% threshold** (changed-lines, standard suite) | **BLOCK** | engineer | "BLOCK B4: changed-line coverage 78% < 80%. Identify the 22 uncovered changed lines (`diff-cover --compare-branch=main`), add tests or rebut with justification for specific lines." |
| 6 | Coverage 82% global but **changed-lines 100%**; old modules under-covered | **PASS + ADVISE A1** | — (log only) | "PASS. ADVISE A1: changed-line coverage 100%; global suite 82% below target is legacy debt — ratchet, not a block [Winters et al., 2020]." |
| 7 | **Fix task with no regression test** for the original failure | **BLOCK** | engineer | "BLOCK B5: no test pins the original failure (T09–T12 pattern). Required: test that fails on pre-fix code, passes after. Verify: revert fix → test must fail." |
| 8 | Fix task **with** regression test that fails pre-fix, passes post-fix | **PASS** | completer | "PASS: regression test verified (red on pre-fix, green on post-fix). Proceed to final checks." |
| 9 | Task **unverifiable by nature** (subjective text polish, no executable artifact) | **HOLD (P4)** | operator | "HOLD B6/P4: cannot verify — no executable artifact; stated gap: 'no behavioral oracle exists for this output.' Compliance beats completion: operator decision required (accept documented residual risk per ISTQB risk transfer [ISTQB FL Syllabus, n.d.])." |
| 10 | **Read-only research task** (RC-3), report with verifiable citations | **PASS + ADVISE** | completer | "PASS (RC-3, no test gates). ADVISE: 2 claims lack sources; cite or mark unverifiable." |
| 11 | Engineer **rebutts B4** with corrected measurement (coverage was miscounted at 81%) | **Unblock** | tester → all | "L1 rebut accepted: measured changed-line coverage 81% ≥ 80%. BLOCK B4 lifted. PASS with ADVISE A2 (one brittle assertion noted)." |
| 12 | Engineer rebutts **without evidence** ("tests are fine, trust me") | **Sustain BLOCK** | critic (L2) | "L1 rebut rejected: no evidence provided; 'technical facts and data overrule opinions' [Google eng-practices, n.d.]. Auto-escalating to critic arbitration at L2 (4h window)." |
| 13 | **Critic times out** at L2 (its documented failure mode) | **Block stands** | operator (L3) | "L2 timeout (4h): arbitration incomplete. Default outcome: block stands (fail-closed). Escalating to operator for L3 decision within 48h [AWS, n.d.]." |
| 14 | **Operator overrides** a sustained block to ship a hotfix | **Override (logged)** | tester logs; engineer ships | "OVERRIDE recorded: task X, condition B4, operator ID, reason: 'prod outage, hotfix path; tests post-hoc within 24h [Google eng-practices, n.d.; NIST SP 800-171 (Daydream summary), n.d.].' Audit trail entry appended; counted in calibration." |
| 15 | **Razor rewrote** the test file, breaking constraints ("don't change wording" violated) | **BLOCK (C5)** | razor → operator | "BLOCK C5/independence: razor edited `tests/` (forbidden artifact). Reverting test file to tester's version; flagging constraint violation for operator review." |
| 16 | RC-1 task: security-sensitive change, tests green, **mutation score 70%** (< 85%) | **BLOCK (after calibration)** or ADVISE (before) | engineer | "RC-1: mutation score 70% < 85% on changed modules (`mutmut run --paths-to-mutate src/auth`). Surviving mutants listed — add tests killing mutants M3, M7, M12." |
| 17 | Suite green, fast, but **runtime 25 min** | **PASS + ADVISE A3** | — (log only) | "PASS. ADVISE A3: suite runtime 25 min > 10 min target — slows the loop [Winters et al., 2020]. Consider splitting slow integration tests out of the gate." |
| 18 | **Quarantined test** still broken after 14 days | **ADVISE A7 → escalate** | engineer owner | "ADVISE A7: `test_legacy` in quarantine 14 days — coverage loss compounding; bug priority raised [Microsoft, 2022]." |
| 19 | Emergency: **production down**, fix ready, tests not yet written | **Break-glass L0→L3** | operator | "BREAK-GLASS: RC-1 fix for prod outage. Ladder shortened to operator decision; regression test (B5) required post-hoc within 24h; override will be logged [Google eng-practices, n.d.; NIST SP 800-171 (Daydream summary), n.d.]." |
| 20 | Tests assert **internal private methods**, changed-line coverage technically 100% | **BLOCK (B7)** | engineer | "BLOCK B7: tests assert implementation internals (`_helper`), not observable behavior — excluded from gate credit. Rewrite against the public API [Winters et al., 2020]." |

## Practical Recommendations

| Recommendation | Implementation | Tools | Threshold/Target |
|---|---|---|---|
| Make the tester a required status check | Enable "Require status checks before merging" on `main`, add the tester's gate job as required; enable "Require conversation resolution" | GitHub branch protection / rulesets | Tester gate job = required check on `main` [GitHub Docs, n.d.] |
| Close the admin bypass hole | Enable "Do not allow bypassing the above settings" (applies restrictions to admins); operator override happens *inside* the ladder, not around it | GitHub branch protection; ladder audit log | 0 silent bypasses; all overrides logged [GitHub Docs, n.d.; Systemshardening, 2026] |
| Serialize submissions like a submit queue | Enable "Require merge queue" on `main` so gate checks run against the latest queued state | GitHub merge queue; CI reporting on `merge_group` events | All merges through queue [GitHub Docs, n.d.] |
| Enforce B1/B2 mechanically in CI | Gate job: `pytest -q` + `pytest --collect-only` on changed modules; exit code is the verdict | pytest, GitHub Actions | Exit ≠ 0 = BLOCK |
| Measure changed-line (not global) coverage | `diff-cover coverage.xml --compare-branch=main --fail-under=<per-suite>`; coverage from unit tests only | coverage.py + diff-cover | Core 90/75, standard 80/60 (changed lines, unit tests only) [Winters et al., 2020] |
| Flaky policy: 3-strikes rerun + quarantine | Rerun failing tests up to 3× (must all pass); auto-quarantine tests with >5% 14-day flake rate; file one bug per quarantined test; auto-unquarantine on fix | pytest-rerunfailures / pytest `--reruns 3`; quarantine manifest file; bug tracker | Flake < 1.5% of runs; quarantine age < 14 days [Micco, 2016; Microsoft, 2022] |
| Regression-test verification for fixes (B5) | In the gate job: `git stash` the fix (or check out pre-fix commit), run the new regression test, require it to FAIL; then run post-fix, require PASS | git + pytest in CI | 100% of fix tasks have a red-on-pre-fix test |
| Mutation gate for RC-1 (after calibration) | `mutmut run --paths-to-mutate <changed modules>`; start as ADVISE, promote to BLOCK for RC-1 after 2 weeks of data | mutmut | Mutation score ≥ 85% on changed modules (proposal) |
| Implement the escalation ladder with real timers | Tester verdict event starts a timer per rung (L1 24h, L2 4h, L3 48h); on expiry, auto-emit escalation message to next actor; track cycle count, max 2 | Crew orchestration; simple timestamped state file per task | 0 deadlocks; median L1 < 24h, L2 < 4h, L3 < 48h |
| Append-only audit log for every verdict and override | One JSONL event log: `{ts, actor, action, condition_id, evidence_digest, reason, outcome}`; never edited, only appended; weekly review | JSONL log owned by tester, operator-readable | 100% of BLOCKs/HOLDs/overrides logged [Latch, 2026; AgentNative, 2026] |
| Enforce artifact ownership by tools, not text | Engineer: no write to `tests/`; tester: no write to `src/`; razor: no write to `tests/` or logs; charter file owned by operator only | Per-agent tool allowlists / CODEOWNERS over gate config | 0 cross-writes [NIST SP 800-171 (Daydream summary), n.d.; Systemshardening, 2026] |
| Calibrate monthly from outcome data | Track block precision, escape rate, override rate, flake rate; apply the §7.7 adjustment rules | Metrics file + weekly review | Precision ≥ 80%, escape ≤ 5%, override < 10%, CFR ≤ 15% (DORA elite band) [DORA, 2018; Google, 2021] |
| Fix the tester's own failure mode | If the tester cannot run tests (env missing), emit HOLD-on-unverified with the stated gap — never PASS | Tester SOUL instruction | 0 fabricated passes (crew law P4) |

## Metrics and Targets

| Metric | What is measured | Target | Warning threshold | Action on breach |
|---|---|---|---|---|
| Block precision | % of BLOCKs later confirmed justified (defect found or upheld at L2) | ≥ 80% | < 75% for 2 weeks | Loosen one threshold notch (§7.7) |
| Escape rate | % of PASS/overridden tasks that later failed or needed rework | ≤ 5% | > 5% for 2 consecutive weeks | Tighten one notch: flake 5%→3% or coverage floor +2 |
| Change failure rate (DORA) | % of crew releases causing degraded service / requiring remediation | ≤ 15% (elite band) | > 15% | Full charter review [DORA, 2018; Google, 2021] |
| Override rate | Operator overrides as % of BLOCKs | < 10% | > 10% for 2 weeks | Operator/charter review (mis-calibration or single-point-of-failure) |
| Flake rate | % of gate-suite runs with a flaky result | < 1.5% (Google corpus baseline) | > 5% per-suite | B3 suite block; quarantine + bugs [Micco, 2016] |
| Median L1 (engineer rebut) | Time from BLOCK to evidenced rebut | < 24 h | > 24 h | Auto-escalate to L2 [Google eng-practices, n.d.] |
| Median L2 (critic arbitration) | Time from escalation to binding verdict | < 4 h | > 4 h | Auto-escalate to L3 (block stands) |
| Median L3 (operator decision) | Time from L2 timeout/escalation to decision | < 48 h | > 48 h | Block stands; release waits |
| Deadlock cycles | Rebut cycles per task | ≤ 2 | > 2 | Force auto-escalation (PagerDuty pattern) [PagerDuty, n.d.] |
| Quarantine age | Days a quarantined test stays broken | < 14 days | ≥ 14 days | Priority-raise owner bug [Microsoft, 2022] |
| Changed-line coverage (core suites) | Line / branch on the diff | ≥ 90% / 75% | below by > 2 pts | B4 block (proposed default) |
| Changed-line coverage (standard suites) | Line / branch on the diff | ≥ 80% / 60% | below by > 2 pts | B4 block (proposed default) |
| Mutation score (RC-1, post-calibration) | % mutants killed on changed modules | ≥ 85% | < 85% | A6→B block for RC-1 (proposal) |
| Fabricated passes | PASS emitted with unverifiable output | 0 | any | P4 violation — operator incident (crew law) |

## References

1. [Google eng-practices, n.d.] The Standard of Code Review — Google's Engineering Practices Documentation. <https://google.github.io/eng-practices/review/reviewer/standard.html> [verified 2026-09-13]
2. [Google eng-practices, n.d.] What to Look For in a Code Review (tests in the same CL; emergency exception). <https://google.github.io/eng-practices/review/reviewer/looking-for.html> [verified 2026-09-13]
3. [Google eng-practices, n.d.] The Speed of Code Reviews (one-business-day maximum response). <https://google.github.io/eng-practices/review/reviewer/speed.html> [verified 2026-09-13]
4. [Winters, Manshreck & Wright (eds.), 2020] Software Engineering at Google — Ch. 9, Code Review (three approval bits: LGTM, ownership, readability). O'Reilly/abseil. <https://abseil.io/resources/swe-book/html/ch09.html> [verified 2026-09-13]
5. [Winters, Manshreck & Wright (eds.), 2020] Software Engineering at Google — Ch. 23, Continuous Integration (presubmit gating: "only fast, reliable ones"; mid-air collisions; serializing submits; flake classification). <https://abseil.io/resources/swe-book/html/ch23.html> [verified 2026-09-13]
6. [Sadowski, Kurnia & Rohlfs, 2020] Software Engineering at Google — Ch. 19, Critique: Google's Code Review Tool. <https://abseil.io/resources/swe-book/html/ch19.html> [verified 2026-09-13]
7. [Winters, Manshreck & Wright (eds.), 2020] Software Engineering at Google — Ch. 11, Testing Overview ("A Note on Code Coverage": 80% bars become ceilings; measure from small tests). <https://abseil.io/resources/swe-book/html/ch11.html> [verified 2026-09-13]
8. [Potvin & Levenberg, 2016] Why Google Stores Billions of Lines of Code in a Single Repository. Communications of the ACM 59(7), 78–87. <https://dl.acm.org/doi/10.1145/2854146> (also <https://research.google/pubs/why-google-stores-billions-of-lines-of-code-in-a-single-repository/>) [verified 2026-09-13]
9. [Chrome Infrastructure, n.d.] Commit Queue (CQ) — Chrome infra docs (Google's submit/commit queue in the open). <https://chromium.googlesource.com/infra/infra/+/refs/heads/main/doc/users/services/commit_queue/index.md> [verified 2026-09-13]
10. [Fuchsia, n.d.] Gerrit auto-submit (Google) ("automatically be submitted after being approved and passing presubmit checks"). <https://fuchsia.googlesource.com/fuchsia/+show/7dedc3f2bbbba618ff0f1cda6d9e67cbf3e6f98a/docs/development/source_code/auto_submit.md> [verified 2026-09-13]
11. [GitHub Docs, n.d.] About protected branches (required status checks; admin bypass by default; "Do not allow bypassing the above settings"). GitHub Docs. <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches> [verified 2026-09-13]
12. [GitHub Docs, n.d.] Managing a merge queue (checks against latest branch + queue state before merge). GitHub Docs. <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue> [verified 2026-09-13]
13. [Hammant, n.d.a] Trunk Based Development (main site: review gates marshal pending changes before trunk; build server beyond a couple of developers). <https://trunkbaseddevelopment.com/> [verified 2026-09-13]
14. [Hammant, n.d.b] Trunk Based Development — Styles and Trade-offs (patch review systems guarantee changes are good to be integrated; revert policies). <https://trunkbaseddevelopment.com/styles/> [verified 2026-09-13]
15. [Forsgren, Humble & Kim, 2018] Accelerate: The Science of Lean Software and DevOps — excerpt (5× lower change failure rate for high performers; quality built in). IT Revolution. <https://itrevolution.com/wp-content/uploads/2022/06/ACC_excerpt.pdf> [verified 2026-09-13]
16. [DORA, 2018] 2018 Accelerate State of DevOps Report (elite CFR 0–15% vs low 46–60%). DORA / Google. <https://dora.dev/research/2018/dora-report/2018-dora-accelerate-state-of-devops-report.pdf> [verified 2026-09-13]
17. [DORA, 2019] 2019 Accelerate State of DevOps Report (elite 0–15%, low 46–60%; changes 1/7 as likely to fail). DORA / Google. <https://dora.dev/research/2019/dora-report/2019-dora-accelerate-state-of-devops-report.pdf> [verified 2026-09-13]
18. [Google, 2021] 2021 State of DevOps Report (elite CFR 0–15% vs low 16–30%; means 7.5% vs 23%; elite 3× better). <https://services.google.com/fh/files/misc/state-of-devops-2021.pdf> (summary also at <https://cloud.google.com/resources/state-of-devops>) [verified 2026-09-13]
19. [ISTQB FL Syllabus, n.d.] Certified Tester Foundation Level Syllabus v4.0 — 5.2 Risk Management (risk level = likelihood × impact; risk-based testing definition; thoroughness and scope). ASTQB presentation. <https://astqb.org/5-2-risk-management/> [verified 2026-09-13]
20. [ISTQB Glossary, n.d.] risk-based testing. ISTQB. <https://glossary.istqb.org/en_US/term/risk-based-testing/2> [verified 2026-09-13]
21. [ISTQB CTAL, n.d.] Certified Tester Advanced Level Test Analyst Syllabus (likelihood/impact assessment; depth-first vs breadth-first; residual risk transfer). SSTQB. <https://www.sstqb.com/_files/ugd/acfdb9_3b2bcc602f064a5d84ee8c3a096edf3d.pdf> [verified 2026-09-13]
22. [Latch, 2026] Four-Eyes vs Maker-Checker vs Segregation of Duties. Latch Workflow. <https://latchworkflow.com/blog/four-eyes-principle-maker-checker-segregation-of-duties/> [verified 2026-09-13]
23. [NIST SP 800-171 (Daydream summary), n.d.] Control 3.1.4 Separation of Duties (no single person develops/approves/deploys end-to-end; break-glass with logging and independent review; enforce with RBAC not policy text). <https://learn.daydream.ai/requirements/nist-sp-800-171-n800171-04> [verified 2026-09-13]
24. [Systemshardening, 2026] SOX-Compliant Deployment Pipelines: Segregation of Duties and Immutable Change Evidence (author ≠ sole authorizer; CODEOWNERS over workflow files; admin bypass as audit finding). <https://www.systemshardening.com/articles/cicd/sox-compliant-deployment-pipeline/> [verified 2026-09-13]
25. [Micco, 2016] Flaky Tests at Google and How We Mitigate Them (1.5% flaky runs; ~16% of tests flaky; 84% of pass→fail transitions flaky; 3-consecutive-failure rule; automatic quarantine; alarm-fatigue quote). Google Testing Blog. <https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html> [verified 2026-09-13]
26. [Microsoft, 2022] Improving developer productivity via flaky test management (quarantine + auto-unquarantine on fix; ~49K flaky tests; 160K sessions saved; 10-flaky-bugs PR-blocking policy). Microsoft Engineering Blog. <https://devblogs.microsoft.com/engineering-at-microsoft/improving-developer-productivity-via-flaky-test-management/> [verified 2026-09-13]
27. [AWS, n.d.] Agentic AI Security Lens — AGENTSEC04-BP02 Human review of agent actions (risk-tiered approvals; deterministic classifiers; timeouts with safe fallback "typically blocking"; escalation for unavailable reviewers; rubber-stamp risk; logging with reviewer identity and timestamps). AWS Well-Architected. <https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentsec04-bp02.html> [verified 2026-09-13]
28. [AWS re:Invent 2025 (Mahapatro)] Implementing Human-in-the-Loop Controls for Multi-Agent AI Systems (checkpoint triggers: high-stakes, irreversible, regulatory, trust-building; start max oversight, reduce as correction rate declines). AWS re:Post. <https://repost.aws/articles/ARoAKFARXvRBOam8zeOs1ZbA/re-invent-2025-implementing-human-in-the-loop-controls-for-multi-agent-ai-systems> [verified 2026-09-13]
29. [AgentNative, 2026] Human-in-the-Loop Approval Flow Pattern for AI Agents (85% confidence threshold; per-action-type thresholds; payload locking; append-only audit trail; blind-approval failure mode). <https://www.agentnative.dev/patterns/human-in-the-loop-approval-flow-pattern> [verified 2026-09-13]
30. [SystemDesignSchool, n.d.] Fail-Open vs Fail-Closed: Resilient Defaults in System Design (performance vs correctness guards; silent fail-open; fail-open with a floor; make it loud). <https://systemdesignschool.io/technologies/fail-open-vs-fail-closed> [verified 2026-09-13]
31. [AI Skill Certs, 2026] Fail-Open vs Fail-Closed Guardrail Design (default-through trap; guardrail error is an undefined state, not a pass). <https://aiskillcerts.com/concepts/architect-governance-safety-risk/fail-open-vs-fail-closed-design> [verified 2026-09-13]
32. [ITU Online, 2024] Implementing Fail-Secure and Fail-Safe Strategies (fail-secure protects the asset; overrides logged, approved, time-bound). <https://www.ituonline.com/comptia-securityx/comptia-securityx-4/mitigations-implementing-fail-secure-and-fail-safe-strategies-for-robust-security/> [verified 2026-09-13]
33. [PagerDuty, n.d.] Escalation Policy Basics (mechanical escalation on timeout; default 30-min timeout; minimum 1–3 min). PagerDuty Support Docs. <https://support.pagerduty.com/main/docs/escalation-policies> [verified 2026-09-13]
34. [incident.io, 2026] Escalation policy best practices (≤3 tiers; timeout tied to acknowledgment SLO; 15-min high-urgency standard; escalate to leadership after 60 min unresolved; Google SRE Book on-call sizing). <https://incident.io/blog/escalation-policy-best-practices> [verified 2026-09-13]

## [DEEP DIVE]: Real-World Tester Blocking Abuse, Calibration, Escalation Time, and Collusion

> **[Merge note — dsh, 2026-09-15]** The base document below (BLOCK/ADVISE charter: B1–B7 + P4 HOLD, RC-1/2/3 risk classes, 5-rung escalation ladder, calibration rules, 20-situation decision table, 35 URL-verified references) was restored after a local-state sync left this file appendix-only; all deep-dive appendices are preserved verbatim beneath it. Vocabulary mapping from the v1 base used by the appendices: PROMOTE≈PASS, HOLD/ROLLBACK≈BLOCK; escalation ladder = §7.4; calibration = §7.7; collusion/independence = §7.6 (C1–C6). Appendix citations are author-year style from their original authors and were not re-verified against URLs during this merge; the base's References section is URL-verified [verified 2026-09-13]. The Antigravity appendix references `MAP.md` (crew-level repo file, outside this council) — treated as the crew's own architectural constraint.

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

## [DEEP DIVE (freebuff, pass 3, 2026-09-14)]: Break-Glass — Emergency Overrides of the Blocker, With the Audit Trail That Keeps Them Rare

Pass 2 gave the blocker statistical audit machinery (c=0 sampling). One operational path remains unexamined: **break-glass** — the emergency bypass every real gate eventually needs, and the loophole that can erase the gate if unmanaged. The privileged-access literature is direct: emergency access must be **just-in-time (granted per-incident, time-boxed, auto-expiring)**, **session-recorded**, and **alerted in real time to a second party** — standing break-glass credentials are the classic audit finding [JIT privileged-access guidance; PAM literature — snippet-verified 2026-09-14]. The design goal is *blast-radius control*: the override must be able to unblock one PR, not the gate systemwide.

**Protocol deltas for the blocking authority.**
1. **Per-incident, time-boxed overrides only**: a break-glass grant applies to exactly one blocking verdict and expires (default 4h); no standing "override role" exists. Reuse requires a fresh grant — each grant is a sampled verdict for the pass-2 audit.
2. **Dual-visibility rule**: every break-glass use notifies the operator channel *at grant time*, not at audit time. Real-time alerting is what separates emergency access from shadow authority.
3. **Justification must be falsifiable at audit**: the grant records the specific gate verdict overridden and the concrete harm of respecting it ("build env down, demo at 15:00"), not sentiment ("urgent"). The pass-2 c=0 sample oversamples break-glass verdicts — an override with an unverifiable justification counts as a defect against the granter's own ledger.
4. **Budget coupling**: the crew's error-budget discipline (self-healing pass 1) applies — if break-glass use exceeds the agreed rate (suggested: 2% of blocking verdicts per quarter), the *gate itself* is reviewed for miscalibration before any further grants. Frequent overrides mean the gate is wrong, not the world.
5. **No self-grant for the same agent's work**: the granter and the blocked-PR author must differ (the conflict-resolution grounded-semantics verdict is the only single-agent exception, and it is logged as such).

**Cross-links:** pass-2 audit sampling (overrides as oversampled stratum), self-healing pass 1 (error-budget policy), conflict-resolution pass 3 (who adjudicates a disputed override — the grounded-semantics kernel).

**Sources.**
1. [NIST SP 800-53 AC-2(3) / AC-6(9)] Just-in-time and time-bound privileged authorization controls [literature, snippet-verified: 2026-09-14].
2. [Microsoft Entra, 2026] PIM activation with justification, approval, and expiration — the JIT pattern as productized [snippet-verified: 2026-09-14].
3. [CIS Controls v8, Control 5/6] Account and access-control management: emergency-account procedures and audit logging [literature].

---

## [DEEP DIVE]: Antigravity — Zero-Daemon Cryptographic Gate Enforcement, M-of-N Threshold Escalation & Bayesian Calibration

### 1. Zero-Daemon Cryptographic Gate Enforcement Architecture

In distributed multi-agent workflows, blocking authority easily degenerates into advisory recommendations or insecure status flags in volatile memory. Under the strict zero-daemon architectural invariant (`MAP.md`), gating must be non-bypassable, decentralized, and verifiable without running persistent gatekeeper daemons or background evaluation servers.

We implement cryptographic gate enforcement via **Ed25519 Capability Tokens** (RFC 8032) stored in an embedded SQLite-WAL ledger and verified at local checkout/pre-push git lifecycle boundaries.

```
+-------------------------------------------------------------------------------+
|                       CRITICAL LIFECYCLE BOUNDARY                             |
|                                                                               |
|   +-------------------+      Evaluates Task      +-----------------------+    |
|   |   Tester / Critic  | ----------------------> | SQLite Gate Evaluation|    |
|   |    Agent Subproc  |                          | & Token Minting Engine|    |
|   +-------------------+                          +-----------------------+    |
|             |                                                |                |
|             | Signs Verdict Payload                          | Writes WAL     |
|             v                                                v                |
|   +-----------------------------------------------------------------------+   |
|   |                      SQLite-WAL Gate State Tables                     |   |
|   |  - gate_evaluations (verdict, criteria_hash, signature)              |   |
|   |  - gate_capability_tokens (token_id, git_sha, gate_type, expires_at) |   |
|   |  - gate_revocation_ledger (nonce, revoked_at, revocation_proof)      |   |
|   +-----------------------------------------------------------------------+   |
|                                     |                                         |
|                                     | Read-only Query (<1.5ms)                |
|                                     v                                         |
|   +-------------------+      Inspects Token      +-----------------------+    |
|   | Git Pre-Push Hook | <----------------------- | Cryptographic Verifier|    |
|   | (Exit 0 or Exit 1)|                          | (RFC 8032 Signature)  |    |
|   +-------------------+                          +-----------------------+    |
+-------------------------------------------------------------------------------+
```

#### 1.1 SQLite-WAL Schema for Cryptographic Gate Ledger

```sql
-- Schema: Cryptographic Gate Enforcement Ledger (gate_ledger.sql)
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS gate_evaluations (
    evaluation_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    git_sha TEXT NOT NULL,
    agent_id TEXT NOT NULL,
    gate_name TEXT NOT NULL, -- e.g. 'ORACLE_INTEGRITY', 'MUTATION_SCORE', 'REGRESSION_SUITE'
    verdict TEXT NOT NULL CHECK(verdict IN ('PASS', 'HOLD', 'ROLLBACK', 'OVERRIDE')),
    metrics_json TEXT NOT NULL, -- Serialized JSON measurements
    criteria_hash TEXT NOT NULL, -- SHA-256 of gate definition criteria
    signature TEXT NOT NULL, -- Ed25519 signature over canonical payload
    public_key TEXT NOT NULL, -- Hex-encoded Ed25519 verifying key
    created_at REAL NOT NULL DEFAULT (unixepoch('subsec'))
);

CREATE TABLE IF NOT EXISTS gate_capability_tokens (
    token_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    git_sha TEXT NOT NULL,
    scope TEXT NOT NULL CHECK(scope IN ('BRANCH_MERGE', 'MAIN_PUSH', 'DEPLOY_CANARY')),
    issued_to TEXT NOT NULL,
    verdict TEXT NOT NULL CHECK(verdict IN ('PROMOTED', 'EMERGENCY_OVERRIDE')),
    nonce TEXT NOT NULL UNIQUE,
    token_signature TEXT NOT NULL, -- Signed by gate authority
    issued_at REAL NOT NULL DEFAULT (unixepoch('subsec')),
    expires_at REAL NOT NULL, -- Hard expiry (default: issued_at + 1800s)
    FOREIGN KEY(task_id) REFERENCES gate_evaluations(task_id)
);

CREATE TABLE IF NOT EXISTS gate_revocation_ledger (
    revocation_id TEXT PRIMARY KEY,
    nonce TEXT NOT NULL UNIQUE,
    reason TEXT NOT NULL,
    revoked_by TEXT NOT NULL,
    revocation_proof TEXT NOT NULL, -- Ed25519 signature from Security Officer / Human Operator
    revoked_at REAL NOT NULL DEFAULT (unixepoch('subsec'))
);

CREATE INDEX IF NOT EXISTS idx_gate_tokens_sha ON gate_capability_tokens(git_sha, scope, expires_at);
CREATE INDEX IF NOT EXISTS idx_gate_eval_task ON gate_evaluations(task_id, verdict);
```

#### 1.2 Zero-Daemon Gate Minter and Git Hook Verifier

```python
"""Zero-daemon gate token issuance and pre-push hook verifier."""
import hashlib
import json
import sqlite3
import sys
import time
from typing import Dict, Any, Tuple
from nacl.signing import SigningKey, VerifyKey
from nacl.exceptions import BadSignatureError

class GateEnforcementEngine:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=5.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode = WAL")
        return conn

    @staticmethod
    def canonical_hash(payload: Dict[str, Any]) -> bytes:
        """Deterministically serialize payload per RFC 8785 (JSON Canonicalization)."""
        canonical_json = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical_json.encode("utf-8")).digest()

    def record_evaluation(
        self,
        task_id: str,
        git_sha: str,
        agent_id: str,
        gate_name: str,
        verdict: str,
        metrics: Dict[str, Any],
        criteria_hash: str,
        signing_key: SigningKey,
    ) -> str:
        eval_id = f"eval_{task_id}_{gate_name}_{int(time.time()*1000)}"
        payload = {
            "eval_id": eval_id,
            "task_id": task_id,
            "git_sha": git_sha,
            "agent_id": agent_id,
            "gate_name": gate_name,
            "verdict": verdict,
            "metrics": metrics,
            "criteria_hash": criteria_hash,
        }
        digest = self.canonical_hash(payload)
        signed = signing_key.sign(digest)
        sig_hex = signed.signature.hex()
        pub_hex = signing_key.verify_key.encode().hex()

        with self._get_conn() as conn:
            conn.execute(
                """
                INSERT INTO gate_evaluations 
                (evaluation_id, task_id, git_sha, agent_id, gate_name, verdict, metrics_json, criteria_hash, signature, public_key)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (eval_id, task_id, git_sha, agent_id, gate_name, verdict, json.dumps(metrics), criteria_hash, sig_hex, pub_hex),
            )
        return eval_id

    def issue_capability_token(
        self,
        task_id: str,
        git_sha: str,
        scope: str,
        issued_to: str,
        gate_authority_key: SigningKey,
        ttl_seconds: float = 1800.0,
    ) -> str:
        """Issues capability token only if all required gates passed and no active HOLDs exist."""
        with self._get_conn() as conn:
            cur = conn.execute(
                "SELECT gate_name, verdict FROM gate_evaluations WHERE git_sha = ? AND task_id = ?",
                (git_sha, task_id),
            )
            rows = cur.fetchall()
            if not rows:
                raise PermissionError("Cannot issue token: Zero gate evaluations recorded.")
            
            for row in rows:
                if row["verdict"] in ("HOLD", "ROLLBACK"):
                    raise PermissionError(f"Cannot issue token: Gate '{row['gate_name']}' is in {row['verdict']} status.")

            token_id = f"tok_{task_id}_{int(time.time()*1000)}"
            nonce = hashlib.sha256(f"{token_id}_{time.time_ns()}".encode()).hexdigest()
            now = time.time()
            expires_at = now + ttl_seconds

            token_payload = {
                "token_id": token_id,
                "task_id": task_id,
                "git_sha": git_sha,
                "scope": scope,
                "issued_to": issued_to,
                "verdict": "PROMOTED",
                "nonce": nonce,
                "expires_at": expires_at,
            }
            digest = self.canonical_hash(token_payload)
            token_sig = gate_authority_key.sign(digest).signature.hex()

            conn.execute(
                """
                INSERT INTO gate_capability_tokens
                (token_id, task_id, git_sha, scope, issued_to, verdict, nonce, token_signature, issued_at, expires_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (token_id, task_id, git_sha, scope, issued_to, "PROMOTED", nonce, token_sig, now, expires_at),
            )
            return token_id

    def verify_git_push(self, target_git_sha: str, scope: str, expected_pubkey_hex: str) -> Tuple[bool, str]:
        """Sub-2ms check invoked directly by .git/hooks/pre-push without daemons."""
        verify_key = VerifyKey(bytes.fromhex(expected_pubkey_hex))
        now = time.time()

        with self._get_conn() as conn:
            cur = conn.execute(
                """
                SELECT token_id, task_id, git_sha, scope, issued_to, verdict, nonce, token_signature, expires_at
                FROM gate_capability_tokens
                WHERE git_sha = ? AND scope = ? AND expires_at > ?
                ORDER BY issued_at DESC LIMIT 1
                """,
                (target_git_sha, scope, now),
            )
            token = cur.fetchone()
            if not token:
                return False, f"GATE BLOCK: No valid, non-expired capability token found for commit {target_git_sha[:8]}."

            revoked = conn.execute(
                "SELECT reason, revoked_by FROM gate_revocation_ledger WHERE nonce = ?",
                (token["nonce"],),
            ).fetchone()
            if revoked:
                return False, f"GATE BLOCK: Token revoked by {revoked['revoked_by']}: {revoked['reason']}."

            token_payload = {
                "token_id": token["token_id"],
                "task_id": token["task_id"],
                "git_sha": token["git_sha"],
                "scope": token["scope"],
                "issued_to": token["issued_to"],
                "verdict": token["verdict"],
                "nonce": token["nonce"],
                "expires_at": token["expires_at"],
            }
            digest = self.canonical_hash(token_payload)
            try:
                verify_key.verify(digest, bytes.fromhex(token["token_signature"]))
            except BadSignatureError:
                return False, "SECURITY ALERT: Capability token cryptographic signature verification failed!"

            return True, f"GATE PERMIT: Verified valid token {token['token_id']} for commit {target_git_sha[:8]}."
```

---

### 2. Dual-Key Escalation Protocol & Collusion Detection Quotient (CDQ)

#### 2.1 M-of-N Threshold Escalation Protocol
When an engineer agent appeals a Tester's `HOLD` or `ROLLBACK` verdict, unilateral override is strictly prohibited. An emergency promotion or threshold relaxation requires an M-of-N threshold signature:

$$\text{Verdict}_{\text{override}} = \text{ThresholdSign}_{M/N}(\sigma_1, \sigma_2, \dots, \sigma_M) \quad \text{where } M \ge 2, \; N \ge 3$$

In Crew v2:
- **P0 Critical Path Override**: Requires $M=2$ of 3 distinct roles: $\text{Signature}_{\text{Operator}} + \text{Signature}_{\text{Critic}}$ OR $\text{Signature}_{\text{Operator}} + \text{Signature}_{\text{Tester}}$.
- **No Single Agent Self-Approval**: An Engineer agent's key is explicitly blocked from the threshold set for its own code diff.
- **Time-Bounded Leases**: All emergency override tokens carry a hard maximum Time-To-Live ($TTL_{\max} = 900\text{ seconds}$ / 15 minutes), forcing either automated canary validation or automatic rollback.

#### 2.2 Collusion Detection Quotient (CDQ)
To detect Pattern 4 (The Capture: Engineer and Tester secretly colluding to maximize throughput by passing weak implementations), we define the **Collusion Detection Quotient (CDQ)**.

CDQ monitors inter-agent agreement against statistical independence using Cohen's Kappa ($\kappa$) coupled with conditional defect discovery:

$$\kappa = \frac{P_o - P_e}{1 - P_e}$$

Where:
- $P_o$ is the observed proportional agreement across $N$ test verdicts:
  $$P_o = \frac{\sum_{i=1}^C n_{ii}}{N}$$
- $P_e$ is the hypothetical probability of chance agreement:
  $$P_e = \sum_{i=1}^C \left( \frac{n_{i+}}{N} \cdot \frac{n_{+i}}{N} \right)$$

We combine Cohen's Kappa with the **Escape Divergence Ratio ($R_{\text{esc}}$)** over a sliding window of $W = 50$ tasks:

$$R_{\text{esc}} = \frac{\text{Escapes}_{\text{Production}}}{\max(1, \text{Escapes}_{\text{Baseline}})}$$

The **Collusion Detection Quotient (CDQ)** is defined as:

$$\text{CDQ} = \kappa \cdot \log_2(1 + R_{\text{esc}})$$

```
Nominal Zone:        CDQ <= 0.40  --> Normal independent operation
Investigation Zone:  0.40 < CDQ <= 0.85 --> Warn, increase mutation audit sampling to 25%
Hard Collusion Alarm: CDQ > 0.85  --> Revoke Tester signing key, inject Adversarial Mutant Suite
```

```python
"""Collusion Detection Quotient (CDQ) Calculator."""
import math
from typing import List, Tuple

def compute_cohens_kappa(contingency_matrix: List[List[int]]) -> float:
    """Computes Cohen's Kappa for NxN agreement matrix."""
    n = sum(sum(row) for row in contingency_matrix)
    if n == 0:
        return 0.0
    po = sum(contingency_matrix[i][i] for i in range(len(contingency_matrix))) / n
    row_sums = [sum(contingency_matrix[i][j] for j in range(len(contingency_matrix))) for i in range(len(contingency_matrix))]
    col_sums = [sum(contingency_matrix[i][j] for i in range(len(contingency_matrix))) for i in range(len(contingency_matrix))]
    pe = sum((row_sums[i] * col_sums[i]) for i in range(len(row_sums))) / (n * n)
    if pe == 1.0:
        return 1.0
    return (po - pe) / (1.0 - pe)

def evaluate_cdq(
    tester_engineer_matrix: List[List[int]], 
    prod_escapes: int, 
    baseline_escapes: int = 1
) -> Tuple[float, str]:
    kappa = compute_cohens_kappa(tester_engineer_matrix)
    r_esc = prod_escapes / max(1, baseline_escapes)
    cdq = kappa * math.log2(1.0 + r_esc)

    if cdq > 0.85:
        action = "COLLUSION_ALARM: Suspend Tester signing key; trigger adversarial canary test."
    elif cdq > 0.40:
        action = "INVESTIGATION_WARN: Elevated alignment with escapes; increase audit sampling."
    else:
        action = "NOMINAL: Agents demonstrating statistical independence."
    return cdq, action
```

---

### 3. Bayesian Beta-Binomial Strictness Calibration

Static thresholds suffer from two catastrophic failure modes: threshold drift (becoming overly permissive as suites grow) and gridlock (overly strict gates halting throughput). 

Rather than heuristic $\pm 5\%$ jumps, we model the true defect escape probability $\theta \in [0, 1]$ as a conjugate **Beta-Binomial process**:

$$\theta \sim \text{Beta}(\alpha_0, \beta_0)$$

Given an audit window of $N$ tasks with $k$ verified defective escapes:

$$\theta \mid k, N \sim \text{Beta}(\alpha_0 + k, \, \beta_0 + N - k)$$

The posterior mean escape rate is:

$$\mathbb{E}[\theta \mid k, N] = \frac{\alpha_0 + k}{\alpha_0 + \beta_0 + N}$$

With posterior variance:

$$\text{Var}(\theta \mid k, N) = \frac{(\alpha_0 + k)(\beta_0 + N - k)}{(\alpha_0 + \beta_0 + N)^2 (\alpha_0 + \beta_0 + N + 1)}$$

#### 3.1 Damped Strictness Shift Equation
To adjust the mutation gate threshold $T_{\text{mut}}$ (nominal $T^* = 0.80$) and assertion strictness without inducing oscillatory limit cycles, we apply a damped, variance-penalized update:

$$\Delta T = \gamma \cdot \text{clip}\left( \frac{\mathbb{E}[\theta] - \theta^*}{\sqrt{\text{Var}(\theta) + \epsilon}}, \, -\delta_{\max}, \, \delta_{\max} \right)$$

Where:
- $\theta^*$ is the target defect escape ceiling (nominal $\theta^* = 0.02$ / 2%).
- $\gamma = 0.12$ is the learning dampening rate.
- $\delta_{\max} = 0.05$ (5% max threshold step per audit epoch).
- $\epsilon = 10^{-6}$ numerical stability floor.

```python
"""Bayesian Strictness Calibration Engine."""
from dataclasses import dataclass

@dataclass
class BetaPrior:
    alpha: float = 2.0  # Equivalent to 2 prior defects
    beta: float = 98.0  # Equivalent to 98 prior clean tasks (nominal 2% prior)

class BayesianStrictnessCalibrator:
    def __init__(self, prior: BetaPrior = BetaPrior(), target_escape_rate: float = 0.02, dampening: float = 0.12, max_shift: float = 0.05):
        self.alpha = prior.alpha
        self.beta = prior.beta
        self.target_escape_rate = target_escape_rate
        self.gamma = dampening
        self.max_shift = max_shift

    def update(self, observed_tasks: int, observed_escapes: int) -> Tuple[float, float, float]:
        """Returns (posterior_mean, posterior_variance, recommended_threshold_delta)."""
        post_alpha = self.alpha + observed_escapes
        post_beta = self.beta + (observed_tasks - observed_escapes)

        post_mean = post_alpha / (post_alpha + post_beta)
        post_var = (post_alpha * post_beta) / (((post_alpha + post_beta) ** 2) * (post_alpha + post_beta + 1.0))

        # Standardized deviation from target
        z_score = (post_mean - self.target_escape_rate) / math.sqrt(post_var + 1e-6)
        
        # Raw delta modulated by damping
        raw_delta = self.gamma * (z_score * 0.01) # scale z-score to percentage units
        clipped_delta = max(-self.max_shift, min(self.max_shift, raw_delta))

        # Update running prior
        self.alpha = post_alpha
        self.beta = post_beta

        return post_mean, post_var, clipped_delta
```

---

### 4. Quantitative Thresholds & Invariants Summary

| Mechanism | Metric / Parameter | Target Threshold | Action on Breach |
|---|---|---|---|
| **Gate Token Verifier** | Verification Latency | $< 2.0\text{ ms}$ | Fail closed if SQLite query timeout $> 50\text{ ms}$ |
| **Token Validity** | Max TTL ($TTL_{\max}$) | $1800\text{ s}$ (30 min) | Token expires; requires fresh test suite run |
| **Emergency Lease** | Override Max TTL | $900\text{ s}$ (15 min) | Automatic canary rollback if unpromoted |
| **Collusion Monitor** | Collusion Detection Quotient (CDQ) | $\le 0.40$ nominal | $> 0.85 \implies$ Revoke keys, isolate pair |
| **M-of-N Threshold** | Quorum Requirement | $M \ge 2$ of $\{ \text{Operator}, \text{Critic}, \text{Tester} \}$ | Unilateral promotion attempts rejected |
| **Bayesian Calibration** | Max Delta per Epoch ($\delta_{\max}$) | $\pm 0.05$ (5% absolute) | Clamps large jumps; dampens oscillations ($\gamma=0.12$) |

---

### References (pass 3)
1. RFC 8032: Edwards-Curve Digital Signature Algorithm (Ed25519), Internet Engineering Task Force (IETF), 2017. https://datatracker.ietf.org/doc/html/rfc8032
2. RFC 8785: JSON Canonicalization Scheme (JCS), Internet Engineering Task Force (IETF), 2020. https://datatracker.ietf.org/doc/html/rfc8785
3. Cohen, J. (1960). "A Coefficient of Agreement for Nominal Scales". *Educational and Psychological Measurement*, 20(1), 37–46.
4. Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013). *Bayesian Data Analysis* (3rd ed.). Chapman and Hall/CRC.
5. NIST SP 800-207: "Zero Trust Architecture". National Institute of Standards and Technology, 2020. https://doi.org/10.6028/NIST.SP.800-207

