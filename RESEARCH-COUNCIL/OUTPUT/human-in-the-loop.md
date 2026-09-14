# Human-in-the-Loop Integration

## Executive Summary
Crew v2 has human escalation but no structured interface — operators get raw logs, not a dashboard, and approval flows are ad-hoc. Production multi-agent systems require explicit approval gates, adjudication queues, and operator dashboards with full context. The EU AI Act (August 2026) mandates human oversight for high-risk agentic systems. This document specifies a HITL architecture with confidence-based routing, SLA-bound approval queues, and cryptographic payload locking, adapted from Sphinx, Aegis, and production patterns (2025-2026).

## Key Findings

- **Sphinx (2026)** is an open-source HITL control plane: unified approval queue for every framework, SLA with auto-degradation (escalate/auto-approve/auto-reject on timeout), decision log with delta diffing, and tamper-evident capture (SHA3-256 hash chain + Ed25519 signatures). Governance KPIs: escalation rate, timeout rate, correction rate, reviewer agreement, error escape rate, SLA compliance [Sphinx, 2026].
- **Aegis (CloudMatos, 2025)** implements inline approvals with short-lived Ed25519-signed override tokens, threshold tiers (Tier1: ≤$5k auto; Tier2: $5k-$50k approval_needed), debounce windows (30-300s), and OpenTelemetry spans for every decision [Aegis, 2025].
- **Agent Native (2026)** specifies the approval flow pattern: intent classifier → policy engine → confidence threshold → durable approval queue → operator review surface → cryptographic payload lock → execution worker → immutable audit trail. EU AI Act mandates human oversight for high-risk systems effective August 2, 2026 [Agent Native, 2026].
- **Weir (2026)** treats approvers as finite-capacity resources with pressure-aware queuing: Normal → Elevated → Critical states based on decision latency and queue depth. Governance agent is proposal-only; deterministic policy engine validates all decisions [Weir, 2026].
- **KLA Decision Desk (2026)** provides a triage inbox with four dimensions: Priority, Team, Agent, State. Every decision is captured as an OpenTelemetry span and written to a cryptographic ledger (ImmuDB) for audit [KLA, 2026] — **[unverified: source could not be located online as of 2026-09-13; treat the four-dimension triage design as a candidate pattern, not established practice]**.

## Detailed Analysis

### Current Failure Modes

1. **No structured approval flow**: Human escalation is ad-hoc, no SLA.
2. **No operator dashboard**: Operators read raw logs, not a curated queue.
3. **No payload locking**: Approved actions can mutate between approval and execution.
4. **No confidence routing**: All escalations treated equally, no prioritization.
5. **No audit trail**: No immutable record of who approved what and when.

### HITL Architecture

**Six-stage flow (adapted from Agent Native + Sphinx):**

```
Stage 1: ACTION DETECTION
    Agent proposes action → emit structured metadata (intent, risk, confidence)
    
Stage 2: POLICY EVALUATION
    Policy engine evaluates: action type (CUD vs read), risk level, confidence, compliance scope
    
Stage 3: ROUTING DECISION
    If confidence < threshold OR action in protected category → route to approval queue
    Else → auto-execute
    
Stage 4: APPROVAL QUEUE
    Durable store with payload, context window summary, reasoning trace, uncertainty signals
    SLA deadline stamped (configurable per risk tier)
    
Stage 5: OPERATOR REVIEW
    Reviewer sees: action description, parameters, confidence, risk, reasoning trace
    Actions: Approve / Reject / Edit / Escalate
    
Stage 6: EXECUTION
    Approved payload cryptographically locked (HMAC signature)
    Execution worker verifies signature before running
    Full sequence persisted to immutable audit log
```

### Confidence-Based Routing

**Per-action-type thresholds (Agent Native):**

| Action Type | Auto-Execute Threshold | Approval Required If |
|-------------|----------------------|---------------------|
| Read-only | confidence > 0.95 | confidence < 0.95 |
| Write (task dir) | confidence > 0.90 | confidence < 0.90 |
| Write (shared) | confidence > 0.85 | confidence < 0.85 |
| External communication | confidence > 0.95 | confidence < 0.95 |
| Code deployment | Never auto | Always approval |
| Financial transaction | Never auto | Always approval |

