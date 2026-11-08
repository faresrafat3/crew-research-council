# Browser agent attention and context folding (SOTA 2026)

**Artifact:** `RESEARCH-COUNCIL/OUTPUT/browser-agent-attention-folding-sota-2026.md`
**Profile:** auto-researcher · **Date:** 2026-11-08 · **Method:** live web + arXiv + GitHub retrieval, every number traced to a fetched source in the ledger.

## Executive summary

The browser is the hardest observation environment an LLM agent faces because the page is paid for in tokens on every step and the payment is repeated on every subsequent step. Live measurements put a single raw accessibility snapshot at 20,000 to 114,000 tokens, and one Playwright MCP page view at 604,785 tokens against 2,771 for a folding tool [13][8]. The 2024 to 2026 research literature converged on the same diagnosis, observation over-ingestion, but the published cures are incremental: AgentOccam, the strongest simple baseline, cut observation tokens per step by only 14.4% relative to its own no-scroll variant and ended *above* the vanilla baseline per step, while buying a 26.6-point success gain [1]. The only published interventions that reach the 95% class are context-layer mechanisms (snapshot supersession, 142K to 327K input tokens; task replay from memory, 251K to 89K) rather than DOM pruning [12][7]. This monograph records the measured state of the art, names five open gaps, and specifies a five-layer folding engine with a hard 300-token-per-step budget, an identity-bound element model, and a distribution contract built on the stateless MCP 2026-07-28 core.

## Key findings

- **The raw material is enormous and measured.** A Playwright MCP snapshot of one Wikipedia article cost 604,785 tokens; a folding browser tool cost 2,771 on the same page. On a 4,790-element GitHub repository page, rendered HTML was 273,313 tokens and the accessibility snapshot 22,283 tokens, a 12.3x difference [8][9].
- **DOM pruning alone is not the 95% lever.** AgentOccam's own Table 4 shows observation optimisation moving the average from 3,376.2 to 2,891.1 tokens per step, 14.4%, while disabling scrolling (loading the full page) raised it from 2,210.2 to 3,376.2 in the first place [1].
- **FocusAgent is the strongest published pruning result.** A lightweight LLM retriever over the accessibility tree reduced observation size by more than 50% on average and often more than 80%, with modest success degradation on WorkArena L1 and WebArena [10].
- **The context layer beats the page layer.** Gemini CLI's snapshot superseder replaced all but the latest snapshot with a ~30-token placeholder and cut a representative task from 327K+ input tokens over 43 requests to 142K over 20 requests, a 56.6% token cut and a 53.5% call cut [12].
- **Replay from memory is the largest single published lever.** Dejo's first run of 19 tasks cost 251K tokens; every subsequent run cost 89K in 1.2 tool calls, a 78.2% reduction against Playwright MCP's 409K [7].
- **Identifier collapse is a live production defect, not a theoretical one.** Vercel's agent-browser logged stale positional refs silently actuating the wrong element after DOM renumbering and reporting success; ~30% of agent calls were defensive re-snapshots to work around it [27].
- **Stale observations are worse than missing ones.** An independent eight-step test reported 60K to 90K tokens of stale snapshots by steps 12 to 15, with the agent referencing elements that no longer existed [13].
- **Benchmarks are now saturated at the top and broken at the bottom.** Online-Mind2Web's top self-reported score is 97.0% while WorkArena L3 sits at 11.5% for GPT-5 against a 93.9% human baseline, and the two are not measuring the same thing [22][24].
- **No published system holds 300 tokens per step with non-inferior success.** The 95% target is demonstrated by measurement studies and by the folding-tool class, but never with a benchmark-validated success rate. That is the gap this design targets.

## The problem: observation over-ingestion

### Why the browser is the hardest environment

A web page is a document designed for a human with a retina and a working memory of about 4 chunks. A browser agent gets the same document as a token sequence and is charged for all of it. The published measurements agree on the scale:

| Observation form | Measured size | Source |
|---|---|---|
| Rendered HTML, GitHub repo page (4,790 elements) | 273,313 tokens | [9] |
| Accessibility snapshot, same page | 22,283 tokens | [9] |
| Raw DOM on complex pages | 10,000 to 100,000 tokens | [4] |
| Accessibility tree, routine web pages | 20,000 to 80,000 tokens per step | [15] |
| Salesforce accessibility tree (one page) | 114,000 tokens | [13] |
| Playwright MCP page view (Wikipedia) | 604,785 tokens | [8] |
| Same page through a folding tool | 2,771 tokens | [8] |

The accessibility tree is already roughly an order of magnitude smaller than the DOM, and it is still too large [10]. The design conclusion is that the tree is the wrong unit of currency. A task needs a single fact, and the field keeps paying for the whole page to get it [15].

### The arithmetic of a session

Cost is not linear in steps. A loop that re-sends its whole transcript pays `1 + 2 + ... + n` prompt units for `n` steps, so cost is O(n^2) in task length [14]. Measured on a ten-step run, input tokens climbed 637, 677, 716, 759, 800, 839, 876, 917, 953, a 38% rise across the run, and 21% of that run's input bill was re-reading text the agent had already sent, on a page that distills to 10 nodes [14].

The second-order effect is the expensive one. Every screenshot and every snapshot stays in the conversation history for the rest of the session and is re-sent on every subsequent call [39]. On browser workloads the observation layer is 5 to 10x more expensive than a regular MCP workload, and doubling task length quadruples the bill [39].

## Reference methods 2024 to 2026

### AgentOccam

AgentOccam (arXiv:2410.13825, ICLR 2025) is the reference point for the observation-and-action alignment school. It makes three rule-based changes: remove non-essential actions, simplify web page elements into Markdown, and add `branch` and `prune` planning actions that let the agent self-organise a planning tree and filter past traces [1].

**Success, WebArena (812 tasks):**

| Agent | Model | Success rate |
|---|---|---|
| WebArena replication | GPT-4-Turbo | 16.5% |
| SteP replication | GPT-4-Turbo | 33.3% |
| AWM | GPT-4 | 35.5% |
| WebPilot | GPT-4o | 37.2% |
| AgentOccam | GPT-4-Turbo | **43.1%** |
| AgentOccam + Judge | GPT-4-Turbo | 45.7% |

