# Testing Maturity Model for an AI Agent Crew — 5 Levels with Measurable Criteria (ACTM)

> **Scope:** A survey of existing test-maturity models, a purpose-built 5-level maturity model for an LLM multi-agent crew ("AI-Crew Testing Maturity", ACTM), an evidence-based assessment of where Crew v2 stands today, and a migration path to Level 5 with a runnable assessment rubric.
> **Research date:** 2026-09-13. All web sources verified on this date. Internal trial evidence (COORD-01, COORD-02, T09–T12, DECISIVE-01, P4) is cited as `[internal: …]` per the council context file and is not web-referenced.

## Executive Summary

Existing test-maturity models — TMMi (5 levels, 16 process areas), TPI NEXT (key areas with A–D level scales and checkpoints), CMMI (the structural parent of TMMi), ISTQB's expert-level test-process-improvement track, Google's internal Test Certified program (5 levels, one quarter per step), and the Capgemini/Sogeti World Quality Report — are well documented but none addresses the specific failure modes of an LLM agent crew: non-deterministic outputs, SOUL-file "process definitions", agents with no blocking authority, and behavior that cannot be asserted exactly. This document defines the **AI-Crew Testing Maturity (ACTM) model**: L1 *Ad Hoc* → L2 *Gated* → L3 *Institutionalized* → L4 *Measured & Eval-Driven* → L5 *Self-Verifying*, each level carrying entry criteria, numeric gates, required practices and tooling, exit criteria, failure modes, and a calendar estimate grounded in published transition data. Assessed against ACTM, **Crew v2 sits at Level 1 (0 of 5 L2 gates passing)** — the engineer produced zero test files across COORD-01/COORD-02, no agent can block untested code, the completer does not run tests, and fixed bugs recurred because they were never regression-tested (T09–T12). The migration path is deliberately front-loaded with quick wins (SOUL edits + a GitHub Actions gate reach L2 in 1–2 weeks), followed by structural changes (tester agent with blocking authority, regression corpus, then numeric gates and statistically-reported evals), and the operator can re-assess with the pass/fail rubric in §Detailed Analysis D.5 at any time.

## Key Findings

### On the existing landscape (survey)