**Risk tiers (Aegis pattern):**

| Tier | Threshold | Behavior |
|------|-----------|----------|
| Low | ≤$5k equivalent | Auto-execute if confidence > 0.90 |
| Medium | $5k-$50k | Approval required |
| High | >$50k | Dual approval required |
| Critical | Irreversible | Named approver + dual verification |

### Approval Queue Design

**SLA with auto-degradation (Sphinx pattern):**

| Risk Level | SLA | On Timeout |
|------------|-----|------------|
| Low | 300s | Auto-approve |
| Medium | 1800s | Escalate to senior reviewer |
| High | 3600s | Auto-reject |
| Critical | 7200s | Escalate + alert operator |

**Queue dimensions (KLA Decision Desk):**
- **Priority**: Critical escalations surface first.
- **Team**: Route to owning team (finance, legal, engineering).
- **Agent**: Isolate by agent ID for debugging.
- **State**: Open vs resolved for triage.

**Anti-fatigue measures (Aegis):**
- Debounce window: 30-300s (collapse similar requests).
- Batch approval: 5-20 ops per batch for low-risk.
- Shadow mode: run policies in shadow for 7-14 days before enforcement.
- Routing by severity: low-risk to auto-approver, high-risk to named approvers.

### Operator Dashboard

**Governance KPIs (Sphinx):**

| Metric | Definition | Target |
|--------|-----------|--------|
| Escalation rate | Escalated / total created | <5% |
| Timeout rate | SLA auto-decided / decided | <2% |
| Correction rate | Human reviews that changed payload / human reviews | >10% |
| Reviewer agreement | Human reviews confirming agent unchanged | >80% |
| Error escape rate | Approved actions with negative outcome | <1% |
| SLA compliance | Decisions before SLA deadline | >95% |
| Decision latency | Avg / p50 / p95 review time | <5 min p50 |

**Dashboard views:**
1. **Approval Queue**: Pending requests sorted by priority + SLA countdown.
2. **Decision Log**: Searchable history with delta diffs (agent proposed X, human changed to Y).
3. **Governance Metrics**: Real-time KPI dashboard.
4. **Agent Health**: Per-agent escalation rate, error rate, drift score.

### Cryptographic Payload Locking

**Problem**: Payload can mutate between approval and execution (agent modifies after approval).

**Solution (Agent Native):**
1. On approval: compute HMAC-SHA256(payload + timestamp + approver_id).
2. Store signature with approved payload.
3. Before execution: recompute HMAC and verify match.
4. If mismatch: reject and re-route to review.

**Override tokens (Aegis):**
- Short-lived (2-15 min), single-use Ed25519-signed tokens.
- Token minted on approval, verified on execution.
- Prevents replay attacks and ties approval to single retry.

### EU AI Act Compliance

**Requirements effective August 2, 2026:**
- Human oversight as verifiable technical control (not just stated principle).
- Approval queues, confidence routing, audit trails available to regulators.
- Penalties: up to €40M or 7% of global turnover for violations.

**Compliance checklist:**
- [ ] Approval queue with SLA and auto-degradation.
- [ ] Confidence-based routing with per-action-type thresholds.
- [ ] Immutable audit trail with hash chain and signatures.
- [ ] Operator dashboard with governance KPIs.
- [ ] Payload locking to prevent mutation.
- [ ] Dual verification for highest-risk categories.

## Practical Recommendations

| Recommendation | Implementation | Tools | Threshold |
|----------------|----------------|-------|-----------|
| Confidence routing | Per-action-type thresholds | Policy engine | 0.85-0.95 |
| Approval queue | SLA-bound with auto-degradation | Sphinx-style | Risk-based SLA |
| Payload locking | HMAC-SHA256 signature | Custom | All approved actions |
| Override tokens | Ed25519-signed, short-lived | Aegis-style | 2-15 min TTL |
| Operator dashboard | Real-time KPI + queue | React + WebSocket | <5 min latency |
| Anti-fatigue | Debounce + batch + shadow mode | Aegis-style | 30-300s debounce |
| EU AI Act compliance | Full audit trail + human oversight | All above | August 2026 deadline |