The headline deltas are +9.8 absolute points (+29.4%) over the previous state of the art and +5.9 (+15.8%) over concurrent work, and +26.6 absolute points (+161%) over a similar plain agent [1].

**Observation tokens per step, Table 4 of the paper (gpt2 tokenizer, average across WebArena sites):**

| Variant | All | Shopping | Shopping Admin | GitLab | Map | Reddit | Multisite |
|---|---|---|---|---|---|---|---|
| Vanilla | 2210.2 | 2272.1 | 2460.2 | 2199.1 | 1883.2 | 2132.4 | 1751.0 |
| Remove actions | 1652.0 | 1644.7 | 2133.1 | 1981.3 | 912.0 | 1081.2 | 1296.8 |
| + no scrolling | 3376.2 | 3148.0 | 5403.7 | 3364.9 | 1378.1 | 2603.6 | 1975.5 |
| + observation optimisation | 2891.1 | 1722.5 | 4791.7 | 2560.8 | 1476.4 | 3332.3 | 1619.4 |
| + history replay | 3051.3 | 1802.6 | 5140.2 | 3153.3 | 862.1 | 3156.1 | 2030.3 |
| AgentOccam | 2930.9 | 1634.2 | 4920.7 | 3126.8 | 1056.0 | 3697.8 | 1282.5 |

**The honest reading.** Relative to the no-scroll variant, observation optimisation cut tokens by 14.4% (3376.2 to 2891.1). Relative to the vanilla baseline, AgentOccam is 32.6% *more* expensive per step (2210.2 to 2930.9), because it deliberately loads the full page instead of scrolling. It also takes more steps (9.0 versus 6.2) [1]. AgentOccam is a success-rate result, not a token-reduction result, and any claim that it cut observation tokens by 95% is false. Its real contribution is the planning tree: `branch` and `prune` let the agent exclude history that belongs to an abandoned sub-plan, which is the ancestor of the folding operation.

### Agent workflow memory

Agent Workflow Memory (AWM, arXiv:2409.07429, ICML 2025) induces reusable sub-routines, workflows, from trajectories and injects them into later prompts [2][3]. It operates offline from annotated examples and online from test-time trajectories.

- **+24.6% relative success on Mind2Web and +51.1% on WebArena**, with fewer steps on WebArena [2][3].
- WebArena success 35.5% against BrowserGym's 23.5% [3].
- Online AWM generalises across tasks, websites and domains, beating baselines by 8.9 to 14.0 absolute points as the train-test gap widens [2][3].
- Online induction beats offline on Mind2Web cross-domain step success, 35.5 against 32.6 [3].
- **Offline plus online is not additive.** Combining both underperforms the better single source, because accumulated prompt memories from mismatched distributions interfere [3].

AWM is the strongest published evidence that crystallising a procedure out of a trajectory works. Its limitation is that the memory is a prompt artifact: it grows the prompt, and the paper reports success and step counts but not a token budget.

### Prune4Web

Prune4Web (arXiv:2511.21398) moves DOM processing from LLM reading to programmatic pruning. An LLM writes a task-specific Python scoring program that traverses the full DOM, scores and ranks elements, and keeps the relevant subset [4].

- Targets DOM structures of 10,000 to 100,000 tokens [4].
- Low-level sub-task grounding rose from 46.80% to 88.28%, a +41.48 absolute point gain [4].
- **Evaluated only on Mind2Web**, which is an offline benchmark of cached static HTML snapshots with replayed reference trajectories [4][10].

The Mind2Web-only evaluation is the load-bearing limitation. FocusAgent states it directly: it is unclear whether the scoring script is generated per step or per episode, and operating on raw DOM is itself costly [10]. Prune4Web demonstrates that a generated pruning program can be effective on static snapshots; it does not demonstrate it on a dynamic live page.

### FocusAgent

FocusAgent (arXiv:2510.03204) is the most useful pruning result because it measures both size and success on live benchmarks. A lightweight LLM retriever reads the accessibility tree with numbered lines, the task goal and optional history, and returns the line spans worth keeping [10].

- **Observation size reduced by more than 50% on average and often more than 80%**, with modest degradation against full-observation baselines [10].
- Evaluated on WorkArena L1 and WebArena through BrowserGym, using the 381-task test split, 15 and 30 step limits, a 40k agent context and a 128k retriever context [10].
- Retrieval models included GPT-4.1-mini, GPT-5-mini, Qwen3-8B and Qwen3.5-9B; backbones included GPT-4.1, Claude-3.7-Sonnet and Qwen3-235B-A22B [10].
- **Security side effect:** the retriever removes prompt-injection content from the observation, cutting attack success while holding task success in attack-free settings [10].
- **Failure mode:** loop traps dominate. Of the WorkArena L1 tasks where the baseline succeeded and FocusAgent failed, 12 of 15 cases (GPT-4.1 backbone) and 16 of 18 (Claude-3.7 backbone) were truncated at the step limit, with loop traps the leading pattern [10].
- **Scope caveat the paper itself reports:** smaller models benefit from compact inputs while stronger models can gain from richer inputs, so pruning matters under cost, security and weak-backbone constraints rather than universally [10].

### Filtering with learned rankers

The filtering line trains a compact ranker over page elements and keeps the top candidates. A DeBERTa model fine-tuned on Mind2Web trajectory data and transferred to WebArena raised a LLaMA-2-70B agent from 1.97% to 2.96% success, and a zero-shot ColBERT retriever reached Recall@10 of 0.52 on Mind2Web and 0.47 on WebArena [11].

The absolute numbers are the finding. On a 4K-context backbone the retriever helps, but the success rate stays under 3%. Learned filtering is a real technique and a dead end as a primary strategy for capable agents, because the bottleneck is not element ranking.

### Set-of-marks prompting

Set-of-Marks (SoM, arXiv:2310.11441) overlays numbered marks on image regions so a multimodal model can ground references symbolically rather than by coordinate regression [26].

- RefCOCOg referring expression comprehension: 25.7% direct coordinate output to **86.4%** ACC@0.5 with SoM [26].
- RefCOCOg referring segmentation: near zero to **75.6%** mIoU [26].
- Zero-shot SoM beat fully fine-tuned specialists including PolyFormer [26].

SoM matters to this design for one reason: it converts a spatial grounding problem into a symbolic reference problem, which is the same move as giving a DOM element a durable id. The mark is the identity; the region is the node. A folding engine should treat element identity as the primitive and coordinates as the fallback.