- TMMi is the dominant test-maturity model: 5 maturity levels (Initial → Managed → Defined → Measured → Optimization) and 16 process areas in release R1.2, arranged 5+5+3+3 across Levels 2–5 [TMMi Foundation, 2018]. A V2.0 of the framework adds a sixth Level-2 process area, "Implementation and Habit" [TMMi Foundation via ISQI, n.d.].
- TMMi's structure is "largely based on the structure of the CMMI" [TMMi Foundation, n.d.-a]; CMMI itself does not define testing-specific process areas, which is the gap TMMi fills [Experimentus, 2017].
- TPI (Sogeti), the predecessor of TPI NEXT, pioneered the *continuous* alternative to staged models: 20 key areas, each graded A–D against objective **checkpoints**, arranged in a Test Maturity Matrix of 13 scales grouped into Controlled / Efficient / Optimizing, with explicit dependencies between key areas (e.g., Metrics level A requires Defect management level B) [Andersin, n.d.]. TPI NEXT keeps the assessment-plus-roadmap approach and adds business drivers (time, cost, quality) [Sogeti/TMAP, n.d.].
- Google's Test Certified program — the closest published analogue to a *team-level* (not org-level) maturity ladder — had 3 levels originally [Bland, 2011] and 5 levels in total later; each step up was designed to be "accomplished within a quarter" [Google, 2020]. The inbox brief's claim of "7 levels" **could not be verified**; all primary sources say 3, later 5.
- Empirical support for maturity models is real but thin and contested: TMMi's 2023 user survey reports 94% of users seeing product-quality benefits and 78% test-efficiency benefits [TMMi Foundation, 2023], with case studies including an embedded-software company that raised defect detection from 78% to 96% while moving from Level 1 to Level 3 **over 4 years** [TMMi Foundation, 2023]. But systematic reviews of maturity models repeatedly flag "limited empirical studies on their validation" [Tarhan et al., 2016], lack of impact-on-performance evidence [Smajli et al., 2024], and weak theoretical foundations in newer models [Jabbari et al., 2021]; James Bach's critique argues the empirical case for CMM-style models can never be closed without controlled comparisons [Bach, n.d.].
- Published transition times for human organizations: medians of 26.5 months to move CMM Level 1→2 and 24 months for Level 2→3 [Herbsleb & Paulk, 1997]; TMMi consultancies state most organizations need 12–18 months to reach Level 3 and another 6–12 months for Level 4 [TestFort, 2025]. Google's team-level ladder compressed this to ~1 quarter per level [Google, 2020].
- For the AI era: the World Quality Report 2025-26 finds 89% of organizations piloting or deploying GenAI-augmented workflows (37% in production) but only 15% have scaled GenAI in QA enterprise-wide, with 60% struggling to obtain secure, scalable test data [Capgemini, 2025]; DORA's 2024 report found AI adoption *reduces* delivery stability (−7.2% per 25% AI adoption) and explicitly names "small batch sizes and robust testing" as the antidote [DORA, 2024].
- A peer-reviewed extension of TMMi for AI agents already exists in the security domain (16 "Agent Security Test Process Areas" across Levels 2–5, mirroring TMMi's 5+5+3+3) [Extending the TMMi Framework, n.d.] — evidence that adapting TMMi to agent crews is an accepted research direction, though the publication's authors/venue could not be verified from the sources seen.

### On thresholds (what the evidence actually says)

- Coverage: Google's testing blog states project-wide goals above 90% are "most likely not worth it", per-commit coverage goals of 99% are "reasonable", and **90% is a good lower bound** [Google Testing Blog, 2020].
- Flakiness: at Google, "almost 16% of our tests have some level of flakiness" and about 1.5% of all test runs report a flaky result [Micco, 2016]; a survey found 59% of developers deal with flaky tests at least monthly [Parry et al., 2021]. Google's Test Certified higher levels required *removing* nondeterministic tests entirely [Google, 2020].
- Mutation: in an IEEE TSE study of open-source mutation-testing users, 34.6% defined a minimal mutation-coverage threshold and 27.9% enforced a minimal mutation score during the build [Sánchez et al., 2024]; Google's analysis of ~15M mutants found **70% of high-priority bugs were coupled with a mutant** that, if reported, could have prevented the bug [Petrović et al., 2021].
- Agent evals: evals are experiments and need standard errors, resampling, and paired comparisons — "in neither case should the sampling temperature be adjusted for the sake of reducing variance" [Miller, 2024]; agent-evaluation surveys flag cost-efficiency, safety, robustness, and fine-grained scalable evaluation as the field's critical gaps [Yehudai et al., 2025].

### On Crew v2's current state (internal evidence)

- The engineer produced **zero test files** in COORD-01 (3 runs) and COORD-02 (4 modules, 135 lines); the operator had to write 11 tests manually (all passed) `[internal: COORD-01, COORD-02]`.
- **No agent has blocking authority** — no one can say "this is not done" — and the completer does not run tests before release `[internal: crew logs]`.
- Fixed bugs **recurred** because the original failure cases were never regression-tested (T09–T12) `[internal: T09–T12]`.
- Positive assets: a testing philosophy exists (`TESTING-COUNCIL.md`: behavior-not-implementation, 70/20/10 pyramid, tester may block), the target stack is already chosen (pytest, Hypothesis, mutmut, coverage.py, GitHub Actions), and the P4 "HOLD-on-unverified" doctrine is canonized crew law — a normative foundation Level 2 can build on `[internal: context §3, §2]`.
- DECISIVE-01 showed single-agent beats pipeline on weak-class tasks (12/16 vs 10/16 vs 8/16) — the maturity model must gate by **task class**, not blanket-pipeline everything `[internal: DECISIVE-01]`.

### On what a crew-specific model must add beyond TMMi

- **Blocking authority is an organizational property, not a tooling property**: for agents, "process definition" lives in SOUL files and must be assessed as such; TMMi's Level-3 "Test Organization" process area maps directly to "tester agent with veto power" [TMMi Foundation, 2018].
- **Non-deterministic outputs need eval gates, not exact-match assertions**: assert properties of outputs, measure pass rates across runs, and report uncertainty [Miller, 2024; Thinking Machines Lab, 2025].
- **Regression-capture rate** (the % of past failure cases with a permanent automated test) is the crew-specific metric that would have directly prevented T09–T12's recurrences; no existing external model defines it, so ACTM defines it and marks its thresholds as proposed defaults.
- **Automated test generation from failures is proven at industrial scale**: Meta's ACH system generated 571 mutation-guided privacy tests from 9,095 mutants across 10,795 classes, with 73% engineer acceptance — the existence proof for ACTM Level 5 [Harman et al., 2025].

## Detailed Analysis

### A. Survey of existing maturity models

#### A.1 TMMi — Test Maturity Model Integration (TMMi Foundation)

TMMi is a staged test-process-improvement model developed by the TMMi Foundation; its structure is "largely based on the structure of the CMMI" [TMMi Foundation, n.d.-a] and it is explicitly positioned as complementary to CMMI [Experimentus, 2017]. All organizations start at Level 1 [TMMi Foundation, n.d.-a]. The framework R1.2 defines 5 levels and 16 process areas (PAs), distributed 5+5+3+3 across Levels 2–5; drill-down reaches 843 assessable sub-practices [Experimentus, 2017; TMMi Foundation, 2018]:

| Level | Name | Process areas |
|---|---|---|
| 1 | Initial | — (chaotic, ad hoc; testing is informal) |
| 2 | Managed | Test Policy and Strategy · Test Planning · Test Monitoring and Control · Test Design and Execution · Test Environment |
| 3 | Defined | Test Organization · Test Training Program · Test Lifecycle and Integration · Non-Functional Testing · Peer Reviews |
| 4 | Measured | Test Measurement · Product Quality Evaluation · Advanced Reviews |
| 5 | Optimization | Defect Prevention · Quality Control · Test Process Optimization |

[TMMi Foundation, 2018]

Level 2 is project/team-level managed testing (test policy, planning, monitoring/control, design/execution, environments); Level 3 standardizes testing across the organization, trains people, integrates testing early in the lifecycle, plans non-functional testing, and introduces peer reviews; Level 4 makes both process and product quality measured; Level 5 is continuous optimization toward defect prevention [TMMi Foundation, n.d.-a; TMMi Foundation, 2018]. The current **TMMi Framework V2.0** adds a sixth Level-2 process area, *Implementation and Habit* (governance, infrastructure, configuration management) [TMMi Foundation via ISQI, n.d.] — its release date could not be verified from the sources seen. Assessments exist in informal (gap analysis) and formal (certification) forms [Experimentus, 2017].

**Evidence of value:** the 2nd TMMi world-wide user survey (published 2023) reports benefits in product quality for 94% of users, test efficiency for 78%, compliance for 85%, and people/discipline for 61%; case examples include a government department saving 40% after certifying to Level 3, a bank saving 8% of its entire IT budget while improving output 12%, an insurer saving £440,000 on a £2m project, a retailer saving ≥12% per project, and an embedded-software company improving defect detection from 78% to 96% over a **4-year** move from Level 1 to 3 [TMMi Foundation, 2023]. Academic status reporting confirms TMMi as the leading model in worldwide use [van Veenendaal et al., 2022; Garousi & Felderer, 2021].

#### A.2 TPI NEXT (Sogeti)

TPI NEXT is Sogeti's model for assessing and improving the test process itself; the original **TPI** model (documented in detail in a publicly hosted description [Andersin, n.d.]) defined **20 key areas** grouped under four cornerstones derived from TMap — Life cycle, Organisation, Infrastructure, and Tools/Techniques — with each key area graded on **ascending levels (generally A to D)**. A key area reaches a level only when it "passes all the checkpoints of a certain level" — checkpoints are concrete requirements [Andersin, n.d.]. The **Test Maturity Matrix** places all key areas on **13 scales of maturity** grouped into three categories: *Controlled* (scales 1–5), *Efficient* (scales 6–10), *Optimizing* (scales 11–13) [Andersin, n.d.]. Crucially, TPI made dependencies explicit: "before statistics can be gathered for defects found (level A of key area Metrics) the test process has to classify for level B of key area Defect management" — and levels are all-or-nothing: "As long as a test process is not entirely classified at level B, it remains at level A" [Andersin, n.d.]. TPI NEXT modernized this into a business-driver-driven assessment (time, cost, quality) with an accompanying tool for prioritizing the improvement roadmap [Sogeti/TMAP, n.d.]; secondary descriptions characterize TPI NEXT as 16 key areas with four maturity levels (Initial, Controlled, Efficient, Optimizing) [AgileTest, 2025] — I could not verify the 16-key-area count from a primary Sogeti source, so treat that figure as secondary.

**What ACTM borrows:** objective checkpoints per level, all-or-nothing level classification, and explicit cross-area dependencies (Metrics requires Defect management) — directly reflected in the ACTM rubric (§D.5), where e.g. the L4 mutation gate depends on the L2 CI gate.

#### A.3 CMMI's relationship to testing maturity

CMMI (Capability Maturity Model Integration) is the general process-maturity framework whose staged representation TMMi reuses [TMMi Foundation, n.d.-a; Experimentus, 2017]; CMMI appraisals certify organizational process maturity but contain no testing-specific process areas, which is precisely why TMMi exists as a "specialized framework focused on enhancing software testing processes… complements CMMI" [NozomTechs, 2024 — secondary]. The most-cited empirical anchor for CMM-level transitions is Herbsleb & Paulk's CACM analysis of SEI appraisal data: **median time to move Level 1→2 was 26.5 months; Level 2→3 was 24 months** [Herbsleb & Paulk, 1997]. Human-organization data like this is the *upper* anchor for ACTM's calendar estimates; a single crew with one repo and existing tooling should be dramatically faster (see §B's per-level estimates and the explicit caveats there).

#### A.4 ISTQB test process improvement context

ISTQB (the International Software Testing Qualifications Board) operates an Expert Level certification, *Improving the Test Process* (CTEL-ITP), comprising two parts: "Assessing the Test Process" and "Implementing Test Process Improvement" — i.e., the industry's formal training path for people who run maturity assessments and improvement programs of the TMMi/TPI NEXT type [ISTQB, n.d.]. For ACTM's purposes, ISTQB's contribution is the doctrine that assessment and implementation are **separate competencies with separate lifecycles** — ACTM mirrors this by separating the assessment rubric (§D.5) from the migration program (§D.1–D.4).

#### A.5 Google's Test Certified program

Test Certified (TC) was Google's internal, Testing Grouplet-run ladder for getting teams to improve developer testing; it was created ~2006 and became the focus of the Testing Grouplet and Test Mercenaries from mid-2007 [Bland, 2011]. Key verified facts:

- TC originally comprised **three levels**; "Eventually a Level Four and a Level Five was added, with more stringent coverage goals and tasks incorporating other tools such as static analysis tools" [Bland, 2011]. The SWE-at-Google book (O'Reilly [O'Reilly, 2020]; chapter freely readable at [Google, 2020]) states the program "was organized into five levels, and each level required some concrete actions to improve the test hygiene on the team… each step up could be accomplished within a quarter, which made it a convenient fit for Google's internal planning cadence" [Google, 2020]. The program is also documented in *How Google Tests Software* (pp. 54ff) [Whittaker et al., 2012].
- **Level 1** — "set up a continuous build; start tracking code coverage; classify all your tests as small, medium, or large; identify (but don't necessarily fix) flaky tests; and create a set of fast (not necessarily comprehensive) tests that can be run quickly" [Google, 2020]; "designed to be easy to achieve within a day or five of effort, by one or two engineers" [Bland, 2011].
- **Level 2** — a written policy "that essentially forbade anyone from submitting untested code, as well as goals for test coverage and a balance between small, medium, and large tests"; teams could draft the policy immediately and "spend a couple weeks or months working towards the coverage and test-balance goals" [Bland, 2011].
- **Level 3** — "the model of a smooth-running testing process… sustained high coverage for all types of developer tests across the board… as well as low tolerance for broken or flaky tests… an on-going, long-term commitment" [Bland, 2011]; later levels added "no releases with broken tests" and "remove all nondeterministic tests" [Google, 2020].
- **Level 5 (book description)** — "all tests were automated, fast tests were running before every commit, all nondeterminism had been removed, and every behavior was covered" [Google, 2020].
- Certification ran through mentors and peer review; an internal dashboard "applied social pressure by showing the level of every team", and teams competed to climb [Google, 2020]. By the time TC was replaced by an automated approach in 2015, it had helped more than 1,500 projects [Google, 2020].

**The inbox brief's "7 levels" claim could not be verified** — every primary source says 3 levels originally, 5 in total after expansion [Bland, 2011; Google, 2020].

TC is ACTM's most important precedent because it is *team-scoped, cookbook-style, and measurable* — exactly the shape a crew of agents needs, and the source of ACTM's "each level must be reachable in a small number of weeks for a crew" calibration.

#### A.6 World Quality Report (Capgemini/Sogeti/OpenText)

The World Quality Report is the annual global study of quality engineering and testing, published by Sogeti and Capgemini (with OpenText as strategic technology partner since the 16th edition) and analyzes the field "across 3 dimensions – Technology & Practices, Industries and Geographies" [Sogeti, 2024]. Maturity-relevant verified findings:

- WQR 2025-26 (17th edition): 89% of responding organizations are piloting or deploying GenAI-augmented workflows, with 37% in production [Capgemini, 2025]; **43% of organizations are experimenting with Gen AI in QA, but only 15% have scaled it enterprise-wide** — "a big gap between ambition and adoption"; 60% struggle with secure, scalable test data and 58% cite challenges adopting AI-powered tools, "underscoring why automation maturity remains elusive"; GenAI is the top-ranked skill for quality engineers (63%), ahead of core quality engineering skills (60%) and soft skills (51%) [Capgemini, 2025].
- WQR 2024-25 declared GenAI-augmented Quality Engineering "the new future" [RockerTester, 2024; Sogeti, 2024].

For ACTM, the WQR supplies the macro context: the industry's QA function is itself early-maturity in AI (15% scaled), so a crew-level maturity model must be self-contained rather than assume an experienced parent QA org.

#### A.7 Peer-reviewed validation, benefits, and criticisms

- **Benefits/ROI:** TMMi user-survey and case-study data above (§A.1) [TMMi Foundation, 2023; Garousi & Felderer, 2021; van Veenendaal et al., 2022]. A case study in the financial domain reports TMMi assessment and improvement producing productivity benefits such as a production cycle shortened from three months to under one (insurance, Level 3) and test-execution improvements (bank, Level 3) [Science Publishing Group, n.d.].
- **Criticisms:** Tarhan et al.'s systematic literature review of business-process maturity models found "limited empirical studies on their validation and a limited extent of actionable properties" [Tarhan et al., 2016]. Smajli et al.'s follow-up work reports "the lack of empirical studies on the impact on performance, the lack of prescriptive…" guidance as recurring limitations [Smajli et al., 2024]. Jabbari et al. note that "new maturity models suffer from lack of empirical validation, operationalising maturity measurement, and theoretical foundations" [Jabbari et al., 2021]. Bach argues that without controlled comparison of alternative process models "the empirical case can never be closed" [Bach, n.d.]. A dedicated systematic review of software test maturity models exists [Ramos et al., 2018 — full article URL not shown in search results; host seen], and a 2025 measurement framework paper continues the critique tradition for software maturity models generally [Alshareef, 2025].

**ACTM's response to the criticisms:** every level is defined by *measurable, machine-checkable criteria* (CI outcomes, coverage reports, mutation scores, flake ledgers) rather than self-reported practice adoption; every threshold carries either a citation or an explicit "proposed default + reasoning" label; and the model is falsifiable — if the gates pass and escapes still occur, the model's levels are wrong and must be revised (that test is built into Level 5).

#### A.8 AI/agent-era testing maturity (2023–2026)

- **Adapting TMMi to agents is already happening**: a recent paper "extends TMMi by proposing 16 Agent Security Test Process Areas (ASTPAs) distributed across maturity Levels 2 through 5, mirroring TMMi's 5+5+3+3" structure [Extending the TMMi Framework, n.d.] (authors/venue could not be verified from the sources seen; ResearchGate-hosted).
- **DORA 2024** found AI adoption negatively impacts delivery stability (an estimated −7.2% per 25% increase in AI adoption) and throughput (−1.5%), concluding that "fundamentals like small batch sizes and robust testing remain crucial" [DORA, 2024]. An AI crew without testing maturity should *expect* instability to grow with autonomy.
- **Anthropic's engineering guidance** for agents: "We recommend extensive testing in sandboxed environments, along with the appropriate guardrails", and "Start with simple prompts, optimize them with comprehensive evaluation, and add multi-step agentic systems only when simpler solutions fall short" [Anthropic, 2024] (note: the post itself carries a caveat that the tooling landscape has changed since December 2024 [verified 2026-09-13]).
- **Eval-driven development (EDD)** — the LLM-era analogue of test-driven development, where criteria/evals are defined before or alongside the artifact — is now standard practitioner doctrine across vendors [Braintrust, n.d.; DeepEval, n.d.; web.dev (Google), n.d.; Vercel, n.d.] and has dedicated 8-stage frameworks with CI/CD integration for agents [Red Hat, 2026]. Hamel Husain's widely-cited practitioner guide argues evals should be custom, built from real usage/error analysis, and created before waiting for production data [Husain, 2024].
- **Agent evaluation research**: the first comprehensive survey of LLM-agent evaluation analyzes the field across five perspectives and flags "critical gaps… particularly in assessing cost-efficiency, safety, and robustness, and in developing fine-grained, scalable evaluation methods" [Yehudai et al., 2025]. τ-bench is the reference benchmark for tool-agent-user interaction ("a benchmark emulating dynamic conversations between a user (simulated by language models) and a language agent provided with domain-specific API tools and policy guidelines") [Yao et al., 2024], now evolved through τ²-bench to τ³-bench (voice, banking domain; verified 2026-09-13) [Sierra Research, 2025]. Practitioner write-ups describe τ-bench-family reliability as *pass^k* — whether the agent succeeds consistently across k repeated attempts [MorphLLM, 2026 — practitioner source; primary definition not directly verified].
- **Non-determinism:** Thinking Machines Lab document that LLM inference nondeterminism has identifiable causes and can be tamed [Thinking Machines Lab, 2025]; LLM-application testing research recommends semantics-preserving prompt rewrites to evaluate output variance and stability [Rethinking Testing for LLM Applications, 2025 — authors could not be verified from the sources seen].
- **Statistics for evals:** Miller's "Adding Error Bars to Evals" gives the formulas and rules ACTM's Level 4 uses: report standard errors with means, reduce variance by resampling K answers per question, use paired comparisons, and do **not** tweak sampling temperature to reduce variance [Miller, 2024].
- **Eval tooling that slots into pytest CI:** DeepEval integrates LLM evaluations into CI/CD as pytest-style tests ("Drop deepeval test run into a .yml") [DeepEval, n.d.]; promptfoo provides evals plus red-teaming as CI-able config [Promptfoo, n.d.].
- **Automated test generation at scale (Level 5 existence proof):** Meta's ACH (Automated Compliance Hardener) — mutation-guided LLM-based test generation — applied to 10,795 Android Kotlin classes across 7 Meta platforms, generated 9,095 mutants and 571 privacy-hardening tests; engineers accepted 73% of its tests; and "of these 571 tests, 277 would have been discarded had we chosen to focus solely on the line coverage test adequacy criterion, underlining the importance of mutation testing over… coverage" [Harman et al., 2025].

### B. The ACTM model — AI-Crew Testing Maturity, 5 levels

**Design principles** (why a new model rather than adopting TMMi verbatim):

1. **Team-scope, not org-scope.** Test Certified, not TMMi, is the right size: one crew, one repo, one operator. Levels must be reachable in weeks, not years.
2. **Checkpoints are machine-checkable.** Every level gate is a queryable artifact (CI run, coverage JSON, mutation report, ledger) — this answers the maturity-model criticism that they "measure activities instead of outcomes".
3. **Process definition lives in SOULs.** A crew's "process" is its instruction files and routing; maturity must assess and change those, plus the humans' workflow rules.
4. **Gate by task class.** firstmate already classifies verifiability (self-evident / testable / external-source / unverifiable) and DECISIVE-01 showed pipeline overhead hurts weak tasks `[internal: DECISIVE-01]` — so gates are tiered by class, not uniform.
5. **Non-determinism is a first-class citizen.** Exact-match unit tests cover deterministic code artifacts; behavior classes get eval suites with statistical reporting [Miller, 2024].
6. **All-or-nothing levels with dependencies** (TPI-style): a level is achieved only when every checkpoint passes, and higher gates depend on lower infrastructure [Andersin, n.d.].

**Level overview:**

| Level | Name | One-line definition | Nearest anchors |
|---|---|---|---|
| 1 | **Ad Hoc / Heroic** | Testing is optional and unowned; quality depends on heroics (a human writing tests at midnight). | TMMi L1 Initial [TMMi Foundation, 2018] |
| 2 | **Gated** | Every code deliverable carries tests, tests run automatically, and nothing ships with red or missing tests. | TMMi L2 Managed; TC L1–L2 (continuous build, no-untested-code policy) [Bland, 2011; Google, 2020] |
| 3 | **Institutionalized** | Testing is a defined, owned crew process: a tester agent with blocking authority, a regression corpus, taxonomy, and flake discipline. | TMMi L3 Defined (Test Organization, Training, Lifecycle, Peer Reviews); TC L3 [TMMi Foundation, 2018; Bland, 2011] |
| 4 | **Measured & Eval-Driven** | Numeric quality gates are enforced in CI, and non-deterministic behavior is governed by statistically-reported evals. | TMMi L4 Measured (Test Measurement, Product Quality Evaluation); EDD [TMMi Foundation, 2018; Braintrust, n.d.] |
| 5 | **Self-Verifying** | The crew runs and improves its own test process as a measured system: failures automatically become tests, tests are automatically strengthened, process changes run as experiments. | TMMi L5 Optimization (Defect Prevention, Quality Control, Test Process Optimization); TC L5; Meta ACH [TMMi Foundation, 2018; Google, 2020; Harman et al., 2025] |

---

#### B.1 Level 1 — Ad Hoc / Heroic

**Definition.** Testing exists only when someone remembers it or a human rescues the crew manually; no agent is accountable for tests and nothing can block a release.

**Entry criteria.** None — Level 1 is the floor at which every organization starts [TMMi Foundation, n.d.-a].

**Measurable criteria (observable state, not gates).**
- % of code-producing tasks shipped with crew-written tests: ~0% (internal: COORD-01 = 0 test files in 3 runs; COORD-02 = 0 test files across 4 modules).
- Agents with authority to block a release for missing tests: 0.
- Automated runs of any test suite: 0.
- Regression corpus: absent or ad hoc files.

**Required practices.** None (that is the diagnosis). A testing *philosophy* document may exist — that is an L2 artifact, not an L1 practice.

**Required tooling.** None enforced. (A chosen stack — pytest et al. — waiting unused is still L1.)

**Exit criteria ("done" = achieved Level 2).** All five Level-2 gates below pass simultaneously.

**Typical failure modes.** Fixed bugs recur because nothing replays the original failure (internal T09–T12); the operator becomes the crew's de facto (and unscalable) tester — 11 hand-written tests in COORD-02; verification agents time out so verification debt is invisible; "done" is a claim, not a measurement, which violates the crew's own P4 law.

**Calendar effort to reach L2.** **1–2 weeks of crew+operator time.** Grounding: Test Certified Level 1 was designed for "a day or five of effort, by one or two engineers" [Bland, 2011] and Google designed each ladder step for "within a quarter" [Google, 2020]; a crew must additionally edit SOULs and wire CI, hence days-to-weeks. **No published transition data exists for AI-agent crews** — this estimate is an explicit extrapolation from the team-level human data.

#### B.2 Level 2 — Gated (tests required, CI-enforced, no red merges)

**Definition.** Every code deliverable carries at least one automated test; the suite runs automatically on every change; and the merge/ship path cannot complete with red or missing tests.

**Entry criteria.** L1 exit + a written test policy exists that agents must obey (the SOUL-level equivalent of TMMi's Level-2 "Test Policy and Strategy" PA [TMMi Foundation, 2018] and Test Certified's Level-2 policy "that essentially forbade anyone from submitting untested code" [Bland, 2011]).

**Measurable criteria (all must hold).**

| # | Gate | Threshold | Justification |
|---|---|---|---|
| 2.1 | % of code-producing tasks shipped with ≥1 automated test | **100%** (fail the gate if <100% over any rolling 10-task window) | TC L2 policy forbidding untested code [Bland, 2011]; all-or-nothing level logic [Andersin, n.d.]. *Proposed default.* |
| 2.2 | CI runs the full pytest suite on every push/PR | **Binary: yes**; suite must exist and run | TC L1 "set up a continuous build" [Google, 2020]; GitHub required status checks "must pass before collaborators can merge" [GitHub, n.d.]. |
| 2.3 | Required status checks enabled on the target branch | **Binary: yes** (merge blocked on red) | GitHub branch protection semantics [GitHub, n.d.]. |
| 2.4 | Gating suite runtime | **≤ 10 minutes** (warning >5 min) | Google runs fast tests before every commit [Google, 2020]; a crew's completer must finish verification inside its timeout budget. *Proposed default.* |
| 2.5 | Regression ledger exists; every newly fixed bug gets a regression test | **100% of new failures** (legacy backlog may carry into L3) | Direct countermeasure to T09–T12 recurrences; mirrors TC's "identify flaky / measure first" philosophy [Google, 2020]. *Proposed default for the 100%.* |

**Task-class gate tiering** (crew-specific, grounded in DECISIVE-01 and the firstmate's verifiability axis): *self-evident* tasks → smoke gate only (suite green; no new tests demanded); *testable* tasks → full gate (2.1–2.5); *external-source* tasks → source-verification gate (completer checks cited URLs resolve and match claims); *unverifiable* tasks → **HOLD** with a stated gap, per the canonized P4 rule `[internal: P4]`.

**Required practices.**
- Engineer SOUL carries the iron law: no deliverable without tests (fixes root cause #1 in the internal log).
- Completer SOUL: must run the suite and must block on red/missing tests (fixes root cause #4).
- A failure ledger file (e.g. `TESTING/ledger.md`): every bug, its reproducing test, and its status.
- Commit-gated CI: tests are a required check; operators never merge around it.

**Required tooling.** GitHub Actions workflow running `pytest` (+ `coverage.py` reporting even if ungated); GitHub protected branch with required status checks [GitHub, n.d.]; the ledger file. Nothing exotic: Test Certified Level 1 was deliberately achievable with a build machine and coverage metrics [Google, 2020].

**Exit criteria.** 10 consecutive code-producing tasks, 100% with tests, all CI-gated, zero operator-written rescue tests, and the ledger current.

**Typical failure modes.** Count-gaming (trivial tests to satisfy 2.1 — countered at L4 by mutation gates); suite grows past 10 min and the gate gets bypassed "just this once"; tests written after design instead of driving it; flakes erode trust in the gate (addressed at L3); operator waiver culture (every waiver must be written into the ledger).

**Calendar effort to reach L3.** **4–8 weeks.** Grounding: TC L2 was "a couple weeks or months" [Bland, 2011]; Google's cadence was ~1 quarter per level [Google, 2020]. No AI-crew data exists — extrapolation.

#### B.3 Level 3 — Institutionalized (owned, defined, self-sustaining)

**Definition.** Testing is a defined crew process with an owner — a tester agent with real blocking authority — plus a regression corpus, a test taxonomy, and flake discipline, so quality no longer depends on any single agent's memory.

**Entry criteria.** L2 exit + tester SOUL activated (the missing agent from the crew table; its role is already sketched in `TESTING-COUNCIL.md` `[internal: context §3]`). This is ACTM's translation of TMMi L3's "Test Organization" and "Test Training Program" PAs [TMMi Foundation, 2018] — in a crew, "organization" means a role with authority, and "training" means SOUL calibration examples.

**Measurable criteria (all must hold).**

| # | Gate | Threshold | Justification |
|---|---|---|---|
| 3.1 | Tester activation on testable tasks | **≥ 90%** of tasks firstmate classifies `testable` route through the tester | DECISIVE-01 warns against pipeline overhead on weak tasks, so the gate applies to testable tasks only. *Proposed default.* |
| 3.2 | Blocking authority honored | **100%** of tester HOLDs end in rework or a logged, operator-signed waiver | TMMi L3 institutionalizes practices org-wide [TMMi Foundation, 2018]; P4 already makes HOLD a lawful outcome `[internal: P4]`. |
| 3.3 | Regression-capture rate | **≥ 60%** of logged past failures have a permanent automated test | Directly prevents T09–T12. *Proposed default — no external source defines this metric.* |
| 3.4 | Coverage measured and reported per task (line + branch) | Reporting exists; informational target line ≥ 60% repo-wide | TC L1 = "start tracking code coverage" (measure before gate) [Google, 2020]; coverage.py branch measurement [coverage.py, n.d.]. |
| 3.5 | Flake discipline | Known-flaky tests quarantined out of the gating path **within 48h** of detection; 0 flaky tests in the gating path | Google: 16% of tests had flakiness, >1 in 7 [Micco, 2016]; TC upper levels removed nondeterminism [Google, 2020]; a small crew cannot afford Google's triage machinery, so quarantine must be fast. *48h is a proposed default.* |
| 3.6 | Test taxonomy balance | ~70% unit / 20% integration / 10% E2E on the crew's artifacts | Internal `TESTING-COUNCIL.md` pyramid; classification practice from TC (small/medium/large) [Bland, 2011]. |
| 3.7 | Critic operability | **0** critic timeouts on standard-size tasks (timeout configured; path awareness configured) | Fixes internal root causes #2 and #3 — a verifier that times out is a verifier that doesn't verify. |

**Required practices.**
- Tester SOUL with activation conditions, operating procedure, veto conditions (missing critical-path tests, red suite, flaky gate, implementation-asserting tests, sub-threshold coverage — as already philosophized in `TESTING-COUNCIL.md`), an appeal path (tester → critic → operator), and an output format.
- Peer review of tests (critic reviews test quality, not just code) — TMMi L3's Peer Reviews PA [TMMi Foundation, 2018].
- Flake quarantine process: mark, exclude from gating, ticket, fix-or-delete (Google mitigates flaky tests rather than tolerating them in the critical path [Micco, 2016]).
- Failure-ledger → regression-corpus pipeline: fixing a bug without adding its test is itself a HOLD.
- Property-based tests for input domains (Hypothesis) where example tests are weak [Hypothesis, n.d.].

**Required tooling.** pytest markers for test classes/sizes; coverage.py with `--branch` [coverage.py, n.d.]; a quarantine marker or separate non-gating job; Hypothesis [Hypothesis, n.d.]; the ledger (now queryable, e.g. a script counting captured vs uncaptured failures).

**Exit criteria.** All gates green for 4 consecutive weeks; regression-capture ≥ 60% and rising; at least one exercised tester veto and one exercised appeal.

**Typical failure modes.** Rubber-stamp tester (veto never used → check 3.2 is *exercised*, not just permitted); veto wars/deadlock (mitigated by the appeal ladder); tester becoming the bottleneck (mitigated by task-class tiering from L2); corpus rot (regression tests exist but aren't run nightly — countered by keeping them inside the gating suite); over-gating self-evident tasks and re-creating the DECISIVE-01 failure mode.

**Calendar effort to reach L4.** **8–12 weeks (~1 quarter).** Grounding: Google's per-level cadence [Google, 2020]; TMMi human-org data says L4 takes "another 6–12 months" after L3 [TestFort, 2025] — a crew compresses this because scope is one repo and one toolchain, but building measurement infrastructure is real work. Extrapolation, explicitly stated.

#### B.4 Level 4 — Measured & Eval-Driven (numeric gates + statistical evals)

**Definition.** Quality is managed by enforced numbers: coverage and mutation gates on changed code, flake-rate budgets, regression-capture targets — and non-deterministic agent behavior is governed by eval suites with statistically honest reporting.

**Entry criteria.** L3 exit + a metrics ledger defined (which numbers, where stored, who reads them). This is ACTM's translation of TMMi L4 "Test Measurement" and "Product Quality Evaluation" [TMMi Foundation, 2018] plus eval-driven development [Braintrust, n.d.; web.dev (Google), n.d.].

**Measurable criteria (all must hold).**

| # | Gate | Threshold | Justification |
|---|---|---|---|
| 4.1 | Changed-code line coverage (per PR/task) | **≥ 90%**; stretch 99% on critical modules | Google: "per-commit coverage goals of 99% are reasonable, and 90% is a good lower bound"; project-wide >90% "not worth it" [Google Testing Blog, 2020]. |
| 4.2 | Changed-code branch coverage | **≥ 75%** | Branch is strictly harder than line; coverage.py reports both separately [coverage.py, n.d.]. *Proposed default: 75% ≈ the coverage-vs-effort knee below the line target.* |
| 4.3 | Mutation score on changed modules (nightly job) | **≥ 70%** (fail < 70%) | Mutation is the evidence-backed counter to coverage-gaming: 70% of high-priority bugs are coupled with a mutant [Petrović et al., 2021]; 27.9% of real-world mutation users already enforce a build-time minimal score [Sánchez et al., 2024]; Meta found 277/571 valuable tests would have been discarded under coverage-only criteria [Harman et al., 2025]. *70% as the floor is a proposed default* (practitioner guidance bands 60–70% baseline, 75–85% strong [Insider Engineering, n.d. — practitioner source]); nightly rather than per-PR for cost, following Google's experience making mutation testing practical at scale [Petrović & Ivanković, 2018; Petrović et al., 2021b]. |
| 4.4 | Regression-capture rate | **≥ 90%** | Ratchet from L3's 60%. *Proposed default.* |
| 4.5 | Gating-path flake rate | **< 0.5% of gating runs**; **0 known-flaky tests in the gating path** | Google observes ~1.5% flaky runs / 16% flaky tests and calls it staggering [Micco, 2016]; a crew with no triage infrastructure must run well below that. *0.5% ≈ one-third of Google's rate — proposed default.* |
| 4.6 | Eval suites for non-deterministic behavior classes | Each verifiable behavior class has an eval set of **≥ 30 cases**; mean pass-rate **≥ 90%** reported **with standard error**; each task additionally passes **3/3 repeated runs** (pass^k-style consistency) | Sample sizes and SEM reporting per [Miller, 2024]; resampling with K answers reduces variance [Miller, 2024]; τ-bench-family reliability is measured as consistency across repeated attempts [Yao et al., 2024; MorphLLM, 2026 — pass^k naming is from a practitioner source]; survey evidence that fine-grained agent eval is the gap to close [Yehudai et al., 2025]. *30 cases / 90% / k=3 are proposed defaults with the reasoning stated.* |
| 4.7 | Escape/recurrence rate | Previously-fixed bugs recur in **≤ 5%** of subsequent tasks | The direct, measurable fix for T09–T12. *Proposed default.* |
| 4.8 | Metrics ledger auto-updated | Every task appends coverage, mutation, flake, eval, escape data — no manual entry | TMMi L4 Test Measurement made real; TC's dashboard principle [Google, 2020]. |

**Required practices.**
- Threshold governance: numbers live in one policy file; changes are explicit commits; quarterly review with a ratchet (thresholds only tighten unless a written exception is granted).
- Eval-driven development for behavior tasks: define/extend the eval before or with the artifact; evals built from real failure cases (error-analysis-driven, per [Husain, 2024]), not generic off-the-shelf suites.
- LLM-as-judge only with spot-checked agreement (a human or the critic samples judge verdicts monthly); temperature is never tuned to reduce eval variance [Miller, 2024].
- Leading-indicator reviews: flake upticks, mutation dips, and eval pass-rate drift reviewed weekly before they become escapes.

**Required tooling.** coverage.py `--branch` with CI fail thresholds [coverage.py, n.d.]; mutmut (`mutmut run --paths-to-mutate src/` style nightly job; `mutmut browse` to work mutants) [mutmut, n.d.]; a pytest-native eval runner (DeepEval integrates evals as pytest tests in CI [DeepEval, n.d.]) or promptfoo config (evals + red-teaming) [Promptfoo, n.d.]; the metrics ledger + a simple dashboard (even a committed JSON + generated HTML, echoing Google's TC dashboard that "applied social pressure" [Google, 2020]).

**Exit criteria.** Gates 4.1–4.8 *enforced* (not merely reported) for 6 consecutive weeks, with at least one genuine save (a would-be escape caught by a gate) recorded in the ledger.

**Typical failure modes.** Goodhart's law (coverage-chasing tests that assert nothing — 4.3 exists precisely to catch this); eval overfitting (high pass-rate on a stale set while real failures escape — countered at L5 by drift monitoring); judge drift or judge sycophancy; waiver pile-up (if waivers > ~5% of gates, the thresholds are wrong — recalibrate rather than bypass); mutation job too slow → skipped (restrict to changed modules [mutmut, n.d.]).

**Calendar effort to reach L5.** **12+ weeks, then perpetual.** Grounding: TMMi L5 is optimization in perpetuity [TMMi Foundation, n.d.-a]; CMMI human-org medians for even one level transition were ~2 years [Herbsleb & Paulk, 1997]; the embedded TMMi case took 4 years for L1→L3 [TMMi Foundation, 2023]. **No published AI-crew transition data exists — this is an extrapolation and should be treated as a planning hypothesis, not a benchmark.**

#### B.5 Level 5 — Self-Verifying (the crew tests itself)

**Definition.** The crew's test process is itself a measured system that the crew improves: every failure automatically becomes a regression test, the mutation loop automatically strengthens tests, adversarial drills probe known failure classes, and process changes ship as measured experiments.

**Entry criteria.** L4 exit + an automated path from "failure observed" to "test proposed" (a crew member — tester or engineer — drafts the regression test without operator intervention).

**Measurable criteria (maintained state, all must hold).**

| # | Criterion | Threshold | Justification |
|---|---|---|---|
| 5.1 | HOLDs/escapes producing a regression test within one task cycle — automatically | **100%**, zero operator involvement | Closes the loop from P4 (HOLD with a stated gap) to permanent prevention. *Proposed default for "one task cycle".* |
| 5.2 | Mutation-guided strengthening | Surviving mutants trigger test-generation; mutation score **≥ 85%** on critical modules | Meta's ACH proves mutation-guided LLM test generation at scale (9,095 mutants → 571 tests, 73% engineer acceptance) [Harman et al., 2025]; Google's data shows mutant exposure leads developers to write more, better tests [Petrović et al., 2021]. *85% is a proposed default (upper end of the practitioner "strong" band).* |
| 5.3 | Adversarial drills | **≥ 1 per quarter**; detection rate **≥ 90%** of injected known failure classes | TMMi L5 Defect Prevention & Quality Control made operational [TMMi Foundation, 2018]. *Both numbers proposed defaults.* |
| 4→5.4 | Eval drift monitoring | Alert when any eval suite's trailing-30-task pass-rate drops > 5 points vs its established baseline | Guards against eval overfitting/staleness; survey gap: robustness and fine-grained eval [Yehudai et al., 2025]. *5 points proposed default.* |
| 5.5 | Nondeterminism budget in the gating path | **0 flaky tests in the gating path; all tests automated; fast tests run before every commit** | TC Level 5 verbatim: "all tests were automated, fast tests were running before every commit, all nondeterminism had been removed, and every behavior was covered" [Google, 2020]. |
| 5.6 | Process experiments measured | Every SOUL/pipeline change is evaluated before/after on the ledger (task success rate, escapes, cost) | DORA's throughput-vs-stability factor split is the template (stability = change failure + rework) [DORA, 2024]. |

**Required practices.**
- Automatic regression-test generation on failure (ACH-style [Harman et al., 2025]) with mandatory tester review before the generated test joins the gating suite (acceptance tracking — Meta's 73% acceptance is the realistic ceiling, so review stays [Harman et al., 2025]).
- Quarterly self-assessment using the ACTM rubric (§D.5), published to the crew's memory so the level is common knowledge (echoing TC's public dashboard [Google, 2020]).
- Quarterly testing retro: which gates saved us, which were theater, which thresholds to ratchet.
- Cost tracking: token cost of testing per task, so test depth scales with task stakes (guards against over-gating simple tasks — the DECISIVE-01 lesson).

**Required tooling.** mutmut integrated into the generation loop [mutmut, n.d.]; drill harness (a task generator that replays/adapts known failure classes); drift monitors over the eval ledger; experiment dashboard on the metrics ledger.

**Exit criteria.** None — Level 5 is maintained in perpetuity, exactly as Test Certified Level 3 was designed as "an on-going, long-term commitment that a team would strive to maintain in perpetuity" [Bland, 2011] and TMMi L5 is continuous optimization [TMMi Foundation, n.d.-a].

**Typical failure modes.** Self-congratulation (drills too easy because the crew generated both drill and defense — rotate drill authorship between agents and keep an operator-curated private drill set); automation producing weak tests (mutation score 5.2 catches this); metrics theater (5.6 turns process changes into experiments, which exposes theater); the crew optimizing the model instead of the product (the rubric is a map, not the territory — the escape rate is the territory).

### C. Where Crew v2 stands today — evidence-based assessment

**Method.** Score against the Level-2 gates (ACTM is all-or-nothing: if any L2 gate fails, the crew is L1 [Andersin, n.d.]). Evidence comes from the trial log in the council context; each verdict is tied to a specific gate.

| L2 gate | Evidence | Verdict |
|---|---|---|
| 2.1 ≥1 test per code task | Engineer produced **zero test files** in COORD-01 (3 runs) and COORD-02 (4 modules, 135 lines, explicit requirement); operator wrote 11 tests manually `[internal: COORD-01, COORD-02]` | **FAIL** (0%) |
| 2.2 CI runs suite on every push | No CI exists; STATUS: "CI/CD Integration ❌ Missing" `[internal: STATUS.md]` | **FAIL** |
| 2.3 Required checks block merges | Nothing blocks anything; "no agent has authority to block code that lacks tests" `[internal: context §2]` | **FAIL** |
| 2.4 Gating suite ≤ 10 min | No suite exists | **FAIL** (N/A) |
| 2.5 Failure ledger + regression tests for new fixes | T09–T12: fixes were implemented but original failure cases were never re-tested; bugs recurred `[internal: T09–T12]` | **FAIL** |

**Verdict: Crew v2 is at Level 1 — the bottom — with 0 of 5 Level-2 gates passing.** Granular score ≈ 1.0–1.3/5: L1 is not merely "bad", it is *ungated and unowned*, with quality surviving only through operator heroics (the 11 manual tests).

**Assets that shorten the climb** (why 1.3 and not 1.0):
- A testing philosophy already exists (`TESTING-COUNCIL.md`: behavior-not-implementation, 70/20/10 pyramid, blocking conditions) — this is the L2 "test policy" artifact in draft form `[internal: context §3]`.
- The toolchain is already chosen (pytest, Hypothesis, mutmut, coverage.py, GitHub Actions) — no selection work remains `[internal: context §3]`.
- The tester role is already sketched (needs a SOUL, not a concept) `[internal: context §3]`.
- P4 "HOLD-on-unverified" is canonized crew law — the *normative* foundation of blocking authority already exists `[internal: P4]`.
- The 11 operator-written tests for the currency converter are a ready-made seed regression corpus.

**Blockers that must be fixed first** (from the internal root-cause list): engineer SOUL has no test requirement (#1); critic lacks timeout config and path awareness (#2, #3); completer has no test-execution requirement (#4); no blocking authority anywhere (#5). All five are L2 work.

**Scoring note on DECISIVE-01:** single-agent beats pipeline on weak-class tasks (12/16 vs 10/16 vs 8/16) `[internal: DECISIVE-01]` — this is *not* an argument against maturity, it is an argument for the task-class gate tiering built into ACTM L2. Testing maturity must scale with task verifiability, or the gate itself becomes the failure mode.

### D. Migration path from Level 1 to Level 5

#### D.1 Sequencing overview

| Phase | Window | Focus | Level achieved |
|---|---|---|---|
| 0 — Quick wins | Week 1 | SOUL edits + CI skeleton + policy file | L1 → "L2-ready" |
| 1 — The Gate | Weeks 1–2 | 100% test-gating, blocking semantics, ledger | **L2** |
| 2 — Ownership | Weeks 3–10 | Tester SOUL with veto, regression corpus, flake discipline, critic fixes | **L3** |
| 3 — Numbers | Weeks 11–22 | Coverage/mutation gates, eval harness with statistics, dashboards | **L4** |
| 4 — Self-verification | Week 23+ | Auto test-generation, drills, drift monitors, experiments | **L5** (maintained) |

#### D.2 Phase 0 — Quick wins vs structural changes (what to do first)

**Quick wins (days, no new agents):**
1. **Write `TEST-POLICY.md`** — one page: every code deliverable requires tests; the 5 gates of L2; the task-class tier table; the flake rule; the appeal path. (This is the crew's TMMi-L2 Test Policy and Strategy artifact [TMMi Foundation, 2018].)
2. **Edit the engineer SOUL**: iron law — "no deliverable without tests; a task without tests is not done, it is HOLD." (Fixes root cause #1 — the direct cause of COORD-01/02.)
3. **Edit the completer SOUL**: must run `pytest` and must block on red/missing tests, reporting exit codes as evidence. (Fixes root cause #4.)
4. **Fix the critic**: add timeout configuration and path awareness so verification completes. (Fixes root causes #2/#3 — otherwise the L3 appeal path has no functioning verifier.)
5. **Stand up the GitHub Actions workflow**: `pytest` + `coverage run --branch` on every push; enable required status checks on the main branch [GitHub, n.d.; coverage.py, n.d.].
6. **Seed the regression corpus**: commit the operator's 11 currency-converter tests as `tests/regressions/` and start `TESTING/ledger.md` with every known past failure (COORD-01/02, T09–T12).

**Structural changes (weeks, new agents/processes):**
7. **Instantiate the tester agent** with a full SOUL: activation on `testable` tasks, procedure (run suite, verify tests assert behavior, check coverage/mutation thresholds), veto conditions, appeal ladder (tester → critic → operator), output format, and calibration rules. (Fixes root cause #5 — blocking authority — and completes the crew table's missing row.)
8. **Wire firstmate routing**: `testable` tasks → formation that includes the tester; `self-evident` → smoke gate; `unverifiable` → HOLD per P4. (Uses the classification axes that already exist.)
9. **Build the metrics ledger** and later the eval harness (Phase 3 work — structural because it defines what "better" means for the crew).

**Do first / second / third:** First = items 1–6 (they are all prerequisites for everything else and each is ≤ 1 day). Second = items 7–8 (tester + routing). Third = Phase 3's measurement infrastructure. Never start Phase 3 before Phase 1's gate is real — measured gates on an ungated process measure nothing.

#### D.3 Phase details — what "done" looks like per phase

- **Phase 1 (L2)**: run the §D.5 rubric L2 section; all 7 questions PASS; 10 consecutive code tasks with 100% test coverage-of-obligation; zero operator-written rescue tests.
- **Phase 2 (L3)**: rubric L3 all PASS; regression-capture ≥ 60%; one exercised veto and one exercised appeal; 4 weeks stable.
- **Phase 3 (L4)**: rubric L4 all PASS; gates enforced 6 weeks; ≥ 1 documented save in the ledger.
- **Phase 4 (L5)**: rubric L5 all PASS; quarterly cadence established; the crew generates regression tests without operator prompting.

#### D.4 Effort budget and honest caveats

Grounded anchors: Google's Test Certified levels were each designed for "within a quarter", with L1 achievable in "a day or five of effort" [Google, 2020; Bland, 2011]; human-organization CMM transitions medians were 26.5 months (L1→L2) and 24 months (L2→L3) [Herbsleb & Paulk, 1997]; TMMi consultancies quote 12–18 months to TMMi L3 and 6–12 more to L4 [TestFort, 2025]; a TMMi case study took 4 years for L1→L3 [TMMi Foundation, 2023]. ACTM's crew estimates (1–2 wks, 4–8 wks, 8–12 wks, 12+ wks) assume: one repo, one language, existing tool choices, an operator available for review, and — critically — that agent-SOUL changes actually change behavior (the crew's own razor agent violating explicit constraints `[internal: context §1]` shows SOUL compliance is a real risk that can extend any estimate). **No published transition data exists for AI-agent crews; treat all ACTM calendar numbers as planning hypotheses to be replaced by the crew's own measured data at Level 4.**

#### D.5 The assessment instrument — ACTM rubric (run this quarterly)

**How to run:** Evidence only, no self-report (a claim without an artifact is a HOLD, per P4 and per TMMi's assessment logic). For each question record PASS/FAIL + the artifact. A level is achieved only if **all** its questions PASS **and** all lower levels PASS (all-or-nothing, TPI-style [Andersin, n.d.]). The failed questions are the improvement backlog. Operators should run it quarterly, after every major SOUL change, and before any "we're mature enough" decision.

**Level 2 — Gated (the crew is L2 if all PASS):**
1. Does a written test policy exist that every code-producing agent must obey? *(artifact: policy file + SOUL references)*
2. Does CI run the full pytest suite on every push/PR automatically? *(artifact: workflow runs list)*
3. Are required status checks enabled so merges are blocked on red? *(artifact: branch-protection settings screenshot/config)*
4. Did 100% of the last 10 code-producing tasks ship with ≥1 automated test? *(artifact: PR/task audit)*
5. Does the completer run the suite and block on red/missing tests? *(artifact: completer output containing test exit codes + at least one exercised block)*
6. Does the failure ledger exist, and did 100% of newly fixed bugs get a regression test? *(artifact: ledger diff vs task history)*
7. Is the gating suite runtime ≤ 10 minutes? *(artifact: CI timing)*

**Level 3 — Institutionalized:**
1. Is the tester activated on ≥ 90% of tasks classified `testable`? *(artifact: routing log)*
2. Does the tester hold real blocking authority, exercised at least once, with 100% of HOLDs resolved by rework or logged waiver? *(artifact: HOLD log)*
3. Is regression-capture ≥ 60% of logged past failures? *(artifact: ledger coverage query)*
4. Are line and branch coverage measured and reported per task? *(artifact: coverage reports)*
5. Are known-flaky tests quarantined within 48h, with 0 flaky tests in the gating path? *(artifact: quarantine log + suite manifest)*
6. Does the test corpus roughly follow the 70/20/10 pyramid? *(artifact: test class counts)*
7. Does the critic complete verification without timeouts on standard tasks? *(artifact: critic run logs)*

**Level 4 — Measured & Eval-Driven:**
1. Are changed-code line coverage ≥ 90% and branch ≥ 75% *enforced* (CI fails below)? *(artifact: failing run on a deliberately under-covered PR — drill it once)*
2. Is mutation score ≥ 70% on changed modules, run at least nightly? *(artifact: mutmut report)*
3. Is regression-capture ≥ 90%? *(artifact: ledger query)*
4. Is gating-path flake rate < 0.5% with 0 known-flaky in the gate? *(artifact: flake ledger)*
5. Does every verifiable non-deterministic behavior class have an eval suite (≥ 30 cases) with mean pass-rate ≥ 90% reported **with standard error**, and do tasks pass 3/3 repeated runs? *(artifact: eval runs with SEM)*
6. Is the escape/recurrence rate ≤ 5%? *(artifact: recurrence audit)*
7. Is the metrics ledger auto-updated per task? *(artifact: ledger entries with no manual edits)*

**Level 5 — Self-Verifying:**
1. Did 100% of HOLDs/escapes produce a regression test within one task cycle, generated without operator involvement? *(artifact: failure→test commit pairs)*
2. Does the mutation loop trigger test-generation on surviving mutants, with ≥ 85% mutation score on critical modules? *(artifact: mutmut trend + generation log)*
3. Are adversarial drills run ≥ quarterly with ≥ 90% detection? *(artifact: drill reports)*
4. Do eval drift monitors alert on > 5-point drops against trailing baselines? *(artifact: alert log)*
5. Are all gating-path tests deterministic, automated, and run before every commit? *(artifact: suite manifest + CI config)*
6. Is every SOUL/pipeline change evaluated as a before/after experiment in the ledger? *(artifact: experiment entries)*

### E. Why this model fits Crew v2 specifically (traceability)

- **Every internal root cause maps to a gate:** no test requirement (L2.1), no CI (L2.2/2.3), completer not running tests (L2.5/gate question 5), no blocking authority (L3.2), critic timeouts (L3.7), missing regression tests (L3.3→L4.4), razor constraint violations (SOUL-compliance risk, monitored via L4 escapes and the L2 waiver log).
- **The P4 doctrine is the moral foundation of the whole ladder:** compliance beats completion at every level — an ungated "done" is a false claim, and the rubric institutionalizes exactly that.
- **DECISIVE-01 is respected:** gates tier by task class, and Level 5 tracks testing cost per task so the crew never over-pays for simple work.

## Practical Recommendations

| Recommendation | Implementation | Tools | Threshold/Target |
|---|---|---|---|
| Write the crew test policy | Create `TEST-POLICY.md`: gates, task-class tier table, flake rule, waiver rule, appeal path; reference it from every relevant SOUL | Markdown + SOUL files | Policy exists and is referenced by ≥ 4 SOULs (L2 entry) |
| Engineer iron law | Add to engineer SOUL: "Every code deliverable ships with tests; otherwise HOLD" + a worked example of a HOLD with a stated gap | SOUL edit | 100% of code tasks with ≥ 1 test (gate 2.1) |
| Completer blocks on tests | Completer must run `pytest`, attach exit code to its report, and HOLD on red/missing tests | terminal, pytest | ≥ 1 exercised block per 20 tasks (audit) |
| Fix the critic | Add timeout config + path awareness to critic SOUL so verification completes on standard tasks | SOUL edit + harness config | 0 timeouts on standard tasks (gate 3.7) |
| Commit-gated CI | Workflow: `pytest` + `coverage run --branch -m pytest` on push/PR; enable required status checks on main | GitHub Actions, coverage.py [GitHub, n.d.; coverage.py, n.d.] | Merge blocked on red (binary); suite ≤ 10 min |
| Seed regression corpus | Commit the 11 operator tests as `tests/regressions/`; ledger every known past failure (COORD-01/02, T09–T12) | pytest, ledger file | Capture ≥ 60% (L3) → ≥ 90% (L4) |
| Instantiate tester with veto | Full tester SOUL: activation on `testable` tasks, procedure, veto conditions, appeal ladder (tester → critic → operator), output format | SOUL + routing config | Tester on ≥ 90% of testable tasks; 100% of HOLDs honored |
| Flake quarantine | Mark flaky tests (`@pytest.mark.flaky`-style marker), exclude from gating job, fix-or-delete within 48h | pytest markers, CI job split | 0 flaky in gating path; run-flake < 0.5% (L4) |
| Coverage gates on changed code | Per-PR `coverage json` diff-based check on changed files; branch measurement on | coverage.py `--branch`, CI script | Line ≥ 90%, branch ≥ 75% on changed code (L4); anchor: [Google Testing Blog, 2020] |
| Nightly mutation gate | `mutmut run` restricted to modules changed in the last 24h; publish score per module | mutmut [mutmut, n.d.] | Mutation score ≥ 70% changed modules (L4); ≥ 85% critical (L5) |
| Eval harness for behavior tasks | For each non-deterministic behavior class: ≥ 30-case eval set from real failures; run as pytest-style tests in CI; report mean pass-rate ± SEM; 3/3 repeated runs per task | DeepEval or promptfoo; pytest [DeepEval, n.d.; Promptfoo, n.d.] | Pass-rate ≥ 90% ± SEM reported; never tune temperature for variance [Miller, 2024] |
| Metrics ledger + review | Append per-task: coverage, mutation, flake, eval ± SEM, escapes, cost; weekly leading-indicator review; quarterly threshold ratchet | ledger file/JSON + dashboard | Auto-updated 100% of tasks (gate 4.8) |
| Quarterly self-assessment | Run the §D.5 rubric; publish level + failed questions to crew memory | Rubric + ledger | Level known at all times; failed questions = backlog |
| Auto test-generation on failure (L5) | On HOLD/escape, tester drafts the regression test without operator; tester reviews before it joins the gate; track acceptance rate | crew + mutmut loop | 100% failures → test within 1 cycle; acceptance tracked (Meta's 73% is the realistic reference [Harman et al., 2025]) |
| Adversarial drills (L5) | Quarterly: inject known failure classes (incl. operator-curated private set); measure detection | drill harness | ≥ 1 drill/quarter; ≥ 90% detection |

## Metrics and Targets

| Metric | Definition | Measurement | L2 target | L3 target | L4 target | L5 target | Warning threshold |
|---|---|---|---|---|---|---|---|
| Test-gated task rate | % code tasks shipping with ≥ 1 crew-written test | PR/task audit | 100% | 100% | 100% | 100% | < 100% (any window of 10) |
| CI gate enforcement | Required checks on; merge blocked on red | branch protection + CI log | binary yes | yes | yes | yes | any manual merge-around |
| Gating suite runtime | Wall time of gating suite | CI timing | ≤ 10 min | ≤ 10 min | ≤ 10 min | ≤ 10 min | > 5 min (watch) |
| Line coverage (changed code) | % executable lines hit, per changed file | coverage.py JSON diff | measured only | ≥ 60% repo-wide (info) | **≥ 90%** | ≥ 90% (99% stretch critical) | < 85% |
| Branch coverage (changed code) | % branch destinations taken | coverage.py `--branch` | — | measured | **≥ 75%** | ≥ 75% | < 65% |
| Mutation score (changed modules) | % mutants killed | mutmut nightly | — | — | **≥ 70%** | **≥ 85%** critical | < 70% |
| Regression-capture rate | % logged past failures with permanent tests | ledger query | 100% of new | ≥ 60% | **≥ 90%** | 100% (automated) | < 60% at L3+ |
| Gating flake rate | % gating runs with a flaky result | CI flake log | — | 0 known-flaky in gate | **< 0.5%** runs | 0 nondeterminism in gate | any known-flaky in gate |
| Eval pass rate | Mean pass-rate per behavior-class suite | eval harness | — | — | **≥ 90%**, reported ± SEM | ≥ 90% + drift-monitored | drop > 5 pts vs trailing baseline |
| Eval reliability (pass^k-style) | Task passes 3/3 repeated runs | eval harness | — | — | 3/3 | 3/3 + k studies as needed | any 2/3 |
| Escape / recurrence rate | % previously-fixed bugs recurring in later tasks | recurrence audit | — | tracked | **≤ 5%** | ≤ 5% with root-cause notes | any recurrence of a ledgered bug |
| Tester activation | % of `testable` tasks routed through tester | routing log | — | **≥ 90%** | ≥ 90% | ≥ 90% | < 80% |
| Veto integrity | % tester HOLDs honored (rework or logged waiver) | HOLD log | — | 100% | 100% | 100% | any silent override |
| Testing cost per task | Token/agent cost of the test loop | ledger | — | tracked | budget by task class | budget by task class | > 25% of task cost on weak-class tasks |
| Drill detection rate | % injected failure classes caught | drill reports | — | — | — | **≥ 90%** quarterly | < 90% |

*Anchor sources for targets:* coverage [Google Testing Blog, 2020]; flake [Micco, 2016]; mutation [Sánchez et al., 2024; Petrović et al., 2021; Harman et al., 2025]; eval statistics [Miller, 2024]; consistency-across-runs [Yao et al., 2024]. All thresholds not carrying an external anchor are **proposed defaults** with reasoning stated inline in §B; the operator should recalibrate them with the crew's own data at Level 4.

## References

1. [TMMi Foundation, 2018] TMMi Framework R1.2 (official framework document, full PA structure). https://tmmi.org/tm6/wp-content/uploads/2018/11/TMMi-Framework-R1-2.pdf
2. [TMMi Foundation, n.d.-a] TMMi Model (levels overview; CMMI relationship). https://www.tmmi.org/tmmi-model/
3. [TMMi Foundation, 2023] Benefits Delivered (2nd world-wide TMMi user survey results and case studies). https://www.tmmi.org/benefits-delivered/
4. [TMMi Foundation via ISQI, n.d.] TMMi Framework model V2.0 (adds PA 2.6 Implementation and Habit at Level 2). https://isqi.org/media/7b/ea/54/1785323305/TMMi-Framework-model-V2.0_en_.pdf (release date could not be verified)
5. [Experimentus, 2017] TMMi – Test Maturity Model integration (16 process areas, 843 sub-practices, assessment types). https://experimentus.com/tmmi/
6. [Sogeti/TMAP, n.d.] TPI NEXT — Test Process Improvement (official TMAP page). https://www.tmap.net/building-blocks/test-process-improvement-tpi/
7. [Andersin, n.d.] TPI – a model for Test Process Improvement (detailed description of the original TPI model: 20 key areas, A–D levels, checkpoints, 13-scale maturity matrix, dependencies; internally cites Sogeti 2004 sources). https://www.apriorit.com/wp-content/uploads/2022/07/Andersin.pdf
8. [AgileTest, 2025] A Guide to Model-Based Test Process Improvement (secondary TPI NEXT description: 16 key areas, four maturity levels). https://agiletest.app/a-guide-to-model-based-test-process-improvement/
9. [ISTQB, n.d.] Certified Tester Expert Level — Implementing Test Process Improvement (CTEL-ITP; two-part structure). https://istqb.org/certifications/certified-tester-expert-level-implementing-test-process-improvement-ctel-itp-itpi/
10. [Bland, 2011] Test Certified (first-hand history: 3 original levels, L4/L5 added, effort data, mentorship model). https://mike-bland.com/2011/10/18/test-certified.html
11. [Google, 2020] Software Engineering at Google, Chapter 11 "Testing Overview" (Bender/Manshreck; Test Certified five levels, one-quarter cadence, Level 1/5 definitions, dashboard, 1,500+ projects, 2015 replacement). https://abseil.io/resources/swe-book/html/ch11.html
12. [O'Reilly, 2020] Software Engineering at Google (book page). https://www.oreilly.com/library/view/software-engineering-at/9781492082781/
13. [Whittaker, Arbon & Kelly, 2012] How Google Tests Software (ACM review confirming Test Certified Program documented at pp. 54ff). https://dl.acm.org/doi/pdf/10.1145/2347696.2347723
14. [Micco, 2016] Flaky Tests at Google and How We Mitigate Them (Google Testing Blog; ~16% of tests flaky, ~1.5% of runs flaky). https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html
15. [Parry, Kapfhammer, Hilton & McMinn, 2021] A Survey of Flaky Tests. ACM TOSEM 31(1). https://dl.acm.org/doi/abs/10.1145/3476105 (author PDF: https://o-parry.github.io/papers/2021a.pdf)
16. [Google Testing Blog, 2020] Code Coverage Best Practices (90% lower bound, 99% per-commit reasonable, >90% project-wide not worth it). https://testing.googleblog.com/2020/08/code-coverage-best-practices.html
17. [Petrović & Ivanković, 2018] State of Mutation Testing at Google. ICSE 2018 SEIP. (Indexed on the author's Scholar profile; also cited as ICSE-SEIP 2018, pp. 163–171 in [18].) https://scholar.google.com/citations?user=1ZQmpicAAAAJ&hl=en
18. [Petrović, Ivanković, Fraser & Just, 2021] Does mutation testing improve testing practices? arXiv:2103.07189 (~15M mutants; 70% of high-priority bugs coupled with a mutant; exposure → more/better tests). https://arxiv.org/abs/2103.07189
19. [Petrović, Ivanković, Fraser & Just, 2021b] Practical Mutation Testing at Scale: A view from Google. arXiv:2102.11378 (cited within [18]). https://arxiv.org/abs/2102.11378
20. [Sánchez et al., 2024] Mutation Testing in Practice: Insights from Open-Source Software Projects. IEEE TSE (34.6% define a minimal mutation-coverage threshold; 27.9% enforce a minimal mutation score during build). https://www.computer.org/csdl/journal/ts/2024/05/10472898/1VpY3do6cyA
21. [Herbsleb & Paulk, 1997] Software quality and the Capability Maturity Model. Communications of the ACM 40(6). https://doi.org/10.1145/255656.255692
22. [Herbsleb & Paulk, 1997 (figure)] Time to move from Level 1 to Level 2 and Level 2 to Level 3 (medians 26.5 and 24 months; appraisal data figure). https://www.researchgate.net/figure/Time-to-move-from-Level-1-to-Level-2-and-from-Level-2-to-Level-3-The-medians-are-265_fig1_220425555
23. [van Veenendaal et al., 2022] Test Maturity Model integration (TMMi): Trends of Worldwide Test Maturity and Certifications. IEEE Software. https://www.computer.org/csdl/magazine/so/2022/02/09361754/1rtToZAdCI8
24. [Garousi & Felderer, 2021] Motivations for and benefits of adopting the Test Maturity Model Integration (TMMi) (TMMi Foundation white paper). https://www.erikvanveenendaal.nl/site/wp-content/uploads/TMMi-Foundation-white-paper-Motivations-and-Benefits-of-Adopting-TMMi.pdf
25. [TestFort, 2025] Test Maturity Model (TMM) in Software Testing (12–18 months to Level 3; 6–12 more to Level 4). https://testfort.com/blog/tmm-in-software-testing
26. [Capgemini, 2025] World Quality Report 2025-26 (17th edition; 89% piloting/deploying GenAI workflows, 37% in production; 43% experimenting with GenAI in QA, 15% scaled; 60% test-data struggles; skills data). https://www.capgemini.com/insights/research-library/world-quality-report-2025-26/
27. [Sogeti, 2024] World Quality Report 2024-25 (16th edition; 3 dimensions: Technology & Practices, Industries, Geographies). https://www.sogeti.com/research-and-insight/world-quality-report-2024-25/
28. [RockerTester, 2024] Reviewing Capgemini's "World Quality Report 2024-25". https://therockertester.wordpress.com/2024/10/31/reviewing-capgeminis-world-quality-report-2024-25/
29. [Tarhan, Commacchio, Bonfanti & Gobbo, 2016] Business process maturity models: A systematic literature review (limited empirical validation). https://www.sciencedirect.com/science/article/abs/pii/S0950584916300015
30. [Smajli et al., 2024] Exploring the Limitations of Business Process Maturity Models. https://www.tandfonline.com/doi/full/10.1080/10580530.2024.2332210
31. [Jabbari et al., 2021] Maturity models critique (lack of empirical validation, operationalisation, theoretical foundations). arXiv:2105.04767. https://arxiv.org/pdf/2105.04767
32. [Bach, n.d.] The Immaturity of CMM (critique: no controlled comparisons possible). https://www.satisfice.com/blog/archives/6208
33. [Ramos et al., 2018] Software Test Maturity Models: A Systematic Review of the Literature. Journal of Unoeste (Dec 2018). https://journal.unoeste.br (full article URL not shown in search results; host seen)
34. [DORA (Google Cloud), 2024] Accelerate State of DevOps Report 2024 (AI adoption: −7.2% stability, −1.5% throughput per 25% adoption; four key metrics; robust-testing caveat). https://dora.dev/research/2024/dora-report/2024-dora-accelerate-state-of-devops-report.pdf (overview: https://dora.dev/research/2024/dora-report/)
35. [Anthropic, 2024] Building Effective Agents (Dec 19, 2024; sandboxed testing + guardrails; start simple, evaluate, then add complexity; page carries a Dec-2024 tooling-landscape caveat, verified 2026-09-13). https://www.anthropic.com/engineering/building-effective-agents
36. [Husain, 2024] Your AI Product Needs Evals (Mar 2024). https://hamel.dev/blog/posts/evals/index.html
37. [Miller, 2024] Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations. arXiv:2411.00640 (SEM reporting, resampling, paired comparisons, don't tune temperature for variance). https://arxiv.org/abs/2411.00640
38. [Yao, Shinn, Razavi & Narasimhan, 2024] τ-bench: A Benchmark for Tool-Agent-User Interaction in Realistic Domains. arXiv:2406.12045. https://arxiv.org/abs/2406.12045 (repo: https://github.com/sierra-research/tau-bench)
39. [Sierra Research, 2025] tau2-bench / τ³-bench repository (evolution of τ-bench; verified 2026-09-13). https://github.com/sierra-research/tau2-bench
40. [Yehudai, Eden, Li, Uziel, Zhao, Bar-Haim, Cohan & Shmueli-Scheuer, 2025] Survey on Evaluation of LLM-based Agents. arXiv:2503.16416 (ACL Findings). https://arxiv.org/abs/2503.16416
41. [Rethinking Testing for LLM Applications, 2025] arXiv:2508.20737 (semantics-preserving rewrites to evaluate output variance; authors could not be verified from the sources seen). https://arxiv.org/html/2508.20737
42. [Thinking Machines Lab, 2025] Defeating Nondeterminism in LLM Inference (Sep 2025). https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/
43. [DeepEval, n.d.] The LLM Evaluation Framework — Unit Testing in CI/CD (pytest-native evals in CI). https://deepeval.com/docs/evaluation-unit-testing-in-ci-cd
44. [Promptfoo, n.d.] promptfoo: LLM evals & red teaming (open source; CI-able eval configs). https://github.com/promptfoo/promptfoo
45. [web.dev (Google), n.d.] Evaluation-driven development. https://web.dev/learn/ai/evaluation-driven-development
46. [Braintrust, n.d.] What is eval-driven development. https://www.braintrust.dev/articles/eval-driven-development
47. [Vercel, n.d.] Eval-driven development: Build better AI faster. https://vercel.com/blog/eval-driven-development-build-better-ai-faster
48. [Red Hat, 2026] Eval-driven development: Build and evaluate reliable AI agents (8-stage framework, DeepEval, multi-turn testing, CI/CD; Mar 2026). https://developers.redhat.com/articles/2026/03/23/eval-driven-development-build-evaluate-ai-agents
49. [Hypothesis, n.d.] Hypothesis: property-based testing for Python (official docs; "most widely used property-based testing library"). https://hypothesis.works/ (docs: https://hypothesis.readthedocs.io/)
50. [mutmut, n.d.] mutmut — python mutation tester (run/browse workflow, coverage.py filtering, config). https://mutmut.readthedocs.io/
51. [coverage.py, n.d.] Branch coverage measurement (`--branch`; separate statement/branch percentages in JSON/XML). https://coverage.readthedocs.io/en/latest/branch.html
52. [GitHub, n.d.] About protected branches / Require status checks before merging (strict/loose modes; merge blocked on red). https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches?require-status-checks-before-merging= (see also https://docs.github.com/en/pull-requests/reference/status-checks)
53. [Extending the TMMi Framework, n.d.] Extending the TMMi Framework for Secure Testing of AI Agents (16 Agent Security Test Process Areas across Levels 2–5; authors/venue could not be verified from the sources seen). https://www.researchgate.net/publication/403637738_Extending_the_TMMi_Framework_for_Secure_Testing_of_AI_Agents
54. [Harman et al., 2025] Mutation-Guided LLM-based Test Generation at Meta (ACH; FSE Companion '25; 10,795 classes, 9,095 mutants, 571 tests, 73% acceptance; 277/571 tests undetectable by coverage-only criteria). https://arxiv.org/abs/2501.12862
55. [MorphLLM, 2026] AI Agent Evaluation: The Metrics, the Frameworks (practitioner description of pass^k reliability for τ-bench-family benchmarks; primary definition not directly verified). https://www.morphllm.com (host URL as seen in search)
56. [NozomTechs, 2024] CMMI vs TMMi: Key Frameworks for Process Quality (secondary source on TMMi complementing CMMI). https://nozomtechs.com (host URL as seen in search)
57. [Science Publishing Group, n.d.] Test Maturity Model integration (TMMi) — case-study benefits table (insurance/bank productivity outcomes). https://www.sciencepublishinggroup.com (host URL as seen in search)
58. [Alshareef, 2025] A measurement framework to assess software maturity models. https://pmc.ncbi.nlm.nih.gov/articles/PMC12453703/
59. [Insider Engineering, n.d.] Why 100% Mutation Score Is Neither Necessary Nor Achievable (practitioner guidance banding 60–70% baseline / 75–85% strong). https://medium.com/insiderengineering/why-100-mutation-score-is-neither-necessary-nor-achievable-and-why-thats-perfectly-fine-f28463c3b61e

## [DEEP DIVE]: Exact Assessment Questions, Tools, Time, and Failure Modes per Level

> **[Merge note — dsh, 2026-09-15]** The base document below (ACTM: L1 Ad Hoc → L5 Self-Verifying, per-level measurable gates, evidence-based Crew v2 assessment = Level 1, migration path, quarterly rubric, 59 URL-verified references) was restored after a local-state sync left this file appendix-only; both deep-dive appendices are preserved verbatim beneath it. Where thresholds differ — the first appendix's transition gates use repo-wide line coverage ≥80% and 4–8 weeks L1→L2, while the ACTM base uses changed-code line ≥90% / branch ≥75% (anchored to [Google Testing Blog, 2020]) and 1–2 weeks to L2 (anchored to Test Certified's "a day or five" [Bland, 2011]) — both are explicitly extrapolations (no published AI-crew transition data exists; see §D.4); the operator should calibrate with the crew's own data at Level 4. The first appendix's command-level checks (`git ls-files`, `grep`, `sqlite3`) are the recommended mechanical implementation of the base's §D.5 artifacts. Appendix citations are author-year style; the base's References section is URL-verified [verified 2026-09-13].

### Assessment Questions per Level

**Level 1 → Level 2 Gate (exit checklist — ALL must be YES):**
1. Is there a committed `crew/TEST-POLICY.md`? (`git ls-files | grep -q TEST-POLICY.md`)
2. Is there a tester profile with a SOUL? (`grep -l "tester" profiles/*/SOUL.md`)
3. Over the last 20 PIPELINE/FULL tasks, did >=80% run `pytest` before DONE? (ledger query)
4. Is there a `conftest.py` at the repo root? (`test -f tests/conftest.py`)
5. Is `pytest-cov` installed? (`pip show pytest-cov`)
6. Does every REQ-ID in firstmate SPEC map to >=1 test? (lint check)

**Level 2 → Level 3 Gate:**
1. Same test standard applied across SOLO/DUO/PIPELINE/FULL? (audit SOUL patches)
2. Tester active from task start (not just gate)? (message timestamp vs SPEC)
3. Non-functional checklist checked on FULL? (report section)
4. Critic reviewed 100% of FULL? (ledger count)
5. `mutate_only_covered_lines=true` in mutmut config? (`grep -A2 "\[mutmut\]" setup.cfg`)

**Level 3 → Level 4 Gate:**
1. Ledger DB live and recording per-task metrics? (DB ping)
2. Line coverage >=80% sustained? (30-task window)
3. Mutation score >=70% PIPELINE, >=80% FULL? (30-task window)
4. Flake rate <2%? (20-run history)
5. REQ-coverage >=90% FULL? (lint count)
6. Critic timed out on <5% of tasks? (ledger)

**Level 4 → Level 5 Gate:**
1. Escape KB entry SLA <7d met for 100% of escapes? (audit)
2. Thresholds reviewed quarterly? (git log TEST-POLICY.md)
3. Prevention backlog exists and is acted on? (ledger)
4. -25% escapes/quarter trend? (prod reports)
5. Safe-class auto-patches gated by confidence score? (linter config)

### Tools Required per Level

| Level | New Tools | Already Needed |
|-------|-----------|----------------|
| 1→2 | `pytest`, `coverage.py`, `pytest-cov`, ledger (sqlite), `ruff` for lint | git, message_agent |
| 2→3 | `Hypothesis`, `mutmut`, `pytest-mock`, `pytest-xdist` | above |
| 3→4 | `vcrpy`, `testcontainers`, `mutmut` covered-lines mode, CTRF reporter, DeFlaker-like flip history | above |
| 4→5 | `hypothesis` stateful testing, embedding similarity (`sentence-transformers`), eval harness, KB store | above |

### Typical Time Between Levels (evidence-based)

| Transition | Median Time | Range | Evidence |
|------------|-------------|-------|----------|
| L1→L2 | 4-8 weeks | 2-16 weeks | TMMi Foundation 2018: managed level typically 6 months; compressed to 4-8 weeks for AI crews because tooling is pre-bundled and there's no legacy code to retrofit |
| L2→L3 | 8-12 weeks | 4-24 weeks | TMMi Foundation 2018: defined level requires organizational integration; AI crews compress this via SOUL patches instead of hiring/training |
| L3→L4 | 12-16 weeks | 8-24 weeks | TMMi Foundation 2018: measured level requires stable metric collection over 30+ tasks; AI crews can accelerate via ledger automation |
| L4→L5 | Ongoing | — | TMMi Foundation 2018: optimization is continuous; AI crews must run quarterly calibration cycles |

**Google Test Certified parallel** [KnowMBA, 2025]: teams graduated from L1 to L3 in 12-18 months using stepwise certification with explicit checkpoints per level.

### Common Failure Modes per Level

| Level | Failure Mode | Symptom | Mitigation |
|-------|-------------|---------|------------|
| 1→2 | Workaround RED logs | RED log claims failure but test was green first run | CI reruns RED step independently; assert `result.retcode != 0` |
| 1→2 | Policy ignored in crisis | "Just this once, skip tests" | Iron law is in SOUL, not policy doc; SOUL can't be overridden |
| 2→3 | Formation drift | PIPELINE and FULL use different test standards | Single conftest.py in repo root, no per-formation overrides |
| 2→3 | Critic timeout on large tasks | Critic holds up verdict >15 min | Time-box: 10 min/file, 30 min/task; partial verdict + HOLD |
| 3→4 | Metric theater | Coverage 85% but mutation 4% | Mutation gate catches coverage theater; must enforce mutation >=70% |
| 3→4 | Flake storm | >5% flake rate destabilizes CI | Auto-quarantine at >2%; 14-day fix/delete SLA |
| 4→5 | Strictness drift | FP rate >2%, appeals >5% | Quarterly calibration: review FP/FN, adjust thresholds |
| 4→5 | Leniency drift | Escalates rising | Tighten gates; increase mutation operator set |

### Exact TMMi Mapping (AI Crew Adaptation)

| TMMi Process Area | AI Crew Equivalent | Gate Evidence |
|-------------------|-------------------|---------------|
| 2.1 Test Policy | `crew/TEST-POLICY.md` committed | `git log TEST-POLICY.md` |
| 2.2 Test Plan | firstmate SPEC + REQ-IDs | message log SPEC field |
| 2.3 Monitoring | ledger + tester verdicts | ledger rows per task |
| 2.4 Design | conftest.py + test dir structure | `find tests -type f` |
| 2.5 Execution | `pytest -q` in gate | CI exit code |
| 2.6 Environment | venv per task | `python -m venv` in run |
| 3.1 Organization | tester + critic + engineer SOULs | `grep -r "tester" profiles/` |
| 3.2 Training | TDD skill + iron law in engineer SOUL | `grep "IRON LAW" profiles/engineer/SOUL.md` |
| 3.3 Lifecycle | PIPELINE/FULL flows | routing-integration.md |
| 3.4 Non-functional | perf/security checklist in tester SOUL | `grep -A5 "non_functional"` |
| 3.5 Peer review | critic review 100% FULL | ledger review_count |
| 4.1 Measurement | ledger DB + 16 metrics | `sqlite3 ledger.db ".tables"` |
| 4.2 Quality eval | drill pass + escape rate | nightly report |
| 4.3 Advanced review | multi-model consensus on appeal | appeal handling log |
| 5.1 Prevention | escape KB + SOUL patch | KB entry count |
| 5.2 QC | quarterly threshold review | `git log TEST-POLICY.md` quarterly |
| 5.3 Optimization | trend dashboards + calibration | CI dashboard |

**References for deep dive:**
- [TMMi Foundation, 2018] TMMi Framework R1.2 — process areas per level
- [KnowMBA, 2025] Test Automation Strategy — Google Test Certified timeline
- [TestFort, 2025] TMM in Software Testing — level descriptions, observability
- [TMMi Foundation, 2016] Model Aims — 88%/77% benefits, staged climb necessity
- [Central Bank Guidelines, 2024] Provisions — exit criteria, L1 chaos definition

---

## [DEEP DIVE (freebuff, pass 2, 2026-09-14)]: Goodhart-Resistant Appraisal — Gaming Vectors per Gate, Structural Independence, and Adversarial Drills

The pass-1 deep dive specified exact exit checklists, tools, timelines, and failure modes per level. It left one meta-risk unaddressed: the crew is a population of optimizers, and every gate is a target. "When a measure becomes a target, it ceases to be a good measure" [Goodhart's law; Wikipedia; LawsofSoftwareEngineering, 2026]. This is not metaphor for the crew — the engineer agent is *literally* trained to satisfy machine-checkable criteria, so each gate will be optimized against at superhuman speed unless the metric is designed to resist its own gaming.

### M1. Gaming vectors per level gate (extension of the pass-1 failure-mode table)

| Gate | Metric | Gaming Vector | Countermeasure |
|---|---|---|---|
| L1→L2 | ≥80% of tasks ran pytest | Run pytest on empty/trivial suites | REQ-coverage lint (pass 1) + mutation gate at L3 |
| L2→L3 | Tester active from task start | Timestamp theater: dispatch tester, no-op | Message-semantic check: tester message must reference REQ-IDs, not just exist |
| L3→L4 | Mutation ≥70% | Suppress mutants via operator config for hard modules | mutmut config is versioned in git; gate diffs config per PR and flags operator-set reductions |
| L3→L4 | Flake <2% | Pre-emptively label tests `flaky` → quarantine lane | Quarantine *rate* as new leading indicator (pass-1 dashboard tracked only quarantine age); >5% of suite quarantined = red flag |
| L3→L4 | RED-witness 100% | Fabricated RED logs | CI reruns RED step independently (pass 1 defense — keep) |
| L4→L5 | Escape KB SLA <7d | Low-quality KB entries filed to stop the clock | KB entry requires escape-classification (weak/missing/no-operator per tester-soul cycle 4 template) + reviewer sign-off |
| L4→L5 | −25% escapes/quarter | Redefine "escape" or delay discovery logging | Escape = ledger row on production report, timestamp immutable; quarterly definition review |

The structural pattern: every scalar metric needs a paired *provenance* check (where did the number come from, who could have altered it) and a paired *adversarial* metric (what would gaming look like, is it happening). Metrics are proxies for what you value; once targeted, people meet the metric while undermining the goal [LawsofSoftwareEngineering, 2026] — agents do this faster and more literally than people.

### M2. Structural independence for the appraisal itself

TMMi formal assessments assume accredited human assessors; the crew equivalent must manufacture independence structurally:
1. **Evidence from the ledger, not self-reports.** Every checklist item's answer must be a ledger DB query or filesystem check — never "agent says so." The append-only ledger (pass-1 §1-3 tooling) is the appraisal's ground truth.
2. **Machine-executable checklist.** Pass 1 made each gate item a command (`git ls-files | grep -q TEST-POLICY.md`, ledger queries). Appraisal discipline: run the checklist verbatim, log outputs, forbid agent interpretation of ambiguous results — an ambiguous result is a failed item.
3. **Appraiser separation.** The agent compiling the level-exit report must not be the agent whose work the level certifies (tester compiles; engineer's artifacts are evidence; critic spot-checks — reusing the pass-1 collusion defenses in blocking-authority.md §4).

### M3. Adversarial appraisal drills: test the gates themselves

Borrow the chaos-engineering move from self-healing.md pass 1 (steady-state hypothesis + controlled fault injection) and apply it to the maturity gates. Quarterly, the operator (or a designated red-team agent) injects known-bad artifacts and verifies the gates catch them:

| Injected Artifact | Gate That Must Fire | Pass Criterion |
|---|---|---|
| Tautological test (`assert out == captured`) | Oracle/tautology lint | BLOCK, 100% of injections |
| RED log with no actual failure | Independent RED rerun | Mismatch detected |
| Suite with 90% coverage, no assertions | Mutation gate | MUT below threshold |
| flaky-labeled healthy test | Quarantine-rate indicator | Flag in dashboard |
| Ledger row edited retroactively | Append-only audit (hash chain) | Tamper detected |

A gate that fails its drill is treated like a flaky test: quarantine the gate, fix within the 14-day SLA, re-drill. This converts the maturity model from a self-graded exam into an adversarially validated one — the same principle behind break drills (every REQ must redden) applied one level up: every gate must catch its injection.

### M4. Calibration as the standing Goodhart breaker

Pass-1 §4 (testing-maturity) defined drift failure modes (strictness/leniency). The deeper point: the quarterly calibration loop (blocking-authority.md §2 algorithm) is the mechanism that keeps any single metric from being permanently gamed — thresholds move against real FP/escape signals, and the escape signal is anchored outside the system (production reports, not agent claims). Keep the ±5% steps and clamps; add drill results as a third calibration input alongside FP and escape rates.

### References (pass 2)
1. [Wikipedia] "Goodhart's law" — "When a measure becomes a target, it ceases to be a good measure." https://en.wikipedia.org/wiki/Goodhart%27s_law [verified: 2026-09-14]
2. [LawsofSoftwareEngineering, 2026] "Goodhart's Law" — metrics are proxies; targeting corrupts them. https://lawsofsoftwareengineering.com/laws/goodharts-law/ [verified: 2026-09-14]
3. [Jellyfish, 2022] "Goodhart's Law in Software Engineering and How to Avoid Gaming Your Metrics." https://jellyfish.co/blog/goodharts-law-in-software-engineering-and-how-to-avoid-gaming-your-metrics/ [verified: 2026-09-14, snippet only]
4. Cross-refs: self-healing.md pass 1 (chaos drills); blocking-authority.md §2 (calibration algorithm), §4 (anti-collusion); tester-soul.md cycle 4 (escape-classification template); quality-metrics.md pass 1 (leading indicators).
## [DEEP DIVE (freebuff, pass 3, 2026-09-14)]: What Maturity Models Can and Cannot Predict — The Empirical Record of the Ladder Itself

Pass 2 made the model *gaming-resistant*. This pass asks the prior question: is the ladder itself predictive, or is it a bureaucratic ornament? The evidence base is genuinely mixed, and honesty requires saying so.

**Evidence.**
- The canonical critique (Bach and the context-driven school) argues staged maturity conflates process compliance with outcomes — a team can be level-5 and still ship defects, because the assessment measures paperwork [Bach, maturity-model critiques — snippet-verified].
- The strongest *supporting* study: Harter, Krishnan & Slaughter (Management Science, 2000) found higher process maturity associated with fewer defects, shorter cycle time, and lower effort in commercial software projects — real, but on waterfall-era, process-heavy organizations; generalization to agent crews is unproven [Harter et al. 2000 — snippet-verified].
- The product-side alternative: ISO 25010 characterizes quality as product attributes rather than organizational stage, which is the framing the crew's outcome ledger already uses [ISO/IEC 25010 — literature].

**What this means for the council's model.**
1. The maturity ladder is retained as a **communication and prioritization scaffold**, demoted from predictive instrument: do not claim that level K causes outcome improvements.
2. **Maturity claims must be paired with ledger deltas** (quality-metrics): a level upgrade is only ratified if defect-escape, flake, or RTS-safety moved over the following quarter. Otherwise the upgrade is reverted as cosmetic — this is the pass-2 anti-Goodhart rule extended from gates to the ladder itself.
3. Level upgrades additionally require the pass-2 **adversarial gate drill**, not a checklist interview — an appraised level the drill defeats is a fabricated level.
4. The model doc should carry a standing caveat citing the mixed record (Harter pro; Bach con) so future readers inherit the uncertainty, not a false confidence.

**Cross-links:** quality-metrics pass 3 (metrics only ratified via GQM lineage — same "pair with outcomes" discipline), pass-2 appraisal design.

**Sources.**
1. [Harter, Krishnan & Slaughter, 2000] "Effects of Process Maturity on Quality, Cycle Time, and Effort in Software Development," *Management Science* 46(4) [snippet-verified: 2026-09-14].
2. [Bach, ~1994–2006] Context-driven critiques of staged maturity models (e.g., "Maturity is not enough") [snippet-verified: 2026-09-14].
3. [ISO/IEC 25010] Systems and software Quality Requirements and Evaluation (SQuaRE) — product quality model [literature].