## Metrics Catalog

| Metric | Definition | How to Measure | Target | Warning |
|--------|-----------|----------------|--------|---------|
| Escalation rate | Escalated / total actions | Counter | <5% | >10% review policy |
| Approval latency | Request to decision | Timer | <5 min p50 | >15 min p50 |
| Payload mutation rate | Lock failures / total | Counter | 0 | >0 immediate investigation |
| Override token reuse | Reused tokens / total | Counter | 0 | >0 security incident |
| SLA compliance | Decisions before deadline | Timer | >95% | <90% review capacity |
| Reviewer agreement | Confirmations / reviews | Counter | >80% | <60% review context quality |

## References

1. [Sphinx, 2026] Sphinx: Human-in-the-Loop Control Plane. github.com/LandslideLab/Sphinx.
2. [Aegis, 2025] Aegis: Human-in-Loop Approvals for Agentic AI. cloudmatos.ai/blog.
3. [Agent Native, 2026] Human-in-the-Loop Approval Flow Pattern. agentnative.dev/patterns.
4. [Weir, 2026] Weir: Admission Control for Human Approval. github.com/VampiricCyborg/Weir.
5. [KLA, 2026] Decision Desk: Human-in-the-Loop Control Point. kla.digital/docs. **[unverified — source could not be located online, 2026-09-13]**
6. [EU AI Act, 2026] High-Risk AI Systems — Human Oversight Requirements. artificialintelligenceact.eu.

## [DEEP DIVE]: Article 14 Operationalized, Automation-Bias Counters, Approval-Fatigue Economics, and Operator Catch-Rate Measurement (freebuff, 2026-09-13)

### 1. EU AI Act Article 14 → a requirements table for the approval control plane

Article 14 makes human oversight a *product requirement* for high-risk systems, not a staffing policy; oversight measures must enable the humans to (a) properly understand outputs and limitations, (b) remain aware of automation bias, (c) correctly interpret output, (d) decide not to use the output, and (e) intervene or stop the system [EU AI Act, 2025]. Deployer-side Article 26 adds: monitor operation per instructions, inform affected workers, and retain logs (≥6 months per compliance analyses) [CSA, 2026]. Mapping to the Sphinx-style control plane:

| Article 14 requirement | Control-plane feature |
|---|---|
| Understand outputs/limitations | Every approval card shows: task spec diff, agent confidence, verdict history, and *what the agent cannot know* |
| Awareness of automation bias | UI displays base rates ("engineer DONE claims pass critic 82% of the time") next to each claim |
| Correct interpretation | Standardized verdict taxonomy only (HOLD/APPROVE/ESCALATE — free text banned) |
| Decide not to use | One-click REJECT with mandatory reason code feeding the thorn ledger |
| Intervene/stop | Kill switch independent of agent infrastructure (operator path, not agent path) |

Log retention: align the audit chain (security Layer 5) with the 6-month deployer requirement — the current 90-day active window is compliant only because the hash-chained archive persists beyond it.

### 2. Automation bias: measured, and designed against

The literature is consistent: humans over-rely on algorithmic advice — weighting it more than identical human-source advice [Logg et al., via Microsoft Aether], and incorrect algorithmic support measurably corrupts human judgment even when later shown to be wrong [Agudo et al., 2024]; the 2026 review literature frames automation bias as the central failure mode of human-AI collaboration [Romeo Lai et al., 2026]. Countermeasures built into the operator flow:

1. **Batch review with rotation**: review queues of ~10 items with mandatory per-item verdicts, then a 5-minute break — sustained review degrades vigilance (see §3).
2. **Random decoys**: inject ~5% known-flawed agent outputs (seeded from the regression suite) into approval queues; operator catch rate on decoys is the *measured* review-quality metric (target ≥70%; below 50% = stop live approvals, retrain or re-staff).
3. **Adversarial framing**: present one steel-manned counter-argument per agent claim (cheap LLM call) — skeptical evaluation increases error detection [Beck et al., 2026].