### Signal-driven observation

Signal-Driven Observation (SDO, arXiv:2606.06708) names the architectural error precisely: coupling observation frequency to action frequency forces the agent to re-read the full page state at every step regardless of whether the state changed [15].

SDO proposes a dedicated sub-call that reads the full DOM but returns only task-relevant elements and selectors, re-invoked only when a lightweight signal detector fires on URL transitions, newly visible interactive elements, action failures or exogenous browser events [15].

The paper is a position paper and reports no benchmark numbers, but it supplies the three downstream failure modes the field should design against: **context rot**, **loop-trapping** and **goal drift** [15]. It also states the open problem honestly: as the trajectory lengthens, older observations must be summarised or discarded, and how to do that without losing the information needed for backtracking or loop detection is unresolved [15].

### AgentFold

AgentFold (arXiv:2510.24699) treats context as a dynamic workspace and learns a `folding` operation that manages the trajectory at multiple scales, performing granular condensations to preserve detail or deep consolidations to abstract away entire multi-step sub-tasks [16].

- AgentFold-30B-A3B reached **36.2% on BrowseComp and 47.3% on BrowseComp-ZH** with supervised fine-tuning only, no reinforcement learning [16].
- It matched or surpassed DeepSeek-V3.1-671B-A37B and OpenAI o4-mini [16].

This is the closest published relative to the folding engine, and the name collision is exact. The difference is the substrate: AgentFold folds the *conversation* with a learned policy, while the design below folds the *page* with deterministic rules and folds the conversation as a by-product.

### Probe to act

Probe to Act (arXiv:2609.33646) keeps in the history only the elements or regions the agent explicitly probed, acted on or committed as evidence [17].

- The pruned observation history reached about **1.2x** the peak retained input context of a no-observation history, against about **3x** for retaining full observations [17].
- Retention window N=5 steps by default [17].
- A K=2 neighbourhood heuristic used the same 1.2x budget but reached only 31.0% success, below evidence memory, showing that *which* elements survive matters more than how many [17].
- Images were dynamically encoded into 16 to 2,500 visual tokens with a hard 20,480-token context cap [17].

This is the strongest published evidence for the evidential memory rule: memory should be a by-product of perception, not a log of it.

### Related work the design must absorb

Three further results constrain the design. **ARC** (ACL Findings 2026) reports that on BrowseComp a raw interaction history reached 58,500 context tokens by turn 20 while its active context management held at 10,500, an 82% reduction [32]. **Beyond Browsing: API-Based Web Agents** (ACL Findings 2025) reports a browsing agent at 14.8% on WebArena while an API-based agent solved the same intents in three lines of code where browsing failed after 15 steps [37]. **anchortree** supplies the identity mechanism: CDP `backendNodeId` as the primary key, rebinding a logical id to a recreated node by scoring a content fingerprint, and emitting a token-cheap diff instead of a fresh snapshot [29].

## Token and latency measurements

### Raw observation sizes

| Measurement | Value | Source |
|---|---|---|
| HTML to accessibility snapshot ratio, GitHub page | 273,313 to 22,283 tokens (12.3x) | [9] |
| Playwright MCP versus folding tool, Wikipedia | 604,785 versus 2,771 tokens | [8] |
| Playwright MCP versus folding tool, one Hacker News step | 12,494 versus 462 tokens | [8] |
| Playwright MCP versus Chrome DevTools MCP, Wikipedia | 604,785 versus 393,149 tokens | [8] |
| Playwright MCP versus browser-use 0.13.10, Wikipedia | 604,785 versus 8,369 tokens | [8] |
| Playwright MCP snapshot on a complex page | more than 50,000 tokens | [13] |
| Salesforce accessibility tree | 114,000 tokens | [13] |
| Playwright CLI through MCP versus directly | 114,000 versus 27,000 tokens per test | [13] |
| Eight-step test through MCP versus CLI | 89,000 versus 24,000 tokens | [13] |
| Tool schema share of a static toolset | 60 to 80 percent of token usage | [13] |
| Playwright MCP tool schemas | about 4,200 tokens across 26+ tools; CLI `--help` about 68 | [13] |
| Anthropic code execution with MCP | 150,000 down to 2,000 tokens (98.7%) | [13] |

The pattern is consistent across independent measurers: the general-purpose browser tool pays 10 to 200 times what a purpose-built observation layer pays for the same page, and the tool schema is a fixed tax paid before the first action [13].

### Session-level accumulation

The supersession and replay levers are the only published mechanisms that reach the 95% class, and both operate on the *context*, not on the page.

**Supersession.** Gemini CLI's snapshot superseder scans the chat history for `take_snapshot` responses and, when two or more exist, replaces all but the last with a ~30-token placeholder before each model call [12]. On a representative Wordle task with gemini-3-flash-preview:

| Configuration | Input tokens | Model requests |
|---|---|---|
| With superseder | 142K | 20 |
| Without superseder | 327K+ | 43 |
| Reduction | 56.6% tokens | 53.5% calls |

[12]

**Replay.** Dejo measured 19 tasks on lesser-known websites in fresh sessions, with Claude Sonnet 5 at medium effort [7]:

| Configuration | Correct | Tokens | Tool calls | Cost | Time |
|---|---|---|---|---|---|
| Dejo, first run | 19 of 19 | 251K | 4.7 | $0.17 | 31 s |
| Dejo, every run after | 19 of 19 | 89K | 1.2 | $0.02 | 16 s |
| Playwright MCP, every run | 17 of 19 | 409K | 6.5 | $0.23 | 40 s |
| Playwright CLI, every run | 18 of 19 | 559K | 8.4 | $0.28 | 38 s |

The 89K replay is a 64.5% cut against Dejo's own first run and a 78.2% cut against Playwright MCP [7]. The mechanism is crystallisation: the second visit does not re-read the site.

**Context accumulation curves.** ARC reports raw history at 4,500 tokens on turn 1 and 58,500 on turn 20, against 4,000 and 10,500 with active management [32]. The rote project reports a ten-step run climbing from 637 to 953 input tokens with 21% of the bill re-reading already-sent text [14]. An independent eight-step test reports 60K to 90K tokens of stale snapshots by steps 12 to 15, with the agent beginning to reference elements that no longer existed [13].

### The replay lever

The three published replay mechanisms are complementary and none is distributed:

- **Prompt memory (AWM):** induce workflows from trajectories and inject them; +24.6% relative on Mind2Web, +51.1% on WebArena, but offline plus online interferes [2][3].
- **Skill abstraction (SCAFFOLD, EMNLP Findings 2026):** recursive parametric skill abstraction with selector memoisation, caching a resolved accessibility-tree path with a structural signature keyed by site, skill and parameter, falling back to VLM grounding only on mismatch [3].
- **Memory replay (rote):** three tiers, working within a run at O(n^2), episodic across runs of a task, semantic across tasks on a site, with the precondition that memory that might be wrong is worse than no memory [14].

### Industrial tool comparison

The webdriverio benchmark runs a fixed sample of 100 Online-Mind2Web tasks against seven browser tool setups with the same model, harness and prompt [5]. Medians per run; tokens include cache reads and writes [5].

**DeepSeek V4.1 Flash, run 2026-10-09:**

| Setup | Tokens per task | Cost per task | Success | Time per task | Tool calls |
|---|---|---|---|---|---|
| playwright-mcp | 652k | $0.028 | 48% | 123 s | 28 |
| playwright-mcp-tuned | 574k | $0.029 | 50% | 106 s | 27.5 |
| stagehand | 354k | $0.022 | 56% | 91 s | 22 |
| wdio-mcp | 340k | $0.016 | 54% | 114 s | 32 |
| wdio-session | 168k | $0.010 | 58% | 150 s | 26.5 |
| agent-browser | 735k | $0.036 | 50% | 157 s | 36.5 |
| playwright-cli | 641k | $0.029 | 57% | 149 s | 33 |

**Claude Sonnet 5, run 2026-10-05 (50 tasks):**

| Setup | Tokens per task | Cost per task | Success | Time per task | Tool calls |
|---|---|---|---|---|---|
| playwright-mcp | 363k | $0.177 | 32% | 74 s | 16 |
| playwright-mcp-tuned | 284k | $0.165 | 36% | 76 s | 14 |
| stagehand | 549k | $0.216 | 60% | 105 s | 26 |
| wdio-mcp | 241k | $0.107 | 52% | 73 s | 18.5 |
| wdio-session | 306k | $0.128 | 54% | 109 s | 20 |
| agent-browser | 1116k | $0.355 | 48% | 127 s | 32.5 |
| playwright-cli | 680k | $0.259 | 40% | 119 s | 26.5 |

[5]

Two readings matter. First, the spread is 3.9x in tokens and 3.6x in success within the same benchmark and model, so the tool layer is a first-order variable and not a rounding error [5]. Second, the ranking inverts between models: stagehand is third on tokens and first on success with DeepSeek, but second most expensive and first on success with Sonnet, while agent-browser is the most expensive on both [5]. There is no dominant tool; there is a dominant *design property*, which is whether the tool returns a diff or a snapshot.

A nine-task comparison of Sentinel, Stagehand and browser-use on Gemini 3 Flash, five runs per cell, reports Sentinel using 3.13x to 56.93x fewer tokens than browser-use and 1.42x to 13.33x fewer than Stagehand, with 45/45 reliability against browser-use 45/45 and Stagehand 39/45, and Stagehand failing a login-plus-logout task 0/5 in its default DOM mode [6]. The author builds Sentinel and discloses the bias; the raw per-run JSON is published for recomputation [6]. The per-task extremes are instructive: 770 tokens for product extraction against browser-use's 43,838 (56.93x), and 2,884 against 114,796 for an authentication flow (39.80x) [6].

Browser Use's own changelog records a Rust rebuild in beta, a 30B-A3B open model at 200 tasks per dollar, a hosted MCP server, and a v4 snapshot approach that Browserbase reports as about 80% more token efficient than Playwright [36]. LangChain's comparison for Deep Agents reports Stagehand passing 90% of tasks for $1.98 at a median 17.4 seconds against Playwright MCP passing 78% for $26.71 at three times the duration, with 26 model turns per task against 10 [21]. Skyvern reports a WebVoyager score of about 68.7% for version 2.0, an 11% token cut and a 3.9% success gain from switching its element description from JSON to HTML, and a 2.3x speedup after deleting RAG [20]. LaVague is reported at 84% success and a 139-second median on an independent FBA benchmark with a stateless memory profile, but that is a vendor-adjacent measurement rather than a standard leaderboard [21].

## Benchmark landscape

### WebArena and its verified variant

WebArena is 812 tasks across e-commerce, a social forum, collaborative software development and content management, with programmatic grading [33]. The original paper reported GPT-4 at 14.41% against a human baseline of 78.24% [33].

| Leaderboard | Top entry | Score | Note |
|---|---|---|---|
| BrowserGym slice (2026-08-11) | GenericAgent-Claude-3.7-Sonnet | 44.6% ± 2.5 | A3-Qwen3.5-9B second at 42.1% [34] |
| Community sheet (2026-11-07) | Narada AI Code | 86.1% | Closed system, 09/2026 [35][38] |
| Community sheet, best open | Deepseek v3.2 | 74.3% | 02/2026 [35][38] |
| WebArena-Verified | Muse Spark 1.1 | 69% | Provider self-report [35] |

WebArena-Verified is a reproducible re-evaluation that reduces the false-negative rate by approximately 11 percentage points, which matters because a measurement artifact of that size is larger than most published improvements [35]. Its leaderboard is compiled from provider self-reports and the site itself warns that rows are comparable only when the subset, environment revision, scaffold, observation interface, step budget and evaluator all match [35].

### Online-Mind2Web

Online-Mind2Web is 300 live tasks across 136 websites with easy, medium and hard stratification [22]. The leaderboard is the most-cited number in the industry and the least comparable:

| System | Score | Caveat |
|---|---|---|
| Browser Use Cloud (bu-max) | 97.0% | Self-reported with a custom agentic judge built on Claude Agent SDK [22] |
| GPT-5.4 native computer use | 93.0% | OpenAI-reported, raw data not public [22] |
| ABP + Claude Opus 4.6 | 90.53% | All 300 task results published; previous SOTA 78.7% [22] |
| TinyFish | 90.0% | All 300 runs published [22] |
| CUAWright + GPT-5.5 | 89.4% | Harness result, not GUI-only [22] |
| UI-TARS-2 | 88.2% | Technical report [22] |
| OpenAI Operator | 61.3% | Judge, harness and task-level results not published [22] |
| SeeAct (gpt-4o) | 30.7% | January 2024 [22] |