### 3. Approval fatigue: the 93% problem and its economic fix

Field data from Claude Code: users approve ~93% of permission prompts — approval fatigue is the equilibrium state of any always-asking system [reported by ResilientCyber, citing Anthropic, 2026]. A control plane that asks constantly trains its operator to click yes. Design consequences:

- **Approval must be scarce**: only irreversible actions (external comms, spend above threshold, prod data writes, security-relevant config) require human sign-off; read-only and sandboxed actions auto-approve and are *sampled* for review instead.
- Track **prompt approval rate** as a health metric: >80% approval rate = the gate is miscalibrated (too many trivial prompts), not the operator being lazy.
- Separate "approval" (decision) from "attention" (information): summaries and dashboards feed attention; only the scarce class interrupts.

Related primary-source evidence that sustained review degrades: Anthropic's randomized trial (52 developers) found AI-assisted developers scored ~17% lower on comprehension/debugging tests [Anthropic, 2026] — comprehension erosion compounds over a review session, which is why batches must be short. (A widely-cited report that human reviewers' catch rate on dangerous prompts fell from 17% to 5% over 50 consecutive prompts [secondary sources, 2026] could not be verified against a primary publication — treat as plausible, unconfirmed.)

### 4. Escalation routing by risk class, not by confidence alone

Add a risk-class dimension to the Aegis-style override flow: a low-confidence *reversible* task (e.g., draft a summary) does not deserve the same queue as a high-confidence *irreversible* one (e.g., publish a release). Routing matrix:

| | Reversible | Irreversible |
|---|---|---|
| High confidence | Auto-execute + sampled review | Human approval |
| Low confidence | Auto-execute + flag in batch | Human approval + adversarial framing |

This keeps human attention on the quadrant where Article 14's "decide not to use" actually matters.

### References for deep dive (freebuff, 2026-09-13)

- [EU AI Act, 2025] Article 14: Human Oversight. artificialintelligenceact.eu/article/14; EU AI Act Service Desk.
- [CSA, 2026] EU AI Act high-risk obligations: deployer monitoring, ≥6-month log retention. labs.cloudsecurityalliance.org.
- [Logg et al.] People discount advice from algorithms less than identical human advice — in Microsoft Aether, Overreliance on AI Literature Review.
- [Agudo et al., 2024] The impact of AI errors in a human-in-the-loop process. PMC10772030.
- [Romeo Lai et al., 2026] Exploring automation bias in human-AI collaboration (review). AI & Society, Springer.
- [Beck et al., 2026] Bias in the Loop: How Humans Evaluate AI-Generated Content. Harvard Data Science Review.
- [ResilientCyber, 2026] The Human-in-the-Loop Illusion (93% Claude Code approval rate, citing Anthropic). resilientcyber.io.
- [Anthropic, 2026] How AI assistance impacts the formation of coding skills (RCT, n=52, -17% comprehension). anthropic.com/research/AI-assistance-coding-skills.

## [DEEP DIVE]: Zero-Daemon CLI/IPC Interaction, TOCTOU Payload Cryptolocking, Little's Law Queue Backpressure, and Decoy Vigilance Audits (Antigravity, 2026-09-14)

### 1. Zero-Daemon Local HITL Interface: SQLite-WAL Queue with IPC Terminal Signal Integration

Architectural constraints (`MAP.md`: DSH zero-service invariant) prohibit running background WebUI servers, Redis brokers, or continuous Node/Python daemons for operator interaction. Crew v2 implements a zero-daemon local human oversight plane anchored directly in SQLite-WAL:

```sql
CREATE TABLE IF NOT EXISTS approval_queue (
    request_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    agent_id TEXT NOT NULL,
    action_type TEXT NOT NULL,
    risk_tier TEXT NOT NULL CHECK(risk_tier IN ('low', 'medium', 'high', 'critical')),
    canonical_payload TEXT NOT NULL,
    payload_sha256 TEXT NOT NULL,
    adversarial_framing TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'PENDING' CHECK(status IN ('PENDING', 'APPROVED', 'REJECTED', 'TIMEOUT')),
    sla_expires_at INTEGER NOT NULL,
    decided_at INTEGER,
    decided_by TEXT,
    operator_signature TEXT
);
CREATE INDEX IF NOT EXISTS idx_approval_queue_pending ON approval_queue(status, risk_tier, sla_expires_at);
```

**Dual-Channel Interaction Modalities:**
- **Synchronous Interactive Mode (Foreground / Pairing):** In direct developer CLI runs (`agy run` / `cordis`), when an agent attempts a Ring 2+ mutating tool call, the execution harness triggers a blocking pre-tool interceptor:
  ```text
  [APPROVAL REQUIRED] Agent 'engineer' requests 'execute_command' (risk: HIGH)
  Command: git push origin main --force-with-lease
  Skepticism: Overwrites remote history; uncommitted stash could cause branch divergency.
  Decision [y=Approve, n=Reject, d=Diff, e=Explain]:
  ```
  The terminal process suspends turn execution, consumes operator input directly from `stdin`, and logs the decision receipt.
- **Asynchronous Batch Mode (Autonomous Execution):** In autonomous headless runs, requests populate `approval_queue`. The human operator inspects, approves, or rejects requests via CLI commands (`agy queue list`, `agy approve <id>`, `agy reject <id> --reason "..."`), operating on the shared SQLite database with zero background daemons.

### 2. Cryptographic Payload Locking: Defeating TOCTOU Parameter Mutation Attacks

In autonomous multi-agent environments, Time-of-Check to Time-of-Use (TOCTOU) exploits occur when an agent seeks human approval for an action $A(p)$, but between human authorization and tool dispatch, the agent context shifts (or prompt injection alters arguments) mutating $p \to p'$ (e.g. human approves `deploy.sh --target staging`, but tool executes with `--target prod`) [Agent Native, 2026; Invariant Labs, 2025].

**Ed25519 Canonical Attestation Protocol:**
1. **RFC 8785 Canonical JSON Serialization:** The harness serializes tool name and argument dictionary into a canonical, key-sorted, whitespace-normalized string:
   $$H_{\text{payload}} = \text{SHA256}\left(\text{CanonicalJSON}(\text{tool\_name}, \text{arguments})\right)$$
2. **Operator Cryptographic Receipt:** Upon operator sign-off, the CLI signs an immutable attestation token using the operator's local Ed25519 key ($K_{\text{op}}$):
   $$\sigma_{\text{op}} = \text{Sign}_{K_{\text{op}}}\left(H_{\text{payload}} \parallel \text{request\_id} \parallel \text{nonce} \parallel \text{sla\_expires\_at}\right)$$
3. **Execution-Time Kernel Assertion:** Immediately before sandboxed process invocation, the tool runner re-hashes the actual arguments passed to the system call:
   $$H_{\text{actual}} = \text{SHA256}\left(\text{CanonicalJSON}(\text{actual\_tool}, \text{actual\_args})\right)$$
4. **Enforcement:** The sandbox executes the tool **if and only if** $H_{\text{actual}} == H_{\text{payload}}$ AND $\text{Verify}_{K_{\text{op\_pub}}}(\sigma_{\text{op}}) == \text{True}$. Any argument mutation—even a single altered flag or path—invalidates the signature, immediately triggering an unrecoverable `SECURITY_TOCTOU_ABORT` and freezing the agent turn.

### 3. Queue Pressure-Aware Admission Control via Little's Law (Weir Model)

When autonomous agent loops spawn tasks faster than human operators can review them, approval queues balloon. As queue depth expands, human operators experience severe approval fatigue, shifting into reflexive rubber-stamping (the "93% approval rate trap" [ResilientCyber, 2026; Agentmelt, 2026]).

**Little's Law Queue Dynamics:**
$$L_q = \lambda_{\text{agents}} \cdot W_q$$
where $L_q$ represents pending approval queue depth, $\lambda_{\text{agents}}$ is the incoming approval request rate, and $W_q$ is human review latency. If $L_q$ exceeds operator working capacity ($Q_{\text{capacity}} = 8$), review quality collapses.