[22]

The judge is the score. Human evaluation, WebJudge and custom agentic judges produce different numbers for the same agent, and WebJudge agrees with humans about 85% of the time [22]. Any cross-submission comparison that ignores the judge is not evidence.

### WorkArena L3

WorkArena++ contributes 682 compositional enterprise tasks in ServiceNow, split into L2 (explicit instructions) and L3 (implicit goals via tickets requiring knowledge-base retrieval and independent planning) [23]. Humans solve 93.9% [23].

| Model | WorkArena-L3 success |
|---|---|
| GPT-5 | 11.5% ± 2.1 |
| Claude-3.5-Sonnet | 0.4% ± 0.4 |
| Llama-3.1-70b | 0% |
| Llama-3.1-405b | 0% |
| GPT-4o | 0% |

[24]

This is the strongest counterweight to the Online-Mind2Web optimism. On tasks that require retrieving a procedure, planning, and executing without explicit guidance, the best published result is 11.5% against a 93.9% human baseline, and the original paper reported zero L3 success for every model it tested [23][24]. If a folding engine is to be trusted for enterprise work, this is the benchmark it must move.

### OSWorld

OSWorld is a real-computer environment of 369 tasks with execution-based evaluation [18]. The original paper reported humans at 72.36% and the best model at 12.24% [18]. The current state of the art has moved sharply: EvoCUA-32B reached 56.7% as the best open-weights result, beating OpenCUA-72B at 45.0% and UI-TARS-2 at 53.1% under a strict 50-step constraint where baselines typically need 100 steps [19]. OSWorld-Verified's top entry reached 90.19% at 100 steps and the top general model 85.96%, both above the roughly 72% human baseline [35]. OSWorld 2.0 tells a more cautious story, with Claude Opus 5 at 44.33% binary completion and 77.67% partial credit at a 500-step cap on 108 tasks [35].

The divergence is the lesson: the same benchmark family yields 12.24%, 56.7%, 85.96% and 44.33% depending on the version, step cap, task scope and whether partial credit counts [18][19][35]. A folding engine must be evaluated against a pinned version with a pinned step cap, or the number is meaningless.

### Reading the leaderboards honestly

Four rules fall out of the tables above. First, judge identity dominates: Online-Mind2Web's 97.0% and 30.7% are the same benchmark under different evaluators [22]. Second, step caps dominate: OSWorld's 12.24% and 90.19% differ by evaluation protocol as much as by model [18][35]. Third, self-reporting dominates the top of every table: the highest WebArena, Online-Mind2Web and WebArena-Verified entries are all vendor-reported with unpublished raw data [22][35]. Fourth, the benchmarks that measure *enterprise* work, WorkArena L3, show the smallest gains and the largest human gap [24]. The correct posture is to treat the leaderboards as a map of harness quality, not of model quality.

## Open gaps in 2026

### Gap 1: history pollution is solved in one harness only

Snapshot supersession exists as a merged PR in Gemini CLI and as an architectural argument in SDO, and nowhere else in the surveyed tooling [12][15]. Playwright MCP, browser-use, Stagehand and Skyvern all return snapshots that remain in the conversation. The eight-step test that reported 60K to 90K tokens of stale snapshots by steps 12 to 15 is the clearest published account of the failure, and it concludes that the agent did not run out of context, it ran out of *accurate* context [13]. No benchmark measures stale-snapshot carry-over as a metric.

### Gap 2: identifier collapse is acknowledged but not standardised

Vercel's agent-browser documented the failure precisely: positional refs renumbered by a DOM mutation silently actuate the wrong element and report success, and combobox widgets that insert a node per committed selection shift every later ref by one [27]. Real-world impact included wrong category selections shipped to live product-directory listings, and a Google Maps feed re-render that moved an element from ref e36 to e28 during sequential extraction [27]. The same issue reports that about 30% of agent calls were defensive re-snapshots because refs can become stale [27]. The merged fix binds refs to CDP `backendNodeId` plus frame id, retires ref generations on snapshot, reclaims ids for surviving nodes, never reuses a retired number, and fails loudly on a detached node [28]. anchortree independently reached the same design and reports that Playwright MCP declined persistent element identity for performance reasons [29]. **No standard contract exists.** Every harness implements its own ref lifecycle, and the failure is silent in most of them.

### Gap 3: no published system holds 300 tokens per step with non-inferior success

The 95% target is supported by measurement studies and by the folding-tool class: Anthropic reports 150,000 to 2,000 tokens through MCP, and the folding tools report 2,771 tokens where Playwright MCP reports 604,785 [13][8]. But no peer-reviewed or benchmark-pinned evaluation reports a 300-token-per-step budget with a non-inferiority result against full observation. FocusAgent's 50% to 80% reduction is the strongest academic result and it still lands in the thousands of tokens [10]. **The gap is not the ratio, it is the evidence at the ratio.**

### Gap 4: site crystallisation is demonstrated but not distributed

AWM, SCAFFOLD, rote and Dejo all demonstrate that a second visit can be dramatically cheaper than the first: Dejo 251K to 89K in 1.2 tool calls, AWM +51.1% relative on WebArena, rote's episodic and semantic tiers [7][2][14]. But each is a research artifact or a proprietary service. No open, standard, shareable site-lens format exists, and AWM's own ablation shows that naively accumulating prompt memories from different distributions actively interferes [3]. Crystallisation works and does not compose.

### Gap 5: no universal folding contract exists

MCP 2026-07-28 provides the transport: a stateless core with no handshake and no `Mcp-Session-Id`, per-request protocol version and client capabilities in `_meta`, Multi Round-Trip Requests with a `resultType` of `complete` or `input_required`, cacheable list results carrying `ttlMs` and `cacheScope`, header-based routing via `Mcp-Name` and `Mcp-Method`, and a formal extensions framework [30][31]. The Tasks extension adds `tasks/get`, `tasks/update` and `tasks/cancel` with unguessable task ids and no `tasks/list` [30]. **None of this defines what a browser observation is.** The protocol can carry a folded observation; it does not specify one. That is the contract this design proposes.

## The folding engine design

### Design stance