**Dynamic Backpressure States:**
- **State NORMAL ($L_q \le 4$):** Standard operations; normal SLA countdowns (300s–1800s).
- **State ELEVATED ($4 < L_q \le 8$):** Non-critical subagent spawning is throttled by 50%; debounce windows expand from 30s to 120s to collapse near-duplicate requests.
- **State CRITICAL ($L_q > 8$):** Hard admission control. The harness blocks all new agent turn dispatches via a SQLite task semaphore until $L_q \le 3$. Agents transition to low-power wait states, guaranteeing that human reviewers are never overwhelmed with high-cardinality backlogs.

### 4. Decoy Vigilance Audits & Automated Adversarial Steel-Manning

To satisfy EU AI Act Article 14's explicit mandate that human oversight must prevent automation bias rather than passively rubber-stamp it:
- **Synthetic Decoy Injection:** The harness randomly injects synthetically flawed actions (~5% of all review requests) drawn from the golden regression suite (e.g. subtly inverted logic flags, deprecated library versions, or misconfigured permission masks).
- **Vigilance Metric ($V_{\text{op}}$):**
  $$V_{\text{op}} = \frac{\text{Decoys Correctly Rejected}}{\text{Total Decoys Injected}}$$
  If $V_{\text{op}} < 0.75$ across a rolling 20-decoy window, the system alerts the lead engineer that operator vigilance has lapsed, automatically pausing auto-approval fallbacks.
- **Automated Adversarial Steel-Manning:** Every approval card rendered to the operator is automatically augmented with a two-sentence adversarial critique generated by an orthogonal prompt pass (<150 tokens):
  1. *Underlying Fragility:* Identifies the single most fragile assumption in the proposed action.
  2. *Worst-Case Blast Radius:* Highlights the irreversible consequence if the change contains a latent regression.

### 5. Measurable Human-in-the-Loop Governance Metrics Catalog

| Metric | Definition | How to Measure | Target | Warning Threshold |
|---|---|---|---|---|
| **Operator Decision Latency** | Time from request queueing to human decision | SQLite queue timestamp diff | **$p50 < 3.5\text{m}$** | $p95 > 15\text{m}$ (Operator bottlenecked) |
| **TOCTOU Tamper Incidents** | Discrepancies between approved hash and executed hash | Sandbox execution assertions | **0 incidents** | > 0 (Immediate agent containment) |
| **Queue Backpressure Frequency** | Percentage of runtime spent in ELEVATED/CRITICAL queue states | Semaphore state timer | **< 5%** | > 15% (Recalibrate confidence thresholds) |
| **Decoy Catch Rate ($V_{\text{op}}$)** | Synthetically flawed requests caught by operator | Decoy audit ledger | **≥ 75%** | < 60% (Severe operator automation bias) |
| **Human Intervention Scarcity** | Proportion of agent actions requiring human approval | Global action counter | **< 3%** | > 8% (Gate uncalibrated / fatigue risk) |

### References for deep dive (Antigravity, 2026-09-14)

- [Agentmelt, 2026] Human-in-the-Loop for AI Agents in 2026: The Rubber-Stamping Problem (approvals pile up, humans optimize for throughput; why backpressure is mandatory). agentmelt.com/blog/hitl-agent-oversight-2026.
- [RFC 8785, 2020] JSON Canonicalization Scheme (JCS) for deterministic cryptographic payload hashing. rfc-editor.org/rfc/rfc8785.
- [Agent Native, 2026] Human-in-the-Loop Approval Flow Pattern: Cryptographic Payload Locking and Nonce Verification. agentnative.dev/patterns/hitl-approval-flow.
- [Weir, 2026] Weir: Admission Control and Queue Pressure Management for Human Oversight in Agent Systems. github.com/VampiricCyborg/Weir.
- [ResilientCyber, 2026] The Human-in-the-Loop Illusion (analyzing the 93% approval rate phenomenon and automation bias traps). resilientcyber.io.