The engine is a thalamus, not a spotlight. Flat softmax attention can only brighten tokens; the thalamic reticular nucleus gates which signals reach the cortex at all, and the cortex then operates on a pre-filtered stream with a working memory of about 4 chunks [Peircean engine foundations, docs/SCIENTIFIC_FOUNDATIONS.md, sections 2.1 to 2.4]. The design rule is therefore **subtractive gating first**: the default action is deletion, and an addition is admissible only if the retained-token count falls or the task success improves. This is the browser-side translation of the engine's Occam gate.

The engine has one job: produce, for each step, a **fold** of the page bounded at 300 tokens, with a stable element identity, and evict everything else from the context.

### The six laws translated to the browser

| Law | Browser realisation |
|---|---|
| I. Baseline and skeleton folding | Measure `H0`, the raw accessibility-tree token count, before folding. Record it per site. No reduction claim without a baseline. |
| II. Reductive distillation and ratchet | A fold is accepted only if retained tokens fall, or tokens hold flat while task success improves. A fold that adds structure without reducing tokens is rejected. |
| III. Double-blind isolation | Task success is graded by the benchmark's own programmatic validator, never by the folding engine's self-assessment. |
| IV. Remediation-aware arbitration | If the only remedy for a failure is to change the benchmark's oracle, record it as a boundary for human review instead of forcing a patch. |
| V. Right to scientific halt | If a site's DOM, ARIA or framework contract forbids an abstraction, halt and record the boundary rather than fabricate a fold. |
| VI. Dual-polarity and anti-overfitting | The fold must be validated on at least two sites with opposite layouts, and a fold that overfits one site's DOM is rejected. |

### Layer 0: network interception

The cheapest page is the one never rendered. A fetch and XHR interceptor runs before DOM analysis and answers from the network layer when the task is answerable there. The published justification is direct: an API-based agent solved WebArena intents in three lines of code where a browsing agent failed after 15 steps, while the browsing agent averaged 14.8% [37].

Rules:

1. Intercept `fetch`, `XMLHttpRequest` and `WebSocket` frames from the page's own origin.
2. Build a method index: URL pattern, request shape, response shape, and the UI action that triggers it.
3. If the task goal maps to an index entry with a high-confidence match, execute the call and return the structured result. Skip the DOM entirely.
4. If the match is uncertain, fall through to Layer 1 and record the miss.
5. Never intercept authenticated or state-changing calls without an explicit allowlist; a folding engine must not become a confused deputy.

The index is a crystallisation artifact and belongs to Layer 3.

### Layer 1: folded observation

The fold is a deterministic function of the page and the task goal, with a hard budget.

**Inputs.** The accessibility tree, the DOM where the tree is lossy, the current URL, and the task goal.

**Procedure.**

1. **Prune to interactives and task-bearing text.** Keep elements with a role in the interactive set (button, link, textbox, combobox, checkbox, radio, switch, tab, menuitem, slider, spinbutton) plus text nodes that carry task terms. This is AgentOccam's element simplification plus FocusAgent's goal-conditioned line selection [1][10].
2. **Convert structure to Markdown.** Tables and lists become Markdown, eliminating repetitive structural tokens [1].
3. **Bind identity, not position.** Every kept element receives a durable handle from CDP `backendNodeId` plus frame id, with a content fingerprint (stable attributes, then role and accessible name, then a landmark-scoped structural path) used to rebind when a node is destroyed and recreated [29][28].
4. **Emit a diff, not a snapshot.** If a previous fold of the same page exists, emit only the change since the last fold: rebound ids, added nodes, removed nodes, changed text. A fold that is unchanged from the previous step costs a constant.
5. **Cap at 300 tokens.** If the fold exceeds the budget, apply the retrieval step again with a tighter span, then drop the lowest-salience tail. Dropping is logged with the dropped element ids so the decision is auditable.
6. **Hash the fold.** The fold's SHA-256 is recorded so that two folds of the same page can be compared mechanically.

**The identity contract** is the part the field has not standardised. A handle is `(backendNodeId, frameId, fingerprint, generation)`. Taking a snapshot retires the previous generation instead of clearing it. Surviving nodes reclaim their original id. New nodes get fresh numbers. A retired number is never reused within a page. A handle whose node has left the DOM fails loudly with a teaching error, and the role-plus-name fallback that silently rebinds is removed [28][27]. Handles are cleared only on navigation, reload, tab switch or launch [28].

**Why 300.** The budget is not arbitrary. The largest single fact a step needs, a form field with a label, a price, a button name, is under 20 tokens. A 300-token fold holds roughly 10 to 15 such facts plus the diff and the URL, which respects the 4-chunk working-memory bound with room for the goal and the last action. It is also 20x below the smallest measured accessibility snapshot of 22,283 tokens and 2000x below the Playwright MCP Wikipedia measurement [9][8].

### Layer 2: ephemeral snapshot eviction

The eviction layer operates on the conversation, not the page, and it is the highest-leverage component per the published measurements.

**Rule.** Before every model call, scan the history for observation artifacts. Keep the latest. Replace every earlier artifact with a placeholder carrying only its step index, its URL and a one-line state summary. The placeholder is bounded at 30 tokens [12].

**Measured effect.** 142K input tokens over 20 requests with eviction against 327K+ over 43 without, on a representative task [12].

**Additional rules.**

1. Evict screenshots and accessibility snapshots alike; both are re-sent forever [39].
2. Keep the *evidence*, not the observation. Retain only elements the agent probed, acted on or committed as evidence, over a window of the last N steps, N=5 by default [17].
3. Never evict the task goal, the current plan, the last action, or an element id the agent has named in its last two outputs.
4. Eviction is idempotent and runs as a `onBeforeTurn` hook, so it composes with any harness [12].

### Layer 3: site crystallisation

On the first visit to a site, the engine induces a **lens**: a compact, reusable description of the site's structure and the procedures that work on it. On later visits, the lens replaces the fold.

**Lens contents.** The site's URL patterns, the network method index from Layer 0, the durable handle map for recurring elements, the induced workflows (AWM-style abstractions) [2], and the selector memoisation table mapping semantic references to accessibility-tree paths with structural signatures [3].

**Rules.**

1. Induce from a successful trajectory only. A failed trajectory contributes a negative example, not a workflow.
2. Abstract the workflow: replace example-specific contexts with parameters, because abstract workflows beat concrete exemplars [3].
3. Prefer online induction under distribution shift: online induction beat offline on Mind2Web cross-domain step success, 35.5 against 32.6 [3].
4. **Do not accumulate blindly.** Offline plus online workflows interfered rather than composed, so the lens has a promotion gate: a candidate workflow is admitted only if it reduces steps or tokens on a held-out task from the same site [3].
5. Store the lens with a version and an invalidate-on-DOM-signature-change rule. A lens that might be wrong is worse than no lens [14].

**Measured effect.** Dejo's replayed tasks ran in 89K tokens and 1.2 tool calls against 251K and 4.7 on the first run, and 409K and 6.5 through Playwright MCP [7].

### Layer 4: universal MCP plugin

The engine ships as an MCP server implementing the 2026-07-28 core.

**Transport contract.**

| Property | Choice | Reason |
|---|---|---|
| Sessions | None | Stateless core; every request carries its version and capabilities in `_meta` [30] |
| Handshake | None | No `initialize` exchange [30] |
| Long runs | Tasks extension | `tasks/get`, `tasks/update`, `tasks/cancel` for runs that outlive a request [30] |
| Tool catalog | Cacheable | `tools/list` carries `ttlMs` and `cacheScope`, so the catalog is cached and prefix caches stay stable [31] |
| Routing | Headers | `Mcp-Name` and `Mcp-Method` for gateways and rate limiters [30] |
| Interim results | MRTR | `resultType: input_required` when the engine needs a human decision [30] |

**Tool surface.** Keep it under 15 tools; tool-count failure curves show a collapse on huge catalogs, and tool schemas are 60 to 80 percent of a static toolset's token usage [13].

| Tool | Returns |
|---|---|
| `fold` | The 300-token fold for the current page, with durable handles |
| `act` | Execute an action by durable handle, never by position |
| `diff` | The change since the last fold of this page |
| `network_index` | The site's intercepted method index |
| `lens_get` | The crystallised lens for a site |
| `lens_induce` | Induce a lens from the current trajectory |
| `evict` | Apply the eviction rule to a history blob (for harnesses that manage their own context) |

`evict` is the escape hatch that makes the engine useful to a harness that owns its own conversation. A harness that cannot be modified can still hand its history to `evict` and receive a compacted history back.

### Token budget arithmetic

| Layer | Observed cost | Source |
|---|---|---|
| Raw DOM, complex page | 10,000 to 100,000 tokens | [4] |
| Accessibility snapshot | 20,000 to 114,000 tokens | [15][13] |
| Folded observation, target | 300 tokens | Design target |
| Reduction from accessibility snapshot | 98.5% to 99.7% | Computed |
| Eviction placeholder per stale snapshot | 30 tokens | [12] |
| Replayed task after crystallisation | 89K tokens total, 1.2 calls | [7] |

The reduction is computed against the smallest published accessibility snapshot, 22,283 tokens, and the largest, 114,000. A 300-token fold is 98.65% and 99.74% smaller respectively. Against the raw DOM the figure exceeds 99.7%.

**Session cost.** With eviction, a 20-step session carries one 300-token fold plus 19 placeholders plus the goal, the plan and the last action. That is under 3,000 tokens of observation across the session, against ARC's reported 58,500 for a raw history at turn 20 [32].

## Verification protocol and acceptance gates

The design is not credible without a falsification protocol. Each gate is binary and mechanical, following the engine's rule that a measurement instrument must agree with itself.

| Gate | Condition | Rejection code if violated |
|---|---|---|
| G1. Fold ratio | Fold is at most 300 tokens on 100% of steps in a 300-task sample | `FOLD_BUDGET_BREACH` |
| G2. Non-inferiority | Task success within 2 percentage points of the full-observation baseline on the BrowserGym WebArena test split | `FOLD_REGRESSION` |
| G3. Determinism | Two folds of the same page produce the same SHA-256 | `NONDETERMINISTIC_FOLD` |
| G4. Identity stability | 100% of handles survive a re-render that swaps the DOM node; a detached node produces a loud error, never a silent success | `SILENT_REBIND` |
| G5. Eviction | Zero stale observation tokens carried past the previous step; verified by scanning the history before each call | `STALE_CARRYOVER` |
| G6. Crystallisation | A replayed task completes in at most 1 network call and at most 40% of the first run's tokens | `CRYSTALLISATION_MISS` |
| G7. Generalisation | The fold is validated on at least two sites with opposite layouts; a fold that works on one and fails the other is rejected | `SINGLE_SITE_OVERFIT` |
| G8. Network safety | Zero state-changing network calls without an explicit allowlist | `UNAUTHORISED_MUTATION` |

**Protocol.** Measure H0 on the raw tree. Run the full-observation baseline and record success and tokens. Run the folded agent on the identical task set with identical seeds. Report the paired delta, not the absolute. A gate that cannot fail is not a gate.

**Negative results to publish regardless of outcome.** If G2 fails, the fold ratio that preserves success is the finding. If G6 fails, the crystallisation precondition is the finding. If G4 shows silent rebinds in the wild, the identity contract is the finding. The engine's own rule applies: a falsified hypothesis is data, not noise.

## Honest limits and negative results

- **This is a design monograph, not an empirical paper.** No experiment was run for this document. Every number is from a live fetched source, and the 300-token target is a design claim supported by measurement studies, not a measured result of this engine.
- **AgentOccam does not support the 95% narrative.** Its own table shows 14.4% from observation optimisation and a net increase over vanilla [1]. The 95% target must come from the combination of network interception, eviction and crystallisation, and that combination has not been evaluated.
- **Pruning can hurt.** FocusAgent reports that stronger models can gain from richer inputs while weaker models hallucinate more as inputs grow, so the value of pruning is conditional on backbone capability, cost pressure and security requirements [10].
- **Loop traps are the dominant pruning failure.** 12 of 15 and 16 of 18 FocusAgent failure cases were step-limit truncations [10]. A smaller observation does not fix a planning failure; it may hide the evidence needed to escape one.
- **Learned filtering is a dead end at the top end.** A DeBERTa ranker moved LLaMA-2-70B from 1.97% to 2.96% [11]. The technique is real and the ceiling is low.
- **Benchmarks disagree with each other by more than the effects being measured.** WebArena-Verified reduces false negatives by 11 percentage points [35]; Online-Mind2Web's top and bottom entries differ by 66.3 points under different judges [22]. Any single-number claim about a folding engine should be treated as a harness measurement first.
- **Self-reported leaderboard entries dominate the top of every table** [22][35]. The design should be judged against programmatically graded benchmarks with published raw data, which means WebArena and WorkArena rather than Online-Mind2Web.
- **The crystallisation evidence is proprietary where it is strongest.** Dejo's 89K replay is a vendor measurement on 19 tasks [7]; AWM's workflows are a research artifact [2]. Neither is a standard, shareable format.
- **The 300-token budget may be too small for canvas applications, unlabelled widgets and visually-only data.** The accessibility tree is known to lose visual-only content, and the field's own recommendation is a blended agent that uses the tree for acting and the DOM or a screenshot for fields the tree loses [9]. A folding engine must expose an escalation path to the DOM or a screenshot when the fold is insufficient, and the budget must be a default rather than a hard ceiling.

## Conversion paths

1. **Open MCP server, MIT licensed.** Ship the seven-tool surface with the 2026-07-28 stateless core and cacheable tool catalog. This is the smallest artifact with the largest distribution, and it is the only path that lets any harness adopt the fold without adopting the engine.
2. **Harness plugin.** Implement `evict` as an `onBeforeTurn` hook for the major harnesses, following the Gemini CLI pattern [12]. This is the highest-leverage integration because eviction is harness-agnostic.
3. **Benchmark submission.** Run the verification protocol on the BrowserGym WebArena test split and WorkArena L1, and publish the paired deltas. WorkArena L3 is the target that matters for enterprise credibility and the one no current agent passes [24].
4. **Site-lens registry.** A shared, versioned, invalidate-on-DOM-change lens format is the artifact the field lacks. It should be specified before it is built, because AWM's interference result shows that ungoverned accumulation is worse than none [3].
5. **Independent verification product.** The measurement protocol itself, H0, fold ratio, identity stability and stale carry-over, is a product: a harness that tells a team what their browser agent is actually paying per step.

## References

Render: `python3 ~/.hermes/profiles/auto-researcher/skills/research/grounded-citations/scripts/sources.py render --cited-in RESEARCH-COUNCIL/OUTPUT/browser-agent-attention-folding-sota-2026.md`

## Sources

[1] https://arxiv.org/html/2410.13825 — AgentOccam (arXiv HTML)
[2] https://arxiv.org/abs/2409.07429 — Agent Workflow Memory (arXiv)
[3] https://proceedings.mlr.press/v267/wang25bx — AWM (ICML 2025 PMLR)
[4] https://arxiv.org/html/2511.21398v1 — Prune4Web (arXiv)
[5] https://github.com/webdriverio/benchmark — webdriverio browser tool benchmark
[6] https://github.com/ArasHuseyin/browser-agent-benchmark — Sentinel vs Stagehand vs browser-use benchmark
[7] https://dejo.run/benchmark — Dejo vs Playwright MCP token benchmark
[8] https://scalebrowser.net/blog/playwright-mcp-tokens — Playwright MCP token usage measured
[9] https://aismith.dev/insights/browser-automation-for-ai-agents-dom-vs-vision — DOM vs AX tree vs vision token costs
[10] https://arxiv.org/html/2510.03204v2 — FocusAgent: trimming large context of web agents
[11] https://arxiv.org/html/2609.27770v1 — Improving LLM web agents with filtering (DeBERTa)
[12] https://github.com/google-gemini/gemini-cli/pull/24440 — Gemini CLI snapshot superseder PR
[13] https://lite.ego.app/article/context-engineering-browser-agents — Context engineering for browser agents: observation cost
[14] https://github.com/kedarvartak/rote — rote: O(n^2) browser agent token cost
[15] https://arxiv.org/html/2606.06708 — Signal-Driven Observation for Long-Horizon Web Agents
[16] https://huggingface.co/papers/2510.24699 — AgentFold: proactive context management
[17] https://aclanthology.org/2026.findings-emnlp.1135.pdf — Probe to Act: active visual probing browser-use agent
[18] https://os-world.github.io — OSWorld benchmark
[19] https://arxiv.org/pdf/2601.15876v1 — EvoCUA OSWorld 56.7 percent
[20] https://www.skyvern.com/blog/skyvern-2-0-webvoyager-benchmark-results — Skyvern 2.0 WebVoyager results
[21] https://awesomeagents.ai/leaderboards/web-agent-benchmarks-leaderboard — Web agent benchmarks leaderboard Apr 2026
[22] https://leaderboard.steel.dev/leaderboards/online-mind2web — Online-Mind2Web leaderboard
[23] https://alphaxiv.org/overview/2407.05291 — WorkArena++ benchmark paper
[24] https://benchmarklist.com/benchmarks/workarena_l3 — WorkArena-L3 leaderboard
[26] https://arxiv.org/abs/2310.11441 — Set-of-Mark Prompting GPT-4V
[27] https://github.com/vercel-labs/agent-browser/issues/1443 — agent-browser stale snapshot refs issue 1443
[28] https://github.com/vercel-labs/agent-browser/pull/1444/files — agent-browser identity-bound refs PR 1444
[29] https://github.com/truffle-dev/anchortree — anchortree durable element identity and diff observations
[30] https://modelcontextprotocol.io/specification/2026-07-28/basic/utilities/ping — MCP 2026-07-28 key changes
[31] https://blog.modelcontextprotocol.io/posts/2026-07-28 — MCP 2026-07-28 specification announcement
[32] https://aclanthology.org/2026.findings-acl.930.pdf — ARC active context management token efficiency
[33] https://arxiv.org/html/2307.13854v4 — WebArena original paper
[34] https://benchmarklist.com/benchmarks/webarena — BrowserGym WebArena leaderboard
[35] https://www.aievals.co/task-types/computer-browser-use — OSWorld and WebArena 2026 snapshot
[36] https://browser-use.com/changelog — Browser Use changelog
[37] https://aclanthology.org/2025.findings-acl.577.pdf — Beyond Browsing API-Based Web Agents
[38] https://leaderboard.steel.dev/leaderboards/webarena — Steel WebArena leaderboard
[39] https://www.browseract.com/blog/reduce-mcp-token-usage-browser-automation — BrowserAct MCP token usage bloat
